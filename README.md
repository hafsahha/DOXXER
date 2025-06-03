# DOXXER: Mesin Pencari Informasi Publik Organisasi

<div align="center">
  <img src="https://img.shields.io/badge/Python-3.7+-blue.svg" alt="Python 3.7+">
  <img src="https://img.shields.io/badge/Flask-2.0.0+-green.svg" alt="Flask 2.0.0+">
  <img src="https://img.shields.io/badge/License-Educational-yellow.svg" alt="License">
  <img src="https://img.shields.io/badge/Last%20Updated-June%202025-orange.svg" alt="Last Updated">
</div>

<p align="center">
  <i>Sistem pencarian informasi berbasis crawler dengan algoritma BFS/DFS</i>
</p>

---

## 🔍 Overview

DOXXER adalah mesin pencari web internal yang dirancang untuk memudahkan pengguna menemukan informasi di situs-situs organisasi yang kompleks, seperti website universitas. Dengan menggunakan algoritma penelusuran graf Breadth-First Search (BFS) dan Depth-First Search (DFS), DOXXER menelusuri struktur website organisasi dan menyimpannya ke dalam database terpisah sesuai domain dan metode crawling. Sistem ini menyediakan pencarian berdasarkan kata kunci dengan fitur visualisasi rute yang memungkinkan pengguna melihat jalur navigasi dari halaman awal hingga halaman target.

## 🐈 Preview

https://github.com/user-attachments/assets/207b41d5-5922-4da0-810e-6e56b8415013


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
| Pencarian | Frekuensi kata kunci |
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
│   │   └── engine.py              # Mesin pencari
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
│   ├── bfs-[domain].db            # Database hasil BFS (contoh: bfs-ipb.ac.id.db)
│   └── dfs-[domain].db            # Database hasil DFS (contoh: dfs-harvard.edu.db)
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
   git clone https://github.com/hafsahha/DOXXER.git
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

Konfigurasi utama dapat diubah di file [`config.py`](config.py):

| Parameter | Deskripsi | Default |
|-----------|-----------|---------|
| `MAX_CRAWL_PAGES` | Batas maksimal halaman yang di-crawl | 200 |
| `MAX_CRAWL_DEPTH` | Batas kedalaman maksimal (hanya DFS) | 5 |
| `MAX_CRAWL_DEGREE` | Batas ekspansi node maksimal | 20 |
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
def crawl(seed_url, max_pages=Config.MAX_CRAWL_PAGES, max_degree=Config.MAX_CRAWL_DEGREE):
    seed_url = seed_url.replace("www.", "")
    seed_url = seed_url[:-1] if seed_url.endswith("/") else seed_url  # Hapus trailing slash jika ada

    driver = initialize_driver()
    driver.set_page_load_timeout(15)
    driver.get(seed_url)
    
    domain = get_domain_from_url(seed_url)
    session, engine = get_session_for_domain(domain, "bfs")
    Base.metadata.create_all(engine)
    visited = set()
    failed = set()
    queue = deque([(seed_url, 0, None)])
    
    log_message(f"Mulai crawling BFS dari {seed_url}...")

    while queue and len(visited) < max_pages:
        url, depth, parent_url = queue.popleft()
        url = url.replace("www.", "")
        url = url[:-1] if url.endswith("/") else url  # Hapus trailing slash jika ada
        
        # Lewati URL yang sudah dikunjungi
        if any(url == v[0] for v in visited) or url in failed:
            continue
        
        # Lewati URL yang sudah ada di database
        if session.query(CrawledPage).filter_by(url=url).first():
            continue

        # Batasi derajat (degree) crawling
        parent_count = sum(1 for _, p in visited if p == parent_url)
        print(f"Parent URL: {parent_url}, Count: {parent_count}")
        if parent_count >= max_degree:
            log_message(f"Melebihi batas derajat (degree) crawling untuk {url}.")
            continue
        
        log_message(f"{depth} - Mengunjungi: {url}")
        success = False
        for attempt in range(3):
            try:
                driver.get(url)
                time.sleep(2)
                success = True
                break

            except Exception as e:
                log_message(f"Error saat mengunjungi {url} (attempt {attempt + 1}): {str(e)}")

        if not success:
            log_message(f"Error saat mengunjungi {url} setelah 3 percobaan. Melanjutkan ke URL berikutnya...")
            failed.add(url)
            continue
        
        try:
            html_content = driver.page_source
            soup = BeautifulSoup(html_content, "html.parser")
            title = extract_title(soup, url)
            text = extract_text(soup)
            links = extract_links(soup, url)
            
            page = CrawledPage(
                url = url,
                title = title,
                text = text,
                parent = parent_url
            )
            page.set_links(links)

            session.add(page)
            session.commit()
            
            log_message(f"Halaman tersimpan: {title} ({url})")
            visited.add((url, parent_url))  # Simpan URL yang sudah dikunjungi

            # Tambahkan semua link yang belum dikunjungi dan belum ada di queue
            qty = 0
            for target, _ in links:
                target = target.replace("www.", "")
                if target not in visited and all(target != q[0] for q in queue) and is_valid_url(target, url):
                    queue.append((target, depth + 1, url))
                    qty += 1
            log_message(f"Ditemukan {qty} link di halaman ini")
                    
        except Exception as e:
            log_message(f"Error saat mengunjungi {url}: {str(e)}")

    log_message(f"BFS Crawling selesai! Total {len(visited)} halaman dikunjungi.")
    log_stream.clear()  # Kosongkan log stream setelah selesai
    session.remove()  # Tutup session untuk domain ini
    driver.quit()
    return visited
```

**Karakteristik:**
- Menggunakan struktur data queue (antrian)
- Menemukan jalur terpendek ke suatu halaman
- Membutuhkan lebih banyak memori untuk menyimpan antrian

### Depth-First Search (DFS)

DFS menelusuri satu jalur hingga kedalaman maksimum sebelum kembali menjelajahi jalur lain. Algoritma ini lebih hemat memori untuk website dengan struktur dalam.

**Implementasi:**
```python
def crawl(seed_url, max_pages=Config.MAX_CRAWL_PAGES, max_depth=Config.MAX_CRAWL_DEPTH, max_degree=Config.MAX_CRAWL_DEGREE):
    seed_url = seed_url.replace("www.", "")
    seed_url = seed_url[:-1] if seed_url.endswith("/") else seed_url  # Hapus trailing slash jika ada

    driver = initialize_driver()
    driver.set_page_load_timeout(15)
    driver.get(seed_url)

    domain = get_domain_from_url(seed_url)
    session, engine = get_session_for_domain(domain, "dfs")
    Base.metadata.create_all(engine)
    visited = set()
    failed = set()
    stack = [(seed_url, 0, None)]  # Menyimpan URL dan kedalaman (depth)
    
    log_message(f"Mulai crawling DFS dari {seed_url}...")

    while stack and len(visited) < max_pages:
        url, depth, parent_url = stack.pop()
        url = url.replace("www.", "")
        url = url[:-1] if url.endswith("/") else url  # Hapus trailing slash jika ada
        
        # Lewati URL yang sudah dikunjungi atau gagal
        if any(url == v[0] for v in visited) or url in failed:
            continue

        # Lewati URL yang sudah ada di database
        if session.query(CrawledPage).filter_by(url=url).first():
            continue
        
        # Batasi kedalaman crawling
        if depth > max_depth:
            continue

        # Batasi derajat (degree) crawling
        parent_count = sum(1 for _, p in visited if p == parent_url)
        print(f"Parent URL: {parent_url}, Count: {parent_count}")
        if parent_count >= max_degree:
            log_message(f"Melebihi batas derajat (degree) crawling untuk {url}.")
            continue
            
        log_message(f"{depth} - Mengunjungi {url}")
        success = False
        for attempt in range(3):
            try:
                driver.get(url)
                time.sleep(2)
                success = True
                break

            except Exception as e:
                log_message(f"Error saat mengunjungi {url} (attempt {attempt + 1}): {str(e)}")

        if not success:
            log_message(f"Error saat mengunjungi {url} setelah 3 percobaan. Melanjutkan ke URL berikutnya...")
            failed.add(url)
            continue

        try:
            html_content = driver.page_source
            soup = BeautifulSoup(html_content, "html.parser")
            title = extract_title(soup, url)
            text = extract_text(soup)
            links = extract_links(soup, url)
            
            page = CrawledPage(
                url = url,
                title = title,
                text = text,
                parent = parent_url
            )
            page.set_links(links)

            session.add(page)
            session.commit()
            
            log_message(f"Halaman tersimpan: {title} ({url})")
            visited.add((url, parent_url))  # Simpan URL yang sudah dikunjungi

            # Tambahkan semua link yang belum dikunjungi dan belum ada di queue
            qty = 0
            for target, _ in links:
                target = target.replace("www.", "")
                if target not in visited and all(target != s[0] for s in stack) and is_valid_url(target, url):
                    stack.append((target, depth + 1, url))
                    qty += 1
            log_message(f"Ditemukan {qty} link di halaman ini")

        except Exception as e:
            log_message(f"Error saat mengunjungi {url}: {str(e)}")

    log_message(f"DFS Crawling selesai! Total {len(visited)} halaman dikunjungi.")
    log_stream.clear()
    session.remove()
    driver.quit()
    return visited
```

**Karakteristik:**
- Menggunakan struktur data stack (tumpukan)
- Dapat menjelajahi jauh ke dalam struktur website
- Membutuhkan pembatasan kedalaman untuk mencegah penelusuran terlalu dalam
- Lebih hemat memori dalam beberapa kasus

## 📚 Dokumentasi

- **[Analisis Kompleksitas](ANALYSIS_COMPLEXITY.md)** - Analisis detail tentang kompleksitas waktu dan ruang algoritma yang digunakan

## 👥 Tim Pengembang

| Nama | NIM |
|------|-----|
| Datuk Daneswara R. Samsura | 2308224 |
| Hafsah Hamidah | 2311474 |
| Klara Ollivviera A. G | 2306205 |
| Naeya Adeani Putri | 2304017 |

## 📝 Lisensi

Dibuat sebagai Proyek UTS Analisis Algoritma,  
Universitas Pendidikan Indonesia, 2025




