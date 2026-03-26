// script.js
import { database, auth, signInAnonymously, onAuthStateChanged } from './firebase-config.js';
import { 
  ref, push, onValue, set, update, get, 
  query, orderByChild, limitToLast, remove,
  increment, serverTimestamp
} from "https://www.gstatic.com/firebasejs/10.7.2/firebase-database.js";

// ---------- تكوين Cloudinary ----------
const CLOUD_NAME = "dnillsbmi";
const UPLOAD_PRESET = "ekxzvogb";
const CLOUDINARY_UPLOAD_URL = `https://api.cloudinary.com/v1_1/${CLOUD_NAME}/video/upload`;

// ---------- متغيرات عامة ----------
let currentUser = null;
let currentUserId = null;
let currentUsername = null;
let allVideos = [];
let currentVideoIdForComment = null;
let selectedVideoFile = null;

// ---------- تهيئة المستخدم ----------
async function initUser() {
  return new Promise((resolve) => {
    onAuthStateChanged(auth, async (user) => {
      if (user) {
        currentUser = user;
        currentUserId = user.uid;
        
        // جلب أو إنشاء بيانات المستخدم
        const userRef = ref(database, `users/${currentUserId}`);
        const snapshot = await get(userRef);
        
        if (!snapshot.exists()) {
          let username = localStorage.getItem("username");
          if (!username) {
            username = prompt("أهلاً بك في Tokixx! 👋\nأدخل اسم المستخدم الخاص بك:", "مستخدم_Tokixx");
            if (!username || username.trim() === "") username = "مستخدم_" + Math.random().toString(36).substr(2, 6);
            localStorage.setItem("username", username);
          }
          currentUsername = username;
          await set(userRef, {
            username: currentUsername,
            createdAt: serverTimestamp(),
            followers: {},
            following: {},
            totalLikes: 0,
            avatar: `https://ui-avatars.com/api/?background=ff0050&color=fff&name=${encodeURIComponent(currentUsername)}`
          });
        } else {
          currentUsername = snapshot.val().username;
        }
        
        document.getElementById("profileUsername").innerText = currentUsername;
        resolve();
      } else {
        // تسجيل دخول مجهول
        const result = await signInAnonymously(auth);
        currentUser = result.user;
        currentUserId = currentUser.uid;
        let username = localStorage.getItem("username");
        if (!username) {
          username = prompt("أهلاً بك في Tokixx! 👋\nأدخل اسم المستخدم الخاص بك:", "مستخدم_Tokixx");
          if (!username || username.trim() === "") username = "مستخدم_" + Math.random().toString(36).substr(2, 6);
          localStorage.setItem("username", username);
        }
        currentUsername = username;
        const userRef = ref(database, `users/${currentUserId}`);
        await set(userRef, {
          username: currentUsername,
          createdAt: serverTimestamp(),
          followers: {},
          following: {},
          totalLikes: 0,
          avatar: `https://ui-avatars.com/api/?background=ff0050&color=fff&name=${encodeURIComponent(currentUsername)}`
        });
        document.getElementById("profileUsername").innerText = currentUsername;
        resolve();
      }
    });
  });
}

// ---------- دوال مساعدة ----------
function showToast(msg, duration = 2000) {
  const toast = document.getElementById('toastMsg');
  toast.innerText = msg;
  toast.style.opacity = '1';
  setTimeout(() => { toast.style.opacity = '0'; }, duration);
}

// ---------- جلب الفيديوهات ----------
function loadVideosFromFirebase() {
  const videosRef = ref(database, 'videos');
  onValue(videosRef, (snapshot) => {
    const data = snapshot.val();
    if (data) {
      allVideos = Object.entries(data).map(([id, video]) => ({ id, ...video }));
      allVideos.sort((a, b) => (b.timestamp || 0) - (a.timestamp || 0));
      renderFeed('feedContainer', allVideos);
      renderFeed('friendsFeed', allVideos);
      updateProfileStats();
    } else {
      allVideos = [];
      renderFeed('feedContainer', []);
      renderFeed('friendsFeed', []);
    }
  });
}

// عرض الفيديوهات
function renderFeed(containerId, videos) {
  const container = document.getElementById(containerId);
  if (!container) return;
  
  if (!videos || videos.length === 0) {
    container.innerHTML = '<div class="loading"><i class="fas fa-video"></i> لا توجد فيديوهات حالياً<br><span style="font-size:12px;">قم برفع أول فيديو لك!</span></div>';
    return;
  }
  
  container.innerHTML = '';
  videos.forEach(video => {
    const likesCount = video.likes ? Object.keys(video.likes).length : 0;
    const isLiked = video.likes && video.likes[currentUserId];
    
    const videoDiv = document.createElement('div');
    videoDiv.className = 'video-item';
    videoDiv.setAttribute('data-vid', video.id);
    videoDiv.innerHTML = `
      <video class="video-element" src="${video.videoUrl}" loop muted playsinline autoplay></video>
      <div class="floating-right">
        <div class="action-btn avatar-ring">
          <img src="${video.userAvatar || `https://ui-avatars.com/api/?background=ff0050&color=fff&name=${encodeURIComponent(video.username || 'U')}`}">
        </div>
        <div class="action-btn like-btn" data-id="${video.id}">
          <i class="${isLiked ? 'fas' : 'far'} fa-heart"></i>
          <span class="like-count">${likesCount}</span>
        </div>
        <div class="action-btn comment-open-btn" data-id="${video.id}">
          <i class="far fa-comment-dots"></i>
          <span class="comment-count">${video.commentCount || 0}</span>
        </div>
        <div class="action-btn share-btn" data-url="${video.videoUrl}">
          <i class="fas fa-share"></i>
          <span>شارك</span>
        </div>
        <div class="action-btn sound-icon">
          <i class="fas fa-music"></i>
        </div>
      </div>
      <div class="video-info">
        <div class="username">${video.username || "مستخدم"} <i class="fas fa-check-circle verified-icon"></i></div>
        <div class="caption">${video.caption || ""}</div>
        <div class="sound-marquee">
          <i class="fas fa-record-vinyl"></i>
          <span class="sound-name">${video.sound || "صوت شائع"}</span>
          <i class="fas fa-angle-right"></i>
        </div>
      </div>
    `;
    container.appendChild(videoDiv);
  });
  attachVideoEvents(containerId);
}

// ربط الأحداث
function attachVideoEvents(containerId) {
  const container = document.getElementById(containerId);
  if (!container) return;
  
  container.querySelectorAll('.like-btn').forEach(btn => {
    btn.removeEventListener('click', handleLike);
    btn.addEventListener('click', handleLike);
  });
  
  container.querySelectorAll('.comment-open-btn').forEach(btn => {
    btn.removeEventListener('click', openCommentPanel);
    btn.addEventListener('click', openCommentPanel);
  });
  
  container.querySelectorAll('.share-btn').forEach(btn => {
    btn.removeEventListener('click', handleShare);
    btn.addEventListener('click', handleShare);
  });
  
  container.querySelectorAll('.sound-icon').forEach(btn => {
    btn.addEventListener('click', () => showToast("🎵 استمع إلى هذا الصوت على Tokixx"));
  });
  
  // تحسين تشغيل الفيديو عند التمرير
  const videos = container.querySelectorAll('.video-element');
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.play().catch(e => console.log('Auto-play prevented:', e));
      } else {
        entry.target.pause();
      }
    });
  }, { threshold: 0.5 });
  
  videos.forEach(video => observer.observe(video));
}

// معالجة الإعجاب
async function handleLike(e) {
  e.stopPropagation();
  const btn = e.currentTarget;
  const videoId = btn.getAttribute('data-id');
  const likeRef = ref(database, `videos/${videoId}/likes/${currentUserId}`);
  const videoRef = ref(database, `videos/${videoId}`);
  
  const snapshot = await get(likeRef);
  if (snapshot.exists()) {
    await remove(likeRef);
    btn.querySelector('i').classList.remove('fas');
    btn.querySelector('i').classList.add('far');
    const countSpan = btn.querySelector('.like-count');
    countSpan.innerText = parseInt(countSpan.innerText) - 1;
  } else {
    await set(likeRef, true);
    btn.querySelector('i').classList.remove('far');
    btn.querySelector('i').classList.add('fas');
    const countSpan = btn.querySelector('.like-count');
    countSpan.innerText = parseInt(countSpan.innerText) + 1;
  }
}

// معالجة المشاركة
function handleShare(e) {
  e.stopPropagation();
  const btn = e.currentTarget;
  const videoUrl = btn.getAttribute('data-url');
  if (videoUrl) {
    navigator.clipboard.writeText(videoUrl);
    showToast("✅ تم نسخ رابط الفيديو!");
  }
}

// فتح لوحة التعليقات
async function openCommentPanel(e) {
  const btn = e.currentTarget;
  const videoId = btn.getAttribute('data-id');
  currentVideoIdForComment = videoId;
  const panel = document.getElementById('commentPanel');
  const listDiv = document.getElementById('commentList');
  
  const commentsRef = ref(database, `comments/${videoId}`);
  const snapshot = await get(commentsRef);
  const comments = snapshot.val() ? Object.values(snapshot.val()) : [];
  
  listDiv.innerHTML = '';
  if (comments.length === 0) {
    listDiv.innerHTML = '<div style="color:#aaa; text-align:center; padding:20px;">💬 لا توجد تعليقات بعد، كن أول من يعلق!</div>';
  } else {
    comments.reverse().forEach(comm => {
      const commentEl = document.createElement('div');
      commentEl.innerHTML = `
        <div class="comment-item">
          <img class="comment-avatar" src="${comm.avatar || `https://ui-avatars.com/api/?background=ff0050&color=fff&name=${encodeURIComponent(comm.username)}`}">
          <div class="comment-content">
            <div><span class="comment-name">${comm.username}</span><span class="comment-time"> ${comm.time}</span></div>
            <div class="comment-text">${comm.text}</div>
          </div>
        </div>
      `;
      listDiv.appendChild(commentEl);
    });
  }
  panel.classList.add('open');
}

// إرسال تعليق
document.getElementById('sendCommentBtn')?.addEventListener('click', async () => {
  const input = document.getElementById('commentInput');
  const text = input.value.trim();
  if (!text || !currentVideoIdForComment) return;
  
  const newCommentRef = push(ref(database, `comments/${currentVideoIdForComment}`));
  await set(newCommentRef, {
    username: currentUsername,
    userId: currentUserId,
    avatar: `https://ui-avatars.com/api/?background=ff0050&color=fff&name=${encodeURIComponent(currentUsername)}`,
    text: text,
    time: new Date().toLocaleString('ar'),
    likes: 0
  });
  
  const videoRef = ref(database, `videos/${currentVideoIdForComment}/commentCount`);
  const currentCount = (await get(videoRef)).val() || 0;
  await set(videoRef, currentCount + 1);
  
  const videoItem = document.querySelector(`.video-item[data-vid="${currentVideoIdForComment}"]`);
  if (videoItem) {
    const commentSpan = videoItem.querySelector('.comment-count');
    if (commentSpan) commentSpan.innerText = currentCount + 1;
  }
  
  input.value = '';
  openCommentPanel({ currentTarget: { getAttribute: () => currentVideoIdForComment } });
  showToast("✨ تم إضافة تعليقك");
});

document.getElementById('closeComment')?.addEventListener('click', () => {
  document.getElementById('commentPanel').classList.remove('open');
});

// ---------- رفع الفيديو ----------
document.getElementById('selectVideoBtn')?.addEventListener('click', () => {
  document.getElementById('videoFile').click();
});

document.getElementById('videoFile')?.addEventListener('change', (e) => {
  if (e.target.files.length) {
    selectedVideoFile = e.target.files[0];
    if (selectedVideoFile.size > 100 * 1024 * 1024) {
      showToast("⚠️ حجم الفيديو كبير جداً (الحد الأقصى 100MB)");
      selectedVideoFile = null;
      return;
    }
    showToast(`✅ تم اختيار: ${selectedVideoFile.name.substring(0, 30)}`);
  }
});

document.getElementById('uploadToCloudinaryBtn')?.remove();
const uploadBtn = document.createElement('button');
uploadBtn.className = 'upload-btn';
uploadBtn.id = 'uploadToCloudinaryBtn';
uploadBtn.innerHTML = '<i class="fas fa-cloud-upload-alt"></i> رفع إلى السحابة';
uploadBtn.style.background = '#20d5ec';
document.querySelector('.upload-area').appendChild(uploadBtn);

uploadBtn.addEventListener('click', async () => {
  if (!selectedVideoFile) {
    showToast("📹 الرجاء اختيار فيديو أولاً");
    return;
  }
  
  const caption = document.getElementById('videoCaption').value.trim() || "فيديو جديد على Tokixx";
  const formData = new FormData();
  formData.append('file', selectedVideoFile);
  formData.append('upload_preset', UPLOAD_PRESET);
  formData.append('resource_type', 'video');
  
  uploadBtn.disabled = true;
  uploadBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> جاري الرفع...';
  
  try {
    const response = await fetch(CLOUDINARY_UPLOAD_URL, {
      method: 'POST',
      body: formData
    });
    const data = await response.json();
    
    if (data.secure_url) {
      const newVideoRef = push(ref(database, 'videos'));
      await set(newVideoRef, {
        videoUrl: data.secure_url,
        caption: caption,
        username: currentUsername,
        userId: currentUserId,
        userAvatar: `https://ui-avatars.com/api/?background=ff0050&color=fff&name=${encodeURIComponent(currentUsername)}`,
        timestamp: Date.now(),
        likes: {},
        commentCount: 0,
        sound: "🎵 صوت جديد"
      });
      
      showToast("🎉 تم رفع الفيديو بنجاح!");
      document.getElementById('videoCaption').value = '';
      document.getElementById('videoFile').value = '';
      selectedVideoFile = null;
      switchView('home');
    } else {
      showToast("❌ فشل الرفع إلى السحابة");
    }
  } catch (err) {
    console.error(err);
    showToast("⚠️ حدث خطأ أثناء الرفع");
  } finally {
    uploadBtn.disabled = false;
    uploadBtn.innerHTML = '<i class="fas fa-cloud-upload-alt"></i> رفع إلى السحابة';
  }
});

// ---------- إحصائيات الملف الشخصي ----------
async function updateProfileStats() {
  const videosRef = ref(database, 'videos');
  const snapshot = await get(videosRef);
  const videos = snapshot.val();
  if (!videos) {
    document.getElementById('postCount').innerText = '0';
    document.getElementById('totalLikes').innerText = '0';
    document.getElementById('profileGrid').innerHTML = '<div style="color:white; text-align:center; grid-column:span 3;">لا توجد فيديوهات بعد</div>';
    return;
  }
  
  let userVideos = 0;
  let totalLikes = 0;
  const userVideoList = [];
  
  Object.entries(videos).forEach(([id, vid]) => {
    if (vid.userId === currentUserId) {
      userVideos++;
      const likesCount = vid.likes ? Object.keys(vid.likes).length : 0;
      totalLikes += likesCount;
      userVideoList.push({ id, ...vid, likesCount });
    }
  });
  
  document.getElementById('postCount').innerText = userVideos;
  document.getElementById('totalLikes').innerText = totalLikes;
  document.getElementById('followersCount').innerText = Math.floor(Math.random() * 1000);
  
  const grid = document.getElementById('profileGrid');
  grid.innerHTML = '';
  
  if (userVideos === 0) {
    grid.innerHTML = '<div style="color:white; text-align:center; grid-column:span 3; padding:40px;"><i class="fas fa-video"></i> لا توجد فيديوهات بعد<br><span style="font-size:12px;">انقر على + لرفع أول فيديو</span></div>';
  } else {
    userVideoList.forEach(video => {
      const item = document.createElement('div');
      item.className = 'grid-item';
      item.style.backgroundImage = `url(${video.videoUrl})`;
      item.style.backgroundSize = 'cover';
      item.innerHTML = `<div class="view-count-badge"><i class="fas fa-heart"></i> ${video.likesCount}</div>`;
      item.onclick = () => {
        const videoIndex = allVideos.findIndex(v => v.id === video.id);
        if (videoIndex !== -1) {
          switchView('home');
          setTimeout(() => {
            const feedContainer = document.getElementById('feedContainer');
            const videoElements = feedContainer.querySelectorAll('.video-item');
            if (videoElements[videoIndex]) {
              videoElements[videoIndex].scrollIntoView({ behavior: 'smooth' });
            }
          }, 100);
        }
      };
      grid.appendChild(item);
    });
  }
}

// ---------- نظام التنقل ----------
function switchView(viewId) {
  document.querySelectorAll('.view').forEach(v => v.classList.remove('active'));
  document.getElementById(viewId + 'View').classList.add('active');
  document.querySelectorAll('.nav-icon').forEach(icon => icon.classList.remove('active'));
  const activeNav = document.querySelector(`.nav-icon[data-nav="${viewId}"]`);
  if (activeNav) activeNav.classList.add('active');
  if (viewId === 'profile') updateProfileStats();
  if (viewId === 'inbox') loadInbox();
}

document.querySelectorAll('.nav-icon').forEach(icon => {
  icon.addEventListener('click', () => {
    const nav = icon.getAttribute('data-nav');
    switchView(nav);
  });
});

// صندوق الوارد
function loadInbox() {
  const inboxDiv = document.getElementById('inboxContainer');
  inboxDiv.innerHTML = `
    <div class="conversation-row" onclick="showToast('قريباً ستدعم المحادثات المباشرة')">
      <div class="conv-avatar"><img src="https://randomuser.me/api/portraits/men/1.jpg"></div>
      <div class="conv-details"><div class="conv-name">🤖 فريق Tokixx</div><div class="conv-preview">مرحباً! شارك الفيديوهات مع أصدقائك 🎬</div></div>
    </div>
    <div class="conversation-row" onclick="showToast('يمكنك دعوة الأصدقاء للمشاركة')">
      <div class="conv-avatar"><img src="https://randomuser.me/api/portraits/women/2.jpg"></div>
      <div class="conv-details"><div class="conv-name">✨ دعوة الأصدقاء</div><div class="conv-preview">انقر هنا لدعوة أصدقائك إلى Tokixx</div></div>
    </div>
  `;
}

// أحداث إضافية
document.getElementById('editProfileBtn')?.addEventListener('click', () => {
  const newName = prompt("تعديل اسم المستخدم:", currentUsername);
  if (newName && newName.trim()) {
    currentUsername = newName.trim();
    localStorage.setItem("username", currentUsername);
    update(ref(database, `users/${currentUserId}`), { username: currentUsername });
    document.getElementById("profileUsername").innerText = currentUsername;
    showToast("✅ تم تحديث اسم المستخدم");
  }
});

document.getElementById('addFriendBtn')?.addEventListener('click', () => {
  showToast("👥 شارك رابط حسابك مع الأصدقاء!");
  navigator.clipboard.writeText(window.location.href);
});

// تهيئة التطبيق
async function init() {
  await initUser();
  loadVideosFromFirebase();
}

init();
