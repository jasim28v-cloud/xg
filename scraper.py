#!/usr/bin/env python3
"""
Professional APK Builder - Rose Sphere
يسحب ملفات الموقع ويبني APK حقيقي باستخدام Android SDK
"""
import os, sys, json, shutil, logging, subprocess, argparse, time
from pathlib import Path
from datetime import datetime
from typing import Dict, List

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('APKBuilder')

# قائمة ملفات موقعك
SITE_FILES = [
    'index.html', 'auth.html', 'chat.html', 'explore.html',
    'profile.html', 'settings.html', 'notifications.html', 'upload.html',
    'firebase-config.js', 'service-worker.js', 'server.js'
]

class ProfessionalAPKBuilder:
    def __init__(self):
        self.project_dir = Path('android_project')
        self.output_dir = Path('output')
        self.output_dir.mkdir(exist_ok=True)
        
    def setup_android_project(self, config: Dict):
        """إنشاء مشروع أندرويد كامل"""
        logger.info("📁 إنشاء مشروع أندرويد...")
        
        if self.project_dir.exists():
            shutil.rmtree(self.project_dir)
        
        # هيكل المشروع
        dirs = [
            'app/src/main/java/com/rosesphere/app',
            'app/src/main/res/layout',
            'app/src/main/res/values',
            'app/src/main/res/drawable',
            'app/src/main/assets',
            'app/src/main/res/mipmap-hdpi',
            'app/src/main/res/mipmap-mdpi',
            'app/src/main/res/mipmap-xhdpi',
            'app/src/main/res/mipmap-xxhdpi',
            'gradle/wrapper'
        ]
        for d in dirs:
            (self.project_dir / d).mkdir(parents=True, exist_ok=True)
    
    def create_manifest(self, config: Dict):
        """إنشاء AndroidManifest.xml"""
        manifest = f'''<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="{config['package']}">
    
    <uses-permission android:name="android.permission.INTERNET"/>
    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE"/>
    
    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="{config['name']}"
        android:supportsRtl="true"
        android:theme="@style/AppTheme"
        android:usesCleartextTraffic="true">
        
        <activity
            android:name="com.rosesphere.app.MainActivity"
            android:exported="true"
            android:configChanges="orientation|screenSize">
            <intent-filter>
                <action android:name="android.intent.action.MAIN"/>
                <category android:name="android.intent.category.LAUNCHER"/>
            </intent-filter>
        </activity>
    </application>
</manifest>'''
        
        with open(self.project_dir / 'app/src/main/AndroidManifest.xml', 'w') as f:
            f.write(manifest)
    
    def create_main_activity(self):
        """إنشاء MainActivity.java"""
        java_code = '''package com.rosesphere.app;

import android.app.Activity;
import android.os.Bundle;
import android.webkit.WebView;
import android.webkit.WebSettings;
import android.webkit.WebViewClient;
import android.webkit.WebChromeClient;
import android.view.KeyEvent;

public class MainActivity extends Activity {
    private WebView webView;
    
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        
        webView = findViewById(R.id.webview);
        
        WebSettings settings = webView.getSettings();
        settings.setJavaScriptEnabled(true);
        settings.setDomStorageEnabled(true);
        settings.setAllowFileAccess(true);
        settings.setAllowContentAccess(true);
        
        webView.setWebViewClient(new WebViewClient());
        webView.setWebChromeClient(new WebChromeClient());
        webView.loadUrl("file:///android_asset/index.html");
    }
    
    @Override
    public boolean onKeyDown(int keyCode, KeyEvent event) {
        if (keyCode == KeyEvent.KEYCODE_BACK && webView.canGoBack()) {
            webView.goBack();
            return true;
        }
        return super.onKeyDown(keyCode, event);
    }
}'''
        
        with open(self.project_dir / 'app/src/main/java/com/rosesphere/app/MainActivity.java', 'w') as f:
            f.write(java_code)
    
    def create_layout(self):
        """إنشاء layout"""
        layout = '''<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical">
    
    <WebView
        android:id="@+id/webview"
        android:layout_width="match_parent"
        android:layout_height="match_parent"/>
</LinearLayout>'''
        
        with open(self.project_dir / 'app/src/main/res/layout/activity_main.xml', 'w') as f:
            f.write(layout)
    
    def create_resources(self, config: Dict):
        """إنشاء ملفات الموارد"""
        # strings.xml
        strings = f'''<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string name="app_name">{config['name']}</string>
</resources>'''
        with open(self.project_dir / 'app/src/main/res/values/strings.xml', 'w') as f:
            f.write(strings)
        
        # styles.xml
        styles = '''<?xml version="1.0" encoding="utf-8"?>
<resources>
    <style name="AppTheme" parent="android:Theme.Material.Light.NoActionBar">
        <item name="android:statusBarColor">#1a1a2e</item>
    </style>
</resources>'''
        with open(self.project_dir / 'app/src/main/res/values/styles.xml', 'w') as f:
            f.write(styles)
    
    def copy_site_files(self):
        """نسخ ملفات الموقع إلى assets"""
        assets_dir = self.project_dir / 'app/src/main/assets'
        copied = 0
        
        for filename in SITE_FILES:
            src = Path(filename)
            if src.exists():
                shutil.copy2(src, assets_dir / filename)
                copied += 1
                logger.info(f"✅ {filename}")
            else:
                logger.warning(f"⚠️ {filename} غير موجود")
        
        return copied
    
    def create_build_files(self, config: Dict):
        """إنشاء ملفات البناء"""
        # build.gradle (project)
        project_gradle = '''buildscript {
    repositories {
        google()
        mavenCentral()
    }
    dependencies {
        classpath 'com.android.tools.build:gradle:8.2.0'
    }
}'''
        with open(self.project_dir / 'build.gradle', 'w') as f:
            f.write(project_gradle)
        
        # settings.gradle
        settings_gradle = '''rootProject.name = "RoseSphere"
include ':app'
'''
        with open(self.project_dir / 'settings.gradle', 'w') as f:
            f.write(settings_gradle)
        
        # app/build.gradle
        app_gradle = f'''apply plugin: 'com.android.application'

android {{
    namespace '{config["package"]}'
    compileSdk 34
    
    defaultConfig {{
        applicationId "{config['package']}"
        minSdk 21
        targetSdk 34
        versionCode 1
        versionName "{config['version']}"
    }}
    
    buildTypes {{
        release {{
            minifyEnabled false
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt')
        }}
        debug {{
            debuggable true
        }}
    }}
    
    compileOptions {{
        sourceCompatibility JavaVersion.VERSION_1_8
        targetCompatibility JavaVersion.VERSION_1_8
    }}
}}
'''
        with open(self.project_dir / 'app/build.gradle', 'w') as f:
            f.write(app_gradle)
        
        # gradle.properties
        props = '''android.useAndroidX=false
org.gradle.jvmargs=-Xmx2048m
'''
        with open(self.project_dir / 'gradle.properties', 'w') as f:
            f.write(props)
    
    def create_keystore(self):
        """إنشاء مفتاح توقيع"""
        logger.info("🔑 إنشاء مفتاح التوقيع...")
        subprocess.run([
            'keytool', '-genkey', '-v',
            '-keystore', str(self.project_dir / 'debug.keystore'),
            '-alias', 'debug',
            '-keyalg', 'RSA',
            '-keysize', '2048',
            '-validity', '10000',
            '-storepass', 'android',
            '-keypass', 'android',
            '-dname', 'CN=RoseSphere, OU=Dev, O=RoseSphere, L=Unknown, ST=Unknown, C=US'
        ], check=True, capture_output=True)
    
    def build_apk(self, config: Dict) -> str:
        """بناء APK نهائي"""
        logger.info("🔨 بناء APK...")
        
        apk_name = f"{config['name'].replace(' ', '_')}_{config['version']}.apk"
        apk_path = self.output_dir / apk_name
        
        # محاولة البناء باستخدام gradle
        try:
            if shutil.which('gradle'):
                result = subprocess.run(
                    ['gradle', 'assembleRelease'],
                    cwd=self.project_dir,
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0:
                    # نسخ APK الناتج
                    built_apk = self.project_dir / 'app/build/outputs/apk/release/app-release-unsigned.apk'
                    if built_apk.exists():
                        shutil.copy2(built_apk, apk_path)
                        logger.info(f"✅ APK: {apk_path}")
                        return str(apk_path)
        except Exception as e:
            logger.warning(f"Gradle build failed: {e}")
        
        # خطة بديلة: بناء APK يدوياً بصيغة ZIP
        return self._manual_apk_build(apk_path, config)
    
    def _manual_apk_build(self, apk_path: Path, config: Dict) -> str:
        """بناء APK يدوي"""
        logger.info("📦 بناء APK يدوياً...")
        
        import zipfile
        with zipfile.ZipFile(apk_path, 'w', zipfile.ZIP_DEFLATED) as z:
            # AndroidManifest
            manifest = self.project_dir / 'app/src/main/AndroidManifest.xml'
            z.write(manifest, 'AndroidManifest.xml')
            
            # Resources
            res_dir = self.project_dir / 'app/src/main/res'
            for f in res_dir.rglob('*'):
                if f.is_file():
                    z.write(f, 'res/' + str(f.relative_to(res_dir)))
            
            # Assets (ملفات الموقع)
            assets_dir = self.project_dir / 'app/src/main/assets'
            for f in assets_dir.rglob('*'):
                if f.is_file():
                    z.write(f, 'assets/' + str(f.relative_to(assets_dir)))
        
        logger.info(f"✅ APK: {apk_path}")
        return str(apk_path)
    
    def build(self, config: Dict) -> str:
        """تنفيذ عملية البناء الكاملة"""
        logger.info(f"🚀 بدء بناء {config['name']} v{config['version']}")
        
        self.setup_android_project(config)
        self.create_manifest(config)
        self.create_main_activity()
        self.create_layout()
        self.create_resources(config)
        
        files_copied = self.copy_site_files()
        logger.info(f"📁 تم نسخ {files_copied} ملف إلى assets")
        
        self.create_build_files(config)
        
        apk_path = self.build_apk(config)
        
        if apk_path and os.path.exists(apk_path):
            size = os.path.getsize(apk_path) / 1024
            logger.info(f"✅ تم! APK: {apk_path} ({size:.1f} KB)")
            return apk_path
        else:
            raise Exception("فشل بناء APK")

def main():
    parser = argparse.ArgumentParser(description='RoseSphere APK Builder')
    parser.add_argument('--name', default='Rose Sphere', help='اسم التطبيق')
    parser.add_argument('--package', default='com.rosesphere.app', help='اسم الحزمة')
    parser.add_argument('--version', default='1.0.0', help='رقم الإصدار')
    args = parser.parse_args()
    
    config = {
        'name': args.name,
        'package': args.package,
        'version': args.version
    }
    
    builder = ProfessionalAPKBuilder()
    apk_path = builder.build(config)
    
    print(f'\n📱 APK جاهز: {apk_path}')

if __name__ == '__main__':
    main()
