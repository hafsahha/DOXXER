from flask import Response, Blueprint, request, stream_with_context, render_template, redirect, url_for, flash
from app.search.engine import search_keyword, load_data_from_db, get_available_databases
from app.search.similarity import SearchEngine
from app.crawler import bfs, dfs
from app.crawler.bfs import log_stream as bfs_log
from app.crawler.dfs import log_stream as dfs_log
from app.models import CrawledPage
from config import Config
import requests
import time
import os

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    # Get a list of all available databases for the dropdown
    databases = get_available_databases()
    return render_template('index.html', databases=databases)

@main_bp.route('/crawl', methods=['POST'])
def crawl():
    url = request.form.get('url')
    algorithm = request.form.get('algorithm')
    
    try:
        response = requests.get(url, timeout=5)
        valid_url = response.status_code == 200
    except Exception:
        valid_url = False

    if not url or not valid_url:
        flash('URL tidak valid atau tidak dapat diakses.', 'error_crawl')
        return redirect(url_for('main.index'))

    if algorithm == 'bfs':
        bfs.crawl(url)
    elif algorithm == 'dfs':
        dfs.crawl(url)
    else:
        flash('Pilih algoritma crawling yang valid.', 'error_crawl')
        return redirect(url_for('main.index'))
    
    flash('Crawling berhasil!', 'message')
    return redirect(url_for('main.index'))

@main_bp.route('/search', methods=['POST', 'GET'])
def search():
    if request.method == 'POST':
        keyword = request.form.get('keyword', '').strip()
        if not keyword:
            flash('Masukkan kata kunci pencarian.', 'error_search')
            return redirect(url_for('main.index'))
        
        # Get selected database
        database = request.form.get('database', '')
        
        # Redirect to GET with keyword and database parameters to allow pagination
        return redirect(url_for('main.search', keyword=keyword, database=database, page=1))
    else:
        keyword = request.args.get('keyword', '').strip()
        if not keyword:
            return redirect(url_for('main.index'))
        
        # Handle pagination
        page = request.args.get('page', 1, type=int)
        per_page = Config.MAX_SEARCH_RESULTS  # Items per page (reusing the existing config)
        
        # Get selected database
        database = request.args.get('database', '')
        
        # Load data from the selected database or all databases
        data = load_data_from_db(database)
        
        # Use more advanced search with TF-IDF if available
        try:
            if hasattr(Config, 'USE_ADVANCED_SEARCH') and Config.USE_ADVANCED_SEARCH and len(data) > 5:
                search_engine = SearchEngine(data)
                all_results = search_engine.search(keyword)
            else:
                all_results = search_keyword(data, keyword)
        except Exception as e:
            print(f"Error using advanced search: {str(e)}")
            all_results = search_keyword(data, keyword)
        
        # Calculate pagination
        total_results = len(all_results)
        total_pages = max(1, (total_results + per_page - 1) // per_page)  # Ceiling division, minimum 1 page
        
        # Get results for current page
        start_idx = (page - 1) * per_page
        end_idx = min(start_idx + per_page, total_results)  # Prevent index out of bounds
        paginated_results = all_results[start_idx:end_idx] if start_idx < total_results else []
        
        # Get all available databases for the database selector
        databases = get_available_databases()
        
        return render_template(
            'results.html', 
            keyword=keyword,
            database=database,
            databases=databases,
            results=paginated_results,
            total_results=total_results,
            page=page,
            total_pages=total_pages
        )

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

@main_bp.route('/logs/stream/<algorithm>')
def stream_logs(algorithm):
    """
    Endpoint untuk streaming log crawling untuk BFS atau DFS
    """
    if algorithm == 'bfs':
        log_stream = bfs_log
    elif algorithm == 'dfs':
        log_stream = dfs_log
    else:
        return Response("Algoritma tidak valid.", status=400)

    def event_stream():
        previous_length = 0
        while True:
            if len(log_stream) > previous_length:
                new_logs = log_stream[previous_length:]
                for log in new_logs:
                    yield f"data: {log}\n\n"
                previous_length = len(log_stream)

    return Response(stream_with_context(event_stream()), content_type='text/event-stream')
