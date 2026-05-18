#!/usr/bin/env python3
"""
Website Scraper - يسحب موقع كامل بجميع موارده للعمل offline
"""

import os
import sys
import re
import json
import shutil
from pathlib import Path
from urllib.parse import urljoin, urlparse
from datetime import datetime
import requests
from bs4 import BeautifulSoup

class WebsiteScraper:
    def __init__(self, url, output_dir="www"):
        self.url = url.rstrip('/')
        self.domain = urlparse(url).netloc
        self.output_dir = Path(output_dir)
        self.assets_dir = self.output_dir / "assets"
        self.downloaded = set()
        self.failed = []
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Linux; Android 12; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Mobile Safari/537.36'
        })
    
    def scrape(self):
        print(f"🌐 جاري سحب: {self.url}")
        
        # إنشاء المجلدات
        self.output_dir.mkdir(exist_ok=True)
        (self.assets_dir / "css").mkdir(parents=True, exist_ok=True)
        (self.assets_dir / "js").mkdir(parents=True, exist_ok=True)
        (self.assets_dir / "images").mkdir(parents=True, exist_ok=True)
        (self.assets_dir / "fonts").mkdir(parents=True, exist_ok=True)
        
        # تحميل الصفحة الرئيسية
        html = self._download_text(self.url)
        if not html:
            print("❌ فشل تحميل الصفحة")
            return False
        
        soup = BeautifulSoup(html, 'html.parser')
        
        # سحب كل الموارد
        self._download_css(soup)
        self._download_js(soup)
        self._download_images(soup)
        self._download_fonts(soup)
        
        # تحويل الروابط لمحلية
        self._make_links_local(soup)
        
        # حفظ الملف النهائي
        with open(self.output_dir / "index.html", 'w', encoding='utf-8') as f:
            f.write(str(soup))
        
        print(f"✅ تم بنجاح: {len(self.downloaded)} ملف")
        if self.failed:
            print(f"⚠️ فشل: {len(self.failed)} ملف")
        
        return True
    
    def _download_text(self, url):
        try:
            r = self.session.get(url, timeout=30)
            r.raise_for_status()
            r.encoding = r.apparent_encoding or 'utf-8'
            return r.text
        except Exception as e:
            print(f"❌ خطأ: {url} - {e}")
            return None
    
    def _download_file(self, url, save_path):
        if url in self.downloaded:
            return True
        
        try:
            r = self.session.get(url, timeout=30)
            r.raise_for_status()
            save_path.parent.mkdir(parents=True, exist_ok=True)
            with open(save_path, 'wb') as f:
                f.write(r.content)
            self.downloaded.add(url)
            print(f"  ✅ {save_path.name}")
            return True
        except Exception as e:
            print(f"  ⚠️ فشل: {save_path.name} - {e}")
            self.failed.append(url)
            return False
    
    def _make_full_url(self, url):
        if not url or url.startswith(('data:', 'javascript:', '#', 'mailto:', 'tel:')):
            return None
        return urljoin(self.url, url)
    
    def _get_filename(self, url, default_ext='.file'):
        parsed = urlparse(url)
        name = os.path.basename(parsed.path)
        if not name or '.' not in name:
            import hashlib
            name = hashlib.md5(url.encode()).hexdigest()[:10] + default_ext
        return name
    
    def _download_css(self, soup):
        for link in soup.find_all('link', rel='stylesheet'):
            href = link.get('href')
            full_url = self._make_full_url(href)
            if full_url:
                fname = self._get_filename(full_url, '.css')
                path = self.assets_dir / "css" / fname
                if self._download_file(full_url, path):
                    link['href'] = f"assets/css/{fname}"
        
        # CSS inline
        for style in soup.find_all('style'):
            if style.string:
                urls = re.findall(r'url\([\'"]?([^\'"()]+)[\'"]?\)', style.string)
                for u in urls:
                    full_u = self._make_full_url(u)
                    if full_u:
                        fname = self._get_filename(full_u, '.png')
                        path = self.assets_dir / "images" / fname
                        if self._download_file(full_u, path):
                            style.string = style.string.replace(u, f"assets/images/{fname}")
    
    def _download_js(self, soup):
        for script in soup.find_all('script', src=True):
            src = script.get('src')
            full_url = self._make_full_url(src)
            if full_url:
                fname = self._get_filename(full_url, '.js')
                path = self.assets_dir / "js" / fname
                if self._download_file(full_url, path):
                    script['src'] = f"assets/js/{fname}"
    
    def _download_images(self, soup):
        for img in soup.find_all('img'):
            src = img.get('src') or img.get('data-src')
            full_url = self._make_full_url(src)
            if full_url:
                fname = self._get_filename(full_url, '.png')
                path = self.assets_dir / "images" / fname
                if self._download_file(full_url, path):
                    img['src'] = f"assets/images/{fname}"
                    if 'srcset' in img.attrs:
                        del img['srcset']
        
        # صور background
        for tag in soup.find_all(style=True):
            style = tag['style']
            urls = re.findall(r'url\([\'"]?([^\'"()]+)[\'"]?\)', style)
            for u in urls:
                full_u = self._make_full_url(u)
                if full_u:
                    fname = self._get_filename(full_u, '.png')
                    path = self.assets_dir / "images" / fname
                    if self._download_file(full_u, path):
                        tag['style'] = style.replace(u, f"assets/images/{fname}")
    
    def _download_fonts(self, soup):
        for link in soup.find_all('link'):
            if 'font' in link.get('as', '') or 'icon' in link.get('rel', [''])[0]:
                href = link.get('href')
                full_url = self._make_full_url(href)
                if full_url:
                    fname = self._get_filename(full_url, '.woff2')
                    path = self.assets_dir / "fonts" / fname
                    if self._download_file(full_url, path):
                        link['href'] = f"assets/fonts/{fname}"
    
    def _make_links_local(self, soup):
        # إزالة روابط النطاق
        html = str(soup)
        html = html.replace(f'https://{self.domain}', '')
        html = html.replace(f'http://{self.domain}', '')
        html = html.replace(f'//{self.domain}', '')
        
        # إعادة تحليل
        return BeautifulSoup(html, 'html.parser')


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='سحب موقع ويب كامل')
    parser.add_argument('url', help='رابط الموقع')
    parser.add_argument('-o', '--output', default='www', help='مجلد الإخراج')
    
    args = parser.parse_args()
    
    scraper = WebsiteScraper(args.url, args.output)
    scraper.scrape()
