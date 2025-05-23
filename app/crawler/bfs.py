from collections import deque
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def is_valid_url(url, base_domain):
    """
    Cek apakah url masih dalam domain/subdomain yang sama dengan base_domain.
    """
    try:
        parsed = urlparse(url)
        return parsed.netloc.endswith(base_domain)
    except Exception:
        return False

def bfs_crawl(seed_url, max_pages=100):
    """
    Crawling menggunakan BFS dimulai dari seed_url.
    Mengembalikan dictionary data halaman dengan format:
    {
        url: {
            'title': <judul halaman>,
            'text': <isi teks halaman>,
            'links': [(link_url, anchor_text), ...]
        },
        ...
    }
    """
    base_domain = urlparse(seed_url).netloc
    visited = set()
    queue = deque([seed_url])
    pages = {}

    while queue and len(visited) < max_pages:
        current_url = queue.popleft()

        if current_url in visited:
            continue

        try:
            response = requests.get(current_url, timeout=5)
            if response.status_code != 200:
                continue

            soup = BeautifulSoup(response.text, 'html.parser')

            title = soup.title.string.strip() if soup.title else current_url
            text = soup.get_text(separator=' ', strip=True)

            links = []
            for a_tag in soup.find_all('a', href=True):
                href = urljoin(current_url, a_tag['href'])
                if is_valid_url(href, base_domain) and href not in visited:
                    links.append((href, a_tag.get_text(strip=True)))
                    queue.append(href)

            pages[current_url] = {
                'title': title,
                'text': text,
                'links': links
            }

            visited.add(current_url)

        except Exception as e:
            print(f"Error crawling {current_url}: {e}")

    return pages
