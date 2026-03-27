import { auth, db, storage } from './firebase-config.js';
import { 
  signInWithPopup, GoogleAuthProvider, signInWithEmailAndPassword, 
  createUserWithEmailAndPassword, onAuthStateChanged, signOut 
} from "firebase/auth";
import { 
  collection, addDoc, getDocs, query, orderBy, limit, where, 
  doc, getDoc, updateDoc, arrayUnion, arrayRemove, onSnapshot,
  serverTimestamp, deleteDoc, setDoc, writeBatch
} from "firebase/firestore";
import { ref, uploadBytes, getDownloadURL, deleteObject } from "firebase/storage";

// ------------------- DOM Elements -------------------
const feedContainer = document.getElementById('feedContainer');
const friendsFeedContainer = document.getElementById('friendsFeedContainer');
const profilePage = document.getElementById('profilePage');
const inboxContent = document.getElementById('inboxContent');
const modalOverlay = document.getElementById('modalOverlay');
const authSheet = document.getElementById('authSheet');
const uploadModal = document.getElementById('uploadModal');
const searchModal = document.getElementById('searchModal');
const commentsModal = document.getElementById('commentsModal');
const openSearchBtn = document.getElementById('openSearchBtn');
const liveIconBtn = document.getElementById('liveIconBtn');
const videoFileInput = document.getElementById('videoFile');
const uploadArea = document.getElementById('uploadArea');
const submitUpload = document.getElementById('submitUpload');
const videoCaption = document.getElementById('videoCaption');
const searchInput = document.getElementById('searchInput');
const searchResultsDiv = document.getElementById('searchResults');
const newCommentInput = document.getElementById('newComment');
const postCommentBtn = document.getElementById('postCommentBtn');

let currentUser = null;
let currentFeed = 'forYou';
let activeVideoId = null;
let isAdmin = false;
let allVideos = []; // cache for feed

// ------------------- Helper Functions -------------------
const showModal = (modal) => { modal.classList.add('open'); modalOverlay.style.display = 'block'; };
const hideModals = () => { document.querySelectorAll('.modal-sheet').forEach(m => m.classList.remove('open')); modalOverlay.style.display = 'none'; };
modalOverlay.addEventListener('click', hideModals);

// ------------------- Auth -------------------
document.getElementById('googleSignIn').onclick = async () => {
  const provider = new GoogleAuthProvider();
  try {
    const result = await signInWithPopup(auth, provider);
    await ensureUserDocument(result.user);
    hideModals();
  } catch (err) { alert(err.message); }
};

let isLoginMode = true;
document.getElementById('toggleAuthMode').onclick = () => {
  isLoginMode = !isLoginMode;
  document.getElementById('toggleAuthMode').innerText = isLoginMode ? "Create new account" : "Already have account? Sign in";
  document.getElementById('submitAuthBtn').innerText = isLoginMode ? "Sign In" : "Sign Up";
};
document.getElementById('emailAuthBtn').onclick = () => { document.getElementById('emailForm').style.display = 'block'; };
document.getElementById('submitAuthBtn').onclick = async () => {
  const email = document.getElementById('authEmail').value;
  const pwd = document.getElementById('authPassword').value;
  try {
    let userCred;
    if (isLoginMode) userCred = await signInWithEmailAndPassword(auth, email, pwd);
    else userCred = await createUserWithEmailAndPassword(auth, email, pwd);
    await ensureUserDocument(userCred.user);
    hideModals();
  } catch (err) { alert(err.message); }
};

async function ensureUserDocument(user) {
  const userRef = doc(db, "users", user.uid);
  const userSnap = await getDoc(userRef);
  if (!userSnap.exists()) {
    await setDoc(userRef, {
      username: user.displayName || user.email.split('@')[0],
      email: user.email,
      avatar: user.photoURL || 'https://via.placeholder.com/96',
      followers: [],
      following: [],
      likes: 0,
      bio: '',
      createdAt: serverTimestamp()
    });
  }
}

// ------------------- Navigation -------------------
const pages = {
  home: document.getElementById('homePage'),
  friends: document.getElementById('friendsPage'),
  inbox: document.getElementById('inboxPage'),
  profile: document.getElementById('profilePage')
};
const navItems = document.querySelectorAll('.nav-item');
const setActivePage = (pageId) => {
  Object.keys(pages).forEach(p => pages[p].classList.remove('active-page'));
  pages[pageId].classList.add('active-page');
  navItems.forEach(item => item.classList.remove('active'));
  document.querySelector(`[data-nav="${pageId}"]`).classList.add('active');
  if (pageId === 'profile' && currentUser) loadProfile(currentUser.uid);
  if (pageId === 'inbox') loadInbox();
  if (pageId === 'home' || pageId === 'friends') loadFeed();
};
navItems.forEach(item => {
  item.addEventListener('click', () => {
    const nav = item.getAttribute('data-nav');
    if (nav === 'plus') {
      if (!currentUser) { showModal(authSheet); return; }
      showModal(uploadModal);
      return;
    }
    setActivePage(nav);
  });
});

// ------------------- Video Feed -------------------
async function loadFeed() {
  const container = currentFeed === 'forYou' ? feedContainer : friendsFeedContainer;
  if (!container) return;
  container.innerHTML = '<div class="loading">Loading videos...</div>';
  const q = query(collection(db, "videos"), orderBy("timestamp", "desc"), limit(50));
  const snapshot = await getDocs(q);
  allVideos = [];
  container.innerHTML = '';
  for (const docSnap of snapshot.docs) {
    const vid = { id: docSnap.id, ...docSnap.data() };
    if (currentFeed === 'following' && currentUser) {
      const userDoc = await getDoc(doc(db, "users", currentUser.uid));
      const following = userDoc.data()?.following || [];
      if (!following.includes(vid.userId)) continue;
    }
    allVideos.push(vid);
    renderVideoCard(container, vid);
  }
  attachVideoScroll();
}

function renderVideoCard(container, video) {
  const card = document.createElement('div');
  card.className = 'video-card';
  card.innerHTML = `
    <video src="${video.videoUrl}" poster="${video.thumbnailUrl || ''}" loop muted playsinline></video>
    <div class="video-overlay">
      <div class="video-info">
        <div class="video-username" data-userid="${video.userId}">
          <img src="${video.userAvatar || 'https://via.placeholder.com/32'}" style="width:32px;height:32px;border-radius:50%">
          @${video.username || 'user'}
        </div>
        <div class="video-caption">${video.caption || ''}</div>
      </div>
      <div class="video-actions">
        <div class="action-btn like-btn" data-vid="${video.id}"><i class="far fa-heart"></i><span>${video.likes || 0}</span></div>
        <div class="action-btn comment-btn" data-vid="${video.id}"><i class="far fa-comment"></i><span>${video.commentsCount || 0}</span></div>
        <div class="action-btn share-btn"><i class="fas fa-share"></i><span>Share</span></div>
      </div>
    </div>
  `;
  container.appendChild(card);

  // Like
  card.querySelector('.like-btn').addEventListener('click', async (e) => {
    e.stopPropagation();
    if (!currentUser) { showModal(authSheet); return; }
    const vidId = card.querySelector('.like-btn').dataset.vid;
    const vidRef = doc(db, "videos", vidId);
    const vidSnap = await getDoc(vidRef);
    const likedBy = vidSnap.data().likedBy || [];
    const isLiked = likedBy.includes(currentUser.uid);
    const newLikes = isLiked ? (vidSnap.data().likes - 1) : (vidSnap.data().likes + 1);
    await updateDoc(vidRef, {
      likes: newLikes,
      likedBy: isLiked ? arrayRemove(currentUser.uid) : arrayUnion(currentUser.uid)
    });
    loadFeed(); // refresh
  });

  // Comments
  card.querySelector('.comment-btn').addEventListener('click', () => {
    if (!currentUser) { showModal(authSheet); return; }
    activeVideoId = video.id;
    loadComments(video.id);
    showModal(commentsModal);
  });

  // Profile click
  card.querySelector('.video-username').addEventListener('click', (e) => {
    e.stopPropagation();
    const userId = card.querySelector('.video-username').dataset.userid;
    setActivePage('profile');
    loadProfile(userId);
  });
}

function attachVideoScroll() {
  const containers = [feedContainer, friendsFeedContainer];
  containers.forEach(cont => {
    if (!cont) return;
    const videos = cont.querySelectorAll('video');
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        const vid = entry.target;
        if (entry.isIntersecting) vid.play().catch(e=>console.log);
        else vid.pause();
      });
    }, { threshold: 0.6 });
    videos.forEach(v => observer.observe(v));
  });
}

// ------------------- Profile -------------------
async function loadProfile(userId) {
  if (!userId) return;
  const userDoc = await getDoc(doc(db, "users", userId));
  if (!userDoc.exists()) return;
  const userData = userDoc.data();
  const isOwnProfile = currentUser?.uid === userId;
  const videosQuery = query(collection(db, "videos"), where("userId", "==", userId), orderBy("timestamp", "desc"));
  const videosSnap = await getDocs(videosQuery);

  profilePage.innerHTML = `
    <div class="profile-header">
      <img class="avatar-large" src="${userData.avatar || 'https://via.placeholder.com/96'}" />
      <div class="stats-row">
        <div class="stat"><div class="stat-number">${userData.following?.length || 0}</div><div class="stat-label">Following</div></div>
        <div class="stat"><div class="stat-number">${userData.followers?.length || 0}</div><div class="stat-label">Followers</div></div>
        <div class="stat"><div class="stat-number">${userData.likes || 0}</div><div class="stat-label">Likes</div></div>
      </div>
      <div class="bio"><strong>@${userData.username}</strong><br>${userData.bio || ''}</div>
      <div class="action-buttons">
        ${isOwnProfile ? '<button class="btn-outline" id="editProfileBtn">Edit Profile</button>' : 
          `<button class="btn-outline" id="followBtn">${userData.followers?.includes(currentUser?.uid) ? 'Unfollow' : 'Follow'}</button>`}
        <button class="btn-outline" id="shareProfileBtn">Share Profile</button>
      </div>
    </div>
    <div class="tabs-profile">
      <div class="profile-tab active-tab" data-tab="grid"><i class="fas fa-th"></i></div>
      <div class="profile-tab" data-tab="liked"><i class="fas fa-heart"></i></div>
    </div>
    <div id="profileContent" class="video-grid"></div>
  `;

  const gridContainer = document.getElementById('profileContent');
  videosSnap.forEach(doc => {
    const vid = doc.data();
    const div = document.createElement('div');
    div.className = 'grid-video';
    div.innerHTML = `<video src="${vid.videoUrl}" muted></video><div class="play-icon-overlay"><i class="fas fa-play"></i> ${vid.likes || 0}</div>`;
    div.addEventListener('click', () => {
      // play video in feed? we'll just scroll to it in feed view
      setActivePage('home');
      setTimeout(() => {
        const targetVideo = Array.from(document.querySelectorAll('.video-card')).find(card => card.querySelector('video')?.src === vid.videoUrl);
        if (targetVideo) targetVideo.scrollIntoView({ behavior: 'smooth' });
      }, 100);
    });
    gridContainer.appendChild(div);
  });

  if (!isOwnProfile) {
    document.getElementById('followBtn')?.addEventListener('click', async () => {
      const userRef = doc(db, "users", userId);
      const currentUserRef = doc(db, "users", currentUser.uid);
      const isFollowing = userData.followers?.includes(currentUser.uid);
      if (isFollowing) {
        await updateDoc(userRef, { followers: arrayRemove(currentUser.uid) });
        await updateDoc(currentUserRef, { following: arrayRemove(userId) });
      } else {
        await updateDoc(userRef, { followers: arrayUnion(currentUser.uid) });
        await updateDoc(currentUserRef, { following: arrayUnion(userId) });
      }
      loadProfile(userId);
    });
  }

  // Admin Panel
  if (isAdmin && isOwnProfile) {
    const adminPanel = document.createElement('div');
    adminPanel.className = 'admin-panel';
    adminPanel.innerHTML = `
      <h3 style="margin:20px; color:#fe2c55;">🛡️ Admin Dashboard</h3>
      <div class="admin-section">
        <h4>👥 Users Management</h4>
        <div id="adminUserList" class="admin-list"></div>
      </div>
      <div class="admin-section">
        <h4>🎬 Videos Management</h4>
        <div id="adminVideoList" class="admin-list"></div>
      </div>
    `;
    profilePage.appendChild(adminPanel);
    loadAllUsersForAdmin();
    loadAllVideosForAdmin();
  }
}

async function loadAllUsersForAdmin() {
  const usersSnap = await getDocs(collection(db, "users"));
  const container = document.getElementById('adminUserList');
  if (!container) return;
  container.innerHTML = '';
  usersSnap.forEach(docSnap => {
    const userData = docSnap.data();
    const userDiv = document.createElement('div');
    userDiv.className = 'admin-item';
    userDiv.innerHTML = `
      <span>${userData.username} (${userData.email})</span>
      <button class="delete-user-btn" data-uid="${docSnap.id}">Delete</button>
    `;
    container.appendChild(userDiv);
  });
  document.querySelectorAll('.delete-user-btn').forEach(btn => {
    btn.addEventListener('click', async () => {
      const uid = btn.dataset.uid;
      if (confirm(`Delete user ${uid} and all their videos?`)) {
        // Delete user's videos from Firestore and Storage
        const videosSnap = await getDocs(query(collection(db, "videos"), where("userId", "==", uid)));
        for (const vidDoc of videosSnap.docs) {
          const videoData = vidDoc.data();
          if (videoData.videoUrl) {
            try {
              const storageRef = ref(storage, videoData.videoUrl);
              await deleteObject(storageRef);
            } catch(e) { console.log("Storage delete error", e); }
          }
          await deleteDoc(doc(db, "videos", vidDoc.id));
        }
        // Delete user document
        await deleteDoc(doc(db, "users", uid));
        loadAllUsersForAdmin();
        loadAllVideosForAdmin();
        loadFeed(); // refresh feed
      }
    });
  });
}

async function loadAllVideosForAdmin() {
  const videosSnap = await getDocs(collection(db, "videos"));
  const container = document.getElementById('adminVideoList');
  if (!container) return;
  container.innerHTML = '';
  videosSnap.forEach(docSnap => {
    const vid = docSnap.data();
    const videoDiv = document.createElement('div');
    videoDiv.className = 'admin-item';
    videoDiv.innerHTML = `
      <span>${vid.username}: ${vid.caption || 'no caption'}</span>
      <button class="delete-video-btn" data-vid="${docSnap.id}">Delete</button>
    `;
    container.appendChild(videoDiv);
  });
  document.querySelectorAll('.delete-video-btn').forEach(btn => {
    btn.addEventListener('click', async () => {
      const vidId = btn.dataset.vid;
      if (confirm('Delete this video?')) {
        const vidRef = doc(db, "videos", vidId);
        const vidSnap = await getDoc(vidRef);
        if (vidSnap.exists() && vidSnap.data().videoUrl) {
          try {
            const storageRef = ref(storage, vidSnap.data().videoUrl);
            await deleteObject(storageRef);
          } catch(e) {}
        }
        await deleteDoc(vidRef);
        loadAllVideosForAdmin();
        loadFeed();
      }
    });
  });
}

// ------------------- Inbox (DM) -------------------
async function loadInbox() {
  if (!currentUser) { inboxContent.innerHTML = '<p style="padding:20px">Login to see messages</p>'; return; }
  const q = query(collection(db, "conversations"), where("participants", "array-contains", currentUser.uid));
  const snap = await getDocs(q);
  inboxContent.innerHTML = '<div class="inbox-list"><div class="active-status-row">📱 Your conversations</div>';
  for (const docSnap of snap.docs) {
    const conv = docSnap.data();
    const otherId = conv.participants.find(p => p !== currentUser.uid);
    const otherUser = await getDoc(doc(db, "users", otherId));
    const otherData = otherUser.data();
    inboxContent.innerHTML += `
      <div class="conv-item" data-conv="${docSnap.id}" data-user="${otherId}">
        <img class="conv-img" src="${otherData?.avatar || 'https://via.placeholder.com/50'}" />
        <div class="conv-info"><div class="conv-name">${otherData?.username}</div><div class="conv-preview">${conv.lastMessage || ''}</div></div>
      </div>
    `;
  }
  document.querySelectorAll('.conv-item').forEach(el => {
    el.addEventListener('click', () => openChat(el.dataset.conv, el.dataset.user));
  });
}

async function openChat(convId, userId) {
  const userDoc = await getDoc(doc(db, "users", userId));
  const username = userDoc.data()?.username;
  const chatModal = document.createElement('div');
  chatModal.className = 'modal-sheet open';
  chatModal.style.zIndex = '1100';
  chatModal.innerHTML = `
    <div class="chat-header"><i class="fas fa-arrow-left" id="closeChat"></i><strong>${username}</strong></div>
    <div id="chatMessages" style="height:60vh; overflow-y:auto; padding:12px;"></div>
    <div style="display:flex; gap:8px; padding:12px;"><input id="chatMsgInput" placeholder="Message..." style="flex:1"/><button id="sendMsgBtn">Send</button></div>
  `;
  document.body.appendChild(chatModal);
  document.getElementById('closeChat').onclick = () => chatModal.remove();
  const messagesRef = collection(db, "conversations", convId, "messages");
  onSnapshot(query(messagesRef, orderBy("timestamp")), (snap) => {
    const msgsDiv = document.getElementById('chatMessages');
    msgsDiv.innerHTML = '';
    snap.forEach(doc => {
      const msg = doc.data();
      const div = document.createElement('div');
      div.style.textAlign = msg.senderId === currentUser.uid ? 'right' : 'left';
      div.style.margin = '8px';
      div.innerHTML = `<div style="background:${msg.senderId === currentUser.uid ? '#fe2c55' : '#2c2c2c'}; padding:8px 12px; border-radius:20px; display:inline-block">${msg.text}</div>`;
      msgsDiv.appendChild(div);
    });
  });
  document.getElementById('sendMsgBtn').onclick = async () => {
    const text = document.getElementById('chatMsgInput').value;
    if (!text.trim()) return;
    await addDoc(messagesRef, { text, senderId: currentUser.uid, timestamp: serverTimestamp() });
    await updateDoc(doc(db, "conversations", convId), { lastMessage: text, lastUpdated: serverTimestamp() });
    document.getElementById('chatMsgInput').value = '';
  };
}

// ------------------- Comments -------------------
async function loadComments(videoId) {
  const commentsRef = collection(db, "videos", videoId, "comments");
  const q = query(commentsRef, orderBy("timestamp", "desc"));
  const snap = await getDocs(q);
  const commentsDiv = document.getElementById('commentsList');
  commentsDiv.innerHTML = '';
  snap.forEach(doc => {
    const c = doc.data();
    commentsDiv.innerHTML += `<div><strong>${c.username}</strong>: ${c.text}</div>`;
  });
}
postCommentBtn.onclick = async () => {
  const text = newCommentInput.value;
  if (!text || !activeVideoId || !currentUser) return;
  await addDoc(collection(db, "videos", activeVideoId, "comments"), {
    text, userId: currentUser.uid, username: currentUser.displayName || currentUser.email, timestamp: serverTimestamp()
  });
  const videoRef = doc(db, "videos", activeVideoId);
  const videoSnap = await getDoc(videoRef);
  const newCount = (videoSnap.data().commentsCount || 0) + 1;
  await updateDoc(videoRef, { commentsCount: newCount });
  loadComments(activeVideoId);
  newCommentInput.value = '';
};

// ------------------- Video Upload -------------------
uploadArea.addEventListener('click', () => videoFileInput.click());
videoFileInput.addEventListener('change', (e) => {
  const file = e.target.files[0];
  if (file) uploadArea.innerHTML = `<p>Selected: ${file.name}</p><i class="fas fa-check-circle"></i>`;
});
submitUpload.onclick = async () => {
  if (!currentUser) { alert('Login first'); hideModals(); showModal(authSheet); return; }
  const file = videoFileInput.files[0];
  if (!file) return alert('Select a video');
  const caption = videoCaption.value;
  const storageRef = ref(storage, `videos/${currentUser.uid}/${Date.now()}_${file.name}`);
  await uploadBytes(storageRef, file);
  const videoUrl = await getDownloadURL(storageRef);
  const userDoc = await getDoc(doc(db, "users", currentUser.uid));
  const userData = userDoc.data();
  await addDoc(collection(db, "videos"), {
    userId: currentUser.uid,
    username: userData?.username || currentUser.displayName || currentUser.email,
    userAvatar: userData?.avatar || currentUser.photoURL || 'https://via.placeholder.com/32',
    videoUrl,
    caption,
    likes: 0,
    commentsCount: 0,
    timestamp: serverTimestamp(),
    likedBy: []
  });
  hideModals();
  loadFeed();
};

// ------------------- Search -------------------
openSearchBtn.onclick = () => showModal(searchModal);
searchInput.addEventListener('input', async () => {
  const term = searchInput.value.toLowerCase();
  if (!term) { searchResultsDiv.innerHTML = ''; return; }
  const usersSnap = await getDocs(collection(db, "users"));
  const videosSnap = await getDocs(collection(db, "videos"));
  let html = '<h4>Users</h4>';
  usersSnap.forEach(doc => {
    const u = doc.data();
    if (u.username?.toLowerCase().includes(term)) html += `<div class="conv-item search-result" data-uid="${doc.id}"><img class="conv-img" src="${u.avatar || 'https://via.placeholder.com/50'}"/> @${u.username}</div>`;
  });
  html += '<h4>Videos</h4>';
  videosSnap.forEach(doc => {
    const v = doc.data();
    if (v.caption?.toLowerCase().includes(term)) html += `<div class="conv-item" data-vid="${doc.id}">🎬 ${v.caption.substring(0,40)}</div>`;
  });
  searchResultsDiv.innerHTML = html;
  document.querySelectorAll('[data-uid]').forEach(el => {
    el.addEventListener('click', () => {
      setActivePage('profile');
      loadProfile(el.dataset.uid);
      hideModals();
    });
  });
});

// ------------------- Auth State -------------------
onAuthStateChanged(auth, async (user) => {
  currentUser = user;
  if (user) {
    isAdmin = user.email === 'jasim28v@gmail.com';
    await ensureUserDocument(user);
    hideModals();
    loadFeed();
    if (pages.profile.classList.contains('active-page')) loadProfile(user.uid);
  } else {
    showModal(authSheet);
  }
});

// Top Tabs
document.querySelectorAll('.tab-item').forEach(tab => {
  tab.addEventListener('click', () => {
    document.querySelectorAll('.tab-item').forEach(t => t.classList.remove('active'));
    tab.classList.add('active');
    currentFeed = tab.getAttribute('data-feed');
    loadFeed();
  });
});

liveIconBtn.onclick = () => alert("Live streaming coming soon");

// Initial load
loadFeed();
