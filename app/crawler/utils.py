from urllib.parse import urljoin, urlparse

def extract_links(soup, base_url, base_domain):
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
    try:
        parsed = urlparse(url)
        return parsed.netloc.endswith(base_domain)
    except:
        return False

def extract_text(soup):
    if soup is None:
        return ''
    return soup.get_text(separator=' ', strip=True)

def extract_title(soup, url):
    if soup is None:
        return url
    if soup.title and soup.title.string:
        return soup.title.string.strip()
    return url
