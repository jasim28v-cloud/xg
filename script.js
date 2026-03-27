import { database, auth, storage, signInWithEmailAndPassword, createUserWithEmailAndPassword, signOut, onAuthStateChanged, storageRef, uploadBytes, getDownloadURL } from './firebase-config.js';
import { ref, push, onValue, set, update, get, remove, serverTimestamp } from "https://www.gstatic.com/firebasejs/10.7.2/firebase-database.js";

// Admin credentials
const ADMIN_EMAIL = "jasim28v@gmail.com";

// Global variables
let currentUser = null;
let currentUserId = null;
let currentUsername = null;
let isAdmin = false;
let allVideos = [];
let currentVideoIdForComment = null;
let currentChatWith = null;
let allUsers = [];

// Helper: toast message
function showToast(msg) {
  const toast = document.getElementById('toastMsg');
  toast.innerText = msg;
  toast.style.opacity = '1';
  setTimeout(() => { toast.style.opacity = '0'; }, 2000);
}

// Admin panel functions
function showAdminPanel() {
  const panel = document.getElementById('adminPanel');
  const content = document.getElementById('adminContent');
  const usersRef = ref(database, 'users');
  onValue(usersRef, (snapshot) => {
    const users = snapshot.val();
    content.innerHTML = '<h3 style="color:white; padding:10px;">👥 المستخدمين</h3>';
    if (users) {
      Object.entries(users).forEach(([uid, user]) => {
        content.innerHTML += `
          <div class="admin-item">
            <span>👤 ${user.username} (${user.email || 'لا يوجد بريد'})</span>
            <div>
              <button class="ban-btn" onclick="window.banUser('${uid}')"><i class="fas fa-ban"></i> حظر</button>
            </div>
          </div>
        `;
      });
    }
    content.innerHTML += '<h3 style="color:white; padding:10px;">🎬 الفيديوهات</h3>';
    const videosRef = ref(database, 'videos');
    onValue(videosRef, (snapshot) => {
      const videos = snapshot.val();
      if (videos) {
        Object.entries(videos).forEach(([vid, video]) => {
          content.innerHTML += `
            <div class="admin-item">
              <span>🎥 ${video.username}: ${video.caption?.substring(0, 30) || 'بدون وصف'}</span>
              <button class="delete-btn" onclick="window.deleteVideo('${vid}')"><i class="fas fa-trash"></i> حذف</button>
            </div>
          `;
        });
      }
    });
  });
  panel.classList.add('show');
}

window.banUser = async (userId) => {
  if (confirm('هل أنت متأكد من حظر هذا المستخدم؟')) {
    await set(ref(database, `banned/${userId}`), true);
    showToast('✅ تم حظر المستخدم');
  }
};

window.deleteVideo = async (videoId) => {
  if (confirm('هل أنت متأكد من حذف هذا الفيديو؟')) {
    await remove(ref(database, `videos/${videoId}`));
    showToast('✅ تم حذف الفيديو');
  }
};

// Video rendering with watermark and hashtags
function renderFeed(videos) {
  const container = document.getElementById('feedContainer');
  if (!videos.length) {
    container.innerHTML = '<div class="loading">لا توجد فيديوهات حالياً</div>';
    return;
  }
  container.innerHTML = '';
  videos.forEach(video => {
    const likesCount = video.likes ? Object.keys(video.likes).length : 0;
    const isLiked = video.likes && video.likes[currentUserId];
    const hashtags = video.hashtags || [];
    const videoDiv = document.createElement('div');
    videoDiv.className = 'video-item';
    videoDiv.setAttribute('data-vid', video.id);
    videoDiv.innerHTML = `
      <video class="video-element" src="${video.videoUrl}" loop muted playsinline autoplay></video>
      <div class="floating-right">
        <div class="action-btn avatar-ring"><img src="${video.userAvatar || `https://ui-avatars.com/api/?background=ff0050&color=fff&name=${encodeURIComponent(video.username)}`}"></div>
        <div class="action-btn like-btn" data-id="${video.id}"><i class="${isLiked ? 'fas' : 'far'} fa-heart"></i><span class="like-count">${likesCount}</span></div>
        <div class="action-btn comment-open-btn" data-id="${video.id}"><i class="far fa-comment-dots"></i><span>${video.commentCount || 0}</span></div>
        <div class="action-btn share-btn" data-url="${video.videoUrl}"><i class="fas fa-share"></i><span>شارك</span></div>
      </div>
      <div class="video-info">
        <div class="username">${video.username} <i class="fas fa-check-circle verified-icon"></i></div>
        <div class="caption">${video.caption || ""}</div>
        <div class="hashtags">${hashtags.map(t => `<span class="hashtag">#${t}</span>`).join('')}</div>
      </div>
    `;
    container.appendChild(videoDiv);
    // Add watermark
    setTimeout(() => {
      const watermark = document.createElement('div');
      watermark.className = 'watermark';
      watermark.innerHTML = `<i class="fas fa-heart"></i> Tokixx | @${video.username}`;
      videoDiv.appendChild(watermark);
    }, 100);
  });
  attachVideoEvents();
}

function attachVideoEvents() {
  document.querySelectorAll('.like-btn').forEach(btn => {
    btn.onclick = async (e) => {
      e.stopPropagation();
      const videoId = btn.getAttribute('data-id');
      const likeRef = ref(database, `videos/${videoId}/likes/${currentUserId}`);
      const snapshot = await get(likeRef);
      if (snapshot.exists()) {
        await remove(likeRef);
        btn.querySelector('i').classList.replace('fas', 'far');
        const countSpan = btn.querySelector('.like-count');
        countSpan.innerText = parseInt(countSpan.innerText) - 1;
      } else {
        await set(likeRef, true);
        btn.querySelector('i').classList.replace('far', 'fas');
        const countSpan = btn.querySelector('.like-count');
        countSpan.innerText = parseInt(countSpan.innerText) + 1;
      }
    };
  });
  document.querySelectorAll('.comment-open-btn').forEach(btn => {
    btn.onclick = () => openCommentPanel(btn.getAttribute('data-id'));
  });
  document.querySelectorAll('.share-btn').forEach(btn => {
    btn.onclick = () => {
      navigator.clipboard.writeText(btn.getAttribute('data-url'));
      showToast('✅ تم نسخ الرابط');
    };
  });
}

async function openCommentPanel(videoId) {
  currentVideoIdForComment = videoId;
  const panel = document.getElementById('commentPanel');
  const listDiv = document.getElementById('commentList');
  const commentsRef = ref(database, `comments/${videoId}`);
  const snapshot = await get(commentsRef);
  const comments = snapshot.val() ? Object.values(snapshot.val()) : [];
  listDiv.innerHTML = comments.length ? '' : '<div style="color:#aaa; text-align:center;">لا توجد تعليقات</div>';
  comments.reverse().forEach(comm => {
    listDiv.innerHTML += `
      <div class="comment-item">
        <img class="comment-avatar" src="${comm.avatar}">
        <div class="comment-content">
          <div><span class="comment-name">${comm.username}</span><span class="comment-time"> ${comm.time}</span></div>
          <div class="comment-text">${comm.text}</div>
        </div>
      </div>
    `;
  });
  panel.classList.add('open');
}

document.getElementById('sendCommentBtn')?.addEventListener('click', async () => {
  const input = document.getElementById('commentInput');
  if (!input.value.trim() || !currentVideoIdForComment) return;
  await push(ref(database, `comments/${currentVideoIdForComment}`), {
    username: currentUsername,
    userId: currentUserId,
    avatar: `https://ui-avatars.com/api/?background=ff0050&color=fff&name=${encodeURIComponent(currentUsername)}`,
    text: input.value,
    time: new Date().toLocaleString('ar'),
  });
  const videoRef = ref(database, `videos/${currentVideoIdForComment}/commentCount`);
  const count = (await get(videoRef)).val() || 0;
  await set(videoRef, count + 1);
  input.value = '';
  openCommentPanel(currentVideoIdForComment);
  showToast('✅ تم إضافة التعليق');
});

document.getElementById('closeComment')?.addEventListener('click', () => {
  document.getElementById('commentPanel').classList.remove('open');
});

// Chat functionality
function loadChatUsers() {
  const usersRef = ref(database, 'users');
  onValue(usersRef, (snapshot) => {
    allUsers = [];
    const users = snapshot.val();
    if (users) {
      Object.entries(users).forEach(([uid, user]) => {
        if (uid !== currentUserId) {
          allUsers.push({ uid, ...user });
        }
      });
      renderChatUsers();
    }
  });
}

function renderChatUsers() {
  const container = document.getElementById('chatUsersList');
  container.innerHTML = '<div style="color:#aaa; padding:5px;">المستخدمين المتاحين</div>';
  allUsers.forEach(user => {
    container.innerHTML += `
      <div class="chat-user" onclick="window.selectChatUser('${user.uid}', '${user.username}')">
        <img src="${user.avatar}">
        <span style="color:white; font-size:12px;">${user.username}</span>
      </div>
    `;
  });
}

window.selectChatUser = (userId, username) => {
  currentChatWith = { id: userId, username };
  loadMessages(userId);
};

function loadMessages(otherUserId) {
  const messagesRef = ref(database, `messages/${currentUserId}_${otherUserId}`);
  onValue(messagesRef, (snapshot) => {
    const messages = snapshot.val();
    const container = document.getElementById('chatMessagesArea');
    container.innerHTML = '';
    if (messages) {
      Object.values(messages).forEach(msg => {
        const bubble = document.createElement('div');
        bubble.className = `chat-bubble ${msg.senderId === currentUserId ? 'sent' : 'received'}`;
        if (msg.text) bubble.innerText = msg.text;
        if (msg.imageUrl) bubble.innerHTML += `<img src="${msg.imageUrl}">`;
        container.appendChild(bubble);
      });
      container.scrollTop = container.scrollHeight;
    }
  });
}

document.getElementById('chatSendBtn')?.addEventListener('click', async () => {
  const input = document.getElementById('chatMessageInput');
  if (!input.value.trim() || !currentChatWith) return;
  await push(ref(database, `messages/${currentUserId}_${currentChatWith.id}`), {
    text: input.value,
    senderId: currentUserId,
    senderName: currentUsername,
    timestamp: serverTimestamp()
  });
  input.value = '';
});

document.getElementById('chatImageBtn')?.addEventListener('click', () => {
  document.getElementById('chatImageInput').click();
});

document.getElementById('chatImageInput')?.addEventListener('change', async (e) => {
  const file = e.target.files[0];
  if (!file || !currentChatWith) return;
  const imageRef = storageRef(storage, `chat_images/${Date.now()}_${file.name}`);
  await uploadBytes(imageRef, file);
  const imageUrl = await getDownloadURL(imageRef);
  await push(ref(database, `messages/${currentUserId}_${currentChatWith.id}`), {
    imageUrl: imageUrl,
    senderId: currentUserId,
    senderName: currentUsername,
    timestamp: serverTimestamp()
  });
  showToast('✅ تم إرسال الصورة');
});

// Profile grid (user videos)
async function updateProfileGrid() {
  const videosRef = ref(database, 'videos');
  const snapshot = await get(videosRef);
  const videos = snapshot.val();
  const grid = document.getElementById('profileGrid');
  grid.innerHTML = '';
  if (videos) {
    Object.entries(videos).forEach(([id, video]) => {
      if (video.userId === currentUserId) {
        const likesCount = video.likes ? Object.keys(video.likes).length : 0;
        const item = document.createElement('div');
        item.className = 'grid-item';
        item.style.backgroundImage = `url(${video.videoUrl})`;
        item.style.backgroundSize = 'cover';
        item.innerHTML = `<div class="view-count-badge"><i class="fas fa-heart"></i> ${likesCount}</div>`;
        item.onclick = () => {
          const idx = allVideos.findIndex(v => v.id === id);
          if (idx !== -1) {
            switchView('home');
            setTimeout(() => {
              const feed = document.getElementById('feedContainer');
              const items = feed.querySelectorAll('.video-item');
              if (items[idx]) items[idx].scrollIntoView({ behavior: 'smooth' });
            }, 100);
          }
        };
        grid.appendChild(item);
      }
    });
  }
  if (grid.children.length === 0) {
    grid.innerHTML = '<div style="color:white; text-align:center; grid-column:span 3;">لا توجد فيديوهات بعد</div>';
  }
}

// Load videos from Firebase
function loadVideos() {
  const videosRef = ref(database, 'videos');
  onValue(videosRef, (snapshot) => {
    const data = snapshot.val();
    if (data) {
      allVideos = Object.entries(data).map(([id, video]) => ({ id, ...video }));
      allVideos.sort((a, b) => (b.timestamp || 0) - (a.timestamp || 0));
      renderFeed(allVideos);
    } else {
      renderFeed([]);
    }
  });
}

// Switch views
function switchView(viewId) {
  document.querySelectorAll('.view').forEach(v => v.classList.remove('active'));
  document.getElementById(viewId + 'View').classList.add('active');
  document.querySelectorAll('.nav-icon').forEach(icon => icon.classList.remove('active'));
  document.querySelector(`.nav-icon[data-nav="${viewId}"]`).classList.add('active');
  if (viewId === 'chat') {
    loadChatUsers();
  }
  if (viewId === 'profile') {
    updateProfileGrid();
  }
}

// Load user data after authentication
async function loadUserData(user) {
  currentUser = user;
  currentUserId = user.uid;
  const userRef = ref(database, `users/${currentUserId}`);
  const snapshot = await get(userRef);
  if (snapshot.exists()) {
    currentUsername = snapshot.val().username;
    document.getElementById('profileUsername').innerText = currentUsername;
    if (user.email === ADMIN_EMAIL) {
      isAdmin = true;
      document.getElementById('adminIcon').style.display = 'flex';
    } else {
      isAdmin = false;
      document.getElementById('adminIcon').style.display = 'none';
    }
  } else {
    // Should not happen because we create user on registration, but just in case
    const username = prompt('أدخل اسم المستخدم الخاص بك:');
    if (username) {
      await set(userRef, {
        username: username,
        email: user.email,
        avatar: `https://ui-avatars.com/api/?background=ff0050&color=fff&name=${encodeURIComponent(username)}`,
        createdAt: serverTimestamp()
      });
      currentUsername = username;
      document.getElementById('profileUsername').innerText = username;
    }
  }
  loadVideos();
  loadChatUsers();
  switchView('home');
}

// Auth UI initialization
function initAuthUI() {
  const authModal = document.getElementById('authModal');
  const loginForm = document.getElementById('loginForm');
  const registerForm = document.getElementById('registerForm');
  const loginBtn = document.getElementById('loginBtn');
  const registerBtn = document.getElementById('registerBtn');
  const logoutBtn = document.getElementById('logoutBtn');
  const tabs = document.querySelectorAll('.auth-tab');

  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      tabs.forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
      if (tab.dataset.tab === 'login') {
        loginForm.classList.remove('hidden');
        registerForm.classList.add('hidden');
      } else {
        loginForm.classList.add('hidden');
        registerForm.classList.remove('hidden');
      }
    });
  });

  loginBtn.addEventListener('click', async () => {
    const email = document.getElementById('loginEmail').value.trim();
    const password = document.getElementById('loginPassword').value;
    const msgDiv = document.getElementById('loginMessage');
    if (!email || !password) {
      msgDiv.innerText = 'الرجاء إدخال البريد وكلمة المرور';
      return;
    }
    try {
      const userCred = await signInWithEmailAndPassword(auth, email, password);
      msgDiv.innerText = 'تم تسجيل الدخول بنجاح';
      setTimeout(() => {
        authModal.classList.add('hide');
        loadUserData(userCred.user);
      }, 500);
    } catch (error) {
      msgDiv.innerText = 'فشل الدخول: ' + error.message;
    }
  });

  registerBtn.addEventListener('click', async () => {
    const username = document.getElementById('regUsername').value.trim();
    const email = document.getElementById('regEmail').value.trim();
    const password = document.getElementById('regPassword').value;
    const msgDiv = document.getElementById('registerMessage');
    if (!username || !email || !password) {
      msgDiv.innerText = 'الرجاء ملء جميع الحقول';
      return;
    }
    try {
      const userCred = await createUserWithEmailAndPassword(auth, email, password);
      const uid = userCred.user.uid;
      await set(ref(database, `users/${uid}`), {
        username: username,
        email: email,
        avatar: `https://ui-avatars.com/api/?background=ff0050&color=fff&name=${encodeURIComponent(username)}`,
        createdAt: serverTimestamp()
      });
      msgDiv.innerText = 'تم إنشاء الحساب بنجاح';
      setTimeout(() => {
        authModal.classList.add('hide');
        loadUserData(userCred.user);
      }, 500);
    } catch (error) {
      msgDiv.innerText = 'فشل التسجيل: ' + error.message;
    }
  });

  logoutBtn.addEventListener('click', async () => {
    await signOut(auth);
    authModal.classList.remove('hide');
    // Reset UI
    document.getElementById('homeView').classList.remove('active');
    document.getElementById('profileView').classList.remove('active');
    document.getElementById('chatView').classList.remove('active');
    document.getElementById('homeView').classList.add('active');
    document.querySelectorAll('.nav-icon').forEach(icon => icon.classList.remove('active'));
    document.querySelector('.nav-icon[data-nav="home"]').classList.add('active');
    showToast('تم تسجيل الخروج');
  });
}

// Edit profile
document.getElementById('editProfileBtn')?.addEventListener('click', async () => {
  const newName = prompt('تعديل اسم المستخدم:', currentUsername);
  if (newName && newName.trim()) {
    currentUsername = newName.trim();
    await update(ref(database, `users/${currentUserId}`), { username: currentUsername });
    document.getElementById('profileUsername').innerText = currentUsername;
    showToast('✅ تم تحديث الاسم');
  }
});

// Admin icon click
document.getElementById('adminIcon')?.addEventListener('click', () => {
  if (isAdmin) showAdminPanel();
});
document.getElementById('closeAdmin')?.addEventListener('click', () => {
  document.getElementById('adminPanel').classList.remove('show');
});

// Navigation
document.querySelectorAll('.nav-icon').forEach(icon => {
  icon.addEventListener('click', () => {
    switchView(icon.getAttribute('data-nav'));
  });
});

// Start app: listen to auth state
onAuthStateChanged(auth, (user) => {
  if (user) {
    document.getElementById('authModal').classList.add('hide');
    loadUserData(user);
  } else {
    document.getElementById('authModal').classList.remove('hide');
  }
});

initAuthUI();
