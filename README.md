# DOXXER: Sistem Pencarian Informasi Publik Organisasi dengan Algoritma BFS/DFS

DOXXER adalah mesin pencari web internal yang dirancang untuk memudahkan pengguna menemukan informasi di situs-situs organisasi yang kompleks, seperti website universitas. Dengan menggunakan algoritma penelusuran graf Breadth-First Search (BFS) dan Depth-First Search (DFS), DOXXER menelusuri struktur website organisasi dan menyediakan fitur pencarian yang efisien.

## Fitur Utama

* **Penelusuran Web dengan BFS dan DFS**: Menjelajahi website dimulai dari seed URL menggunakan algoritma penelusuran graf.  
* **Pencarian Kata Kunci**: Mencari informasi berdasarkan kata kunci yang dimasukkan.  
* **Visualisasi Rute Link**: Menampilkan jalur navigasi dari halaman utama ke halaman yang berisi informasi.  
* **User Interface Web**: Antarmuka web yang mudah digunakan seperti mesin pencari modern.  
* **Fokus pada Satu Organisasi**: Menelusuri halaman-halaman dalam satu organisasi termasuk subdomain.  
* **Penyimpanan Cache**: Hasil crawling disimpan dalam database untuk penggunaan kembali.

## Teknologi

* Python 3.x  
* Flask (Web Framework)  
* SQLAlchemy (ORM)  
* Selenium (Web Crawling)  
* BeautifulSoup (HTML Parsing)  
* Scikit-learn (Pencarian dan Similarity)  
* SQLite (Database)

## Instalasi

### Prasyarat

* Python 3.7 atau lebih baru  
* Pip (Python Package Manager)  
* Google Chrome (untuk Selenium WebDriver)

### Langkah-langkah

1. Clone repository ini:  
   ```bash
   git clone https://github.com/yourusername/DOXXER.git
   cd DOXXER
````

2. Buat dan aktifkan virtual environment:

   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # Linux/Mac
   python -m venv venv
   source venv/bin/activate
   ```

3. Install dependensi:

   ```bash
   pip install -r requirements.txt
   ```

4. Inisialisasi database:

   ```bash
   python init_db.py
   ```

5. Jalankan aplikasi:

   ```bash
   python run.py
   ```

6. Buka browser dan akses:

   ```
   http://127.0.0.1:5000/
   ```

## requirements.txt

Isi file `requirements.txt` yang harus ada di root proyek:

```
Flask>=2.0.0
Flask-SQLAlchemy>=2.5.0
requests>=2.25.0
beautifulsoup4>=4.9.0
selenium>=4.0.0
webdriver-manager>=3.4.0
scikit-learn>=1.0.0
numpy>=1.21.0
```

## Konfigurasi

Konfigurasi utama dapat diubah di file `config.py`:

* `SEED_URL`: URL awal untuk crawler (default: [https://www.upi.edu](https://www.upi.edu))
* `MAX_CRAWL_PAGES`: Batas maksimal halaman yang di-crawl (default: 100)
* `MAX_SEARCH_RESULTS`: Batas maksimal hasil pencarian (default: 20)

## Penggunaan

### Crawling Website

1. Buka halaman utama aplikasi.
2. Pada bagian Crawling, masukkan URL yang ingin di-crawl atau gunakan URL default.
3. Pilih algoritma crawling (BFS atau DFS).
4. Klik tombol **Mulai Crawling**.
5. Tunggu hingga proses crawling selesai.

### Pencarian Informasi

1. Masukkan kata kunci yang ingin dicari di form pencarian.
2. Klik tombol **Cari** atau tekan Enter.
3. Hasil pencarian akan ditampilkan dengan daftar halaman relevan.
4. Klik pada hasil untuk membuka halaman, atau klik **Lihat Rute Link** untuk melihat jalur navigasi.

## Algoritma

### Breadth-First Search (BFS)

BFS menelusuri website level by level, sehingga halaman-halaman yang berjarak sama dari seed URL dikunjungi secara berurutan. Cocok untuk menemukan konten yang lebih dangkal.

### Depth-First Search (DFS)

DFS menelusuri satu jalur hingga kedalaman maksimum sebelum kembali menjelajahi jalur lain. Lebih hemat memori untuk website dengan struktur dalam.

## Dokumentasi

* [Analisis Kompleksitas Algoritma](ANALYSIS_COMPLEXITY.md)
* [Panduan Pengguna (opsional)](docs/user_guide.html)

## Anggota Kelompok

1. Datuk Daneswara R. Samsura (NPM 2308224)
2. Hafsah Hamidah (NPM 2311474)
3. Klara Ollivviera A. G (NPM 2306205)
4. Naeya Adeani Putri (NPM 2304017)

## Lisensi

Proyek ini dilisensikan di bawah MIT License - lihat file LICENSE untuk detail.

---

Dibuat sebagai Proyek UTS Analisis Algoritma,
Universitas Pendidikan Indonesia, 2024