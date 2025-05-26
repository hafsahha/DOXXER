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

def crawl(seed_url, max_pages=Config.MAX_CRAWL_PAGES, max_depth=Config.MAX_CRAWL_DEPTH):
    driver = initialize_driver()
    driver.get(seed_url)

    domain = get_domain_from_url(seed_url)
    session, engine = get_session_for_domain(domain, "dfs")
    Base.metadata.create_all(engine)
    visited = set()
    stack = [(seed_url, 0)]  # Menyimpan URL dan kedalaman (depth)
    
    print(f"Mulai crawling DFS dari {seed_url}...")
    print(f"Base domain: {domain}")

    while stack and len(visited) < max_pages:
        url, depth = stack.pop()
        
        # Batasi kedalaman crawling
        if depth > max_depth:
            continue
        
        if url in visited:
            continue
        visited.add(url)

        existing = session.query(CrawledPage).filter_by(url=url).first()
        if existing:
            continue
            
        log_message(f"Depth {depth}: Mengunjungi {url}")
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

            # Tambahkan link yang belum dikunjungi ke stack dengan penambahan kedalaman
            for link_url, link_text in reversed(links):
                if link_url not in visited and link_url not in stack:
                    stack.append((link_url, depth + 1))  # Increment depth

        except Exception as e:
            log_message(f"Error saat mengunjungi {url}: {str(e)}")
            visited.add(url)  # Tandai sebagai dikunjungi agar tidak dicoba lagi

    log_message(f"DFS Crawling selesai! Total {len(visited)} halaman dikunjungi.")
    log_stream.clear() # Kosongkan log stream setelah selesai
    session.remove()
    driver.quit()
    return visited
