// 👑 MNAENCA 2026 - Gold Configuration
// Firebase: gkom-604f1 | Cloudinary: dshgbhw4h
// ✨ PREMIUM: Notifications + Compact Grid + Delete Videos + PWA

const firebaseConfig = {
    apiKey: "AIzaSyD8AO7Yh8QjuB3ARJUIcHkuuI3euO4ebDw",
    authDomain: "gkom-604f1.firebaseapp.com",
    databaseURL: "https://gkom-604f1-default-rtdb.firebaseio.com",
    projectId: "gkom-604f1",
    storageBucket: "gkom-604f1.firebasestorage.app",
    messagingSenderId: "1034101313659",
    appId: "1:1034101313659:web:18799c20f25cd9965c92de",
    measurementId: "G-R45218BLT7"
};

// Initialize Firebase
firebase.initializeApp(firebaseConfig);
const auth = firebase.auth();
const db = firebase.database();

// Cloudinary Configuration
const CLOUD_NAME = "dshgbhw4h";
const UPLOAD_PRESET = "fk4_gk";

// 👑 MNAENCA Settings
const ADMIN_EMAILS = ['jasim28v@gmail.com'];
const DICEBEAR_URL = "https://api.dicebear.com/7.x/big-smile/svg";
const COVER_COLORS = [
    "linear-gradient(135deg, #5c3a00, #8b6508, #d4a017)",
    "linear-gradient(135deg, #3a2501, #6b4c00, #b8860b)",
    "linear-gradient(135deg, #4a3000, #7a5c00, #c99700)",
    "linear-gradient(135deg, #b8860b, #d4a017, #f0c75e)",
    "linear-gradient(135deg, #8b6508, #b8860b, #ffd700)",
    "linear-gradient(135deg, #2b1c01, #5c3a00, #d4a017)"
];

// 👑 App Info
const APP_NAME = "MNAENCA GOLD";
const APP_VERSION = "2026.1";
const PRIMARY_COLOR = "#d4a017";
const SECONDARY_COLOR = "#f0c75e";

console.log('👑 %c'+APP_NAME+' v'+APP_VERSION+' Ready ✨', 'color: #d4a017; font-size: 16px; font-weight: bold;');

// Register Service Worker for PWA
if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/service-worker.js')
        .then(reg => console.log('👑 SW registered'))
        .catch(err => console.log('SW failed', err));
}
