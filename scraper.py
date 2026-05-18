#!/usr/bin/env python3
"""
ينشئ مشروع Android كامل مع ملفات الموقع جاهز لبناء APK
"""
import os, sys, shutil, logging, argparse, json
from pathlib import Path
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('AndroidProjectCreator')

# ملفات موقعك
SITE_FILES = [
    'index.html', 'auth.html', 'chat.html', 'explore.html',
    'profile.html', 'settings.html', 'notifications.html', 'upload.html',
    'firebase-config.js', 'service-worker.js', 'server.js', 'package.json'
]

class AndroidProjectCreator:
    def __init__(self, config: dict):
        self.config = config
        self.project_dir = Path('android_project')
        self.package_path = config['package'].replace('.', '/')
        
    def create(self):
        """إنشاء مشروع Android كامل"""
        logger.info("🚀 إنشاء مشروع Android...")
        
        if self.project_dir.exists():
            shutil.rmtree(self.project_dir)
        
        # 1. هيكل المجلدات
        self._create_directories()
        
        # 2. ملفات Gradle
        self._create_settings_gradle()
        self._create_project_build_gradle()
        self._create_app_build_gradle()
        self._create_gradle_properties()
        
        # 3. AndroidManifest
        self._create_manifest()
        
        # 4. كود Java
        self._create_main_activity()
        
        # 5. موارد Android
        self._create_layouts()
        self._create_values()
        self._create_drawables()
        
        # 6. نسخ ملفات الموقع
        self._copy_site_files()
        
        # 7. تقرير
        self._create_report()
        
        logger.info("✅ تم إنشاء مشروع Android بنجاح!")
        return str(self.project_dir)
    
    def _create_directories(self):
        """إنشاء هيكل المجلدات"""
        dirs = [
            f'app/src/main/java/{self.package_path}',
            'app/src/main/res/layout',
            'app/src/main/res/values',
            'app/src/main/res/drawable',
            'app/src/main/assets',
            'app/src/main/res/mipmap-hdpi',
            'app/src/main/res/mipmap-mdpi',
            'app/src/main/res/mipmap-xhdpi',
            'app/src/main/res/mipmap-xxhdpi',
            'app/src/main/res/mipmap-xxxhdpi',
            'gradle/wrapper'
        ]
        for d in dirs:
            (self.project_dir / d).mkdir(parents=True, exist_ok=True)
    
    def _create_settings_gradle(self):
        """settings.gradle"""
        content = f'''pluginManagement {{
    repositories {{
        google()
        mavenCentral()
        gradlePluginPortal()
    }}
}}
dependencyResolution {{
    repositories {{
        google()
        mavenCentral()
    }}
}}
rootProject.name = "{self.config['name'].replace(' ', '')}"
include ':app'
'''
        self._write('settings.gradle', content)
    
    def _create_project_build_gradle(self):
        """build.gradle (project)"""
        content = '''plugins {
    id 'com.android.application' version '8.2.0' apply false
}
'''
        self._write('build.gradle', content)
    
    def _create_app_build_gradle(self):
        """app/build.gradle"""
        content = f'''plugins {{
    id 'com.android.application'
}}

android {{
    namespace '{self.config["package"]}'
    compileSdk 34
    
    defaultConfig {{
        applicationId '{self.config["package"]}'
        minSdk 21
        targetSdk 34
        versionCode 1
        versionName '{self.config["version"]}'
    }}
    
    buildTypes {{
        release {{
            minifyEnabled false
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt')
        }}
    }}
    
    compileOptions {{
        sourceCompatibility JavaVersion.VERSION_1_8
        targetCompatibility JavaVersion.VERSION_1_8
    }}
}}
'''
        self._write('app/build.gradle', content)
    
    def _create_gradle_properties(self):
        """gradle.properties"""
        content = '''org.gradle.jvmargs=-Xmx2048m -Dfile.encoding=UTF-8
android.useAndroidX=true
android.nonTransitiveRClass=true
'''
        self._write('gradle.properties', content)
    
    def _create_manifest(self):
        """app/src/main/AndroidManifest.xml"""
        content = f'''<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android">
    
    <uses-permission android:name="android.permission.INTERNET"/>
    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE"/>
    <uses-permission android:name="android.permission.ACCESS_WIFI_STATE"/>
    
    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="{self.config['name']}"
        android:supportsRtl="true"
        android:theme="@style/AppTheme"
        android:usesCleartextTraffic="true"
        android:hardwareAccelerated="true">
        
        <activity
            android:name=".{self.config['name'].replace(' ', '')}Activity"
            android:exported="true"
            android:configChanges="orientation|screenSize|keyboardHidden|screenLayout|smallestScreenSize">
            <intent-filter>
                <action android:name="android.intent.action.MAIN"/>
                <category android:name="android.intent.category.LAUNCHER"/>
            </intent-filter>
        </activity>
    </application>
</manifest>'''
        self._write('app/src/main/AndroidManifest.xml', content)
    
    def _create_main_activity(self):
        """MainActivity.java"""
        app_name = self.config['name'].replace(' ', '')
        content = f'''package {self.config["package"]};

import android.app.Activity;
import android.os.Bundle;
import android.webkit.WebView;
import android.webkit.WebSettings;
import android.webkit.WebViewClient;
import android.webkit.WebChromeClient;
import android.view.KeyEvent;
import android.view.Window;
import android.view.WindowManager;
import android.graphics.Color;

public class {app_name}Activity extends Activity {{
    private WebView webView;
    
    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        
        // إخفاء شريط العنوان
        requestWindowFeature(Window.FEATURE_NO_TITLE);
        getWindow().setFlags(
            WindowManager.LayoutParams.FLAG_FULLSCREEN,
            WindowManager.LayoutParams.FLAG_FULLSCREEN
        );
        
        webView = new WebView(this);
        WebSettings settings = webView.getSettings();
        settings.setJavaScriptEnabled(true);
        settings.setDomStorageEnabled(true);
        settings.setAllowFileAccess(true);
        settings.setAllowContentAccess(true);
        settings.setAllowFileAccessFromFileURLs(true);
        settings.setAllowUniversalAccessFromFileURLs(true);
        settings.setLoadWithOverviewMode(true);
        settings.setUseWideViewPort(true);
        settings.setBuiltInZoomControls(true);
        settings.setDisplayZoomControls(false);
        
        webView.setWebViewClient(new WebViewClient());
        webView.setWebChromeClient(new WebChromeClient());
        webView.setBackgroundColor(Color.WHITE);
        webView.loadUrl("file:///android_asset/index.html");
        
        setContentView(webView);
    }}
    
    @Override
    public boolean onKeyDown(int keyCode, KeyEvent event) {{
        if (keyCode == KeyEvent.KEYCODE_BACK && webView.canGoBack()) {{
            webView.goBack();
            return true;
        }}
        return super.onKeyDown(keyCode, event);
    }}
}}
'''
        self._write(f'app/src/main/java/{self.package_path}/{app_name}Activity.java', content)
    
    def _create_layouts(self):
        """activity_main.xml"""
        content = '''<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical">
    
    <WebView
        android:id="@+id/webview"
        android:layout_width="match_parent"
        android:layout_height="match_parent"/>
</LinearLayout>'''
        self._write('app/src/main/res/layout/activity_main.xml', content)
    
    def _create_values(self):
        """strings.xml, styles.xml, colors.xml"""
        strings = f'''<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string name="app_name">{self.config['name']}</string>
</resources>'''
        self._write('app/src/main/res/values/strings.xml', strings)
        
        styles = '''<?xml version="1.0" encoding="utf-8"?>
<resources>
    <style name="AppTheme" parent="android:Theme.Material.Light.NoActionBar">
        <item name="android:statusBarColor">@color/colorPrimaryDark</item>
        <item name="android:navigationBarColor">@color/colorPrimaryDark</item>
    </style>
</resources>'''
        self._write('app/src/main/res/values/styles.xml', styles)
        
        colors = '''<?xml version="1.0" encoding="utf-8"?>
<resources>
    <color name="colorPrimary">#1a1a2e</color>
    <color name="colorPrimaryDark">#16213e</color>
    <color name="colorAccent">#0f3460</color>
</resources>'''
        self._write('app/src/main/res/values/colors.xml', colors)
    
    def _create_drawables(self):
        """ic_launcher.xml"""
        launcher = '''<?xml version="1.0" encoding="utf-8"?>
<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">
    <background android:drawable="@color/colorPrimary"/>
    <foreground android:drawable="@color/colorAccent"/>
</adaptive-icon>'''
        self._write('app/src/main/res/drawable/ic_launcher.xml', launcher)
    
    def _copy_site_files(self):
        """نسخ ملفات الموقع إلى assets"""
        assets_dir = self.project_dir / 'app/src/main/assets'
        copied = 0
        
        logger.info("📁 نسخ ملفات الموقع إلى assets...")
        for filename in SITE_FILES:
            src = Path(filename)
            if src.exists():
                shutil.copy2(src, assets_dir / filename)
                logger.info(f"✅ {filename}")
                copied += 1
            else:
                logger.warning(f"⚠️ {filename} غير موجود")
        
        logger.info(f"📊 تم نسخ {copied} ملف من {len(SITE_FILES)}")
        
        # إنشاء index.html افتراضي إذا لم يكن موجوداً
        if not (assets_dir / 'index.html').exists():
            self._create_default_index(assets_dir)
    
    def _create_default_index(self, assets_dir: Path):
        """إنشاء صفحة افتراضية"""
        html_files = list(assets_dir.glob('*.html'))
        links = ''.join(f'<li><a href="{f.name}">{f.stem}</a></li>' for f in html_files)
        
        index = f'''<!DOCTYPE html>
<html dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{self.config['name']}</title>
    <style>
        body {{ font-family: Arial; background: linear-gradient(135deg, #1a1a2e, #16213e); color: white; min-height: 100vh; padding: 20px; }}
        h1 {{ text-align: center; }}
        ul {{ list-style: none; max-width: 600px; margin: 20px auto; }}
        li {{ margin: 10px 0; }}
        a {{ display: block; background: rgba(255,255,255,0.1); padding: 15px; border-radius: 10px; color: white; text-decoration: none; }}
    </style>
</head>
<body>
    <h1>🚀 {self.config['name']}</h1>
    <ul>{links if links else '<li>لا توجد صفحات</li>'}</ul>
</body>
</html>'''
        with open(assets_dir / 'index.html', 'w', encoding='utf-8') as f:
            f.write(index)
    
    def _create_report(self):
        """إنشاء تقرير البناء"""
        report = {
            'app_name': self.config['name'],
            'package': self.config['package'],
            'version': self.config['version'],
            'created_at': datetime.now().isoformat(),
            'project_path': str(self.project_dir)
        }
        self._write('project_info.json', json.dumps(report, indent=2, ensure_ascii=False))
    
    def _write(self, relative_path: str, content: str):
        """كتابة ملف"""
        path = self.project_dir / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)

def main():
    parser = argparse.ArgumentParser(description='إنشاء مشروع Android مع ملفات الموقع')
    parser.add_argument('--name', default='Rose Sphere', help='اسم التطبيق')
    parser.add_argument('--package', default='com.rosesphere.app', help='اسم الحزمة')
    parser.add_argument('--version', default='1.0.0', help='الإصدار')
    args = parser.parse_args()
    
    config = {
        'name': args.name,
        'package': args.package,
        'version': args.version
    }
    
    print("="*50)
    print("🚀 إنشاء مشروع Android")
    print("="*50)
    print(f"📱 الاسم: {config['name']}")
    print(f"📦 الحزمة: {config['package']}")
    print(f"📌 الإصدار: {config['version']}")
    print("="*50)
    
    creator = AndroidProjectCreator(config)
    project_path = creator.create()
    
    print(f"\n✅ تم إنشاء المشروع في: {project_path}")
    print("\nالخطوة التالية: شغّل apk.yml لبناء APK")

if __name__ == '__main__':
    main()
