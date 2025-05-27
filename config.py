class Config:
    # Batas maksimal halaman yang akan di-crawl
    MAX_CRAWL_PAGES = 200

    # Batas maksimal kedalaman crawling (hanya untuk DFS)
    MAX_CRAWL_DEPTH = 3

    # Batas maksimal hasil pencarian yang ditampilkan
    MAX_SEARCH_RESULTS = 20

    # Secret key Flask (ubah jika mau pakai session atau fitur keamanan)
    SECRET_KEY = 'your-secret-key-here'

    # Mode debug Flask (ubah jadi False saat produksi)
    DEBUG = True
