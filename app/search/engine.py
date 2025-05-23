def search_keyword(data, keyword, max_results=20):
    """
    Cari keyword dalam data hasil crawling.
    
    Args:
        data (dict): Dictionary hasil crawling dengan format:
                     {url: {'title': ..., 'text': ..., 'links': [...]}, ...}
        keyword (str): Kata kunci pencarian.
        max_results (int): Maksimum jumlah hasil yang dikembalikan.
        
    Returns:
        list of dict: Daftar hasil pencarian dengan format:
                      [{'url': ..., 'title': ...}, ...]
    """
    keyword_lower = keyword.lower()
    results = []
    
    for url, page in data.items():
        if keyword_lower in page['text'].lower():
            results.append({'url': url, 'title': page.get('title', url)})
            if len(results) >= max_results:
                break
                
    return results
