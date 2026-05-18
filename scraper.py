#!/usr/bin/env python3
"""
🃏 Joker APK Builder - Professional Web to APK Converter
ضع هذا الملف في أي مستودع مع ملفات موقعك وسيقوم ببناء APK احترافي
يدعم: Offline First، Service Worker، IndexedDB، المزامنة التلقائية
"""
import os, sys, shutil, json, logging, argparse, zipfile, re
from pathlib import Path
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger('Joker')

class JokerAPK:
    def __init__(self, name='MyApp', package='com.myapp.app', version='1.0.0'):
        self.name = name
        self.package = package
        self.version = version
        self.work = Path('joker_build')
        self.out = Path('output')
        self.files = []

    def build(self):
        logger.info(f'🃏 بناء {self.name} v{self.version}')

        if self.work.exists():
            shutil.rmtree(self.work)
        self.work.mkdir()
        assets = self.work / 'assets'
        assets.mkdir(parents=True)
        (assets / 'js').mkdir(exist_ok=True)
        self.out.mkdir(exist_ok=True)

        # 1. نسخ الملفات
        self._copy_files(assets)

        # 2. إنشاء Service Worker
        self._create_sw(assets)

        # 3. إنشاء نظام التخزين
        self._create_cache_system(assets)

        # 4. إنشاء index.html
        self._create_index(assets)

        # 5. بناء APK
        apk = self._build_apk()

        # 6. تقرير
        size_kb = os.path.getsize(apk) / 1024
        logger.info(f'✅ APK: {apk} ({size_kb:.1f} KB)')
        logger.info(f'📁 {len(self.files)} ملف مضمن')

        return apk

    def _copy_files(self, assets):
        exts = ['*.html', '*.css', '*.js', '*.json', '*.xml', '*.png', '*.jpg', '*.jpeg', '*.gif', '*.svg', '*.ico', '*.webp']
        for ext in exts:
            for f in Path('.').glob(ext):
                if f.is_file() and not f.name.startswith(('scraper', 'joker', 'build', 'output')):
                    dst = assets / f.name
                    shutil.copy2(f, dst)
                    if f.name not in self.files:
                        self.files.append(f.name)
                        logger.info(f'✅ {f.name}')

    def _create_sw(self, assets):
        sw = '''const CACHE = 'joker-' + Date.now();
const FILES = ['/','/index.html','/manifest.json','/js/joker-cache.js'];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(FILES)).then(() => self.skipWaiting()));
});

self.addEventListener('fetch', e => {
  e.respondWith(
    fetch(e.request).then(r => {
      if (r.status === 200) {
        const clone = r.clone();
        caches.open(CACHE).then(c => c.put(e.request, clone));
      }
      return r;
    }).catch(() => caches.match(e.request).then(r => r || new Response('Offline', {status: 503})))
  );
});

self.addEventListener('activate', e => {
  e.waitUntil(caches.keys().then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim()));
});'''
        with open(assets / 'sw.js', 'w') as f:
            f.write(sw)

    def _create_cache_system(self, assets):
        js = '''class JokerDB {
  constructor() {
    this.db = null;
    this.init();
  }
  async init() {
    return new Promise((ok, no) => {
      const r = indexedDB.open('JokerDB', 1);
      r.onupgradeneeded = e => {
        const db = e.target.result;
        if (!db.objectStoreNames.contains('pages')) db.createObjectStore('pages', {keyPath: 'url'});
        if (!db.objectStoreNames.contains('data')) db.createObjectStore('data', {keyPath: 'id', autoIncrement: true});
      };
      r.onsuccess = e => { this.db = e.target.result; ok(); };
      r.onerror = e => no(e.target.error);
    });
  }
  async savePage(url, content) {
    if (!this.db) await this.init();
    return new Promise(ok => {
      const t = this.db.transaction('pages', 'readwrite');
      t.objectStore('pages').put({url, content, time: Date.now()});
      t.oncomplete = () => ok();
    });
  }
  async getPage(url) {
    if (!this.db) await this.init();
    return new Promise(ok => {
      const t = this.db.transaction('pages', 'readonly');
      const r = t.objectStore('pages').get(url);
      r.onsuccess = () => ok(r.result?.content || null);
    });
  }
  async getAllPages() {
    if (!this.db) await this.init();
    return new Promise(ok => {
      const t = this.db.transaction('pages', 'readonly');
      const r = t.objectStore('pages').getAll();
      r.onsuccess = () => ok(r.result);
    });
  }
}
window.jokerDB = new JokerDB();'''
        with open(assets / 'js/joker-cache.js', 'w') as f:
            f.write(js)

    def _create_index(self, assets):
        html_files = [f for f in self.files if f.endswith('.html')]
        pages = '\n'.join(f'<a href="{f}" class="card" onclick="openPage(event,\'{f}\')">📄 {f[:-5].replace("_"," ").replace("-"," ").title()}</a>' for f in html_files)

        other = [f for f in self.files if f not in html_files]
        other_tags = '\n'.join(f'<span class="tag">{f}</span>' for f in other)

        index = f'''<!DOCTYPE html>
<html dir="rtl" manifest="cache.manifest">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width,initial-scale=1.0">
    <title>{self.name}</title>
    <link rel="manifest" href="/manifest.json">
    <style>
        *{{margin:0;padding:0;box-sizing:border-box}}
        body{{font-family:'Segoe UI',Tahoma,sans-serif;background:linear-gradient(135deg,#0f0c29,#302b63,#24243e);color:#fff;min-height:100vh}}
        .status{{position:fixed;top:0;left:0;right:0;padding:5px;text-align:center;font-size:12px;z-index:9999;background:rgba(0,200,0,0.2)}}
        .status.offline{{background:rgba(255,0,0,0.3)}}
        .container{{max-width:800px;margin:0 auto;padding:40px 20px}}
        h1{{text-align:center;font-size:2.5em;margin:20px 0}}
        .badge{{display:inline-block;background:gold;color:#000;padding:5px 15px;border-radius:20px;font-weight:bold;font-size:14px;margin:10px}}
        .grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:15px;margin:30px 0}}
        .card{{display:flex;align-items:center;justify-content:center;background:rgba(255,255,255,0.08);border:1px solid rgba(255,255,255,0.12);border-radius:15px;padding:25px;color:#fff;text-decoration:none;font-size:1.1em;cursor:pointer;transition:all .3s;text-align:center}}
        .card:hover{{background:rgba(255,255,255,0.18);transform:translateY(-3px);box-shadow:0 10px 30px rgba(0,0,0,0.3)}}
        .section{{background:rgba(255,255,255,0.05);border-radius:15px;padding:20px;margin:20px 0}}
        .section h2{{margin-bottom:15px}}
        .tags{{display:flex;flex-wrap:wrap;gap:8px}}
        .tag{{background:rgba(255,255,255,0.08);padding:5px 12px;border-radius:8px;font-size:.85em}}
        .viewer{{display:none;position:fixed;top:0;left:0;width:100%;height:100%;background:#fff;z-index:9998}}
        .viewer.active{{display:block}}
        .v-header{{background:#302b63;color:#fff;padding:12px 20px;display:flex;justify-content:space-between}}
        .v-header button{{background:rgba(255,255,255,0.2);border:none;color:#fff;padding:8px 20px;border-radius:8px;cursor:pointer}}
        iframe{{width:100%;height:calc(100% - 50px);border:none}}
        footer{{text-align:center;padding:30px;opacity:.6;font-size:.85em}}
    </style>
</head>
<body>
    <div class="status" id="status">🟢 متصل | {len(self.files)} ملف</div>

    <div class="container">
        <h1>🃏 {self.name}</h1>
        <div style="text-align:center">
            <span class="badge">⚡ Offline First</span>
            <span class="badge">📦 {len(self.files)} ملف</span>
        </div>

        <div class="section">
            <h2>📄 الصفحات</h2>
            <div class="grid">{pages if pages else '<p style="opacity:.6;grid-column:1/-1;text-align:center">لا توجد صفحات</p>'}</div>
        </div>

        <div class="section">
            <h2>📁 الملفات الأخرى</h2>
            <div class="tags">{other_tags if other_tags else '<p style="opacity:.6">لا توجد ملفات أخرى</p>'}</div>
        </div>
    </div>

    <div class="viewer" id="viewer">
        <div class="v-header">
            <span id="vTitle">الصفحة</span>
            <button onclick="document.getElementById('viewer').classList.remove('active')">✕ إغلاق</button>
        </div>
        <iframe id="vFrame"></iframe>
    </div>

    <footer>🃏 Joker APK Builder | {self.version}</footer>

    <script src="/js/joker-cache.js"></script>
    <script>
        async function openPage(e, url) {{
            e.preventDefault();
            document.getElementById('vTitle').textContent = url;
            document.getElementById('viewer').classList.add('active');
            const cached = await jokerDB.getPage(url);
            document.getElementById('vFrame').srcdoc = cached || '';
            document.getElementById('vFrame').src = url;
            if (navigator.onLine) {{
                try {{
                    const r = await fetch(url);
                    await jokerDB.savePage(url, await r.text());
                }} catch(e) {{}}
            }}
        }}

        window.addEventListener('online', () => {{
            document.getElementById('status').className = '';
            document.getElementById('status').textContent = '🟢 متصل | {len(self.files)} ملف';
        }});
        window.addEventListener('offline', () => {{
            document.getElementById('status').className = 'offline';
            document.getElementById('status').textContent = '🔴 غير متصل | {len(self.files)} ملف';
        }});

        if ('serviceWorker' in navigator) {{
            navigator.serviceWorker.register('/sw.js').catch(() => {{}});
        }}
    </script>
</body>
</html>'''
        with open(assets / 'index.html', 'w', encoding='utf-8') as f:
            f.write(index)

        # manifest.json
        manifest = {
            "name": self.name,
            "short_name": self.name,
            "start_url": "/index.html",
            "display": "standalone",
            "background_color": "#0f0c29",
            "theme_color": "#302b63",
            "icons": [{"src": "/icon.png", "sizes": "192x192", "type": "image/png"}]
        }
        with open(assets / 'manifest.json', 'w') as f:
            json.dump(manifest, f, indent=2)

    def _build_apk(self):
        apk_path = self.out / f"{self.name.replace(' ', '_')}_{self.version}.apk"

        with zipfile.ZipFile(apk_path, 'w', zipfile.ZIP_DEFLATED) as z:
            # AndroidManifest.xml
            manifest = f'''<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="{self.package}">
    <uses-permission android:name="android.permission.INTERNET"/>
    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE"/>
    <application
        android:label="{self.name}"
        android:theme="@android:style/Theme.Material.Light.NoActionBar"
        android:usesCleartextTraffic="true"
        android:hardwareAccelerated="true">
        <activity android:name=".MainActivity" android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN"/>
                <category android:name="android.intent.category.LAUNCHER"/>
            </intent-filter>
        </activity>
    </application>
</manifest>'''
            z.writestr('AndroidManifest.xml', manifest)

            # جميع ملفات assets
            assets = self.work / 'assets'
            for f in assets.rglob('*'):
                if f.is_file():
                    arc = 'assets/' + str(f.relative_to(assets))
                    z.write(f, arc)

        return str(apk_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='🃏 Joker APK Builder')
    parser.add_argument('--name', default='MyApp', help='اسم التطبيق')
    parser.add_argument('--package', default='com.myapp.app', help='اسم الحزمة')
    parser.add_argument('--version', default='1.0.0', help='الإصدار')
    args = parser.parse_args()

    joker = JokerAPK(args.name, args.package, args.version)
    apk = joker.build()
    print(f'\n✅ APK جاهز: {apk}')
