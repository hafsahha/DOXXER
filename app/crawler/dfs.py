from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from app.models import CrawledPage, Base
from app.database import get_domain_from_url, get_session_for_domain
from bs4 import BeautifulSoup
from .utils import extract_title, extract_text, extract_links, is_valid_url
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

def crawl(seed_url, max_pages=Config.MAX_CRAWL_PAGES, max_depth=Config.MAX_CRAWL_DEPTH, max_degree=Config.MAX_CRAWL_DEGREE):
    seed_url = seed_url.replace("www.", "")
    seed_url = seed_url[:-1] if seed_url.endswith("/") else seed_url  # Hapus trailing slash jika ada

    driver = initialize_driver()
    driver.set_page_load_timeout(15)
    driver.get(seed_url)

    domain = get_domain_from_url(seed_url)
    session, engine = get_session_for_domain(domain, "dfs")
    Base.metadata.create_all(engine)
    visited = set()
    failed = set()
    stack = [(seed_url, 0, None)]  # Menyimpan URL dan kedalaman (depth)
    
    log_message(f"Mulai crawling DFS dari {seed_url}...")

    while stack and len(visited) < max_pages:
        url, depth, parent_url = stack.pop()
        url = url.replace("www.", "")
        url = url[:-1] if url.endswith("/") else url  # Hapus trailing slash jika ada
        
        # Lewati URL yang sudah dikunjungi atau gagal
        if any(url == v[0] for v in visited) or url in failed:
            continue

        # Lewati URL yang sudah ada di database
        if session.query(CrawledPage).filter_by(url=url).first():
            continue
        
        # Batasi kedalaman crawling
        if depth > max_depth:
            continue

        # Batasi derajat (degree) crawling
        parent_count = sum(1 for _, p in visited if p == parent_url)
        print(f"Parent URL: {parent_url}, Count: {parent_count}")
        if parent_count >= max_degree:
            log_message(f"Melebihi batas derajat (degree) crawling untuk {url}.")
            continue
            
        log_message(f"{depth} - Mengunjungi {url}")
        success = False
        for attempt in range(3):
            try:
                driver.get(url)
                time.sleep(2)
                success = True
                break

            except Exception as e:
                log_message(f"Error saat mengunjungi {url} (attempt {attempt + 1}): {str(e)}")

        if not success:
            log_message(f"Error saat mengunjungi {url} setelah 3 percobaan. Melanjutkan ke URL berikutnya...")
            failed.add(url)
            continue

        try:
            html_content = driver.page_source
            soup = BeautifulSoup(html_content, "html.parser")
            title = extract_title(soup, url)
            text = extract_text(soup)
            links = extract_links(soup, url)
            
            page = CrawledPage(
                url = url,
                title = title,
                text = text,
                parent = parent_url
            )
            page.set_links(links)

            session.add(page)
            session.commit()
            
            log_message(f"Halaman tersimpan: {title} ({url})")
            visited.add((url, parent_url))  # Simpan URL yang sudah dikunjungi

            # Tambahkan semua link yang belum dikunjungi dan belum ada di queue
            qty = 0
            for target, _ in links:
                target = target.replace("www.", "")
                if target not in visited and all(target != s[0] for s in stack) and is_valid_url(target, url):
                    stack.append((target, depth + 1, url))
                    qty += 1
            log_message(f"Ditemukan {qty} link di halaman ini")

        except Exception as e:
            log_message(f"Error saat mengunjungi {url}: {str(e)}")

    log_message(f"DFS Crawling selesai! Total {len(visited)} halaman dikunjungi.")
    log_stream.clear()
    session.remove()
    driver.quit()
    return visited
