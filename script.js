// script.js
import { auth, db, storage } from './firebase-config.js';
import { 
  signInWithPopup, GoogleAuthProvider, signInWithEmailAndPassword, 
  createUserWithEmailAndPassword, onAuthStateChanged, signOut 
} from "firebase/auth";
import { 
  collection, addDoc, getDocs, query, orderBy, limit, where, 
  doc, getDoc, updateDoc, arrayUnion, arrayRemove, onSnapshot,
  serverTimestamp, Timestamp, setDoc, deleteDoc
} from "firebase/firestore";
import { ref, uploadBytes, getDownloadURL } from "firebase/storage";

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
let currentProfileUserId = null;

// ------------------- Auth UI -------------------
const showModal = (modal) => {
  modal.classList.add('open');
  modalOverlay.style.display = 'block';
};
const hideModals = () => {
  document.querySelectorAll('.modal-sheet').forEach(m => m.classList.remove('open'));
  modalOverlay.style.display = 'none';
};
modalOverlay.addEventListener('click', hideModals);

document.getElementById('googleSignIn').onclick = async () => {
  const provider = new GoogleAuthProvider();
  try {
    await signInWithPopup(auth, provider);
    hideModals();
  } catch (err) { alert(err.message); }
};
document.getElementById('emailAuthBtn').onclick = () => {
  document.getElementById('emailForm').style.display = 'block';
};
let isLoginMode = true;
document.getElementById('toggleAuthMode').onclick = () => {
  isLoginMode = !isLoginMode;
  document.getElementById('toggleAuthMode').innerText = isLoginMode ? "Create new account" : "Already have account? Sign in";
  document.getElementById('submitAuthBtn').innerText = isLoginMode ? "Sign In" : "Sign Up";
};
document.getElementById('submitAuthBtn').onclick = async () => {
  const email = document.getElementById('authEmail').value;
  const pwd = document.getElementById('authPassword').value;
  try {
    if (isLoginMode) await signInWithEmailAndPassword(auth, email, pwd);
    else await createUserWithEmailAndPassword(auth, email, pwd);
    hideModals();
  } catch (err) { alert(err.message); }
};
document.getElementById('skipInterests').onclick = () => hideModals();

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
  if (pageId === 'profile') loadProfile(currentUser?.uid);
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

// ------------------- Feed Loading -------------------
const loadFeed = async () => {
  const container = currentFeed === 'forYou' ? feedContainer : friendsFeedContainer;
  const q = query(collection(db, "videos"), orderBy("timestamp", "desc"), limit(30));
  const snapshot = await getDocs(q);
  container.innerHTML = '';
  for (const docSnap of snapshot.docs) {
    const vid = { id: docSnap.id, ...docSnap.data() };
    if (currentFeed === 'following' && currentUser && !vid.followersOnly) {
      // simple: check if user follows video author
      const userDoc = await getDoc(doc(db, "users", currentUser.uid));
      const following = userDoc.data()?.following || [];
      if (!following.includes(vid.userId)) continue;
    }
    renderVideoCard(container, vid);
  }
  // attach play observers
  attachVideoScroll();
};
const renderVideoCard = (container, video) => {
  const card = document.createElement('div');
  card.className = 'video-card';
  card.innerHTML = `
    <video src="${video.videoUrl}" poster="${video.thumbnailUrl || ''}" loop muted playsinline></video>
    <div class="video-overlay">
      <div class="video-info">
        <div class="video-username" data-userid="${video.userId}">@${video.username || 'user'}</div>
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
  // like logic
  card.querySelector('.like-btn').addEventListener('click', async (e) => {
    e.stopPropagation();
    if (!currentUser) { showModal(authSheet); return; }
    const vidId = card.querySelector('.like-btn').dataset.vid;
    const vidRef = doc(db, "videos", vidId);
    const vidSnap = await getDoc(vidRef);
    const likes = vidSnap.data().likes || 0;
    const likedBy = vidSnap.data().likedBy || [];
    if (likedBy.includes(currentUser.uid)) {
      await updateDoc(vidRef, { likes: likes-1, likedBy: arrayRemove(currentUser.uid) });
    } else {
      await updateDoc(vidRef, { likes: likes+1, likedBy: arrayUnion(currentUser.uid) });
    }
    loadFeed(); // refresh
  });
  card.querySelector('.comment-btn').addEventListener('click', () => {
    if (!currentUser) { showModal(authSheet); return; }
    activeVideoId = video.id;
    loadComments(video.id);
    showModal(commentsModal);
  });
};
const attachVideoScroll = () => {
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
};

// ------------------- Profile -------------------
const loadProfile = async (userId) => {
  if (!userId) return;
  currentProfileUserId = userId;
  const userDoc = await getDoc(doc(db, "users", userId));
  const userData = userDoc.data() || { username: 'user', avatar: '', bio: '', followers: [], following: [], likes: 0 };
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
        ${isOwnProfile ? '<button class="btn-outline" id="editProfileBtn">Edit Profile</button>' : `<button class="btn-outline" id="followBtn">${userData.followers?.includes(currentUser?.uid) ? 'Unfollow' : 'Follow'}</button>`}
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
    gridContainer.appendChild(div);
  });
  if (!isOwnProfile) document.getElementById('followBtn')?.addEventListener('click', async () => {
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
  document.querySelectorAll('.profile-tab').forEach(tab => {
    tab.addEventListener('click', () => {
      document.querySelectorAll('.profile-tab').forEach(t => t.classList.remove('active-tab'));
      tab.classList.add('active-tab');
      // switch grid content
    });
  });
};

// ------------------- Inbox (DM) -------------------
const loadInbox = async () => {
  if (!currentUser) { inboxContent.innerHTML = '<p style="padding:20px">Login to see messages</p>'; return; }
  const q = query(collection(db, "conversations"), where("participants", "array-contains", currentUser.uid));
  const snap = await getDocs(q);
  inboxContent.innerHTML = '<div class="inbox-list"><div class="active-status-row"><div class="story-circle"><img class="story-img" src="https://via.placeholder.com/52"/><div>Online</div></div></div>';
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
};
const openChat = async (convId, userId) => {
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
};

// ------------------- Comments -------------------
const loadComments = async (videoId) => {
  const commentsRef = collection(db, "videos", videoId, "comments");
  const q = query(commentsRef, orderBy("timestamp", "desc"));
  const snap = await getDocs(q);
  const commentsDiv = document.getElementById('commentsList');
  commentsDiv.innerHTML = '';
  snap.forEach(doc => {
    const c = doc.data();
    commentsDiv.innerHTML += `<div><strong>${c.username}</strong>: ${c.text}</div>`;
  });
};
postCommentBtn.onclick = async () => {
  const text = newCommentInput.value;
  if (!text || !activeVideoId) return;
  const user = currentUser;
  if (!user) return;
  await addDoc(collection(db, "videos", activeVideoId, "comments"), {
    text, userId: user.uid, username: user.displayName || user.email, timestamp: serverTimestamp()
  });
  const videoRef = doc(db, "videos", activeVideoId);
  await updateDoc(videoRef, { commentsCount: (await getDoc(videoRef)).data().commentsCount + 1 });
  loadComments(activeVideoId);
  newCommentInput.value = '';
};

// ------------------- Video Upload -------------------
uploadArea.addEventListener('click', () => videoFileInput.click());
videoFileInput.addEventListener('change', (e) => {
  const file = e.target.files[0];
  if (file) uploadArea.innerHTML = `<p>Selected: ${file.name}</p>`;
});
submitUpload.onclick = async () => {
  if (!currentUser) { alert('Login first'); hideModals(); showModal(authSheet); return; }
  const file = videoFileInput.files[0];
  if (!file) return;
  const caption = videoCaption.value;
  const storageRef = ref(storage, `videos/${currentUser.uid}/${Date.now()}_${file.name}`);
  await uploadBytes(storageRef, file);
  const videoUrl = await getDownloadURL(storageRef);
  await addDoc(collection(db, "videos"), {
    userId: currentUser.uid,
    username: currentUser.displayName || currentUser.email,
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
  const usersSnap = await getDocs(query(collection(db, "users"), limit(5)));
  const videosSnap = await getDocs(query(collection(db, "videos"), limit(5)));
  let html = '<h4>Users</h4>';
  usersSnap.forEach(doc => {
    const u = doc.data();
    if (u.username?.toLowerCase().includes(term)) html += `<div class="conv-item" data-uid="${doc.id}"><img class="conv-img" src="${u.avatar || 'https://via.placeholder.com/50'}"/> @${u.username}</div>`;
  });
  html += '<h4>Videos</h4>';
  videosSnap.forEach(doc => {
    const v = doc.data();
    if (v.caption?.toLowerCase().includes(term)) html += `<div>🎬 ${v.caption}</div>`;
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
    const userRef = doc(db, "users", user.uid);
    const userSnap = await getDoc(userRef);
    if (!userSnap.exists()) {
      await setDoc(userRef, {
        username: user.displayName || user.email.split('@')[0],
        email: user.email,
        avatar: user.photoURL || '',
        followers: [],
        following: [],
        likes: 0,
        bio: ''
      });
    }
    hideModals();
    loadFeed();
    if (pages.profile.classList.contains('active-page')) loadProfile(user.uid);
  } else {
    showModal(authSheet);
  }
});

// Top Tabs (For You / Following)
document.querySelectorAll('.tab-item').forEach(tab => {
  tab.addEventListener('click', () => {
    document.querySelectorAll('.tab-item').forEach(t => t.classList.remove('active'));
    tab.classList.add('active');
    currentFeed = tab.getAttribute('data-feed');
    loadFeed();
  });
});

// Live icon
liveIconBtn.onclick = () => alert("Live streaming coming soon");

// initial
loadFeed();
