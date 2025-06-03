# Analisis Kompleksitas Algoritma DOXXER

## Deskripsi Sistem
DOXXER adalah mesin pencari informasi publik organisasi berbasis penelusuran graf BFS/DFS yang memungkinkan pengguna untuk mencari informasi di situs web universitas dan organisasi lainnya. Sistem ini menggunakan algoritma penelusuran graf untuk menjelajahi halaman web, menyimpannya di database terpisah berdasarkan domain dan metode crawling, dan menggunakan algoritma pencarian berbasis frekuensi kata kunci untuk menemukan informasi yang relevan. DOXXER juga menyediakan fitur visualisasi rute yang menunjukkan jalur navigasi dari seed URL ke halaman target.

## Algoritma Utama yang Digunakan

### 1. Breadth-First Search (BFS)

#### Implementasi
BFS diimplementasikan untuk melakukan crawling pada website organisasi dengan menelusuri halaman web secara level by level.

```python
def crawl(seed_url, max_pages=Config.MAX_CRAWL_PAGES, max_degree=Config.MAX_CRAWL_DEGREE):

    #inisialisasi
    driver = initialize_driver()
    driver.set_page_load_timeout(15)
    driver.get(seed_url)

    visited = set()
    failed = set()
    queue = deque([(seed_url, 0, None)])
    
    # loop semua halaman
    while queue and len(visited) < max_pages:
        url, depth, parent_url = queue.popleft() # ambil komponen dari queue

        # Lewati URL yang sudah dikunjungi
        # ...

        # Lewati URL yang sudah ada di database
        # ...

        # Batasi derajat (degree) crawling
        # ...
        
        success = False
        for attempt in range(3):
            try:
                # Iterasi halaman yang error (max. 3)
                # ...

            except Exception as e:
                # Error message

        # Skip halaman yang tidak bisa diproses dan dump ke failed set
        if not success:
            failed.add(url)
            continue
        
        try:
            # Proses halaman
            # ...
                    
        except Exception as e:
            # Error message

    log_stream.clear()  # Kosongkan log stream setelah selesai
    session.remove()  # Tutup session untuk domain ini
    driver.quit()
    return visited # Kembalikan hasil crawl
```

#### Analisis Kompleksitas
- **Waktu**: O(v + e) di mana v adalah jumlah node (halaman web) dan e adalah jumlah edge (link antar halaman).
  - Setiap node dikunjungi tepat sekali: O(v)
  - Setiap edge diperiksa tepat sekali: O(e)
- **Ruang**: O(v) untuk menyimpan visited set dan queue.
  - Dalam kasus terburuk, semua node bisa ada dalam antrian.

### 2. Depth-First Search (DFS)

#### Implementasi
DFS diimplementasikan untuk melakukan crawling dengan mengeksplorasi jalur terjauh terlebih dahulu sebelum backtracking.

```python
def crawl(seed_url, max_pages=Config.MAX_CRAWL_PAGES, max_depth=Config.MAX_CRAWL_DEPTH, max_degree=Config.MAX_CRAWL_DEGREE):

    # inisialisasi
    driver = initialize_driver()
    driver.set_page_load_timeout(15)
    driver.get(seed_url)

    visited = set()
    failed = set()
    stack = [(seed_url, 0, None)]  # Menyimpan URL dan kedalaman (depth)
    
    # loop semua halaman
    while stack and len(visited) < max_pages:
        url, depth, parent_url = stack.pop() # ambil komponen dari stack
        
        # Lewati URL yang sudah dikunjungi atau gagal
        # ...

        # Lewati URL yang sudah ada di database
        # ...
        
        # Batasi kedalaman crawling
        # ...

        # Batasi derajat (degree) crawling
        # ...
            
        success = False
        for attempt in range(3):
            try:
                # Iterasi halaman yang error (max. 3)
                # ...

            except Exception as e:
                # Error message

        # Skip halaman yang tidak bisa diproses dan dump ke failed set
        if not success:
            failed.add(url)
            continue

        try:
            # Proses halaman
            # ...
                    
        except Exception as e:
            # Error message

    log_stream.clear()  # Kosongkan log stream setelah selesai
    session.remove()  # Tutup session untuk domain ini
    driver.quit()
    return visited # Kembalikan hasil crawl
```

#### Analisis Kompleksitas
- **Waktu**: O(v + e) di mana v adalah jumlah vertex (halaman web) dan e adalah jumlah edge (link antar halaman).
- **Ruang**: O(v) untuk menyimpan visited set dan stack.
  - Dalam kasus terburuk (graf linear), stack bisa berisi semua vertex.

### 3. Pencarian Rute (Find Route)

#### Implementasi
Sistem menggunakan backtracking untuk menemukan rute/jalur dari halaman awal (seed URL) ke halaman target dengan memanfaatkan data parent yang tersimpan dalam database.

```python
def find_route(data, seed_url, target_url):
    # Validasi parameter
    if (not seed_url) or (not target_url) or (seed_url not in data) or (target_url not in data):
        return None

    # Backtracking untuk menemukan rute dari target_url ke seed_url
    path = []
    current = target_url
    while current:
        path.append(current)
        if current == seed_url:
            return path[::-1]  # Balik urutan path untuk mendapatkan rute dari seed ke target
        parent = data[current].get('parent')
        if not parent or parent == current:
            break
        current = parent

    return None
```

#### Analisis Kompleksitas
- **Waktu**: O(d) di mana d adalah kedalaman/jarak dari target URL ke seed URL dalam grafik crawling.
  - Dalam kasus terburuk, jika target adalah daun terdalam, kompleksitasnya bisa menjadi O(n) di mana n adalah jumlah node.
- **Ruang**: O(d) untuk menyimpan path, atau O(n) dalam kasus terburuk.
  - Path berisi node-node yang membentuk jalur dari seed URL ke target URL.

### 4. Algoritma Pencarian Berdasarkan Frekuensi Kata Kunci

#### Implementasi
Sistem menggunakan algoritma pencarian teks sederhana berdasarkan frekuensi kata kunci dalam konten halaman web, yang memungkinkan pengurutan hasil berdasarkan relevansi.

```python
def search_keyword(data, keyword):
    # Ubah keyword menjadi lowercase untuk pencarian case-insensitive
    keyword_lower = keyword.lower()
    results = []

    # Loop seluruh data untuk mencari keyword
    for url, page in data.items():
        if keyword_lower in page['text'].lower():
            relevance = page['text'].lower().count(keyword_lower) # Hitung relevansi berdasarkan jumlah kemunculan keyword
            words = page['text'].split() # Pisahkan teks menjadi kata-kata
            lower_words = [w.lower() for w in words] # Buat versi lowercase dari kata-kata untuk pencarian case-insensitive
            indices = [i for i, w in enumerate(lower_words) if w == keyword_lower] # Temukan indeks dari semua kemunculan keyword

            # Jika ada kemunculan keyword, ambil snippet sekitar kemunculan tersebut
            if indices:
                idx = indices[0]
                snippet_words = words[max(0, idx-10):idx+30] # Ambil 10 kata sebelum dan 30 kata setelah kemunculan keyword
                
                # Cetak tebal keyword dalam snippet
                snippet_words_bolded = [
                    f"<b>{w}</b>" if w.lower() == keyword_lower else w
                    for w in snippet_words
                ]
                snippet = ' '.join(snippet_words_bolded) # Gabungkan kata-kata menjadi satu string
            
            # Jika tidak ada kemunculan keyword, ambil 250 karakter pertama sebagai snippet
            else:
                snippet = page['text'][:250]
            
            # Tambahkan hasil pencarian ke dalam list
            results.append({
                'url': url, 
                'title': page.get('title', url),
                'snippet': snippet,
                'score': relevance
            })
    
    # Urutkan hasil berdasarkan skor relevansi
    results.sort(key=lambda x: x.get('score', 0), reverse=True)
    return results
```

#### Analisis Kompleksitas
- **Waktu**: 
  - Pencarian kata kunci: O(n * m) di mana n adalah jumlah halaman dan m adalah rata-rata panjang teks per halaman
  - Pengurutan hasil berdasarkan relevansi: O(k log k) di mana k adalah jumlah hasil yang cocok
  - Total kompleksitas waktu: O(n * m + k log k)
- **Ruang**: O(k) di mana k adalah jumlah hasil yang cocok

## Perbandingan BFS vs DFS dalam Konteks Web Crawling

### BFS
- **Kelebihan**:
  - Menemukan halaman-halaman yang dekat dengan seed URL terlebih dahulu.
  - Menemukan jalur terpendek dari seed URL ke target URL.
  - Lebih sesuai untuk mencari informasi yang tersebar di berbagai bagian situs web.
  - Memudahkan visualisasi rute karena menjamin jalur terpendek.
- **Kekurangan**:
  - Membutuhkan lebih banyak memori untuk menyimpan antrian.
  - Kurang efisien untuk situs web yang sangat dalam.

### DFS
- **Kelebihan**:
  - Membutuhkan memori yang lebih sedikit.
  - Lebih baik untuk menjelajahi struktur web yang dalam.
  - Dapat menemukan konten spesifik yang berada di level yang lebih dalam.
- **Kekurangan**:
  - Mungkin terjebak dalam jalur yang sangat panjang sebelum menjelajahi bagian lain dari situs web.
  - Tidak menjamin menemukan jalur terpendek.

## Optimasi yang Dilakukan
1. **Multi-Database**: Sistem menyimpan hasil crawling di database terpisah berdasarkan domain dan metode crawling untuk pengelolaan data yang lebih baik.
2. **Parent Tracking**: Mekanisme pelacakan parent URL untuk memudahkan visualisasi rute tanpa perlu algoritma pencarian path tambahan.
3. **Pembatasan Jumlah Halaman**: Parameter `max_pages` membatasi jumlah halaman yang dijelajahi.
4. **Pembatasan Kedalaman**: Untuk DFS, parameter `max_depth` mencegah penelusuran terlalu dalam yang dapat menghabiskan waktu dan sumber daya.
5. **Pembatasan Ekspansi Node**: parameter `max_degree` membatasi jumlah children yang dimiliki suatu node atau ekspansi suatu halaman.
6. **Validasi URL**: Sistem hanya menjelajahi URL yang valid dan termasuk dalam domain yang sama.
7. **Penanganan Error**: Sistem menangani error saat crawling untuk mencegah kegagalan proses keseluruhan.
8. **Relevance Scoring**: Pengurutan hasil pencarian berdasarkan frekuensi kemunculan kata kunci untuk meningkatkan relevansi hasil.

## Kesimpulan
Pemilihan algoritma BFS atau DFS untuk web crawling bergantung pada karakteristik situs web dan tujuan crawling. Untuk pencarian informasi umum dan menemukan jalur terpendek, BFS lebih disarankan. Untuk eksplorasi mendalam pada situs web dengan struktur hierarkis yang dalam, DFS bisa menjadi pilihan yang lebih baik.

Kompleksitas waktu untuk kedua algoritma crawling adalah O(v + e), tetapi BFS umumnya membutuhkan lebih banyak memori dibandingkan DFS. Dalam implementasi nyata, pembatasan jumlah halaman, pembatasan kedalaman, dan teknik pelacakan parent sangat penting untuk menjaga efisiensi sistem dan memudahkan visualisasi rute.

Algoritma pencarian berdasarkan frekuensi kata kunci memberikan hasil yang lebih relevan daripada pencarian teks sederhana, dengan kompleksitas waktu O(n * m + k log k) yang masih efisien untuk ukuran database website organisasi umumnya.