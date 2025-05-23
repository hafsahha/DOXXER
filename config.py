class Config:
    # URL awal (seed) untuk crawler
    SEED_URL = 'https://www.upi.edu'

    # Batas maksimal halaman yang akan di-crawl
    MAX_CRAWL_PAGES = 100

    # Batas maksimal hasil pencarian yang ditampilkan
    MAX_SEARCH_RESULTS = 20

    # Secret key Flask (ubah jika mau pakai session atau fitur keamanan)
    SECRET_KEY = 'your-secret-key-here'

    # Mode debug Flask (ubah jadi False saat produksi)
    DEBUG = True
