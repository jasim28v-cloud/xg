// 👑 GKOM 2026 - Golden Configuration
// Firebase: gkom-604f1 | Cloudinary: dshgbhw4h
// ✨ PREMIUM: Notifications + Compact Grid + Delete Videos

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

// 👑 GKOM Settings
const ADMIN_EMAILS = ['jasim28v@gmail.com'];
const DICEBEAR_URL = "https://api.dicebear.com/7.x/big-smile/svg";
const COVER_COLORS = [
    "linear-gradient(135deg, #0a0a0a, #b8860b, #f59e0b)",
    "linear-gradient(135deg, #000000, #92400e, #fbbf24)",
    "linear-gradient(135deg, #1c1917, #b8860b, #fef3c7)",
    "linear-gradient(135deg, #0f0f0f, #d97706, #fbbf24)",
    "linear-gradient(135deg, #1a1a1a, #b45309, #f59e0b)",
    "linear-gradient(135deg, #0a0a0a, #78350f, #fbbf24)"
];

// 👑 App Info
const APP_NAME = "GKOM";
const APP_VERSION = "2026.1";
const PRIMARY_COLOR = "#f59e0b";
const SECONDARY_COLOR = "#fbbf24";

console.log('👑 %c'+APP_NAME+' v'+APP_VERSION+' Ready ✨', 'color: #f59e0b; font-size: 16px; font-weight: bold;');
