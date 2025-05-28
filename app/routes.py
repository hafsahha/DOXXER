from flask import Response, Blueprint, request, stream_with_context, render_template, redirect, url_for, flash
from app.search.engine import search_keyword, load_data_from_db, get_available_databases
from app.search.similarity import SearchEngine
from app.crawler.bfs import log_stream as bfs_log
from app.crawler.dfs import log_stream as dfs_log
from app.crawler import bfs, dfs
from app.models import CrawledPage
from config import Config
import requests

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """
    Halaman utama aplikasi
    """
    databases = get_available_databases()
    return render_template('index.html', databases=databases)


@main_bp.route('/crawl', methods=['POST'])
def crawl():
    """
    Endpoint untuk memulai crawling
    """

    # Inisialisasi variabel
    url = request.form.get('url')
    algorithm = request.form.get('algorithm')
    
    # Validasi URL
    response = requests.get(url, timeout=5)
    if response.status_code != 200:
        flash('URL tidak valid atau tidak dapat diakses.', 'error_crawl')
        return redirect(url_for('main.index'))

    # Validasi jenis algoritma crawling
    if algorithm == 'bfs':
        bfs.crawl(url)
    elif algorithm == 'dfs':
        dfs.crawl(url)
    else:
        flash('Pilih algoritma crawling yang valid.', 'error_crawl')
        return redirect(url_for('main.index'))
    
    # Pesan crawling berhasil
    flash('Crawling berhasil!', 'success_crawl')
    return redirect(url_for('main.index'))


@main_bp.route('/search', methods=['POST', 'GET'])
def search():
    """
    Endpoint untuk melakukan pencarian
    """

    # Jika request adalah POST, ambil kata kunci dari form
    if request.method == 'POST':
        keyword = request.form.get('keyword', '').strip()
        if not keyword:
            flash('Masukkan kata kunci pencarian.', 'error_search')
            return redirect(url_for('main.index'))
        
        database = request.form.get('database', '')
        return redirect(url_for('main.search', keyword=keyword, database=database, page=1))
    
    # Jika request adalah GET, ambil kata kunci dari query string
    else:
        keyword = request.args.get('keyword', '').strip()
        if not keyword:
            return redirect(url_for('main.index'))
        
        # Ambil indikator halaman
        page = request.args.get('page', 1, type=int)
        per_page = Config.MAX_SEARCH_RESULTS
        
        # Ambil data dari database yang dipilih
        database = request.args.get('database')
        data = load_data_from_db(database)
        
        # Lakukan pencarian berdasarkan kata kunci
        all_results = search_keyword(data, keyword)
        
        # Hitung total hasil dan buat pagination
        total_results = len(all_results)
        total_pages = max(1, (total_results + per_page - 1) // per_page)
        start_idx = (page - 1) * per_page
        end_idx = min(start_idx + per_page, total_results)
        paginated_results = all_results[start_idx:end_idx] if start_idx < total_results else []
        
        # Ambil daftar database yang tersedia
        databases = get_available_databases()
        
        return render_template('results.html', 
            keyword=keyword,
            database=database,
            databases=databases,
            results=paginated_results,
            total_results=total_results,
            page=page,
            total_pages=total_pages
        )


# tinggal route yah yang blum he he he
@main_bp.route('/route/<path:target_url>')
def show_route(target_url):
    seed_url = request.args.get('seed_url')
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
    
    return None

def get_page_title(url):
    """
    Mendapatkan judul halaman dari database
    """

    # Mengambil halaman dari database berdasarkan URL
    page = CrawledPage.query.filter_by(url=url).first()
    if page and page.title:
        return page.title
    return url


@main_bp.route('/logs/stream/<algorithm>')
def stream_logs(algorithm):
    """
    Streaming log crawling untuk BFS atau DFS
    """

    # Validasi algoritma
    if algorithm == 'bfs':
        log_stream = bfs_log
    elif algorithm == 'dfs':
        log_stream = dfs_log
    else:
        return Response("Algoritma tidak valid.", status=400)

    # Streaming log sebagai Server-Sent Events (SSE)
    def event_stream():
        previous_length = 0
        while True:
            if len(log_stream) > previous_length:
                new_logs = log_stream[previous_length:]
                for log in new_logs:
                    yield f"data: {log}\n\n"
                previous_length = len(log_stream)

    # Mengembalikan response dengan streaming log
    return Response(stream_with_context(event_stream()), content_type='text/event-stream')
