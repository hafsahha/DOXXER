from flask import Blueprint, render_template, request, redirect, url_for
from app.search.engine import search_keyword, load_data_from_db
from app.crawler.bfs import bfs_crawl
from app.crawler.dfs import dfs_crawl
from app.models import CrawledPage
from config import Config

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/crawl', methods=['POST'])
def crawl():
    url = request.form.get('url')
    algorithm = request.form.get('algorithm', 'bfs')
    
    if not url:
        return render_template('index.html', error="Masukkan URL untuk crawling.")
    
    if algorithm == 'bfs':
        bfs_crawl(url)
    elif algorithm == 'dfs':
        dfs_crawl(url)
    else:
        return render_template('index.html', error="Algoritma tidak dikenali.")
    
    return render_template('index.html', message=f"Berhasil melakukan crawling dari {url}")

@main_bp.route('/search', methods=['POST'])
def search():
    keyword = request.form.get('keyword', '').strip()
    if not keyword:
        return render_template('index.html', error="Masukkan kata kunci pencarian.")
    
    data = load_data_from_db()
    results = search_keyword(data, keyword)
    
    return render_template('results.html', keyword=keyword, results=results)

@main_bp.route('/route/<path:target_url>')
def show_route(target_url):
    # Implementasi pencarian rute dari seed URL ke target URL
    seed_url = Config.SEED_URL
    route = find_route(seed_url, target_url)
    
    if not route:
        return render_template('index.html', error=f"Tidak dapat menemukan rute ke {target_url}")
    
    return render_template('route.html', route=route)

def find_route(seed_url, target_url):
    """
    Menemukan rute dari seed_url ke target_url menggunakan algoritma BFS
    """
    visited = set()
    queue = [(seed_url, [])]  # (url, path_so_far)
    
    while queue:
        current_url, path = queue.pop(0)
        
        if current_url == target_url:
            # Rute ditemukan
            return path + [{'url': current_url, 'label': get_page_title(current_url)}]
            
        if current_url in visited:
            continue
            
        visited.add(current_url)
        
        # Mengambil semua tautan dari halaman saat ini
        page = CrawledPage.query.filter_by(url=current_url).first()
        if page:
            links = page.get_links()
            
            # Menambahkan semua tautan yang belum dikunjungi ke antrian
            for link_url, link_text in links:
                if link_url not in visited:
                    new_path = path + [{'url': current_url, 'label': get_page_title(current_url)}]
                    queue.append((link_url, new_path))
    
    # Jika tidak ada rute yang ditemukan
    return None

def get_page_title(url):
    """
    Mendapatkan judul halaman dari database
    """
    page = CrawledPage.query.filter_by(url=url).first()
    if page and page.title:
        return page.title
    return url
