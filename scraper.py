#!/usr/bin/env python3
"""
Rose Sphere - Offline APK Builder
يسحب جميع ملفات الموقع من المستودع ويبني APK كامل
"""
import os, sys, shutil, logging, argparse, json
from pathlib import Path
from datetime import datetime
import zipfile

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('RoseSphereAPK')

# قائمة جميع ملفات موقع Rose Sphere
SITE_FILES = [
    'index.html',
    'auth.html', 
    'chat.html',
    'explore.html',
    'profile.html',
    'settings.html',
    'notifications.html',
    'upload.html',
    'firebase-config.js',
    'service-worker.js',
    'server.js',
    'package.json'
]

class RoseSphereAPKBuilder:
    def __init__(self):
        self.output_dir = Path("generated_apks")
        self.output_dir.mkdir(exist_ok=True)
        self.files_found = []
        self.files_missing = []

    def collect_site_files(self) -> dict:
        """جمع جميع ملفات الموقع من المستودع"""
        logger.info("🔍 جمع ملفات Rose Sphere...")
        
        site_content = {}
        
        for filename in SITE_FILES:
            if os.path.exists(filename):
                with open(filename, 'r', encoding='utf-8') as f:
                    site_content[filename] = f.read()
                self.files_found.append(filename)
                logger.info(f"✅ {filename}")
            else:
                self.files_missing.append(filename)
                logger.warning(f"❌ {filename} غير موجود")
        
        logger.info(f"تم العثور على {len(self.files_found)}/{len(SITE_FILES)} ملف")
        return site_content

    def create_index_with_navigation(self, site_content: dict) -> str:
        """إنشاء صفحة رئيسية مع التنقل بين جميع الصفحات"""
        
        # روابط لجميع الصفحات الموجودة
        nav_links = []
        page_names = {
            'index.html': '🏠 الرئيسية',
            'auth.html': '🔐 تسجيل الدخول',
            'chat.html': '💬 المحادثة',
            'explore.html': '🔍 استكشاف',
            'profile.html': '👤 الملف الشخصي',
            'settings.html': '⚙️ الإعدادات',
            'notifications.html': '🔔 الإشعارات',
            'upload.html': '📤 رفع'
        }
        
        for filename in self.files_found:
            if filename.endswith('.html'):
                name = page_names.get(filename, filename)
                nav_links.append(f'<a href="{filename}" class="nav-link">{name}</a>')
        
        return f'''<!DOCTYPE html>
<html dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🌹 Rose Sphere</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Segoe UI', Tahoma, sans-serif; background: linear-gradient(135deg, #0f0c29, #302b63, #24243e); color: white; min-height: 100vh; }}
        .header {{ background: rgba(0,0,0,0.5); padding: 20px; text-align: center; border-bottom: 2px solid rgba(255,255,255,0.1); }}
        .header h1 {{ font-size: 2em; margin-bottom: 10px; }}
        .header p {{ opacity: 0.8; }}
        .nav-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 15px; padding: 20px; max-width: 800px; margin: 0 auto; }}
        .nav-link {{ background: rgba(255,255,255,0.1); padding: 20px; border-radius: 15px; text-align: center; text-decoration: none; color: white; font-size: 1.2em; transition: all 0.3s; border: 1px solid rgba(255,255,255,0.2); display: block; }}
        .nav-link:hover {{ background: rgba(255,255,255,0.2); transform: translateY(-3px); box-shadow: 0 10px 25px rgba(0,0,0,0.3); }}
        .frame-container {{ display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: white; z-index: 1000; }}
        .frame-container.active {{ display: block; }}
        .frame-header {{ background: #302b63; color: white; padding: 15px; display: flex; justify-content: space-between; align-items: center; }}
        .back-btn {{ background: rgba(255,255,255,0.2); border: none; color: white; padding: 10px 20px; border-radius: 8px; cursor: pointer; font-size: 16px; }}
        iframe {{ width: 100%; height: calc(100% - 60px); border: none; }}
        .status {{ text-align: center; padding: 20px; background: rgba(255,255,255,0.05); margin: 20px; border-radius: 10px; }}
        .files-list {{ display: flex; flex-wrap: wrap; gap: 5px; justify-content: center; margin-top: 10px; }}
        .file-tag {{ background: rgba(255,255,255,0.1); padding: 3px 8px; border-radius: 5px; font-size: 0.8em; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🌹 Rose Sphere</h1>
        <p>تطبيق يعمل بدون إنترنت - جميع الصفحات متوفرة</p>
    </div>
    
    <div class="status">
        <p>✅ تم تحميل {len(self.files_found)} ملف بنجاح</p>
        <div class="files-list">
            {"".join(f'<span class="file-tag">📄 {f}</span>' for f in self.files_found)}
        </div>
    </div>
    
    <div class="nav-grid">
        {"".join(nav_links)}
    </div>
    
    <div class="frame-container" id="pageFrame">
        <div class="frame-header">
            <span id="frameTitle">الصفحة</span>
            <button class="back-btn" onclick="closeFrame()">✕ إغلاق</button>
        </div>
        <iframe id="contentFrame" src=""></iframe>
    </div>
    
    <script>
        // فتح الصفحة في iframe
        document.querySelectorAll('.nav-link').forEach(link => {{
            link.addEventListener('click', function(e) {{
                e.preventDefault();
                const url = this.getAttribute('href');
                document.getElementById('contentFrame').src = url;
                document.getElementById('frameTitle').textContent = this.textContent;
                document.getElementById('pageFrame').classList.add('active');
            }});
        }});
        
        // إغلاق iframe
        function closeFrame() {{
            document.getElementById('pageFrame').classList.remove('active');
            document.getElementById('contentFrame').src = '';
        }}
    </script>
</body>
</html>'''

    def build_apk(self, config: dict) -> str:
        """بناء APK كامل بجميع ملفات الموقع"""
        logger.info("🚀 بدء بناء APK لـ Rose Sphere...")
        
        # جمع الملفات
        site_content = self.collect_site_files()
        
        if not self.files_found:
            raise Exception("لم يتم العثور على أي ملفات!")
        
        # إنشاء صفحة التنقل
        index_html = self.create_index_with_navigation(site_content)
        site_content['index.html'] = index_html
        
        # بناء APK
        apk_name = f"{config.get('app_name', 'RoseSphere')}_{config.get('version', '1.0.0')}.apk"
        apk_path = self.output_dir / apk_name
        
        with zipfile.ZipFile(apk_path, 'w', zipfile.ZIP_DEFLATED) as z:
            # AndroidManifest
            manifest = self._create_manifest(config)
            z.writestr('AndroidManifest.xml', manifest)
            
            # موارد الأندرويد
            z.writestr('res/values/strings.xml', 
                f'<?xml version="1.0" encoding="utf-8"?><resources><string name="app_name">{config.get("app_name", "Rose Sphere")}</string></resources>')
            
            # جميع ملفات الموقع
            for filename, content in site_content.items():
                arcname = f'assets/{filename}'
                z.writestr(arcname, content)
                logger.info(f"✅ أضيف: {filename}")
        
        size_mb = os.path.getsize(apk_path) / (1024 * 1024)
        logger.info(f"✅ APK تم بناؤه: {apk_path} ({size_mb:.1f} MB)")
        
        # تقرير
        logger.info(f"\n📊 تقرير البناء:")
        logger.info(f"   ✅ ملفات مضافة: {len(self.files_found)}")
        if self.files_missing:
            logger.info(f"   ❌ ملفات مفقودة: {len(self.files_missing)}")
        
        return str(apk_path)

    def _create_manifest(self, config: dict) -> str:
        return f'''<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="{config.get('package_name', 'com.rosesphere.app')}">
    <uses-permission android:name="android.permission.INTERNET"/>
    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE"/>
    <application 
        android:label="{config.get('app_name', 'Rose Sphere')}" 
        android:icon="@mipmap/ic_launcher"
        android:usesCleartextTraffic="true"
        android:hardwareAccelerated="true">
        <activity 
            android:name=".MainActivity"
            android:configChanges="orientation|screenSize|keyboardHidden">
            <intent-filter>
                <action android:name="android.intent.action.MAIN"/>
                <category android:name="android.intent.category.LAUNCHER"/>
            </intent-filter>
        </activity>
    </application>
</manifest>'''

def main():
    parser = argparse.ArgumentParser(description='Rose Sphere APK Builder')
    parser.add_argument('--name', default='RoseSphere', help='اسم التطبيق')
    parser.add_argument('--package', default='com.rosesphere.app', help='اسم الحزمة')
    parser.add_argument('--version', default='1.0.0', help='الإصدار')
    args = parser.parse_args()
    
    config = {
        'app_name': args.name,
        'package_name': args.package,
        'version': args.version
    }
    
    print("\n" + "="*50)
    print("🌹 Rose Sphere - Offline APK Builder")
    print("="*50)
    
    builder = RoseSphereAPKBuilder()
    apk_path = builder.build_apk(config)
    
    print("\n" + "="*50)
    print("✅ تم بنجاح!")
    print(f"📱 المسار: {apk_path}")
    print(f"📦 الحجم: {os.path.getsize(apk_path)/1024:.1f} KB")
    print(f"📄 عدد الملفات: {len(builder.files_found)}")
    print("="*50)
    print("\n📱 صفحات التطبيق:")
    for f in builder.files_found:
        if f.endswith('.html'):
            print(f"  ✅ {f}")

if __name__ == "__main__":
    main()
