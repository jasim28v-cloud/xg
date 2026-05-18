#!/usr/bin/env python3
"""
Rose Sphere APK Builder - مع دعم كامل للموقع
"""
import os, sys, shutil, logging, argparse, subprocess, zipfile
from pathlib import Path
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('APKBuilder')

class APKBuilder:
    def __init__(self, config):
        self.config = config
        self.work_dir = Path('apk_work')
        self.output_dir = Path('output')
        self.output_dir.mkdir(exist_ok=True)
        self.pkg_path = config['package'].replace('.', '/')
        self.app_class = config['name'].replace(' ', '') + 'Activity'

    def build(self):
        logger.info(f"🚀 بناء APK لـ {self.config['name']}")
        
        if self.work_dir.exists():
            shutil.rmtree(self.work_dir)
        self.work_dir.mkdir()
        
        self._create_structure()
        self._write_manifest()
        self._write_java_advanced()  # كود Java متقدم
        self._write_resources()
        self._copy_all_files()  # نسخ كل الملفات
        
        apk_path = self._build_with_sdk()
        if not apk_path:
            apk_path = self._build_manual()
        
        return apk_path

    def _create_structure(self):
        for d in ['src/' + self.pkg_path, 'res/layout', 'res/values', 'res/xml', 'assets']:
            (self.work_dir / d).mkdir(parents=True, exist_ok=True)

    def _write_manifest(self):
        manifest = f'''<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="{self.config['package']}">
    
    <uses-permission android:name="android.permission.INTERNET"/>
    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE"/>
    <uses-permission android:name="android.permission.ACCESS_WIFI_STATE"/>
    
    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="{self.config['name']}"
        android:supportsRtl="true"
        android:theme="@android:style/Theme.Material.Light.NoActionBar"
        android:usesCleartextTraffic="true"
        android:hardwareAccelerated="true"
        android:networkSecurityConfig="@xml/network_security_config">
        
        <activity
            android:name=".{self.app_class}"
            android:exported="true"
            android:configChanges="orientation|screenSize|keyboardHidden">
            <intent-filter>
                <action android:name="android.intent.action.MAIN"/>
                <category android:name="android.intent.category.LAUNCHER"/>
            </intent-filter>
        </activity>
    </application>
</manifest>'''
        (self.work_dir / 'AndroidManifest.xml').write_text(manifest, encoding='utf-8')
        
        # network_security_config.xml للسماح بـ HTTP و HTTPS
        network_config = '''<?xml version="1.0" encoding="utf-8"?>
<network-security-config>
    <base-config cleartextTrafficPermitted="true">
        <trust-anchors>
            <certificates src="system"/>
        </trust-anchors>
    </base-config>
</network-security-config>'''
        (self.work_dir / 'res/xml/network_security_config.xml').write_text(network_config, encoding='utf-8')

    def _write_java_advanced(self):
        """WebView متقدم يدعم JavaScript و localStorage"""
        java = f'''package {self.config['package']};

import android.app.Activity;
import android.os.Bundle;
import android.webkit.WebView;
import android.webkit.WebSettings;
import android.webkit.WebViewClient;
import android.webkit.WebChromeClient;
import android.webkit.WebResourceRequest;
import android.webkit.WebResourceError;
import android.view.KeyEvent;
import android.view.Window;
import android.view.WindowManager;
import android.graphics.Bitmap;
import android.net.ConnectivityManager;
import android.net.NetworkInfo;
import android.content.Context;

public class {self.app_class} extends Activity {{
    private WebView webView;
    
    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        
        requestWindowFeature(Window.FEATURE_NO_TITLE);
        getWindow().setFlags(
            WindowManager.LayoutParams.FLAG_FULLSCREEN,
            WindowManager.LayoutParams.FLAG_FULLSCREEN
        );
        
        webView = new WebView(this);
        WebSettings settings = webView.getSettings();
        
        // تفعيل جميع الميزات
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
        settings.setCacheMode(WebSettings.LOAD_NO_CACHE);
        settings.setAppCacheEnabled(true);
        settings.setDatabaseEnabled(true);
        settings.setMixedContentMode(WebSettings.MIXED_CONTENT_ALWAYS_ALLOW);
        
        // دعم localStorage و sessionStorage
        settings.setJavaScriptCanOpenWindowsAutomatically(true);
        settings.setSupportMultipleWindows(false);
        
        webView.setWebViewClient(new WebViewClient() {{
            @Override
            public void onPageStarted(WebView view, String url, Bitmap favicon) {{
                super.onPageStarted(view, url, favicon);
            }}
            
            @Override
            public void onPageFinished(WebView view, String url) {{
                super.onPageFinished(view, url);
                // إعادة تحميل إذا فشل التحميل
                if (view.getProgress() < 100) {{
                    view.reload();
                }}
            }}
            
            @Override
            public void onReceivedError(WebView view, WebResourceRequest request, WebResourceError error) {{
                // تحميل من الذاكرة المؤقتة عند الخطأ
                view.loadUrl("file:///android_asset/index.html");
            }}
        }});
        
        webView.setWebChromeClient(new WebChromeClient() {{
            @Override
            public void onProgressChanged(WebView view, int progress) {{
                // يمكن إضافة شريط تقدم هنا
            }}
        }});
        
        // تحميل الملف المحلي
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
        (self.work_dir / f'src/{self.pkg_path}/{self.app_class}.java').write_text(java, encoding='utf-8')

    def _write_resources(self):
        (self.work_dir / 'res/values/strings.xml').write_text(
            f'<resources><string name="app_name">{self.config["name"]}</string></resources>', encoding='utf-8')
        (self.work_dir / 'res/layout/activity_main.xml').write_text(
            '<WebView xmlns:android="http://schemas.android.com/apk/res/android" android:id="@+id/webview" android:layout_width="match_parent" android:layout_height="match_parent"/>', encoding='utf-8')

    def _copy_all_files(self):
        """نسخ جميع ملفات الموقع"""
        assets = self.work_dir / 'assets'
        files_to_copy = [
            'index.html', 'auth.html', 'chat.html', 'explore.html',
            'profile.html', 'settings.html', 'notifications.html', 'upload.html',
            'firebase-config.js', 'service-worker.js', 'server.js', 'package.json'
        ]
        
        copied = 0
        for f in files_to_copy:
            src = Path(f)
            if src.exists():
                shutil.copy2(src, assets / f)
                logger.info(f"✅ {f}")
                copied += 1
            else:
                logger.warning(f"⚠️ {f} غير موجود")
        
        if not (assets / 'index.html').exists():
            self._create_default_index(assets)
        
        logger.info(f"📁 تم نسخ {copied} ملف")

    def _create_default_index(self, assets):
        """إنشاء صفحة افتراضية مع روابط لكل الصفحات"""
        html_files = list(assets.glob('*.html'))
        links = '\n'.join(f'<li><a href="{f.name}">📄 {f.stem}</a></li>' for f in html_files)
        
        index = f'''<!DOCTYPE html>
<html dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{self.config['name']}</title>
    <style>
        * {{ margin:0; padding:0; box-sizing:border-box; }}
        body {{ font-family:Arial; background:linear-gradient(135deg, #1a1a2e, #16213e); color:white; min-height:100vh; padding:20px; }}
        h1 {{ text-align:center; margin:30px 0; font-size:2em; }}
        ul {{ list-style:none; max-width:600px; margin:0 auto; }}
        li {{ margin:12px 0; }}
        a {{ display:block; background:rgba(255,255,255,0.1); padding:18px 20px; border-radius:12px; color:white; text-decoration:none; font-size:1.2em; transition:0.3s; border:1px solid rgba(255,255,255,0.1); }}
        a:hover {{ background:rgba(255,255,255,0.2); transform:translateX(-5px); }}
        .status {{ text-align:center; margin-top:30px; opacity:0.7; }}
    </style>
</head>
<body>
    <h1>🚀 {self.config['name']}</h1>
    <ul>{links if links else '<li style="text-align:center">لا توجد صفحات</li>'}</ul>
    <div class="status">✅ تطبيق يعمل بدون إنترنت</div>
</body>
</html>'''
        (assets / 'index.html').write_text(index, encoding='utf-8')

    def _build_with_sdk(self):
        """بناء APK باستخدام Android SDK"""
        try:
            android_home = os.environ.get('ANDROID_HOME', os.path.expanduser('~/android-sdk'))
            bt = f'{android_home}/build-tools/34.0.0'
            pf = f'{android_home}/platforms/android-34'
            
            if not os.path.exists(bt):
                return None
            
            wd = str(self.work_dir)
            
            # 1. aapt package
            subprocess.run([f'{bt}/aapt', 'package', '-f', '-m',
                '-J', f'{wd}/src', '-M', f'{wd}/AndroidManifest.xml',
                '-S', f'{wd}/res', '-I', f'{pf}/android.jar',
                '-F', f'{wd}/base.apk'], check=True, capture_output=True)
            
            # 2. javac
            classes = f'{wd}/classes'
            os.makedirs(classes, exist_ok=True)
            subprocess.run(['javac', '-source', '1.8', '-target', '1.8',
                '-cp', f'{pf}/android.jar', '-d', classes,
                f'{wd}/src/{self.pkg_path}/{self.app_class}.java'], check=True, capture_output=True)
            
            # 3. d8
            subprocess.run([f'{bt}/d8', '--lib', f'{pf}/android.jar',
                '--output', wd, f'{classes}/{self.pkg_path}/{self.app_class}.class'], check=True, capture_output=True)
            
            # 4. إضافة dex
            subprocess.run([f'{bt}/aapt', 'add', f'{wd}/base.apk', f'{wd}/classes.dex'], check=True, capture_output=True)
            
            # 5. إضافة assets
            for root, dirs, files in os.walk(f'{wd}/assets'):
                for file in files:
                    fp = os.path.join(root, file)
                    an = 'assets/' + os.path.relpath(fp, f'{wd}/assets')
                    subprocess.run([f'{bt}/aapt', 'add', f'{wd}/base.apk', fp, an], check=True, capture_output=True)
            
            # 6. توقيع
            ks = f'{wd}/debug.keystore'
            subprocess.run(['keytool', '-genkey', '-v', '-keystore', ks,
                '-alias', 'debug', '-keyalg', 'RSA', '-keysize', '2048',
                '-validity', '10000', '-storepass', 'android', '-keypass', 'android',
                '-dname', 'CN=Dev'], check=True, capture_output=True)
            
            out = self.output_dir / f"{self.config['name'].replace(' ', '_')}.apk"
            subprocess.run([f'{bt}/apksigner', 'sign', '--ks', ks,
                '--ks-pass', 'pass:android', '--out', str(out),
                f'{wd}/base.apk'], check=True, capture_output=True)
            
            return str(out)
        except Exception as e:
            logger.warning(f"SDK build failed: {e}")
            return None

    def _build_manual(self):
        """بناء APK يدوي"""
        apk = self.output_dir / f"{self.config['name'].replace(' ', '_')}.apk"
        with zipfile.ZipFile(apk, 'w', zipfile.ZIP_DEFLATED) as z:
            z.write(self.work_dir / 'AndroidManifest.xml', 'AndroidManifest.xml')
            for f in (self.work_dir / 'res').rglob('*'):
                if f.is_file():
                    z.write(f, 'res/' + str(f.relative_to(self.work_dir / 'res')))
            for f in (self.work_dir / 'assets').rglob('*'):
                if f.is_file():
                    z.write(f, 'assets/' + str(f.relative_to(self.work_dir / 'assets')))
        return str(apk)

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--name', default='Rose Sphere')
    p.add_argument('--package', default='com.rosesphere.app')
    p.add_argument('--version', default='1.0.0')
    args = p.parse_args()
    
    builder = APKBuilder({'name': args.name, 'package': args.package, 'version': args.version})
    apk = builder.build()
    
    if apk and os.path.exists(apk):
        print(f'✅ {apk} ({os.path.getsize(apk)/1024:.1f} KB)')
    else:
        print('❌ فشل')

if __name__ == '__main__':
    main()
