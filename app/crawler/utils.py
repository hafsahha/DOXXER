from urllib.parse import urljoin, urlparse

def is_valid_url(target_url, base_url):
    """
    Validasi URL
    """
    try:

        # Normalisasi URL dengan menghapus www.
        if "www." in base_url:
            base_url = base_url.replace("www.", "")
        if "www." in target_url:
            target_url = target_url.replace("www.", "")

        # Parse URL untuk mendapatkan komponen
        base = urlparse(base_url)
        target = urlparse(target_url)

        return (
            (target.hostname == base.hostname or target.hostname.endswith('.' + base_url)) # hanya domain yang sama atau subdomain
            and not target.fragment # tidak ada fragment
            and target.scheme in ('http', 'https') # hanya http dan https
        )
    
    except:
        return False


def extract_links(soup, base_url):
    """
    Ekstrak semua link dari BeautifulSoup object
    """

    # Jika soup tidak valid, kembalikan daftar kosong
    links = []
    if soup is None:
        return links

    # Iterasi semua tag <a> dengan atribut href
    for a_tag in soup.find_all('a', href=True):
        target_url = urljoin(base_url, a_tag['href'])

        # Validasi URL
        if not is_valid_url(target_url, base_url):
            continue
        
        # Append ke daftar links
        anchor = a_tag.get_text(strip=True)
        links.append((target_url, anchor))
    
    return links


def extract_text(soup):
    """
    Ekstrak teks dari BeautifulSoup object
    """

    # Jika soup tidak valid, kembalikan string kosong
    if soup is None:
        return ''
    
    # Gunakan get_text untuk mendapatkan teks dari semua elemen
    return soup.get_text(separator=' ', strip=True)


def extract_title(soup, url):
    """
    Ekstrak judul dari BeautifulSoup object
    """

    # Jika soup tidak valid, kembalikan URL
    if soup is None:
        return url
    
    # Cek apakah ada tag <title> dan ambil isinya
    if soup.title and soup.title.string:
        return soup.title.string.strip()
    
    # Jika tidak ada tag <title>, kembalikan URL
    return url
