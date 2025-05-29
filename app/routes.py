from flask import Response, Blueprint, request, stream_with_context, render_template, redirect, url_for, flash
from app.search.engine import search_keyword, load_data_from_db, get_available_databases
from app.crawler.bfs import log_stream as bfs_log
from app.crawler.dfs import log_stream as dfs_log
from app.crawler import bfs, dfs
from config import Config
import requests

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """
    Halaman utama aplikasi
    """
    databases = get_available_databases()
    return render_template('index.html', databases=databases, debug=True)


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


@main_bp.route('/route/<path:db>/<path:target_url>')
def show_route(target_url, db):
    """
    Menampilkan rute dari seed_url ke target_url
    """

    # Validasi URL awal (seed)
    data = load_data_from_db(db)
    urls = [urls for urls, _ in data.items()]
    seed_url = urls[0] if urls else None

    # Cari rute dari seed_url ke target_url
    route = find_route(data, seed_url, target_url)
    
    # Jika tidak ada rute yang ditemukan, tampilkan pesan error
    if not route:
        return render_template('results.html', error=f"Tidak dapat menemukan rute ke {target_url}")
    
    # Jika rute ditemukan, tampilkan halaman rute
    return render_template('route.html', route=route)

def find_route(data, seed_url, target_url):
    """
    Menemukan rute dari seed_url ke target_url menggunakan algoritma BFS dengan backtracking parent.
    """

    # Validasi parameter
    if (not seed_url) or (not target_url) or (seed_url not in data) or (target_url not in data):
        return None

    # Backtracking untuk menemukan rute dari target_url ke seed_url
    path = []
    current = target_url
    while current:
        path.append(current)
        if current == seed_url:
            return path[::-1]
        parent = data[current].get('parent')
        if not parent or parent == current:
            break
        current = parent

    return None


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
