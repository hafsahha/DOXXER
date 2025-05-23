from flask import Blueprint, render_template, request, abort

main_bp = Blueprint('main', __name__)

# Halaman utama: form input kata kunci
@main_bp.route('/')
def index():
    return render_template('index.html')

# Endpoint pencarian: terima POST keyword, tampilkan hasil dummy
@main_bp.route('/search', methods=['POST'])
def search():
    keyword = request.form.get('keyword', '').strip()
    if not keyword:
        # Kalau kosong, kembali ke halaman index dengan pesan error sederhana
        return render_template('index.html', error="Masukkan kata kunci pencarian.")
    
    # Dummy data hasil pencarian
    results = [
        {'url': 'https://www.upi.edu/pendaftaran', 'title': 'Pendaftaran Mahasiswa Baru'},
        {'url': 'https://www.upi.edu/fakultas', 'title': 'Fakultas dan Program Studi'},
        {'url': 'https://www.upi.edu/kontak', 'title': 'Kontak dan Informasi'}
    ]
    
    # Filter dummy hasil berdasarkan keyword (simulasi)
    filtered = [r for r in results if keyword.lower() in r['title'].lower()]
    
    return render_template('results.html', keyword=keyword, results=filtered)

# Endpoint tampilkan rute link dari seed ke halaman hasil (dummy)
@main_bp.route('/route')
def route():
    url = request.args.get('url')
    if not url:
        abort(404)
    
    # Dummy rute contoh (harus diganti dengan hasil traversal BFS/DFS asli nanti)
    route = [
        {'url': 'https://www.upi.edu', 'label': 'Beranda'},
        {'url': url, 'label': 'Halaman Tujuan'}
    ]
    
    return render_template('route.html', route=route)
