# DOXXER: Mesin Pencari Informasi Publik Organisasi

<div align="center">
  <img src="https://img.shields.io/badge/Python-3.7+-blue.svg" alt="Python 3.7+">
  <img src="https://img.shields.io/badge/Flask-2.0.0+-green.svg" alt="Flask 2.0.0+">
  <img src="https://img.shields.io/badge/License-Educational-yellow.svg" alt="License">
</div>

<p align="center">
  <i>Sistem pencarian informasi berbasis crawler dengan algoritma BFS/DFS</i>
</p>

---

## 📋 Daftar Isi

- [Overview](#-overview)
- [Fitur Utama](#-fitur-utama)
- [Teknologi](#-teknologi)
- [Struktur Aplikasi](#-struktur-aplikasi)
- [Instalasi](#-instalasi)
- [Konfigurasi](#-konfigurasi)
- [Penggunaan](#-penggunaan)
- [Algoritma](#-algoritma)
- [Dokumentasi](#-dokumentasi)
- [Tim Pengembang](#-tim-pengembang)
- [Lisensi](#-lisensi)

## 🔍 Overview

DOXXER adalah mesin pencari web internal yang dirancang untuk memudahkan pengguna menemukan informasi di situs-situs organisasi yang kompleks, seperti website universitas. Dengan menggunakan algoritma penelusuran graf Breadth-First Search (BFS) dan Depth-First Search (DFS), DOXXER menelusuri struktur website organisasi dan menyediakan fitur pencarian yang efisien.

## ✨ Fitur Utama

- **Penelusuran Web dengan BFS dan DFS**: Menjelajahi website dimulai dari seed URL menggunakan algoritma penelusuran graf
- **Pencarian Kata Kunci**: Mencari informasi berdasarkan kata kunci yang dimasukkan
- **Visualisasi Rute Link**: Menampilkan jalur navigasi dari halaman awal ke halaman target dengan tampilan terminal-like
- **Multi-Database**: Penyimpanan dan pencarian terpisah berdasarkan domain dan metode crawling
- **Pagination**: Navigasi hasil pencarian dengan sistem pagination yang efisien
- **Modern UI dengan Tailwind**: Antarmuka web yang responsif dan modern
- **Pemilihan Database**: Pencarian spesifik pada database crawling tertentu

## 🛠️ Teknologi

| Komponen | Teknologi |
|----------|-----------|
| Backend | Python 3.7+ |
| Web Framework | Flask |
| Database | SQLite, SQLAlchemy |
| Web Crawling | Selenium, BeautifulSoup |
| Algoritma | BFS, DFS |
| Pencarian | TF-IDF, Cosine Similarity (scikit-learn) |
| Frontend | HTML, Tailwind CSS, JavaScript |

## 📁 Struktur Aplikasi

```
DOXXER/
├── app/                           # Kode aplikasi utama
│   ├── crawler/                   # Modul crawler
│   │   ├── bfs.py                 # Implementasi BFS
│   │   ├── dfs.py                 # Implementasi DFS
│   │   └── utils.py               # Fungsi pembantu crawler
│   ├── search/                    # Modul pencarian
│   │   └──  engine.py              # Mesin pencari
│   ├── __init__.py                # Inisialisasi aplikasi Flask
│   ├── database.py                # Konfigurasi database
│   ├── models.py                  # Model database
│   └── routes.py                  # Route dan controller
├── templates/                     # Template HTML
│   ├── index.html                 # Halaman utama
│   ├── results.html               # Hasil pencarian
│   └── route.html                 # Visualisasi rute
├── static/                        # Aset statis
│   └── style.css                  # CSS untuk tampilan
├── instance/                      # Data lokal (database)
│   ├── bfs-[domain].db            # Database hasil BFS
│   └── dfs-[domain].db            # Database hasil DFS
├── config.py                      # Konfigurasi aplikasi
├── init_db.py                     # Script inisialisasi database
├── requirements.txt               # Dependensi
├── run.py                         # Entry point aplikasi
├── ANALYSIS_COMPLEXITY.md         # Analisis kompleksitas algoritma
└── README.md                      # Dokumentasi proyek
```

## 📥 Instalasi

### Prasyarat

- Python 3.7 atau lebih baru
- Pip (Python Package Manager)
- Google Chrome (untuk Selenium WebDriver)

### Langkah-langkah

1. **Clone repository**

   ```bash
   git clone https://github.com/yourusername/DOXXER.git
   cd DOXXER
   ```

2. **Buat dan aktifkan virtual environment**

   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # Linux/Mac
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install dependensi**

   ```bash
   pip install -r requirements.txt
   ```

4. **Inisialisasi database**

   ```bash
   python init_db.py
   ```

5. **Jalankan aplikasi**

   ```bash
   python run.py
   ```

6. **Akses aplikasi**

   Buka browser dan akses `http://127.0.0.1:5000/`

## ⚙️ Konfigurasi

Konfigurasi utama dapat diubah di file `config.py`:

| Parameter | Deskripsi | Default |
|-----------|-----------|---------|
| `MAX_CRAWL_PAGES` | Batas maksimal halaman yang di-crawl | 200 |
| `MAX_CRAWL_DEPTH` | Batas kedalaman maksimal (hanya DFS) | 3 |
| `MAX_SEARCH_RESULTS` | Batas maksimal hasil pencarian per halaman | 20 |
| `DEBUG` | Mode debug | True |

## 📖 Penggunaan

### Crawling Website

1. Buka halaman utama aplikasi
2. Pada form Crawling, masukkan URL yang ingin di-crawl (misalnya `https://upi.edu`)
3. Pilih algoritma crawling (BFS atau DFS)
4. Klik tombol untuk memulai crawling
5. Pantau proses crawling melalui terminal-like interface yang akan muncul
6. Tunggu hingga proses crawling selesai (ditandai dengan pesan "Crawling selesai!")

### Pencarian Informasi

1. Pada form Pencarian, masukkan kata kunci yang ingin dicari
2. Pilih database dari dropdown (hasil crawling tersimpan berdasarkan domain dan algoritma)
3. Klik tombol Cari atau tekan Enter
4. Hasil pencarian akan menampilkan halaman yang relevan dengan pagination
5. Navigasi antar halaman hasil menggunakan kontrol pagination di bagian bawah

### Melihat Rute Link

1. Pada hasil pencarian, klik tombol "Lihat Rute Link" di samping hasil yang ingin dilihat rutenya
2. Halaman visualisasi rute akan menampilkan jalur dari seed URL ke halaman target
3. Setiap langkah menunjukkan URL dan judul halaman dengan animasi terminal-like
4. Klik link pada rute untuk membuka halaman di tab baru

## 🧮 Algoritma

### Breadth-First Search (BFS)

BFS menelusuri website level by level, sehingga halaman-halaman yang berjarak sama dari seed URL dikunjungi secara berurutan. Algoritma ini cocok untuk menemukan konten yang berada di level yang lebih dangkal dalam struktur website.

**Implementasi:**
```python
def crawl(seed_url, max_pages):
    queue = deque([seed_url])
    visited = set()
    
    while queue and len(visited) < max_pages:
        url = queue.popleft()
        if url in visited:
            continue
            
        visited.add(url)
        # Proses halaman dan ekstrak konten
        
        # Tambahkan semua link yang belum dikunjungi dan belum ada di queue
        for link_url, link_text in links:
            if link_url not in visited and link_url not in queue:
                queue.append(link_url)
```

**Karakteristik:**
- Menggunakan struktur data queue (antrian)
- Menemukan jalur terpendek ke suatu halaman
- Membutuhkan lebih banyak memori untuk menyimpan antrian

### Depth-First Search (DFS)

DFS menelusuri satu jalur hingga kedalaman maksimum sebelum kembali menjelajahi jalur lain. Algoritma ini lebih hemat memori untuk website dengan struktur dalam.

**Implementasi:**
```python
def crawl(seed_url, max_pages, max_depth):
    stack = [(seed_url, 0)]  # (url, depth)
    visited = set()
    
    while stack and len(visited) < max_pages:
        url, depth = stack.pop()
        if depth > max_depth:
            continue
        if url in visited:
            continue
            
        visited.add(url)
        # Proses halaman dan ekstrak konten
        
        # Tambahkan link baru ke stack (terbalik untuk pertahankan urutan)
        for link_url, link_text in reversed(links):
            if link_url not in visited:
                stack.append((link_url, depth + 1))
```

**Karakteristik:**
- Menggunakan struktur data stack (tumpukan)
- Dapat menjelajahi jauh ke dalam struktur website
- Membutuhkan pembatasan kedalaman untuk mencegah penelusuran terlalu dalam
- Lebih hemat memori dalam beberapa kasus

## 📚 Dokumentasi

- Analisis Kompleksitas Algoritma - Analisis detail tentang kompleksitas algoritma yang digunakan
- Panduan Pengguna - Panduan lengkap penggunaan aplikasi

## 👥 Tim Pengembang

| Nama | NPM |
|------|-----|
| Datuk Daneswara R. Samsura | 2308224 |
| Hafsah Hamidah | 2311474 |
| Klara Ollivviera A. G | 2306205 |
| Naeya Adeani Putri | 2304017 |

## 📝 Lisensi

Dibuat sebagai Proyek UTS Analisis dan Desain Algoritma,  
Universitas Pendidikan Indonesia, 2025




