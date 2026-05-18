#!/usr/bin/env python3
import os
import re
import json
import logging
import argparse
from pathlib import Path
from datetime import datetime
from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('WebsiteDownloader')

class WebsiteDownloader:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')
        self.domain = urlparse(base_url).netloc
        self.downloaded_files = set()
        self.failed_files = []
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36'})
        
    def download_website(self, output_dir: Path):
        logger.info(f"🌐 بدء تحميل الموقع: {self.base_url}")
        output_dir.mkdir(parents=True, exist_ok=True)
        assets_dir = output_dir / "assets"
        assets_dir.mkdir(exist_ok=True)
        
        html_content = self._download_page(self.base_url)
        if not html_content:
            raise Exception("فشل تحميل الصفحة الرئيسية")
        
        soup = BeautifulSoup(html_content, 'html.parser')
        self._download_resources(soup, assets_dir)
        modified_html = self._make_links_local(soup, self.base_url)
        
        with open(output_dir / "index.html", 'w', encoding='utf-8') as f:
            f.write(modified_html)
        logger.info(f"✅ تم تحميل الموقع بنجاح داخل {output_dir}")

    def _download_page(self, url: str):
        try:
            res = self.session.get(url, timeout=30)
            res.raise_for_status()
            res.encoding = res.apparent_encoding or 'utf-8'
            return res.text
        except Exception as e:
            logger.error(f"خطأ في تحميل {url}: {e}")
            return None

    def _download_file(self, url: str, save_path: Path):
        if url in self.downloaded_files: return True
        try:
            res = self.session.get(url, timeout=30, stream=True)
            res.raise_for_status()
            save_path.parent.mkdir(parents=True, exist_ok=True)
            with open(save_path, 'wb') as f:
                for chunk in res.iter_content(chunk_size=8192): f.write(chunk)
            self.downloaded_files.add(url)
            return True
        except:
            self.failed_files.append(url)
            return False

    def _make_full_url(self, url: str):
        if url.startswith('data:') or url.startswith('javascript:') or url.startswith('#'): return url
        return urljoin(self.base_url, url)

    def _get_local_filename(self, url: str, ext: str = ''):
        path = urlparse(url).path
        return os.path.basename(path) if (path and os.path.basename(path)) else f"file_{len(self.downloaded_files)}{ext}"

    def _download_resources(self, soup, assets_dir):
        # CSS
        for link in soup.find_all('link', rel='stylesheet'):
            href = link.get('href')
            if href:
                full = self._make_full_url(href)
                name = self._get_local_filename(full, '.css')
                if self._download_file(full, assets_dir / "css" / name):
                    link['href'] = f"assets/css/{name}"
        # JS
        for script in soup.find_all('script', src=True):
            src = script.get('src')
            if src:
                full = self._make_full_url(src)
                name = self._get_local_filename(full, '.js')
                if self._download_file(full, assets_dir / "js" / name):
                    script['src'] = f"assets/js/{name}"
        # Images
        for img in soup.find_all('img'):
            src = img.get('src') or img.get('data-src')
            if src and not src.startswith('data:'):
                full = self._make_full_url(src)
                name = self._get_local_filename(full, '.png')
                if self._download_file(full, assets_dir / "images" / name):
                    img['src'] = f"assets/images/{name}"

    def _make_links_local(self, soup, base_url: str):
        html = str(soup)
        domain = urlparse(base_url).netloc
        html = html.replace(f'https://{domain}', '').replace(f'http://{domain}', '').replace(f'//{domain}', '')
        return html

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('url')
    parser.add_argument('--name', required=True)
    parser.add_argument('--package', required=True)
    parser.add_argument('--version', default='1.0.0')
    args = parser.parse_args()

    # تحميل الموقع مباشرة إلى مجلد الـ www الخاص بـ Cordova
    www_dir = Path("www")
    downloader = WebsiteDownloader(args.url)
    downloader.download_website(www_dir)

if __name__ == "__main__":
    main()
