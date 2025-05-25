from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from app.models import CrawledPage
from app.database import db
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from .utils import extract_title, extract_text, extract_links
import time

# Import Config for access to configuration values
from config import Config

def initialize_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def dfs_crawl(seed_url, max_pages=Config.MAX_CRAWL_PAGES, max_depth=Config.MAX_CRAWL_DEPTH):
    # Set default values from Config
        
    driver = initialize_driver()
    driver.get(seed_url)

    base_domain = urlparse(seed_url).netloc
    visited = set()
    stack = [(seed_url, 0)]  # Menyimpan URL dan kedalaman (depth)
    
    print(f"Mulai crawling DFS dari {seed_url}...")
    print(f"Base domain: {base_domain}")

    while stack and len(visited) < max_pages:
        url, depth = stack.pop()
        
        # Batasi kedalaman crawling
        if depth > max_depth:
            continue
        
        if url in visited:
            continue
            
        print(f"Depth {depth}: Mengunjungi {url}")
        try:
            driver.get(url)
            time.sleep(2)
            
            html_content = driver.page_source
            soup = BeautifulSoup(html_content, "html.parser")
            title = extract_title(soup, url)
            text = extract_text(soup)
            links = extract_links(soup, url, base_domain)
            
            page = CrawledPage.query.filter_by(url=url).first()
            if not page:
                page = CrawledPage(url=url)
            page.title = title
            page.text = text
            page.set_links(links)

            db.session.add(page)
            db.session.commit()
            
            visited.add(url)
            print(f"Halaman tersimpan: {title} ({url})")
            print(f"Ditemukan {len(links)} link di halaman ini")

            # Tambahkan link yang belum dikunjungi ke stack dengan penambahan kedalaman
            for link_url, link_text in reversed(links):
                if link_url not in visited and link_url not in stack:
                    stack.append((link_url, depth + 1))  # Increment depth

        except Exception as e:
            print(f"Error saat mengunjungi {url}: {str(e)}")
            visited.add(url)  # Tandai sebagai dikunjungi agar tidak dicoba lagi

    print(f"DFS Crawling selesai! Total {len(visited)} halaman dikunjungi.")
    driver.quit()
    return visited
