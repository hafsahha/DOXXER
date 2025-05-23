import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def fetch_page(url, timeout=5):
    """
    Ambil konten halaman dari URL.
    Mengembalikan objek BeautifulSoup jika sukses, None jika gagal.
    """
    try:
        response = requests.get(url, timeout=timeout)
        if response.status_code == 200:
            return BeautifulSoup(response.text, 'html.parser')
        else:
            print(f"Warning: Status code {response.status_code} untuk {url}")
            return None
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

def extract_links(soup, base_url, base_domain):
    """
    Ekstrak semua link valid dari halaman yang sudah diparse.
    Hanya link yang masih dalam domain/subdomain yang sama yang dikembalikan.
    Mengembalikan list tuple: (absolute_url, anchor_text)
    """
    links = []
    if soup is None:
        return links

    for a_tag in soup.find_all('a', href=True):
        href = urljoin(base_url, a_tag['href'])
        if is_valid_url(href, base_domain):
            anchor = a_tag.get_text(strip=True)
            links.append((href, anchor))
    return links

def is_valid_url(url, base_domain):
    """
    Cek apakah url masih dalam domain/subdomain base_domain.
    """
    try:
        parsed = urlparse(url)
        return parsed.netloc.endswith(base_domain)
    except Exception:
        return False

def extract_text(soup):
    """
    Ambil teks bersih dari halaman yang sudah diparse.
    """
    if soup is None:
        return ''
    return soup.get_text(separator=' ', strip=True)

def extract_title(soup, url):
    """
    Ambil judul halaman jika ada, jika tidak return url sebagai fallback.
    """
    if soup is None:
        return url
    title_tag = soup.title
    if title_tag and title_tag.string:
        return title_tag.string.strip()
    return url
