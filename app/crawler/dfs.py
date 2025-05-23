import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def is_valid_url(url, base_domain):
    try:
        parsed = urlparse(url)
        return parsed.netloc.endswith(base_domain)
    except:
        return False

def dfs_crawl(seed_url, max_pages=100):
    base_domain = urlparse(seed_url).netloc
    visited = set()
    pages = {}

    def dfs(url):
        if url in visited or len(visited) >= max_pages:
            return
        try:
            response = requests.get(url, timeout=5)
            if response.status_code != 200:
                return
            soup = BeautifulSoup(response.text, 'html.parser')
            title = soup.title.string.strip() if soup.title else url
            text = soup.get_text(separator=' ', strip=True)

            links = []
            for a_tag in soup.find_all('a', href=True):
                href = urljoin(url, a_tag['href'])
                if is_valid_url(href, base_domain) and href not in visited:
                    links.append((href, a_tag.get_text(strip=True)))

            pages[url] = {
                'title': title,
                'text': text,
                'links': links
            }
            visited.add(url)

            for (link_url, _) in links:
                dfs(link_url)
        except Exception as e:
            print(f"Error crawling {url}: {e}")

    dfs(seed_url)
    return pages
