from collections import deque
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from app.models import CrawledPage, Base
from app.database import get_domain_from_url, get_session_for_domain
from bs4 import BeautifulSoup
from .utils import extract_title, extract_text, extract_links
from config import Config
import time

log_stream = []

def initialize_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def log_message(message):
    print(message)
    log_stream.append(message)

def crawl(seed_url, max_pages=Config.MAX_CRAWL_PAGES):
    driver = initialize_driver()
    driver.get(seed_url)

    domain = get_domain_from_url(seed_url)
    session, engine = get_session_for_domain(domain, "bfs")
    Base.metadata.create_all(engine)
    visited = set()
    queue = deque([seed_url])
    
    log_message(f"Mulai crawling BFS dari {seed_url}...")
    log_message(f"Base domain: {domain}")

    while queue and len(visited) < max_pages:
        url = queue.popleft()
        if url in visited:
            continue
        visited.add(url)

        existing = session.query(CrawledPage).filter_by(url=url).first()
        if existing:
            continue
        
        log_message(f"Mengunjungi: {url}")
        try:
            driver.get(url)
            time.sleep(2)
            
            html_content = driver.page_source
            soup = BeautifulSoup(html_content, "html.parser")
            title = extract_title(soup, url)
            text = extract_text(soup)
            links = extract_links(soup, url, domain)
            
            page = CrawledPage(url=url)
            page.title = title
            page.text = text
            page.set_links(links)

            session.add(page)
            session.commit()
            
            log_message(f"Halaman tersimpan: {title} ({url})")
            log_message(f"Ditemukan {len(links)} link di halaman ini")

            # Tambahkan semua link yang belum dikunjungi dan belum ada di queue
            for link_url, link_text in links:
                if link_url not in visited and link_url not in queue:
                    queue.append(link_url)
                    
        except Exception as e:
            log_message(f"Error saat mengunjungi {url}: {str(e)}")

    log_message(f"BFS Crawling selesai! Total {len(visited)} halaman dikunjungi.")
    log_stream.clear()  # Kosongkan log stream setelah selesai
    session.remove()  # Tutup session untuk domain ini
    driver.quit()
    return visited
