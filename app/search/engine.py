from app.models import CrawledPage

def search_keyword(data, keyword, max_results=20):
    keyword_lower = keyword.lower()
    results = []

    for url, page in data.items():
        if keyword_lower in page['text'].lower():
            results.append({'url': url, 'title': page.get('title', url)})
            if len(results) >= max_results:
                break
    return results

def load_data_from_db():
    data = {}
    pages = CrawledPage.query.all()
    for p in pages:
        data[p.url] = {
            'title': p.title,
            'text': p.text,
            'links': p.get_links()
        }
    return data
