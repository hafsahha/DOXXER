# DOXXER: Mesin Pencari Informasi Publik Organisasi

DOXXER adalah mesin pencari web internal yang dirancang untuk memudahkan pengguna menemukan informasi di situs-situs organisasi yang kompleks, seperti website universitas. Dengan menggunakan algoritma penelusuran graf Breadth-First Search (BFS) dan Depth-First Search (DFS), DOXXER menelusuri struktur website organisasi dan menyediakan fitur pencarian yang efisien.

## Fitur Utama

* **Penelusuran Web dengan BFS dan DFS**: Menjelajahi website dimulai dari seed URL menggunakan algoritma penelusuran graf
* **Pencarian Kata Kunci**: Mencari informasi berdasarkan kata kunci yang dimasukkan
* **Visualisasi Rute Link**: Menampilkan jalur navigasi dari halaman utama ke halaman yang berisi informasi
* **User Interface Web**: Antarmuka web yang mudah digunakan seperti mesin pencari modern
* **Fokus pada Satu Organisasi**: Menelusuri halaman-halaman dalam satu organisasi termasuk subdomain
* **Penyimpanan Cache**: Hasil crawling disimpan dalam database untuk penggunaan kembali

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
   ```
   git clone https://github.com/yourusername/DOXXER.git
   cd DOXXER
   ```

2. Buat dan aktifkan virtual environment:
   ```
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # Linux/Mac
   python -m venv venv
   source venv/bin/activate
   ```

3. Install dependensi:
   ```
   pip install -r requirements.txt
   ```

4. Inisialisasi database:
   ```
   python init_db.py
   ```

5. Jalankan aplikasi:
   ```
   python run.py
   ```

6. Buka browser dan akses `http://127.0.0.1:5000/`

## Konfigurasi

Konfigurasi utama dapat diubah di file `config.py`:

* `SEED_URL`: URL awal untuk crawler (default: https://www.upi.edu)
* `MAX_CRAWL_PAGES`: Batas maksimal halaman yang di-crawl (default: 100)
* `MAX_SEARCH_RESULTS`: Batas maksimal hasil pencarian (default: 20)

## Penggunaan

### Crawling Website

1. Buka halaman utama aplikasi
2. Pada bagian Crawling, masukkan URL yang ingin di-crawl atau gunakan URL default
3. Pilih algoritma (BFS atau DFS)
4. Klik "Mulai Crawling"
5. Tunggu proses crawling selesai

### Pencarian Informasi

1. Pada form pencarian, masukkan kata kunci yang ingin dicari
2. Klik tombol "Cari" atau tekan Enter
3. Hasil pencarian akan ditampilkan dengan daftar halaman yang relevan
4. Klik pada hasil untuk membuka halaman, atau klik "Lihat Rute Link" untuk melihat jalur navigasi

## Algoritma

### Breadth-First Search (BFS)

BFS menelusuri website level by level, sehingga halaman-halaman yang berjarak sama dari seed URL akan dikunjungi secara berurutan. Ini membuat BFS lebih cocok untuk menemukan konten yang lebih dangkal dalam struktur website.

### Depth-First Search (DFS)

DFS menelusuri satu jalur hingga kedalaman maksimum sebelum kembali untuk menjelajahi jalur lain. DFS lebih efisien dari sisi memori untuk struktur website yang sangat dalam.

## Dokumentasi

Untuk dokumentasi lebih detail, lihat file-file berikut:

* [Panduan Pengguna](docs/user_guide.html) - Tutorial penggunaan lengkap
* [Analisis Kompleksitas](ANALYSIS_COMPLEXITY.md) - Analisis algoritma yang digunakan

## Kontributor

Lihat [anggota_kelompok.txt](anggota_kelompok.txt) untuk daftar kontributor.

## Lisensi

Proyek ini dilisensikan di bawah MIT License - lihat file LICENSE untuk detail.

---

Dibuat sebagai Proyek UTS Analisis Algoritma, Universitas Pendidikan Indonesia, 2024.
