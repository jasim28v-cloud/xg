#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════╗
║                                                            ║
║  👑  GKOM 2026 - GOLDEN ULTRA EDITION  👑             ║
║     Ultimate Version - 9 Files - 2500+ Lines               ║
║                                                            ║
║  🔥  Firebase: gkom-604f1                                 ║
║  ☁️   Cloudinary: dshgbhw4h / fk4_gk                      ║
║  👑  Admin: jasim28v@gmail.com                            ║
║  👾  Avatars: DiceBear Big Smile (Random)                  ║
║  💎  Design: Golden Glass Morphism                        ║
║                                                            ║
║  ✨  PREMIUM FEATURES:                                     ║
║     • 🔔 Notification System (Working 100%)              ║
║     • 🎬 Compact Video Grid with Description              ║
║     • 🗑️  Delete Videos from Admin Panel                  ║
║     • 🖤 Parallax Cover                                   ║
║     • 💎 Glass Morphism Dark Layers                       ║
║     • 👑 Golden Diamond Story Rings                       ║
║     • ✨ Golden/Amber Glow Effects                         ║
║     • 🌟 Smooth In-App Viewer (No Popups!)               ║
║     • 📱 Floating Bottom Nav                              ║
║     • توثيق + حظر + حذف فيديوهات                          ║
║                                                            ║
╚══════════════════════════════════════════════════════════════╝
"""

import os
import sys
import shutil

# ═══════════════════════════════════════════════════════════
# 👑 CONFIGURATION - الإعدادات
# ═══════════════════════════════════════════════════════════

FIREBASE_CONFIG = {
    "apiKey": "AIzaSyD8AO7Yh8QjuB3ARJUIcHkuuI3euO4ebDw",
    "authDomain": "gkom-604f1.firebaseapp.com",
    "databaseURL": "https://gkom-604f1-default-rtdb.firebaseio.com",
    "projectId": "gkom-604f1",
    "storageBucket": "gkom-604f1.firebasestorage.app",
    "messagingSenderId": "1034101313659",
    "appId": "1:1034101313659:web:18799c20f25cd9965c92de",
    "measurementId": "G-R45218BLT7"
}

CLOUD_NAME = "dshgbhw4h"
UPLOAD_PRESET = "fk4_gk"
ADMIN_EMAILS_JS = "['jasim28v@gmail.com']"
DICEBEAR_URL = "https://api.dicebear.com/7.x/big-smile/svg"

# 👑 Golden Ultra Palette
GOLDEN_COLORS_JS = """[
    "linear-gradient(135deg, #0a0a0a, #b8860b, #f59e0b)",
    "linear-gradient(135deg, #000000, #92400e, #fbbf24)",
    "linear-gradient(135deg, #1c1917, #b8860b, #fef3c7)",
    "linear-gradient(135deg, #0f0f0f, #d97706, #fbbf24)",
    "linear-gradient(135deg, #1a1a1a, #b45309, #f59e0b)",
    "linear-gradient(135deg, #0a0a0a, #78350f, #fbbf24)"
]"""

# ═══════════════════════════════════════════════════════════
# 👑 UTILITY - دوال مساعدة
# ═══════════════════════════════════════════════════════════

TOTAL_LINES = 0

def write(filename, content):
    """حفظ ملف وحساب عدد الأسطر"""
    global TOTAL_LINES
    os.makedirs(os.path.dirname(filename) if os.path.dirname(filename) else '.', exist_ok=True)
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    lines = content.count('\n') + 1
    TOTAL_LINES += lines
    print(f"  ✅ {filename} ({lines} سطر)")

def section(title):
    """طباعة عنوان القسم"""
    print(f"\n{'='*60}")
    print(f"  👑 {title}")
    print(f"{'='*60}")

# ═══════════════════════════════════════════════════════════
# 👑 1. firebase-config.js
# ═══════════════════════════════════════════════════════════

def build_config():
    return f"""// 👑 GKOM 2026 - Golden Configuration
// Firebase: gkom-604f1 | Cloudinary: dshgbhw4h
// ✨ PREMIUM: Notifications + Compact Grid + Delete Videos

const firebaseConfig = {{
    apiKey: "{FIREBASE_CONFIG['apiKey']}",
    authDomain: "{FIREBASE_CONFIG['authDomain']}",
    databaseURL: "{FIREBASE_CONFIG['databaseURL']}",
    projectId: "{FIREBASE_CONFIG['projectId']}",
    storageBucket: "{FIREBASE_CONFIG['storageBucket']}",
    messagingSenderId: "{FIREBASE_CONFIG['messagingSenderId']}",
    appId: "{FIREBASE_CONFIG['appId']}",
    measurementId: "{FIREBASE_CONFIG['measurementId']}"
}};

// Initialize Firebase
firebase.initializeApp(firebaseConfig);
const auth = firebase.auth();
const db = firebase.database();

// Cloudinary Configuration
const CLOUD_NAME = "{CLOUD_NAME}";
const UPLOAD_PRESET = "{UPLOAD_PRESET}";

// 👑 GKOM Settings
const ADMIN_EMAILS = {ADMIN_EMAILS_JS};
const DICEBEAR_URL = "{DICEBEAR_URL}";
const COVER_COLORS = {GOLDEN_COLORS_JS};

// 👑 App Info
const APP_NAME = "GKOM";
const APP_VERSION = "2026.1";
const PRIMARY_COLOR = "#f59e0b";
const SECONDARY_COLOR = "#fbbf24";

console.log('👑 %c'+APP_NAME+' v'+APP_VERSION+' Ready ✨', 'color: #f59e0b; font-size: 16px; font-weight: bold;');
"""

# ═══════════════════════════════════════════════════════════
# 👑 2. auth.html - تسجيل الدخول والاشتراك
# ═══════════════════════════════════════════════════════════

def build_auth():
    return """<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
    <title>👑 GKOM | دخول</title>
    <script src="https://www.gstatic.com/firebasejs/10.7.0/firebase-app-compat.js"></script>
    <script src="https://www.gstatic.com/firebasejs/10.7.0/firebase-database-compat.js"></script>
    <script src="https://www.gstatic.com/firebasejs/10.7.0/firebase-auth-compat.js"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <style>
        *{margin:0;padding:0;box-sizing:border-box}
        body{
            min-height:100vh;
            background:radial-gradient(ellipse at top, #1c1917, #0a0a0a, #000);
            display:flex;align-items:center;justify-content:center;
            font-family:'Segoe UI',sans-serif;overflow:hidden;
        }
        .bg-orb{
            position:fixed;border-radius:50%;filter:blur(130px);opacity:0.3;
            animation:orbFloat 20s infinite alternate;
        }
        .bg-orb:nth-child(1){width:400px;height:400px;background:#b8860b;top:-100px;left:-100px}
        .bg-orb:nth-child(2){width:350px;height:350px;background:#fbbf24;bottom:-100px;right:-100px;animation-delay:5s}
        .bg-orb:nth-child(3){width:300px;height:300px;background:#f59e0b;top:50%;left:50%;animation-delay:10s}
        @keyframes orbFloat{0%{transform:translate(0,0) scale(1)}100%{transform:translate(50px,-50px) scale(1.3)}}

        .card{
            position:relative;z-index:1;width:90%;max-width:420px;
            background:rgba(181,136,11,0.03);
            backdrop-filter:blur(40px);-webkit-backdrop-filter:blur(40px);
            border-radius:32px;padding:36px 24px;
            border:1px solid rgba(245,158,11,0.2);
            box-shadow:0 30px 70px rgba(245,158,11,0.1),inset 0 0 30px rgba(245,158,11,0.02);
            animation:fadeUp 0.8s ease;
        }
        @keyframes fadeUp{from{opacity:0;transform:translateY(40px)}to{opacity:1;transform:translateY(0)}}

        .logo{
            width:70px;height:70px;margin:0 auto 20px;
            background:linear-gradient(135deg, rgba(184,134,11,0.3), rgba(251,191,36,0.3));
            border-radius:20px;display:flex;align-items:center;justify-content:center;
            font-size:36px;border:1px solid rgba(245,158,11,0.2);
            box-shadow:0 15px 40px rgba(245,158,11,0.3);
            animation:logoGlow 3s ease-in-out infinite;
        }
        @keyframes logoGlow{0%,100%{box-shadow:0 15px 40px rgba(245,158,11,0.3)}50%{box-shadow:0 15px 60px rgba(251,191,36,0.7)}}
        h1{text-align:center;font-size:36px;font-weight:900;background:linear-gradient(to bottom, #fff, #fbbf24);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:4px}
        .sub{text-align:center;color:rgba(255,255,255,0.4);font-size:13px;margin-bottom:20px}

        .tabs{display:flex;gap:4px;background:rgba(184,134,11,0.06);border-radius:40px;padding:4px;margin-bottom:24px}
        .tab{flex:1;padding:12px;background:none;border:none;color:rgba(255,255,255,0.5);cursor:pointer;border-radius:40px;font-size:14px;transition:all 0.3s;font-weight:500}
        .tab.active{background:linear-gradient(135deg, #b8860b, #fbbf24);color:#fff;box-shadow:0 8px 20px rgba(245,158,11,0.4)}

        .form{display:none;animation:fadeIn 0.4s ease}
        .form.active{display:block}
        @keyframes fadeIn{from{opacity:0}to{opacity:1}}

        input{
            width:100%;padding:15px 18px;margin:8px 0;
            border-radius:50px;background:rgba(184,134,11,0.04);
            border:1px solid rgba(245,158,11,0.15);color:#fff;
            font-size:14px;outline:none;transition:all 0.4s;
        }
        input:focus{border-color:rgba(245,158,11,0.6);box-shadow:0 0 20px rgba(245,158,11,0.1);background:rgba(184,134,11,0.08)}
        input::placeholder{color:rgba(255,255,255,0.3)}

        button{
            width:100%;padding:15px;margin-top:18px;
            background:linear-gradient(135deg, #b8860b, #fbbf24);
            border:none;border-radius:50px;color:#fff;
            font-weight:bold;font-size:15px;cursor:pointer;
            transition:all 0.3s;box-shadow:0 10px 30px rgba(245,158,11,0.4);
        }
        button:hover{transform:translateY(-2px);box-shadow:0 20px 40px rgba(245,158,11,0.6)}
        button:active{transform:scale(0.97)}
        button:disabled{opacity:0.5;pointer-events:none}

        .msg{text-align:center;color:#fca5a5;font-size:13px;margin-top:12px;min-height:20px}
        .msg.success{color:#4ade80}
    </style>
</head>
<body>
    <div class="bg-orb"></div><div class="bg-orb"></div><div class="bg-orb"></div>

    <div class="card">
        <div class="logo">👑</div>
        <h1>GKOM</h1>
        <p class="sub">Golden Ultra 2026 ✨</p>

        <div class="tabs">
            <button class="tab active" id="tabLogin" onclick="switchTab('login')"><i class="fas fa-sign-in-alt"></i> دخول</button>
            <button class="tab" id="tabRegister" onclick="switchTab('register')"><i class="fas fa-user-plus"></i> اشتراك</button>
        </div>

        <div id="formLogin" class="form active">
            <input type="email" id="loginEmail" placeholder="📧 البريد الإلكتروني" autocomplete="email">
            <input type="password" id="loginPass" placeholder="🔒 كلمة المرور" autocomplete="current-password">
            <button id="btnLogin" onclick="doLogin()"><i class="fas fa-arrow-right-to-bracket"></i> تسجيل الدخول</button>
            <div class="msg" id="loginMsg"></div>
        </div>

        <div id="formRegister" class="form">
            <input type="text" id="regName" placeholder="👤 اسم المستخدم" autocomplete="username">
            <input type="email" id="regEmail" placeholder="📧 البريد الإلكتروني" autocomplete="email">
            <input type="password" id="regPass" placeholder="🔒 كلمة المرور (6 أحرف على الأقل)" autocomplete="new-password">
            <button id="btnRegister" onclick="doRegister()"><i class="fas fa-gem"></i> إنشاء حساب</button>
            <div class="msg" id="regMsg"></div>
        </div>
    </div>

    <script src="firebase-config.js"></script>
    <script>
        function switchTab(type){
            document.getElementById('tabLogin').classList.remove('active');
            document.getElementById('tabRegister').classList.remove('active');
            document.getElementById('formLogin').classList.remove('active');
            document.getElementById('formRegister').classList.remove('active');
            document.getElementById('loginMsg').innerText = '';
            document.getElementById('regMsg').innerText = '';
            if(type === 'login'){
                document.getElementById('tabLogin').classList.add('active');
                document.getElementById('formLogin').classList.add('active');
            } else {
                document.getElementById('tabRegister').classList.add('active');
                document.getElementById('formRegister').classList.add('active');
            }
        }

        async function doLogin(){
            const email = document.getElementById('loginEmail').value.trim();
            const password = document.getElementById('loginPass').value;
            const msg = document.getElementById('loginMsg');
            const btn = document.getElementById('btnLogin');
            if(!email || !password){ msg.innerText = '❌ الرجاء ملء جميع الحقول'; return; }
            btn.disabled = true; btn.innerHTML = '⏳ جاري الدخول...'; msg.innerText = ''; msg.className = 'msg';
            try {
                await auth.signInWithEmailAndPassword(email, password);
                window.location.replace('index.html');
            } catch(error) {
                btn.disabled = false; btn.innerHTML = '<i class="fas fa-arrow-right-to-bracket"></i> تسجيل الدخول';
                switch(error.code) {
                    case 'auth/user-not-found': msg.innerText = '❌ لا يوجد حساب بهذا البريد'; break;
                    case 'auth/wrong-password': case 'auth/invalid-credential': msg.innerText = '❌ كلمة المرور غير صحيحة'; break;
                    case 'auth/invalid-email': msg.innerText = '❌ بريد إلكتروني غير صالح'; break;
                    case 'auth/too-many-requests': msg.innerText = '❌ محاولات كثيرة، حاول لاحقاً'; break;
                    default: msg.innerText = '❌ خطأ: ' + error.message;
                }
            }
        }

        async function doRegister(){
            const username = document.getElementById('regName').value.trim();
            const email = document.getElementById('regEmail').value.trim();
            const password = document.getElementById('regPass').value;
            const msg = document.getElementById('regMsg');
            const btn = document.getElementById('btnRegister');
            if(!username || !email || !password){ msg.innerText = '❌ الرجاء ملء جميع الحقول'; return; }
            if(username.length < 3){ msg.innerText = '❌ اسم المستخدم 3 أحرف على الأقل'; return; }
            if(password.length < 6){ msg.innerText = '❌ كلمة المرور 6 أحرف على الأقل'; return; }
            if(!email.includes('@') || !email.includes('.')){ msg.innerText = '❌ بريد إلكتروني غير صالح'; return; }
            btn.disabled = true; btn.innerHTML = '⏳ جاري إنشاء الحساب...'; msg.innerText = ''; msg.className = 'msg';
            try {
                const userCredential = await auth.createUserWithEmailAndPassword(email, password);
                const uid = userCredential.user.uid;
                const avatarUrl = DICEBEAR_URL + '?seed=' + uid;
                const coverColor = COVER_COLORS[Math.floor(Math.random() * COVER_COLORS.length)];
                const userData = {
                    username: username, email: email, bio: '',
                    website: '', location: '', contactEmail: '',
                    avatarUrl: avatarUrl, hasCustomAvatar: false,
                    coverImageUrl: '', hasCustomCover: false,
                    coverColor: coverColor, followers: {}, following: {},
                    totalLikes: 0, isVerified: false, verifiedAt: null, verifiedBy: null,
                    banned: false, createdAt: Date.now(), lastSeen: Date.now()
                };
                await db.ref('users/' + uid).set(userData);
                msg.innerText = '✅ تم إنشاء الحساب بنجاح! جاري التوجيه...';
                msg.className = 'msg success';
                setTimeout(() => { window.location.replace('index.html'); }, 800);
            } catch(error) {
                btn.disabled = false; btn.innerHTML = '<i class="fas fa-gem"></i> إنشاء حساب'; msg.className = 'msg';
                switch(error.code) {
                    case 'auth/email-already-in-use': msg.innerText = '❌ البريد الإلكتروني مستخدم بالفعل'; break;
                    case 'auth/weak-password': msg.innerText = '❌ كلمة المرور ضعيفة جداً'; break;
                    case 'auth/invalid-email': msg.innerText = '❌ بريد إلكتروني غير صالح'; break;
                    case 'auth/operation-not-allowed': msg.innerText = '❌ التسجيل غير مفعل، راجع إعدادات Firebase'; break;
                    default: msg.innerText = '❌ خطأ: ' + (error.message || 'غير معروف');
                }
            }
        }

        document.querySelectorAll('input').forEach(input => {
            input.addEventListener('keydown', function(e) {
                if(e.key === 'Enter') {
                    e.preventDefault();
                    if(document.getElementById('formLogin').classList.contains('active')) { doLogin(); }
                    else { doRegister(); }
                }
            });
        });

        auth.onAuthStateChanged(user => {
            if(user) { window.location.replace('index.html'); }
        });

        console.log('👑 GKOM Auth Ready');
    </script>
</body>
</html>"""

# ═══════════════════════════════════════════════════════════
# 👑 3. index.html - الرئيسية
# ═══════════════════════════════════════════════════════════

def build_index():
    return """<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
    <title>👑 GKOM | الرئيسية</title>
    <script src="https://www.gstatic.com/firebasejs/10.7.0/firebase-app-compat.js"></script>
    <script src="https://www.gstatic.com/firebasejs/10.7.0/firebase-database-compat.js"></script>
    <script src="https://www.gstatic.com/firebasejs/10.7.0/firebase-auth-compat.js"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <style>
        :root{
            --glass:rgba(184,134,11,0.03);
            --border:rgba(245,158,11,0.12);
            --accent:#f59e0b;
            --accent2:#fbbf24;
            --bg:#0a0a0a;
        }
        *{margin:0;padding:0;box-sizing:border-box}
        body{
            font-family:'Segoe UI',sans-serif;
            background:var(--bg);
            color:#fff;
            height:100vh;overflow:hidden;
            -webkit-tap-highlight-color:transparent;
            user-select:none;
        }

        #loaderScreen{
            position:fixed;inset:0;z-index:9999;
            background:radial-gradient(ellipse at top, #1c1917, #0a0a0a, #000);
            display:flex;align-items:center;justify-content:center;
            flex-direction:column;gap:16px;
        }
        .spinner-big{
            width:50px;height:50px;
            border:4px solid rgba(245,158,11,0.2);
            border-top-color:var(--accent);
            border-radius:50%;
            animation:spin 0.8s linear infinite;
        }
        @keyframes spin{to{transform:rotate(360deg)}}

        #mainApp{display:none;height:100vh;position:relative}

        .topbar{
            position:fixed;top:10px;left:10px;right:10px;z-index:100;
            display:flex;justify-content:space-between;align-items:center;
            padding:8px 16px;
            background:rgba(10,10,10,0.7);
            backdrop-filter:blur(30px);-webkit-backdrop-filter:blur(30px);
            border:1px solid var(--border);
            border-radius:50px;
            box-shadow:0 8px 32px rgba(245,158,11,0.08);
        }
        .logo-icon{
            width:34px;height:34px;
            background:linear-gradient(135deg,var(--accent),var(--accent2));
            border-radius:50%;display:flex;align-items:center;justify-content:center;
            font-weight:900;font-size:12px;
            box-shadow:0 0 20px rgba(245,158,11,0.5), 0 0 40px rgba(245,158,11,0.2);
            animation:pulseIcon 2s ease-in-out infinite;
        }
        @keyframes pulseIcon{0%,100%{box-shadow:0 0 20px rgba(245,158,11,0.5)}50%{box-shadow:0 0 35px rgba(251,191,36,0.8)}}
        .logo-text{
            font-weight:800;font-size:17px;
            background:linear-gradient(to bottom,#fff,#fbbf24);
            -webkit-background-clip:text;-webkit-text-fill-color:transparent;
            margin-left:8px;
        }
        .tabs{display:flex;gap:4px;background:var(--glass);border-radius:30px;padding:3px}
        .tab{
            background:none;border:none;color:rgba(255,255,255,0.5);
            padding:7px 16px;cursor:pointer;border-radius:25px;
            font-size:13px;font-weight:500;transition:all 0.3s;
        }
        .tab.active{background:rgba(245,158,11,0.25);color:#fff}
        .top-icons{display:flex;gap:16px}
        .top-icon{
            background:none;border:none;color:rgba(255,255,255,0.7);
            font-size:18px;cursor:pointer;transition:all 0.3s;position:relative;
        }
        .top-icon:hover{color:var(--accent2)}
        .notif-badge{
            position:absolute;top:-4px;right:-4px;
            width:10px;height:10px;
            background:#ef4444;
            border-radius:50%;
            border:2px solid var(--bg);
            animation:badgePulse 2s ease-in-out infinite;
            display:none;
        }
        @keyframes badgePulse{0%,100%{transform:scale(1)}50%{transform:scale(1.5);box-shadow:0 0 10px #ef4444}}

        .videos-wrap{
            height:100vh;overflow-y:scroll;
            scroll-snap-type:y mandatory;
            scrollbar-width:none;-ms-overflow-style:none;
        }
        .videos-wrap::-webkit-scrollbar{display:none}
        .vid-card{height:100vh;scroll-snap-align:start;position:relative;background:#000}
        .vid-card video{width:100%;height:100%;object-fit:cover}

        .vid-info{
            position:absolute;bottom:90px;left:14px;right:80px;z-index:20;
            text-shadow:0 2px 10px rgba(0,0,0,0.8);
        }
        .author-row{display:flex;align-items:center;gap:10px;margin-bottom:6px}
        .author-avatar{
            width:50px;height:50px;border-radius:50%;overflow:hidden;
            cursor:pointer;position:relative;
            background:linear-gradient(135deg, #b8860b, #fbbf24, #fef3c7);
            padding:3px;
            animation:storyRing 3s ease-in-out infinite;
        }
        @keyframes storyRing{0%,100%{box-shadow:0 0 15px rgba(245,158,11,0.4)}50%{box-shadow:0 0 25px rgba(251,191,36,0.8)}}
        .author-avatar img{width:100%;height:100%;object-fit:cover;border-radius:50%;border:2px solid var(--bg)}
        .author-name{
            font-weight:700;font-size:15px;cursor:pointer;
            display:flex;align-items:center;gap:6px;flex-wrap:wrap;
        }
        .verified-badge-main{
            background:linear-gradient(135deg, #f59e0b, #fbbf24);
            color:#000;
            font-size:10px;
            padding:2px 5px;
            border-radius:50%;
            display:inline-flex;
            align-items:center;
            justify-content:center;
            width:18px;
            height:18px;
            font-weight:bold;
            box-shadow:0 0 12px rgba(251,191,36,0.6);
        }
        .btn-follow{
            background:linear-gradient(135deg,var(--accent),var(--accent2));
            padding:5px 14px;border-radius:20px;font-size:11px;
            font-weight:700;border:none;color:#000;cursor:pointer;
            box-shadow:0 4px 15px rgba(245,158,11,0.4);
            transition:all 0.3s;
        }
        .btn-follow:hover{box-shadow:0 8px 25px rgba(245,158,11,0.7);transform:translateY(-1px)}
        .caption{font-size:14px;margin-bottom:5px;line-height:1.4}
        .tag{color:var(--accent2);cursor:pointer;font-weight:500}
        .music{font-size:12px;opacity:0.8;display:flex;align-items:center;gap:6px;cursor:pointer}
        .music-wave{display:flex;gap:2px;align-items:flex-end;height:16px}
        .music-wave span{width:2px;background:var(--accent2);border-radius:1px;animation:musicWave 1s ease-in-out infinite}
        .music-wave span:nth-child(1){height:8px;animation-delay:0s}
        .music-wave span:nth-child(2){height:14px;animation-delay:0.15s}
        .music-wave span:nth-child(3){height:6px;animation-delay:0.3s}
        .music-wave span:nth-child(4){height:12px;animation-delay:0.45s}
        .music-wave span:nth-child(5){height:4px;animation-delay:0.6s}
        @keyframes musicWave{0%,100%{transform:scaleY(1)}50%{transform:scaleY(1.8)}}

        .side-btns{
            position:absolute;right:14px;bottom:130px;
            display:flex;flex-direction:column;gap:22px;z-index:20;
        }
        .sbtn{
            display:flex;flex-direction:column;align-items:center;gap:3px;
            background:none;border:none;color:#fff;cursor:pointer;
            font-size:10px;transition:transform 0.15s;
        }
        .sbtn:active{transform:scale(0.85)}
        .sbtn i{font-size:28px;filter:drop-shadow(0 3px 8px rgba(0,0,0,0.5))}
        .sbtn.liked i{color:var(--accent);animation:likePop 0.4s ease}
        @keyframes likePop{0%{transform:scale(1)}50%{transform:scale(1.4)}100%{transform:scale(1)}}
        .sbtn .cnt{font-weight:700;font-size:11px}

        /* 👑 Fullscreen Video Player */
        .fullscreen-player {
            position: fixed;top:0;left:0;width:100vw;height:100vh;
            background:#000;z-index:9999;
            display:flex;align-items:center;justify-content:center;
            opacity:0;pointer-events:none;transition:opacity 0.3s ease;flex-direction:column;
        }
        .fullscreen-player.active {opacity:1;pointer-events:auto}
        .fullscreen-player video {max-width:100%;max-height:85vh;object-fit:contain;cursor:pointer}
        .player-controls {
            position:absolute;bottom:100px;left:20px;right:20px;
            display:flex;align-items:center;justify-content:space-between;
            background:rgba(0,0,0,0.6);backdrop-filter:blur(20px);
            border-radius:50px;padding:10px 20px;
            border:1px solid rgba(245,158,11,0.3);z-index:10000;color:#fff;gap:12px;flex-wrap:wrap;
        }
        .player-controls button {background:none;border:none;color:#fff;font-size:20px;cursor:pointer;padding:5px}
        .player-controls button:hover {color:#fbbf24}
        .progress-wrap {flex:1;display:flex;align-items:center;gap:8px;min-width:100px}
        .progress-bar {flex:1;height:4px;background:rgba(255,255,255,0.2);border-radius:4px;cursor:pointer;position:relative}
        .progress-fill {height:100%;background:linear-gradient(90deg,#b8860b,#fbbf24);border-radius:4px;width:0%}
        .close-player {
            position:absolute;top:20px;left:20px;
            background:rgba(0,0,0,0.5);backdrop-filter:blur(10px);
            border:1px solid rgba(245,158,11,0.4);color:#fff;
            width:44px;height:44px;border-radius:50%;
            display:flex;align-items:center;justify-content:center;
            cursor:pointer;font-size:20px;z-index:10001;
        }
        .close-player:hover {background:rgba(245,158,11,0.3);box-shadow:0 0 20px rgba(245,158,11,0.5)}

        /* 👑 Image Lightbox */
        .image-lightbox {
            position:fixed;inset:0;background:rgba(0,0,0,0.96);backdrop-filter:blur(30px);
            z-index:9999;display:flex;align-items:center;justify-content:center;
            opacity:0;pointer-events:none;transition:opacity 0.3s ease;flex-direction:column;
        }
        .image-lightbox.active {opacity:1;pointer-events:auto}
        .image-lightbox img {max-width:95vw;max-height:80vh;border-radius:16px;object-fit:contain;box-shadow:0 20px 60px rgba(245,158,11,0.2);border:1px solid rgba(245,158,11,0.15)}
        .lightbox-actions {display:flex;gap:20px;margin-top:20px;z-index:10000}
        .lightbox-actions button {background:rgba(245,158,11,0.15);border:1px solid rgba(245,158,11,0.3);color:#fff;width:48px;height:48px;border-radius:50%;display:flex;align-items:center;justify-content:center;cursor:pointer;font-size:18px}
        .close-lightbox {position:absolute;top:20px;left:20px;background:rgba(0,0,0,0.5);border:1px solid rgba(245,158,11,0.4);color:#fff;width:44px;height:44px;border-radius:50%;display:flex;align-items:center;justify-content:center;cursor:pointer;font-size:20px;z-index:10001}

        /* 📱 BOTTOM NAV */
        .nav-bottom{
            position:fixed;bottom:12px;left:12px;right:12px;
            display:flex;justify-content:space-around;align-items:center;
            padding:8px 0;background:rgba(10,10,10,0.8);
            backdrop-filter:blur(30px);z-index:100;
            border:1px solid var(--border);border-radius:40px;
        }
        .nav-item{
            display:flex;flex-direction:column;align-items:center;gap:3px;
            background:none;border:none;color:rgba(255,255,255,0.5);
            font-size:10px;cursor:pointer;text-decoration:none;
        }
        .nav-item i{font-size:22px}
        .nav-item.active{color:var(--accent2)}
        .btn-add{
            width:48px;height:48px;
            background:linear-gradient(135deg,var(--accent),var(--accent2));
            border-radius:50%;display:flex;align-items:center;justify-content:center;
            margin-top:-30px;cursor:pointer;
            box-shadow:0 10px 30px rgba(245,158,11,0.6),0 0 40px rgba(245,158,11,0.2);
            border:none;color:#000;font-size:20px;z-index:101;text-decoration:none;
        }

        .toast{
            position:fixed;bottom:120px;left:50%;transform:translateX(-50%);
            background:rgba(10,10,10,0.95);padding:12px 24px;border-radius:50px;
            z-index:1000;opacity:0;transition:opacity 0.3s;pointer-events:none;
            border:1px solid rgba(245,158,11,0.3);font-size:13px;
        }
        .toast.show{opacity:1}

        .overlay{position:fixed;inset:0;background:rgba(10,10,10,0.97);backdrop-filter:blur(40px);z-index:400;overflow-y:auto}
        .overlay-header{display:flex;justify-content:space-between;align-items:center;padding:16px;border-bottom:1px solid var(--border);position:sticky;top:0;background:rgba(10,10,10,0.8)}
        .btn-close{background:rgba(245,158,11,0.1);border:1px solid var(--border);color:#fff;width:36px;height:36px;border-radius:50%;display:flex;align-items:center;justify-content:center;cursor:pointer;font-size:18px}
    </style>
</head>
<body>

<div id="loaderScreen">
    <div class="spinner-big"></div>
    <p style="color:rgba(255,255,255,0.5);font-size:15px">👑 GKOM جاري التحميل...</p>
</div>

<div id="mainApp">
    <div class="topbar">
        <div style="display:flex;align-items:center">
            <div class="logo-icon">👑</div>
            <span class="logo-text">GKOM</span>
        </div>
        <div class="tabs">
            <button class="tab" onclick="switchFeed('following')">متابَعين</button>
            <button class="tab active" onclick="switchFeed('forYou')">لك</button>
        </div>
        <div class="top-icons">
            <i class="fas fa-search top-icon" onclick="openSearch()"></i>
            <i class="fas fa-bell top-icon" onclick="openNotifs()"><span class="notif-badge" id="notifBadge"></span></i>
        </div>
    </div>

    <div class="videos-wrap" id="videosWrap">
        <div style="display:flex;align-items:center;justify-content:center;height:100vh;color:rgba(255,255,255,0.5);flex-direction:column;gap:12px">
            <i class="fas fa-video" style="font-size:48px;opacity:0.3;color:#f59e0b"></i>
            <p>لا توجد فيديوهات بعد</p>
            <p style="font-size:12px;opacity:0.5">ارفع أول فيديو! 👑</p>
        </div>
    </div>

    <!-- 👑 Fullscreen Player -->
    <div class="fullscreen-player" id="fullscreenPlayer" onclick="if(event.target===this)closePlayer()">
        <button class="close-player" onclick="closePlayer()"><i class="fas fa-times"></i></button>
        <video id="fullscreenVideo" controls playsinline></video>
        <div class="player-controls">
            <button onclick="skipTime(-10)"><i class="fas fa-backward"></i></button>
            <button id="btnPlayPause" onclick="togglePlayPause()"><i class="fas fa-pause"></i></button>
            <button onclick="skipTime(10)"><i class="fas fa-forward"></i></button>
            <div class="progress-wrap">
                <span id="currentTime">0:00</span>
                <div class="progress-bar" id="progressBar" onclick="seekVideo(event)"><div class="progress-fill" id="progressFill"></div></div>
                <span id="duration">0:00</span>
            </div>
            <button onclick="toggleMutePlayer()"><i class="fas fa-volume-up" id="muteIcon"></i></button>
            <a id="downloadLink" href="#" download style="color:#fbbf24;text-decoration:none;margin-left:10px;"><i class="fas fa-download"></i></a>
        </div>
    </div>

    <!-- 👑 Image Lightbox -->
    <div class="image-lightbox" id="imageLightbox" onclick="if(event.target===this)closeLightbox()">
        <button class="close-lightbox" onclick="closeLightbox()"><i class="fas fa-times"></i></button>
        <img id="lightboxImage" src="" alt="صورة">
        <div class="lightbox-actions">
            <button onclick="downloadImage()"><i class="fas fa-download"></i></button>
            <button onclick="copyImageLink()"><i class="fas fa-link"></i></button>
        </div>
    </div>

    <div class="nav-bottom">
        <button class="nav-item active"><i class="fas fa-home"></i><span>الرئيسية</span></button>
        <button class="nav-item" onclick="openSearch()"><i class="fas fa-search"></i><span>بحث</span></button>
        <a href="upload.html" class="btn-add"><i class="fas fa-plus"></i></a>
        <a href="chat.html" class="nav-item"><i class="fas fa-envelope"></i><span>رسائل</span></a>
        <a href="profile.html" class="nav-item"><i class="fas fa-user"></i><span>ملفي</span></a>
    </div>

    <div id="toast" class="toast">✅ تم النسخ</div>
</div>

<script src="firebase-config.js"></script>
<script>
    let currentUser=null,currentUserData=null,allUsers={},allVideos=[],allSounds={};
    let isMuted=true,currentFeed='forYou',currentShareUrl=null,playerVideo=null;

    function openPlayer(url,title){
        const p=document.getElementById('fullscreenPlayer'),v=document.getElementById('fullscreenVideo');
        p.classList.add('active');v.src=url;v.load();v.play();
        document.getElementById('downloadLink').href=url;playerVideo=v;
        v.onloadedmetadata=()=>{document.getElementById('duration').innerText=formatTime(v.duration)};
        v.ontimeupdate=()=>{document.getElementById('progressFill').style.width=(v.currentTime/v.duration)*100+'%';document.getElementById('currentTime').innerText=formatTime(v.currentTime)};
    }
    function closePlayer(){const v=document.getElementById('fullscreenVideo');v.pause();v.src='';document.getElementById('fullscreenPlayer').classList.remove('active')}
    function togglePlayPause(){const v=document.getElementById('fullscreenVideo');if(v.paused){v.play()}else{v.pause()}}
    function skipTime(s){if(playerVideo)playerVideo.currentTime+=s}
    function seekVideo(e){if(!playerVideo)return;const b=document.getElementById('progressBar'),r=b.getBoundingClientRect();playerVideo.currentTime=((e.clientX-r.left)/r.width)*playerVideo.duration}
    function toggleMutePlayer(){if(playerVideo){playerVideo.muted=!playerVideo.muted}}
    function openLightbox(url){const l=document.getElementById('imageLightbox');l.classList.add('active');document.getElementById('lightboxImage').src=url}
    function closeLightbox(){document.getElementById('imageLightbox').classList.remove('active')}
    function downloadImage(){const u=document.getElementById('lightboxImage').src;if(u){const a=document.createElement('a');a.href=u;a.download='image.jpg';a.click()}}
    function copyImageLink(){navigator.clipboard.writeText(document.getElementById('lightboxImage').src);const t=document.getElementById('toast');t.classList.add('show');setTimeout(()=>t.classList.remove('show'),2000)}

    auth.onAuthStateChanged(async(u)=>{
        if(!u){window.location.replace('auth.html');return}
        currentUser=u;
        try{const s=await db.ref('users/'+u.uid).get();if(s.exists())currentUserData={uid:u.uid,...s.val()}}catch(e){}
        db.ref('users').on('value',s=>{allUsers=s.val()||{}});
        db.ref('videos').on('value',s=>{
            const d=s.val();allVideos=[];allSounds={};
            if(d){Object.entries(d).forEach(([k,v])=>{allVideos.push({id:k,...v});if(v.music)allSounds[v.music]=(allSounds[v.music]||0)+1});allVideos.sort((a,b)=>(b.timestamp||0)-(a.timestamp||0))}
            renderVideos();
        });
        db.ref('notifications/'+u.uid).on('value',s=>{
            const b=document.getElementById('notifBadge'),c=Object.keys(s.val()||{}).length;
            if(b){b.style.display=c>0?'block':'none';if(c>0){b.innerText=c;b.style.padding='2px 6px';b.style.borderRadius='10px'}else{b.innerText='';b.style.padding='0';b.style.borderRadius='50%'}}
        });
        db.ref('presence/'+u.uid).set(true);db.ref('presence/'+u.uid).onDisconnect().remove();
        db.ref('users/'+u.uid+'/lastSeen').set(Date.now());
        setInterval(()=>{db.ref('users/'+u.uid+'/lastSeen').set(Date.now())},60000);
        document.getElementById('loaderScreen').style.display='none';document.getElementById('mainApp').style.display='block';
    });

    function renderVideos(){
        const c=document.getElementById('videosWrap');if(!c)return;
        let f=currentFeed==='forYou'?allVideos:allVideos.filter(v=>currentUserData?.following?.[v.sender]);
        if(!f.length){c.innerHTML=`<div style="display:flex;align-items:center;justify-content:center;height:100vh;color:rgba(255,255,255,0.5);flex-direction:column;gap:12px"><i class="fas fa-video" style="font-size:48px;opacity:0.3;color:#f59e0b"></i><p>${currentFeed==='forYou'?'لا توجد فيديوهات بعد':'تابع مستخدمين لرؤية فيديوهاتهم'}</p></div>`;return}
        c.innerHTML='';
        f.forEach(v=>{
            const u=allUsers[v.sender]||{username:v.senderName||'مستخدم'};
            const avatar=u.avatarUrl||(DICEBEAR_URL+'?seed='+v.sender);
            const verified=u.isVerified?'<span class="verified-badge-main"><i class="fas fa-check"></i></span>':'';
            const music=v.music?`<div class="music-wave">${[1,2,3,4,5].map(()=>'<span></span>').join('')}</div> ${v.music}`:'Original Sound';
            const d=document.createElement('div');d.className='vid-card';
            d.innerHTML=`<video loop playsinline muted data-src="${v.url}" poster="${v.thumbnail||''}"></video>
                <div class="vid-info">
                    <div class="author-row">
                        <div class="author-avatar" onclick="openUserProfile('${v.sender}')"><img src="${avatar}"></div>
                        <div class="author-name"><span onclick="openUserProfile('${v.sender}')">@${u.username}</span>${verified}${currentUser?.uid!==v.sender?`<button class="btn-follow" onclick="event.stopPropagation();toggleFollow('${v.sender}',this)">${currentUserData?.following?.[v.sender]?'<i class="fas fa-user-check"></i> متابع':'<i class="fas fa-user-plus"></i> متابعة'}</button>`:''}</div>
                    </div>
                    <div class="caption">${(v.description||'').replace(/#(\w+)/g,'<span class="tag">#$1</span>')}</div>
                    <div class="music">${music}</div>
                </div>
                <div class="side-btns">
                    <button class="sbtn" onclick="toggleMute()"><i class="fas ${isMuted?'fa-volume-mute':'fa-volume-up'}"></i></button>
                    <button class="sbtn like-btn ${v.likedBy?.[currentUser?.uid]?'liked':''}" onclick="toggleLike('${v.id}',this)"><i class="fas fa-heart"></i><span class="cnt">${v.likes||0}</span></button>
                    <button class="sbtn" onclick="openComments('${v.id}')"><i class="fas fa-comment"></i><span class="cnt">${v.comments?Object.keys(v.comments).length:0}</span></button>
                    <button class="sbtn" onclick="openPlayer('${v.url}','video.mp4')"><i class="fas fa-expand"></i></button>
                    <button class="sbtn" onclick="openShare('${v.url}')"><i class="fas fa-share"></i></button>
                </div>`;
            d.querySelector('video').addEventListener('dblclick',e=>{e.stopPropagation();const b=d.querySelector('.like-btn');if(b)toggleLike(v.id,b)});
            c.appendChild(d);
        });
        initVideoObserver();
    }

    function openUserProfile(id){window.location.href=id===currentUser?.uid?'profile.html':'profile.html?uid='+id}
    function initVideoObserver(){
        new IntersectionObserver(e=>{e.forEach(e=>{const v=e.target.querySelector('video');if(e.isIntersecting){if(!v.src)v.src=v.dataset.src;v.muted=isMuted;v.play().catch(()=>{})}else{v.pause()}})},{threshold:0.65}).observe(document.querySelectorAll('.vid-card'));
    }
    function toggleMute(){isMuted=!isMuted;document.querySelectorAll('video').forEach(v=>v.muted=isMuted)}
    function switchFeed(f){currentFeed=f;document.querySelectorAll('.tab').forEach(t=>t.classList.remove('active'));event.target.classList.add('active');renderVideos()}
    async function toggleLike(id,btn){
        if(!currentUser)return;const r=db.ref('videos/'+id),s=await r.get(),v=s.val();if(!v)return;
        let l=v.likes||0,lb=v.likedBy||{};
        if(lb[currentUser.uid]){l--;delete lb[currentUser.uid]}else{l++;lb[currentUser.uid]=true;if(v.sender&&v.sender!==currentUser.uid)sendNotification(v.sender,currentUserData?.username,'أعجب بفيديو الخاص بك ❤️')}
        await r.update({likes:l,likedBy:lb});btn.classList.toggle('liked');const c=btn.querySelector('.cnt');if(c)c.innerText=l;
    }
    async function toggleFollow(uid,btn){
        if(!currentUser||currentUser.uid===uid)return;
        const ur=db.ref('users/'+currentUser.uid+'/following/'+uid),tr=db.ref('users/'+uid+'/followers/'+currentUser.uid),s=await ur.get();
        if(s.exists()){await ur.remove();await tr.remove();btn.innerHTML='<i class="fas fa-user-plus"></i> متابعة'}else{await ur.set(true);await tr.set(true);btn.innerHTML='<i class="fas fa-user-check"></i> متابع';sendNotification(uid,currentUserData?.username,'بدأ بمتابعتك 👤')}
    }
    async function sendNotification(to,from,msg){await db.ref('notifications/'+to).push({from:from||'مستخدم',msg:msg,timestamp:Date.now(),read:false})}
    function openShare(url){currentShareUrl=url;showOverlay('📤 مشاركة',`<div onclick="copyLink()" style="display:flex;align-items:center;gap:12px;padding:14px;cursor:pointer"><i class="fas fa-link" style="color:#f59e0b"></i><span>نسخ الرابط</span></div>`)}
    window.copyLink=function(){navigator.clipboard.writeText(currentShareUrl);const t=document.getElementById('toast');t.classList.add('show');setTimeout(()=>t.classList.remove('show'),2000);closeOverlay()}
    async function openComments(id){
        const s=await db.ref('videos/'+id+'/comments').get(),cs=s.val()||{};
        let h='';Object.values(cs).reverse().forEach(c=>{const u=allUsers[c.userId]||{username:c.username||'مستخدم'};h+=`<div style="display:flex;gap:10px;padding:10px 0;border-bottom:1px solid rgba(245,158,11,0.1)"><img src="${u.avatarUrl||(DICEBEAR_URL+'?seed='+c.userId)}" style="width:36px;height:36px;border-radius:50%"><div><div style="font-weight:600">@${u.username}</div><div style="font-size:13px;opacity:0.8">${c.text}</div></div></div>`});
        showOverlay('💬 التعليقات',h+`<div style="display:flex;gap:8px;padding-top:12px"><input type="text" id="cmtInput" placeholder="أضف تعليقاً..." style="flex:1;padding:12px;border-radius:30px;background:rgba(184,134,11,0.04);border:1px solid rgba(245,158,11,0.15);color:#fff;outline:none"><button onclick="addComment('${id}')" style="background:linear-gradient(135deg,#b8860b,#fbbf24);border:none;color:#000;padding:12px 20px;border-radius:30px;font-weight:700;cursor:pointer">نشر</button></div>`);
    }
    window.addComment=async function(id){const i=document.getElementById('cmtInput');if(!i||!i.value.trim())return;await db.ref('videos/'+id+'/comments').push({userId:currentUser.uid,username:currentUserData?.username,text:i.value,timestamp:Date.now()});closeOverlay();openComments(id)}
    async function openNotifs(){
        const s=await db.ref('notifications/'+currentUser.uid).once('value'),ns=s.val()||{},items=Object.values(ns).reverse();
        let h='';items.forEach(n=>{h+=`<div style="display:flex;gap:12px;padding:14px;border-bottom:1px solid rgba(245,158,11,0.1)"><div style="width:40px;height:40px;border-radius:50%;background:rgba(245,158,11,0.15);display:flex;align-items:center;justify-content:center;color:#f59e0b"><i class="fas fa-bell"></i></div><div><div style="font-weight:600">${n.from||'مستخدم'}</div><div style="font-size:12px;opacity:0.6">${n.msg||''}</div></div></div>`});
        if(!items.length)h='<div style="text-align:center;opacity:0.5;padding:40px"><i class="fas fa-bell" style="font-size:48px;color:#f59e0b;display:block;margin-bottom:12px"></i><p>لا توجد إشعارات</p></div>';
        await db.ref('notifications/'+currentUser.uid).remove();document.getElementById('notifBadge').style.display='none';showOverlay('🔔 الإشعارات',h);
    }
    function openSearch(){showOverlay('🔍 بحث',`<input type="text" id="searchQ" onkeyup="doSearch()" placeholder="ابحث..." style="width:100%;padding:14px;border-radius:30px;background:rgba(184,134,11,0.04);border:1px solid rgba(245,158,11,0.15);color:#fff;outline:none;margin-bottom:16px"><div id="searchR"></div>`);setTimeout(()=>document.getElementById('searchQ')?.focus(),300)}
    window.doSearch=function(){
        const q=document.getElementById('searchQ').value.toLowerCase(),r=document.getElementById('searchR');
        if(!q){r.innerHTML='';return}
        const us=Object.values(allUsers).filter(u=>u.username?.toLowerCase().includes(q));
        r.innerHTML=us.length?us.map(u=>`<div onclick="openUserProfile('${Object.keys(allUsers).find(k=>allUsers[k]===u)}')" style="display:flex;align-items:center;gap:10px;padding:10px;cursor:pointer"><img src="${u.avatarUrl||DICEBEAR_URL+'?seed='+(u.uid||'')}" style="width:40px;height:40px;border-radius:50%"><div>@${u.username}${u.isVerified?' <span class="verified-badge-main"><i class="fas fa-check"></i></span>':''}</div></div>`).join(''):'<div style="text-align:center;opacity:0.5;padding:30px">لا توجد نتائج</div>';
    }
    function showOverlay(title,content){const id='overlay_'+Date.now();document.body.insertAdjacentHTML('beforeend',`<div id="${id}" class="overlay"><div class="overlay-header"><h3>${title}</h3><button class="btn-close" onclick="document.getElementById('${id}').remove()"><i class="fas fa-times"></i></button></div><div style="padding:16px">${content}</div></div>`)}
    function closeOverlay(){document.querySelectorAll('.overlay').forEach(o=>{if(o.id?.startsWith('overlay_'))o.remove()})}
    function formatTime(s){if(isNaN(s))return'0:00';const m=Math.floor(s/60);return m+':'+('0'+Math.floor(s%60)).slice(-2)}
    console.log('👑 GKOM Index Ready ✨');
</script>
</body>
</html>"""

# ═══════════════════════════════════════════════════════════
# 👑 4-9: profile, upload, chat, explore, notifications, settings
# ═══════════════════════════════════════════════════════════

def build_profile():
    return """<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
    <title>👑 GKOM | ملف شخصي</title>
    <script src="https://www.gstatic.com/firebasejs/10.7.0/firebase-app-compat.js"></script>
    <script src="https://www.gstatic.com/firebasejs/10.7.0/firebase-database-compat.js"></script>
    <script src="https://www.gstatic.com/firebasejs/10.7.0/firebase-auth-compat.js"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <style>
        :root{--glass:rgba(184,134,11,0.04);--border:rgba(245,158,11,0.15);--accent:#f59e0b;--accent2:#fbbf24;--bg:#0a0a0a;--card:rgba(184,134,11,0.06)}
        *{margin:0;padding:0;box-sizing:border-box}
        body{font-family:'Segoe UI',sans-serif;background:var(--bg);color:#fff;min-height:100vh;overflow-y:auto}
        .cover-section{position:relative;width:100%;height:260px;overflow:hidden;cursor:pointer}
        .cover-img{width:100%;height:130%;object-fit:cover;transition:transform 0.1s linear}
        .cover-gradient{position:absolute;inset:0;background:linear-gradient(to bottom, transparent 30%, rgba(10,10,10,0.4) 60%, rgba(10,10,10,0.95) 100%);pointer-events:none;z-index:1}
        .cover-glow{position:absolute;inset:0;background:radial-gradient(ellipse at center, rgba(245,158,11,0.15) 0%, transparent 70%);pointer-events:none;z-index:2}
        .cover-edit-btn{position:absolute;top:12px;left:12px;background:rgba(0,0,0,0.5);backdrop-filter:blur(15px);width:38px;height:38px;border-radius:50%;display:flex;align-items:center;justify-content:center;cursor:pointer;z-index:5;border:1px solid rgba(245,158,11,0.3);color:#fff;font-size:14px}
        .btn-back{position:fixed;top:20px;right:20px;background:rgba(0,0,0,0.5);backdrop-filter:blur(15px);width:40px;height:40px;border-radius:50%;display:flex;align-items:center;justify-content:center;cursor:pointer;z-index:50;border:1px solid var(--border);color:#fff;font-size:16px}
        .avatar-wrap{position:relative;z-index:2;margin-top:-60px;display:flex;justify-content:center}
        .avatar-lg{width:120px;height:120px;border-radius:50%;overflow:hidden;cursor:pointer;background:linear-gradient(135deg, #b8860b, #fbbf24, #fef3c7);padding:3px;box-shadow:0 0 30px rgba(245,158,11,0.4);animation:avatarGlow 3s ease-in-out infinite}
        @keyframes avatarGlow{0%,100%{box-shadow:0 0 30px rgba(245,158,11,0.4)}50%{box-shadow:0 0 40px rgba(251,191,36,0.7)}}
        .avatar-lg img{width:100%;height:100%;object-fit:cover;border-radius:50%;border:3px solid var(--bg)}
        .avatar-edit-btn{position:absolute;bottom:5px;right:5px;width:30px;height:30px;background:var(--accent);border-radius:50%;display:flex;align-items:center;justify-content:center;cursor:pointer;border:2px solid var(--bg);color:#000;font-size:12px}
        .online-dot{position:absolute;top:10px;right:10px;width:18px;height:18px;background:#22c55e;border-radius:50%;border:3px solid var(--bg);z-index:3}
        .profile-info{padding:20px;text-align:center}
        .username{font-size:22px;font-weight:800;margin-bottom:4px}
        .bio-text{font-size:13px;opacity:0.7;margin-bottom:8px}
        .contact-info{display:flex;justify-content:center;gap:12px;flex-wrap:wrap;margin-bottom:8px;font-size:12px}
        .contact-info a{color:var(--accent2);text-decoration:none;display:flex;align-items:center;gap:5px;background:var(--card);padding:6px 14px;border-radius:20px;border:1px solid var(--border)}
        .stats-row{display:flex;justify-content:center;gap:30px;margin:15px 20px;padding:18px;background:rgba(184,134,11,0.04);backdrop-filter:blur(20px);border-radius:20px;border:1px solid var(--border)}
        .stat-item{text-align:center;cursor:pointer}
        .stat-val{font-size:20px;font-weight:700;color:var(--accent2)}
        .stat-lbl{font-size:10px;opacity:0.6}
        .action-btns{display:flex;gap:8px;justify-content:center;flex-wrap:wrap;margin:0 20px 20px}
        .btn{background:rgba(184,134,11,0.06);border:1px solid var(--border);padding:10px 20px;border-radius:25px;color:#fff;cursor:pointer;font-size:13px;display:flex;align-items:center;gap:6px}
        .btn-primary{background:linear-gradient(135deg,var(--accent),var(--accent2));border:none;font-weight:700;color:#000}
        .btn-follow{background:linear-gradient(135deg,#ef4444,#dc2626);border:none;font-weight:700}
        .btn-follow.following{background:linear-gradient(135deg,var(--accent),var(--accent2));color:#000}
        .badge-verified{background:linear-gradient(135deg, #f59e0b, #fbbf24);color:#000;font-size:12px;padding:3px 6px;border-radius:50%;display:inline-flex;align-items:center;justify-content:center;width:22px;height:22px;font-weight:bold}
        .section-title{font-size:16px;font-weight:700;padding:0 20px;margin-bottom:12px}
        .videos-compact{padding:0 8px 80px}
        .video-compact-item{display:flex;gap:10px;margin-bottom:8px;background:rgba(184,134,11,0.03);border:1px solid rgba(245,158,11,0.08);border-radius:16px;padding:8px;cursor:pointer}
        .video-compact-thumb{width:120px;aspect-ratio:9/16;border-radius:10px;overflow:hidden;background:#000}
        .video-compact-thumb img{width:100%;height:100%;object-fit:cover}
        .video-compact-info .vci-caption{font-size:13px}
        .video-compact-info .vci-meta{font-size:11px;opacity:0.5;display:flex;gap:12px}
        .edit-panel{position:fixed;bottom:0;left:0;right:0;background:rgba(10,10,10,0.98);backdrop-filter:blur(40px);border-top:2px solid var(--accent);border-radius:24px 24px 0 0;padding:24px 20px 40px;z-index:200;transform:translateY(100%);transition:transform 0.4s;max-height:80vh;overflow-y:auto}
        .edit-panel.show{transform:translateY(0)}
        .edit-panel input,.edit-panel textarea{width:100%;padding:12px 16px;border-radius:14px;background:var(--card);border:1px solid var(--border);color:#fff;font-size:14px;outline:none;margin-top:8px}
        .overlay-panel{position:fixed;inset:0;background:rgba(0,0,0,0.7);z-index:150;display:none}
        .overlay-panel.show{display:block}
        .spinner{width:36px;height:36px;border:3px solid rgba(245,158,11,0.2);border-top-color:var(--accent);border-radius:50%;animation:spin 0.7s linear infinite;margin:30px auto}
        @keyframes spin{to{transform:rotate(360deg)}}
        .toast-msg{position:fixed;bottom:100px;left:50%;transform:translateX(-50%);background:rgba(10,10,10,0.95);padding:12px 24px;border-radius:30px;z-index:300;border:1px solid rgba(245,158,11,0.3);font-size:13px;opacity:0;transition:opacity 0.3s}
        .toast-msg.show{opacity:1}

        .fullscreen-player{position:fixed;top:0;left:0;width:100vw;height:100vh;background:#000;z-index:9999;display:flex;align-items:center;justify-content:center;opacity:0;pointer-events:none;transition:opacity 0.3s;flex-direction:column}
        .fullscreen-player.active{opacity:1;pointer-events:auto}
        .fullscreen-player video{max-width:100%;max-height:85vh;object-fit:contain}
        .player-controls{position:absolute;bottom:100px;left:20px;right:20px;display:flex;align-items:center;justify-content:space-between;background:rgba(0,0,0,0.6);backdrop-filter:blur(20px);border-radius:50px;padding:10px 20px;border:1px solid rgba(245,158,11,0.3);z-index:10000;color:#fff;gap:12px}
        .player-controls button{background:none;border:none;color:#fff;font-size:20px;cursor:pointer}
        .progress-wrap{flex:1;display:flex;align-items:center;gap:8px}
        .progress-bar{flex:1;height:4px;background:rgba(255,255,255,0.2);border-radius:4px;cursor:pointer}
        .progress-fill{height:100%;background:linear-gradient(90deg,#b8860b,#fbbf24);border-radius:4px;width:0%}
        .close-player{position:absolute;top:20px;left:20px;background:rgba(0,0,0,0.5);border:1px solid rgba(245,158,11,0.4);color:#fff;width:44px;height:44px;border-radius:50%;display:flex;align-items:center;justify-content:center;cursor:pointer;z-index:10001}
        .admin-panel{background:transparent;border:none;padding:0 8px;margin:0 8px 100px 8px}
        .admin-panel h3{color:#fbbf24;font-size:20px;margin-bottom:20px}
        .admin-stats-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:12px;margin-bottom:24px}
        .stat-card{background:rgba(184,134,11,0.06);border:1px solid rgba(245,158,11,0.15);border-radius:16px;padding:16px;display:flex;align-items:center;gap:14px}
        .stat-icon{width:44px;height:44px;border-radius:12px;background:linear-gradient(135deg,var(--accent),var(--accent2));display:flex;align-items:center;justify-content:center;font-size:20px}
        .admin-user-item,.admin-video-item{display:flex;align-items:center;justify-content:space-between;padding:10px;border-bottom:1px solid rgba(255,255,255,0.03)}
        .admin-btn{border:none;border-radius:20px;padding:8px 16px;font-size:12px;font-weight:700;cursor:pointer}
        .btn-ban{background:rgba(255,255,255,0.1);color:#fff}
        .btn-verify{background:linear-gradient(135deg, #f59e0b, #fbbf24);color:#000}
        .btn-delete-video{background:rgba(239,68,68,0.1);color:#f87171}
    </style>
</head>
<body>
<div class="fullscreen-player" id="fullscreenPlayer" onclick="if(event.target===this)closePlayer()">
    <button class="close-player" onclick="closePlayer()"><i class="fas fa-times"></i></button>
    <video id="fullscreenVideo" controls playsinline></video>
    <div class="player-controls">
        <button onclick="skipTime(-10)"><i class="fas fa-backward"></i></button>
        <button id="btnPlayPause" onclick="togglePlayPause()"><i class="fas fa-pause"></i></button>
        <button onclick="skipTime(10)"><i class="fas fa-forward"></i></button>
        <div class="progress-wrap"><span id="currentTime">0:00</span><div class="progress-bar" id="progressBar" onclick="seekVideo(event)"><div class="progress-fill" id="progressFill"></div></div><span id="duration">0:00</span></div>
        <button onclick="toggleMutePlayer()"><i class="fas fa-volume-up" id="muteIcon"></i></button>
    </div>
</div>
<div id="loader" class="spinner" style="display:flex;align-items:center;justify-content:center;min-height:80vh;flex-direction:column;gap:12px"><div class="spinner"></div><span>👑 تحميل...</span></div>
<div id="content" style="display:none">
    <div class="cover-section" id="coverSection"><img class="cover-img" id="coverImg" src="" style="display:none"><div class="cover-gradient"></div><div class="cover-glow"></div><div class="cover-edit-btn" id="coverEditBtn" onclick="document.getElementById('coverInput').click()" style="display:none"><i class="fas fa-camera"></i></div></div>
    <input type="file" id="coverInput" accept="image/*" style="display:none" onchange="uploadCover(this)">
    <button class="btn-back" onclick="history.back()"><i class="fas fa-arrow-right"></i></button>
    <div class="avatar-wrap"><div class="avatar-lg" id="avatarDisplay"><img src="" id="avatarImg"><div class="avatar-edit-btn" id="avatarEditBtn" onclick="document.getElementById('avatarInput').click()" style="display:none"><i class="fas fa-camera"></i></div><div class="online-dot" id="onlineDot" style="display:none"></div></div></div>
    <input type="file" id="avatarInput" accept="image/*" style="display:none" onchange="uploadAvatar(this)">
    <div class="profile-info"><div class="username"><span id="nameDisplay"></span></div><div class="bio-text" id="bioDisplay"></div><div class="contact-info" id="contactInfo"></div><div class="last-seen" id="lastSeenDisplay" style="font-size:11px;opacity:0.5;margin-top:6px"></div></div>
    <div class="stats-row"><div class="stat-item" onclick="showList('following')"><div class="stat-val" id="statFollowing">0</div><div class="stat-lbl">يتابع</div></div><div class="stat-item" onclick="showList('followers')"><div class="stat-val" id="statFollowers">0</div><div class="stat-lbl">متابع</div></div><div class="stat-item"><div class="stat-val" id="statLikes">0</div><div class="stat-lbl">إعجابات</div></div></div>
    <div class="action-btns" id="actionsBar"></div>
    <div class="section-title"><i class="fas fa-video" style="color:var(--accent)"></i> الفيديوهات</div>
    <div class="videos-compact" id="videosContainer"></div>
</div>
<div class="overlay-panel" id="overlayPanel" onclick="closeEditPanel()"></div>
<div class="edit-panel" id="editPanel"><h3>👑 تعديل الملف</h3><input type="text" id="editUsername" placeholder="اسم المستخدم"><textarea id="editBio" placeholder="السيرة الذاتية..."></textarea><input type="text" id="editWebsite" placeholder="الموقع"><input type="text" id="editContactEmail" placeholder="البريد"><div id="coverColors" style="display:flex;gap:8px;flex-wrap:wrap;margin-top:8px"></div><div style="display:flex;gap:10px;margin-top:20px"><button onclick="closeEditPanel()" style="flex:1;padding:12px;border-radius:25px;background:var(--card);border:1px solid var(--border);color:#fff;cursor:pointer">إلغاء</button><button onclick="saveProfile()" style="flex:1;padding:12px;border-radius:25px;background:linear-gradient(135deg,#b8860b,#fbbf24);border:none;color:#000;font-weight:700;cursor:pointer">حفظ</button></div></div>
<div class="toast-msg" id="toastMsg">✅ تم</div>

<script src="firebase-config.js"></script>
<script>
    let profileUserId=null,currentUser=null,currentUserData=null,allVideos=[],allUsers={},isOwnProfile=false,_selectedCover=null,playerVideo=null;
    function openPlayer(url){const p=document.getElementById('fullscreenPlayer'),v=document.getElementById('fullscreenVideo');p.classList.add('active');v.src=url;v.load();v.play();playerVideo=v;v.onloadedmetadata=()=>{document.getElementById('duration').innerText=formatTime(v.duration)};v.ontimeupdate=()=>{document.getElementById('progressFill').style.width=(v.currentTime/v.duration)*100+'%';document.getElementById('currentTime').innerText=formatTime(v.currentTime)}}
    function closePlayer(){const v=document.getElementById('fullscreenVideo');v.pause();v.src='';document.getElementById('fullscreenPlayer').classList.remove('active')}
    function togglePlayPause(){const v=document.getElementById('fullscreenVideo');v.paused?v.play():v.pause()}
    function skipTime(s){if(playerVideo)playerVideo.currentTime+=s}
    function seekVideo(e){if(!playerVideo)return;const b=document.getElementById('progressBar'),r=b.getBoundingClientRect();playerVideo.currentTime=((e.clientX-r.left)/r.width)*playerVideo.duration}
    function toggleMutePlayer(){if(playerVideo)playerVideo.muted=!playerVideo.muted}
    function formatTime(s){if(isNaN(s))return'0:00';const m=Math.floor(s/60);return m+':'+('0'+Math.floor(s%60)).slice(-2)}

    auth.onAuthStateChanged(async u=>{
        if(!u){window.location.href='auth.html';return}
        currentUser=u;const params=new URLSearchParams(window.location.search);profileUserId=params.get('uid')||u.uid;isOwnProfile=(profileUserId===u.uid);
        const snap=await db.ref('users/'+u.uid).get();if(snap.exists())currentUserData={uid:u.uid,...snap.val()};
        const us=await db.ref('users').once('value');allUsers=us.val()||{};
        const vs=await db.ref('videos').once('value');allVideos=Object.entries(vs.val()||{}).map(([k,v])=>({id:k,...v}));
        loadProfile();
        if(!isOwnProfile){db.ref('presence/'+profileUserId).on('value',s=>{document.getElementById('onlineDot').style.display=s.val()?'block':'none'})}
        document.getElementById('loader').style.display='none';document.getElementById('content').style.display='block';
    });

    function loadProfile(){
        const u=allUsers[profileUserId];if(!u)return;
        document.getElementById('nameDisplay').innerHTML='@'+(u.username||'مستخدم')+' '+(u.isVerified?'<span class="badge-verified"><i class="fas fa-check"></i></span>':'');
        document.getElementById('bioDisplay').innerText=u.bio||'';
        const ci=document.getElementById('contactInfo');ci.innerHTML='';if(u.website)ci.innerHTML+=`<a href="${u.website}" target="_blank"><i class="fas fa-globe"></i></a>`;if(u.contactEmail)ci.innerHTML+=`<a href="mailto:${u.contactEmail}"><i class="fas fa-envelope"></i></a>`;
        document.getElementById('statFollowing').innerText=Object.keys(u.following||{}).length;
        document.getElementById('statFollowers').innerText=Object.keys(u.followers||{}).length;
        const uvs=allVideos.filter(v=>v.sender===profileUserId);
        document.getElementById('statLikes').innerText=uvs.reduce((s,v)=>s+(v.likes||0),0);
        const coverImg=document.getElementById('coverImg');
        if(u.coverImageUrl){coverImg.src=u.coverImageUrl;coverImg.style.display='block'}else{document.getElementById('coverSection').style.background=u.coverColor||COVER_COLORS[0]}
        document.getElementById('avatarImg').src=u.avatarUrl||(DICEBEAR_URL+'?seed='+profileUserId);
        if(isOwnProfile){document.getElementById('avatarEditBtn').style.display='flex';document.getElementById('coverEditBtn').style.display='flex'}
        const vc=document.getElementById('videosContainer');vc.innerHTML='';
        if(uvs.length){uvs.sort((a,b)=>(b.timestamp||0)-(a.timestamp||0)).forEach(v=>{const d=document.createElement('div');d.className='video-compact-item';d.innerHTML=`<div class="video-compact-thumb" onclick="openPlayer('${v.url}')">${v.thumbnail?`<img src="${v.thumbnail}">`:''}<i class="fas fa-play" style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-size:24px;color:#fff"></i></div><div class="video-compact-info"><div class="vci-caption">${(v.description||'').substring(0,80)}</div><div class="vci-meta"><span><i class="fas fa-heart" style="color:#f59e0b"></i> ${v.likes||0}</span><span><i class="fas fa-comment"></i> ${v.comments?Object.keys(v.comments).length:0}</span></div></div>`;vc.appendChild(d)})}else{vc.innerHTML='<div style="text-align:center;opacity:0.5;padding:40px">لا توجد فيديوهات</div>'}
        const ab=document.getElementById('actionsBar');
        if(isOwnProfile){ab.innerHTML=`<button class="btn btn-primary" onclick="openEditPanel()"><i class="fas fa-edit"></i> تعديل</button><button class="btn" onclick="window.location.href='chat.html'"><i class="fas fa-envelope"></i> رسائل</button><button class="btn" onclick="auth.signOut();window.location.href='auth.html'"><i class="fas fa-sign-out-alt"></i> خروج</button>`}
        else{const isF=currentUserData?.following?.[profileUserId];ab.innerHTML=`<button class="btn btn-follow ${isF?'following':''}" id="followBtn" onclick="toggleFollowUser()">${isF?'<i class="fas fa-user-check"></i> متابع':'<i class="fas fa-user-plus"></i> متابعة'}</button><button class="btn btn-primary" onclick="window.location.href='chat.html?uid=${profileUserId}'"><i class="fas fa-comment"></i> مراسلة</button>`}
        if(isOwnProfile&&ADMIN_EMAILS.includes(currentUser?.email))loadAdminPanel();
    }

    function openEditPanel(){const u=allUsers[profileUserId]||currentUserData;document.getElementById('editUsername').value=u.username||'';document.getElementById('editBio').value=u.bio||'';document.getElementById('editWebsite').value=u.website||'';document.getElementById('editContactEmail').value=u.contactEmail||'';_selectedCover=u.coverColor||COVER_COLORS[0];document.getElementById('coverColors').innerHTML=COVER_COLORS.map(c=>`<div onclick="selectCover('${c.replace(/'/g,"\\'")}',this)" style="width:30px;height:30px;border-radius:50%;background:${c};cursor:pointer;border:2px solid ${_selectedCover===c?'#fff':'transparent'}"></div>`).join('');document.getElementById('editPanel').classList.add('show');document.getElementById('overlayPanel').classList.add('show')}
    function selectCover(c,el){_selectedCover=c;document.getElementById('coverSection').style.background=c;document.querySelectorAll('#coverColors div').forEach(d=>d.style.borderColor='transparent');el.style.borderColor='#fff'}
    function closeEditPanel(){document.getElementById('editPanel').classList.remove('show');document.getElementById('overlayPanel').classList.remove('show')}
    async function saveProfile(){const u=document.getElementById('editUsername').value.trim(),b=document.getElementById('editBio').value.trim(),w=document.getElementById('editWebsite').value.trim(),e=document.getElementById('editContactEmail').value.trim();if(!u||u.length<3){showToast('❌ اسم المستخدم 3 أحرف');return}await db.ref('users/'+profileUserId).update({username:u,bio:b,website:w,contactEmail:e,coverColor:_selectedCover});closeEditPanel();location.reload()}
    async function uploadAvatar(inp){const f=inp.files[0];if(!f)return;const fd=new FormData();fd.append('file',f);fd.append('upload_preset',UPLOAD_PRESET);const r=await fetch('https://api.cloudinary.com/v1_1/'+CLOUD_NAME+'/image/upload',{method:'POST',body:fd});const d=await r.json();if(d.secure_url){await db.ref('users/'+profileUserId).update({avatarUrl:d.secure_url,hasCustomAvatar:true});document.getElementById('avatarImg').src=d.secure_url;showToast('✅ تم')}}
    async function uploadCover(inp){const f=inp.files[0];if(!f)return;const fd=new FormData();fd.append('file',f);fd.append('upload_preset',UPLOAD_PRESET);const r=await fetch('https://api.cloudinary.com/v1_1/'+CLOUD_NAME+'/image/upload',{method:'POST',body:fd});const d=await r.json();if(d.secure_url){await db.ref('users/'+profileUserId).update({coverImageUrl:d.secure_url,hasCustomCover:true});document.getElementById('coverImg').src=d.secure_url;document.getElementById('coverImg').style.display='block';showToast('✅ تم')}}
    async function toggleFollowUser(){if(!currentUser||isOwnProfile)return;const b=document.getElementById('followBtn'),ur=db.ref('users/'+currentUser.uid+'/following/'+profileUserId),tr=db.ref('users/'+profileUserId+'/followers/'+currentUser.uid),s=await ur.get();if(s.exists()){await ur.remove();await tr.remove();b.innerHTML='<i class="fas fa-user-plus"></i> متابعة';b.classList.remove('following')}else{await ur.set(true);await tr.set(true);b.innerHTML='<i class="fas fa-user-check"></i> متابع';b.classList.add('following')};location.reload()}
    function showList(type){const u=allUsers[profileUserId],list=type==='followers'?u?.followers||{}:u?.following||{},names=Object.keys(list).map(id=>allUsers[id]?'@'+allUsers[id].username:'مستخدم');alert(names.length?names.join('\\n'):'لا يوجد')}
    function showToast(msg){const t=document.getElementById('toastMsg');t.innerText=msg;t.classList.add('show');setTimeout(()=>t.classList.remove('show'),2500)}
    async function loadAdminPanel(){
        const old=document.getElementById('adminPanelContainer');if(old)old.remove();
        const div=document.createElement('div');div.id='adminPanelContainer';div.className='admin-panel';
        const tu=Object.keys(allUsers).length,tv=allVideos.length;
        div.innerHTML=`<h3><i class="fas fa-crown"></i> لوحة تحكم</h3><div class="admin-stats-grid"><div class="stat-card"><div class="stat-icon"><i class="fas fa-users"></i></div><div><h4>مستخدمين</h4><span>${tu}</span></div></div><div class="stat-card"><div class="stat-icon"><i class="fas fa-video"></i></div><div><h4>فيديوهات</h4><span>${tv}</span></div></div></div><div id="adminUserList"></div><div id="adminVideoList"></div>`;
        document.getElementById('videosContainer').after(div);
        document.getElementById('adminUserList').innerHTML='<h4 style="color:#fbbf24;margin:12px 0">📋 المستخدمين</h4>'+Object.entries(allUsers).slice(0,15).map(([id,u])=>`<div class="admin-user-item"><div><span>@${u.username||'?'}</span>${u.isVerified?' <span class="badge-verified"><i class="fas fa-check"></i></span>':''}</div><div>${u.banned?`<button class="admin-btn btn-ban" onclick="toggleBanUser('${id}')">فك الحظر</button>`:`<button class="admin-btn btn-verify" onclick="toggleVerifyUser('${id}')">${u.isVerified?'إلغاء':'توثيق'}</button><button class="admin-btn btn-ban" onclick="toggleBanUser('${id}')">حظر</button>`}</div></div>`).join('');
        document.getElementById('adminVideoList').innerHTML='<h4 style="color:#fbbf24;margin:12px 0">🎬 الفيديوهات</h4>'+allVideos.slice(0,20).map(v=>`<div class="admin-video-item"><span>${(v.description||'بدون وصف').substring(0,30)}</span><button class="admin-btn btn-delete-video" onclick="deleteVideo('${v.id}')"><i class="fas fa-trash"></i> حذف</button></div>`).join('');
    }
    window.toggleVerifyUser=async(id)=>{const s=await db.ref('users/'+id).once('value'),d=s.val();if(!d)return;const ns=!d.isVerified;await db.ref('users/'+id).update({isVerified:ns,verifiedAt:ns?Date.now():null,verifiedBy:ns?currentUser.uid:null});location.reload()}
    window.toggleBanUser=async(id)=>{const s=await db.ref('users/'+id).once('value'),d=s.val();if(!d)return;const ns=!d.banned;await db.ref('users/'+id).update({banned:ns,bannedAt:ns?Date.now():null,bannedBy:ns?currentUser.uid:null});location.reload()}
    window.deleteVideo=async(id)=>{if(!confirm('حذف الفيديو؟'))return;await db.ref('videos/'+id).remove();location.reload()}
    console.log('👑 GKOM Profile Ready ✨');
</script>
</body>
</html>"""

def build_upload():
    return """<!DOCTYPE html>
<html lang="ar" dir="rtl"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>👑 GKOM | رفع</title>
<script src="https://www.gstatic.com/firebasejs/10.7.0/firebase-app-compat.js"></script>
<script src="https://www.gstatic.com/firebasejs/10.7.0/firebase-database-compat.js"></script>
<script src="https://www.gstatic.com/firebasejs/10.7.0/firebase-auth-compat.js"></script>
<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
<style>:root{--accent:#f59e0b;--border:rgba(245,158,11,0.12);--bg:#0a0a0a;--glass:rgba(184,134,11,0.03)}*{margin:0;padding:0;box-sizing:border-box}body{font-family:'Segoe UI',sans-serif;background:var(--bg);color:#fff;min-height:100vh}.header{display:flex;align-items:center;gap:12px;padding:16px;border-bottom:1px solid var(--border);background:rgba(10,10,10,0.8)}.btn-back{background:rgba(245,158,11,0.1);border:1px solid var(--border);width:38px;height:38px;border-radius:50%;display:flex;align-items:center;justify-content:center;color:#fff;cursor:pointer}.container{max-width:500px;margin:0 auto;padding:20px}.dropzone{border:2px dashed rgba(245,158,11,0.3);border-radius:20px;padding:50px 20px;text-align:center;cursor:pointer;background:var(--glass)}.dropzone i{font-size:48px;color:var(--accent)}.dropzone video{width:100%;max-height:250px;object-fit:contain;margin-top:12px;border-radius:12px;display:none}.form-card{background:rgba(184,134,11,0.03);border:1px solid var(--border);border-radius:20px;padding:20px;margin-top:20px}.form-card textarea,.form-card input{width:100%;padding:14px 16px;border-radius:16px;background:rgba(184,134,11,0.04);border:1px solid var(--border);color:#fff;font-size:14px;outline:none;margin-top:8px}.progress-wrap{display:none;margin:16px 0}.progress-bar{background:rgba(255,255,255,0.1);border-radius:30px;height:6px;overflow:hidden}.progress-fill{background:linear-gradient(90deg,#b8860b,#fbbf24);height:100%;border-radius:30px;width:0%}.btn-upload{width:100%;padding:14px;background:linear-gradient(135deg,#b8860b,#fbbf24);border:none;border-radius:30px;color:#000;font-weight:700;font-size:15px;cursor:pointer;margin-top:16px}</style></head>
<body><div class="header"><button class="btn-back" onclick="window.location.href='index.html'"><i class="fas fa-arrow-right"></i></button><h2>👑 رفع فيديو</h2></div>
<div class="container"><div class="dropzone" onclick="document.getElementById('videoFile').click()"><i class="fas fa-cloud-upload-alt"></i><p>اضغط لاختيار فيديو</p><video id="preview" controls></video></div>
<input type="file" id="videoFile" accept="video/*" style="display:none" onchange="onFilePick(this)">
<div class="form-card"><textarea id="vidDesc" placeholder="وصف الفيديو..."></textarea><input type="text" id="vidMusic" placeholder="Original Sound">
<div class="progress-wrap" id="progressWrap"><div class="progress-bar"><div class="progress-fill" id="progressFill"></div></div><div id="progressText" style="text-align:center;font-size:12px;margin-top:6px;color:#fbbf24">0%</div></div>
<button class="btn-upload" id="uploadBtn" onclick="upload()"><i class="fas fa-gem"></i> رفع</button><div id="status" style="text-align:center;margin-top:12px"></div></div></div>
<script src="firebase-config.js"></script><script>let currentUser=null,selectedFile=null;auth.onAuthStateChanged(async u=>{if(!u)window.location.href='auth.html';currentUser=u});function onFilePick(inp){const f=inp.files[0];if(!f||!f.type.startsWith('video/')){alert('اختر فيديو صحيح');return}selectedFile=f;const r=new FileReader();r.onload=e=>{const v=document.getElementById('preview');v.src=e.target.result;v.style.display='block'};r.readAsDataURL(f)}async function upload(){if(!selectedFile){alert('اختر فيديو');return}const d=document.getElementById('vidDesc').value,m=document.getElementById('vidMusic').value||'Original Sound',pw=document.getElementById('progressWrap'),pf=document.getElementById('progressFill'),pt=document.getElementById('progressText'),st=document.getElementById('status'),btn=document.getElementById('uploadBtn');pw.style.display='block';pf.style.width='0%';pt.innerText='0%';st.innerHTML='';btn.disabled=true;const fd=new FormData();fd.append('file',selectedFile);fd.append('upload_preset',UPLOAD_PRESET);const xhr=new XMLHttpRequest();xhr.open('POST','https://api.cloudinary.com/v1_1/'+CLOUD_NAME+'/video/upload');xhr.upload.onprogress=e=>{if(e.lengthComputable){const p=Math.round(e.loaded/e.total*100);pf.style.width=p+'%';pt.innerText=p+'%'}};xhr.onload=async()=>{const r=JSON.parse(xhr.responseText);await db.ref('videos/').push({url:r.secure_url,thumbnail:r.secure_url.replace('.mp4','.jpg'),description:d,music:m,sender:currentUser.uid,senderName:(await db.ref('users/'+currentUser.uid).get()).val()?.username,likes:0,likedBy:{},comments:{},timestamp:Date.now()});st.innerHTML='✅ تم الرفع!';setTimeout(()=>window.location.href='index.html',1500)};xhr.onerror=()=>{st.innerHTML='❌ فشل';btn.disabled=false};xhr.send(fd)}</script></body></html>"""

def build_chat():
    return """<!DOCTYPE html>
<html lang="ar" dir="rtl"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>👑 GKOM | دردشة</title>
<script src="https://www.gstatic.com/firebasejs/10.7.0/firebase-app-compat.js"></script><script src="https://www.gstatic.com/firebasejs/10.7.0/firebase-database-compat.js"></script><script src="https://www.gstatic.com/firebasejs/10.7.0/firebase-auth-compat.js"></script>
<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
<style>:root{--accent:#f59e0b;--border:rgba(245,158,11,0.12);--bg:#0a0a0a}*{margin:0;padding:0;box-sizing:border-box}body{font-family:'Segoe UI',sans-serif;background:var(--bg);color:#fff;height:100vh;display:flex;flex-direction:column}.header{display:flex;align-items:center;gap:12px;padding:16px;border-bottom:1px solid var(--border);background:rgba(10,10,10,0.8)}.btn-back{background:rgba(245,158,11,0.1);border:1px solid var(--border);width:38px;height:38px;border-radius:50%;display:flex;align-items:center;justify-content:center;color:#fff;cursor:pointer}.msgs{flex:1;overflow-y:auto;padding:16px;display:flex;flex-direction:column;gap:8px}.bubble{max-width:80%;padding:10px 16px;border-radius:20px;word-break:break-word;font-size:14px}.bubble.sent{background:linear-gradient(135deg,#b8860b,#fbbf24);align-self:flex-end;color:#000}.bubble.received{background:rgba(184,134,11,0.06);align-self:flex-start;border:1px solid rgba(245,158,11,0.1)}.bubble img{max-width:200px;border-radius:12px;cursor:pointer;margin-top:4px}.input-bar{display:flex;gap:10px;padding:12px;background:rgba(10,10,10,0.95);border-top:1px solid var(--border)}.input-bar input{flex:1;padding:12px 16px;border-radius:30px;background:rgba(184,134,11,0.04);border:1px solid var(--border);color:#fff;outline:none}.btn-send{width:42px;height:42px;background:linear-gradient(135deg,#b8860b,#fbbf24);border:none;border-radius:50%;color:#000;cursor:pointer;font-size:18px}.conv-item{display:flex;align-items:center;gap:12px;padding:14px;border-bottom:1px solid var(--border);cursor:pointer}.chat-avatar{width:40px;height:40px;border-radius:50%;overflow:hidden}.chat-avatar img{width:100%;height:100%;object-fit:cover}.image-lightbox{position:fixed;inset:0;background:rgba(0,0,0,0.96);z-index:9999;display:flex;align-items:center;justify-content:center;opacity:0;pointer-events:none;transition:opacity 0.3s;flex-direction:column}.image-lightbox.active{opacity:1;pointer-events:auto}.image-lightbox img{max-width:95vw;max-height:80vh;border-radius:16px}.close-lightbox{position:absolute;top:20px;left:20px;background:rgba(0,0,0,0.5);color:#fff;width:44px;height:44px;border-radius:50%;display:flex;align-items:center;justify-content:center;cursor:pointer;z-index:10001}</style></head>
<body>
<div class="image-lightbox" id="imageLightbox" onclick="if(event.target===this)closeLightbox()"><button class="close-lightbox" onclick="closeLightbox()"><i class="fas fa-times"></i></button><img id="lightboxImage" src=""></div>
<div id="loader" style="flex:1;display:flex;align-items:center;justify-content:center"><span>👑 تحميل...</span></div>
<div id="convView" style="display:none;flex:1;flex-direction:column"><div class="header"><button class="btn-back" onclick="window.location.href='index.html'"><i class="fas fa-arrow-right"></i></button><h2>المحادثات</h2></div><div id="convList" style="flex:1;overflow-y:auto"></div></div>
<div id="chatView" style="display:none;flex:1;flex-direction:column"><div class="header"><button class="btn-back" onclick="showConvs()"><i class="fas fa-arrow-right"></i></button><div class="chat-avatar" id="chatAvatar"></div><h3 id="chatName"></h3></div><div class="msgs" id="msgsList"></div><div class="input-bar"><input type="text" id="msgInput" placeholder="اكتب..." onkeydown="if(event.key==='Enter')sendMsg()"><button class="btn-send" onclick="sendMsg()"><i class="fas fa-paper-plane"></i></button></div></div>
<script src="firebase-config.js"></script><script>let currentUser=null,allUsers={},chatUserId=null;function openLightbox(url){document.getElementById('imageLightbox').classList.add('active');document.getElementById('lightboxImage').src=url}function closeLightbox(){document.getElementById('imageLightbox').classList.remove('active')}auth.onAuthStateChanged(async u=>{if(!u){window.location.href='auth.html';return}currentUser=u;const us=await db.ref('users').once('value');allUsers=us.val()||{};document.getElementById('loader').style.display='none';const p=new URLSearchParams(window.location.search),t=p.get('uid');t?openChat(t):showConvs()});function showConvs(){document.getElementById('chatView').style.display='none';document.getElementById('convView').style.display='flex';loadConvs()}async function loadConvs(){const cl=document.getElementById('convList');cl.innerHTML='';const snap=await db.ref('private_messages').once('value'),all=snap.val()||{},found=new Set();Object.keys(all).forEach(cid=>{const[u1,u2]=cid.split('_'),o=u1===currentUser.uid?u2:u2===currentUser.uid?u1:null;if(o&&!found.has(o)&&allUsers[o])found.add(o)});found.forEach(uid=>{const u=allUsers[uid],d=document.createElement('div');d.className='conv-item';d.innerHTML=`<div class="chat-avatar"><img src="${u?.avatarUrl||DICEBEAR_URL+'?seed='+uid}"></div><div>@${u?.username||'?'}</div>`;d.onclick=()=>openChat(uid);cl.appendChild(d)})}function openChat(uid){chatUserId=uid;document.getElementById('chatName').innerText='@'+(allUsers[uid]?.username||'');document.getElementById('chatAvatar').innerHTML=`<img src="${allUsers[uid]?.avatarUrl||DICEBEAR_URL+'?seed='+uid}">`;document.getElementById('convView').style.display='none';document.getElementById('chatView').style.display='flex';loadMsgs()}function getChatId(){return[currentUser.uid,chatUserId].sort().join('_')}async function loadMsgs(){const ml=document.getElementById('msgsList');ml.innerHTML='';const snap=await db.ref('private_messages/'+getChatId()).once('value'),ms=snap.val()||{};Object.values(ms).sort((a,b)=>a.timestamp-b.timestamp).forEach(m=>{const d=document.createElement('div');d.className='bubble '+(m.senderId===currentUser.uid?'sent':'received');d.innerHTML=`${m.type==='image'?`<img src="${m.imageUrl}" onclick="openLightbox('${m.imageUrl}')">`:m.text}<div style="font-size:9px;opacity:0.6;margin-top:4px">${new Date(m.timestamp).toLocaleTimeString('ar-SA')}</div>`;ml.appendChild(d)});ml.scrollTop=ml.scrollHeight}async function sendMsg(){const i=document.getElementById('msgInput'),t=i.value.trim();if(!t)return;await db.ref('private_messages/'+getChatId()).push({senderId:currentUser.uid,text:t,type:'text',timestamp:Date.now()});i.value='';await loadMsgs()}</script></body></html>"""

def build_explore():
    return """<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>👑 GKOM | استكشاف</title><script src="https://www.gstatic.com/firebasejs/10.7.0/firebase-app-compat.js"></script><script src="https://www.gstatic.com/firebasejs/10.7.0/firebase-database-compat.js"></script><script src="https://www.gstatic.com/firebasejs/10.7.0/firebase-auth-compat.js"></script><link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet"><style>:root{--accent:#f59e0b;--border:rgba(245,158,11,0.12);--bg:#0a0a0a}*{margin:0;padding:0;box-sizing:border-box}body{font-family:'Segoe UI',sans-serif;background:var(--bg);color:#fff;min-height:100vh}.header{display:flex;align-items:center;gap:12px;padding:16px;border-bottom:1px solid var(--border)}.btn-back{background:rgba(245,158,11,0.1);border:1px solid var(--border);width:38px;height:38px;border-radius:50%;display:flex;align-items:center;justify-content:center;color:#fff;cursor:pointer}.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:2px;padding:2px}.thumb{aspect-ratio:9/16;background:rgba(245,158,11,0.05);cursor:pointer;position:relative;overflow:hidden}.thumb img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}.thumb i{position:absolute;font-size:24px;color:#fff;z-index:1;opacity:0}.thumb:hover i{opacity:1}.thumb .views{position:absolute;bottom:4px;left:4px;font-size:10px;background:rgba(0,0,0,0.6);padding:2px 6px;border-radius:10px}</style></head><body><div class="header"><button class="btn-back" onclick="window.location.href='index.html'"><i class="fas fa-arrow-right"></i></button><h2>👑 استكشاف</h2></div><div class="grid" id="exploreGrid"></div><script src="firebase-config.js"></script><script>auth.onAuthStateChanged(async u=>{if(!u)window.location.href='auth.html';const s=await db.ref('videos').once('value'),v=s.val()||{},all=Object.entries(v).map(([k,v])=>({id:k,...v})).sort((a,b)=>(b.likes||0)-(a.likes||0)),g=document.getElementById('exploreGrid');g.innerHTML=all.length?all.map(v=>`<div class="thumb" onclick="window.open('${v.url}','_blank')">${v.thumbnail?`<img src="${v.thumbnail}">`:''}<i class="fas fa-play"></i><span class="views">❤️ ${v.likes||0}</span></div>`).join(''):'<div style="grid-column:1/-1;text-align:center;padding:40px;opacity:0.5">لا فيديوهات</div>'})</script></body></html>"""

def build_notifications():
    return """<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>👑 GKOM | إشعارات</title><script src="https://www.gstatic.com/firebasejs/10.7.0/firebase-app-compat.js"></script><script src="https://www.gstatic.com/firebasejs/10.7.0/firebase-database-compat.js"></script><script src="https://www.gstatic.com/firebasejs/10.7.0/firebase-auth-compat.js"></script><link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet"><style>:root{--accent:#f59e0b;--border:rgba(245,158,11,0.12);--bg:#0a0a0a}*{margin:0;padding:0;box-sizing:border-box}body{font-family:'Segoe UI',sans-serif;background:var(--bg);color:#fff;min-height:100vh}.header{display:flex;align-items:center;gap:12px;padding:16px;border-bottom:1px solid var(--border)}.btn-back{background:rgba(245,158,11,0.1);border:1px solid var(--border);width:38px;height:38px;border-radius:50%;display:flex;align-items:center;justify-content:center;color:#fff;cursor:pointer}.notif-item{display:flex;gap:12px;padding:14px 16px;border-bottom:1px solid var(--border)}.notif-icon{width:40px;height:40px;border-radius:50%;background:rgba(245,158,11,0.1);display:flex;align-items:center;justify-content:center;color:var(--accent)}</style></head><body><div class="header"><button class="btn-back" onclick="window.location.href='index.html'"><i class="fas fa-arrow-right"></i></button><h2>👑 إشعارات</h2></div><div id="notifsList"></div><script src="firebase-config.js"></script><script>auth.onAuthStateChanged(async u=>{if(!u)window.location.href='auth.html';const s=await db.ref('notifications/'+u.uid).once('value'),ns=s.val()||{},items=Object.values(ns).reverse(),c=document.getElementById('notifsList');c.innerHTML=items.length?items.map(n=>`<div class="notif-item"><div class="notif-icon"><i class="fas fa-bell"></i></div><div><div style="font-weight:600">${n.from||'مستخدم'}</div><div style="font-size:12px;opacity:0.6">${n.msg||''}</div></div></div>`).join(''):'<div style="text-align:center;opacity:0.5;padding:40px"><i class="fas fa-bell" style="font-size:48px;color:#f59e0b;display:block;margin-bottom:12px"></i><p>لا إشعارات</p></div>'})</script></body></html>"""

def build_settings():
    return """<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>👑 GKOM | إعدادات</title><script src="https://www.gstatic.com/firebasejs/10.7.0/firebase-app-compat.js"></script><script src="https://www.gstatic.com/firebasejs/10.7.0/firebase-database-compat.js"></script><script src="https://www.gstatic.com/firebasejs/10.7.0/firebase-auth-compat.js"></script><link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet"><style>:root{--accent:#f59e0b;--border:rgba(245,158,11,0.12);--bg:#0a0a0a;--glass:rgba(184,134,11,0.03)}*{margin:0;padding:0;box-sizing:border-box}body{font-family:'Segoe UI',sans-serif;background:var(--bg);color:#fff;min-height:100vh}.header{display:flex;align-items:center;gap:12px;padding:16px;border-bottom:1px solid var(--border)}.btn-back{background:rgba(245,158,11,0.1);border:1px solid var(--border);width:38px;height:38px;border-radius:50%;display:flex;align-items:center;justify-content:center;color:#fff;cursor:pointer}.setting-item{display:flex;justify-content:space-between;align-items:center;padding:16px;border-bottom:1px solid var(--border);cursor:pointer}.setting-item:hover{background:var(--glass)}.btn-danger{background:rgba(239,68,68,0.2);border:1px solid rgba(239,68,68,0.3);color:#f87171;padding:12px 24px;border-radius:30px;cursor:pointer;margin:20px auto;display:block}</style></head><body><div class="header"><button class="btn-back" onclick="window.location.href='index.html'"><i class="fas fa-arrow-right"></i></button><h2>👑 إعدادات</h2></div><div><div class="setting-item" onclick="window.location.href='profile.html'"><span>👤 الملف الشخصي</span><i class="fas fa-chevron-left"></i></div><div class="setting-item"><span>🔒 الخصوصية</span></div><div class="setting-item"><span>🌐 اللغة: العربية</span></div><div class="setting-item"><span>ℹ️ GKOM v2026.1 👑</span></div><button class="btn-danger" onclick="if(confirm('تسجيل الخروج؟')){auth.signOut();window.location.href='auth.html'}"><i class="fas fa-sign-out-alt"></i> خروج</button></div><script src="firebase-config.js"></script><script>auth.onAuthStateChanged(u=>{if(!u)window.location.href='auth.html'})</script></body></html>"""

# ═══════════════════════════════════════════════════════════
# 👑 ANDROID PROJECT
# ═══════════════════════════════════════════════════════════

def build_android_project():
    write("android-project/build.gradle", """buildscript{repositories{google();mavenCentral()}dependencies{classpath'com.android.tools.build:gradle:8.2.0'}}allprojects{repositories{google();mavenCentral()}}task clean(type:Delete){delete rootProject.buildDir}""")
    write("android-project/settings.gradle", """rootProject.name="GKOM"\ninclude':app'""")
    write("android-project/gradle.properties", """org.gradle.jvmargs=-Xmx2048m\nandroid.useAndroidX=true\nandroid.enableJetifier=true""")
    write("android-project/app/build.gradle", """plugins{id'com.android.application'}android{namespace'com.gkom.app'compileSdk34 defaultConfig{applicationId"com.gkom.app"minSdk21 targetSdk34 versionCode1 versionName"1.0.0"}buildTypes{release{minifyEnabled false}}}dependencies{implementation'androidx.appcompat:appcompat:1.6.1'\nimplementation'com.google.android.material:material:1.9.0'}""")
    write("android-project/app/src/main/AndroidManifest.xml", """<?xml version="1.0" encoding="utf-8"?><manifest xmlns:android="http://schemas.android.com/apk/res/android"><uses-permission android:name="android.permission.INTERNET"/><uses-permission android:name="android.permission.CAMERA"/><application android:allowBackup="true" android:icon="@mipmap/ic_launcher" android:label="GKOM" android:supportsRtl="true" android:theme="@style/Theme.GKOM"><activity android:name=".MainActivity" android:exported="true" android:configChanges="orientation|screenSize" android:screenOrientation="portrait"><intent-filter><action android:name="android.intent.action.MAIN"/><category android:name="android.intent.category.LAUNCHER"/></intent-filter></activity></application></manifest>""")
    write("android-project/app/src/main/java/com/gkom/app/MainActivity.java", """package com.gkom.app;import android.os.Bundle;import android.webkit.*;import androidx.appcompat.app.AppCompatActivity;public class MainActivity extends AppCompatActivity{@Override protected void onCreate(Bundle s){super.onCreate(s);WebView w=new WebView(this);setContentView(w);WebSettings ws=w.getSettings();ws.setJavaScriptEnabled(true);ws.setDomStorageEnabled(true);ws.setAllowFileAccess(true);ws.setMediaPlaybackRequiresUserGesture(false);ws.setMixedContentMode(WebSettings.MIXED_CONTENT_ALWAYS_ALLOW);w.setWebViewClient(new WebViewClient());w.setWebChromeClient(new WebChromeClient());w.loadUrl("file:///android_asset/www/index.html");}}""")
    write("android-project/app/src/main/res/values/styles.xml", """<?xml version="1.0" encoding="utf-8"?><resources><style name="Theme.GKOM" parent="Theme.MaterialComponents.DayNight.NoActionBar"><item name="android:statusBarColor">#0a0a0a</item><item name="android:windowBackground">#0a0a0a</item></style></resources>""")

def copy_web_files_to_assets():
    assets_dir = "android-project/app/src/main/assets/www"
    os.makedirs(assets_dir, exist_ok=True)
    for file in ["index.html","auth.html","profile.html","upload.html","chat.html","explore.html","notifications.html","settings.html","firebase-config.js"]:
        if os.path.exists(file):
            shutil.copy(file, os.path.join(assets_dir, file))
            print(f"  ✅ نسخ {file} → assets/www/")

# ═══════════════════════════════════════════════════════════
# 👑 GITHUB ACTIONS
# ═══════════════════════════════════════════════════════════

def build_main_yml():
    return """name: 👑 GKOM - Auto Deploy
on:
  push:
    branches: [main, master]
  workflow_dispatch:
permissions:
  contents: write
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - run: python scraper.py
      - uses: stefanzweifel/git-auto-commit-action@v5
        with:
          commit_message: "👑 GKOM Auto Deploy [skip ci]"
          file_pattern: '*.html *.js'
"""

def build_apk_yml():
    return """name: 👑 Build GKOM APK
on:
  push:
    tags: ['v*']
  workflow_dispatch:
permissions:
  contents: write
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - run: python scraper.py
      - uses: actions/setup-java@v4
        with:
          java-version: '17'
          distribution: 'temurin'
      - uses: android-actions/setup-android@v3
        with:
          packages: 'platforms;android-34 build-tools;34.0.0'
      - run: |
          mkdir -p android-project/app/src/main/assets/www
          cp *.html *.js android-project/app/src/main/assets/www/
      - run: |
          cd android-project
          chmod +x gradlew
          ./gradlew assembleRelease
      - run: |
          keytool -genkey -v -keystore release-key.jks -alias gkom -keyalg RSA -keysize 2048 -validity 10000 -storepass gkom2026 -keypass gkom2026 -dname "CN=GKOM"
          $ANDROID_HOME/build-tools/34.0.0/apksigner sign --ks release-key.jks --ks-pass pass:gkom2026 --out GKOM-Release.apk android-project/app/build/outputs/apk/release/app-release-unsigned.apk
      - uses: softprops/action-gh-release@v2
        with:
          files: "GKOM-Release.apk"
          name: "👑 GKOM v${{ github.ref_name }}"
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
"""

# ═══════════════════════════════════════════════════════════
# 👑 MAIN
# ═══════════════════════════════════════════════════════════

def main():
    print("""👑 GKOM 2026 - GOLDEN ULTRA EDITION""")
    section("BUILDING WEB FILES")
    write("firebase-config.js", build_config())
    write("auth.html", build_auth())
    write("index.html", build_index())
    write("profile.html", build_profile())
    write("upload.html", build_upload())
    write("chat.html", build_chat())
    write("explore.html", build_explore())
    write("notifications.html", build_notifications())
    write("settings.html", build_settings())
    section("BUILDING ANDROID PROJECT")
    build_android_project()
    copy_web_files_to_assets()
    section("BUILDING GITHUB ACTIONS")
    os.makedirs(".github/workflows", exist_ok=True)
    write(".github/workflows/main.yml", build_main_yml())
    write(".github/workflows/build-apk.yml", build_apk_yml())
    print(f"""✅ DONE! | Firebase: gkom-604f1 | Cloudinary: dshgbhw4h | Admin: jasim28v@gmail.com""")

if __name__ == "__main__":
    main()
