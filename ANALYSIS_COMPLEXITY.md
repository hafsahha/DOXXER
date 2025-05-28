# Analisis Kompleksitas Algoritma DOXXER

## Deskripsi Sistem
DOXXER adalah mesin pencari informasi publik organisasi berbasis penelusuran graf BFS/DFS yang memungkinkan pengguna untuk mencari informasi di situs web universitas dan organisasi lainnya. Sistem ini menggunakan algoritma penelusuran graf untuk menjelajahi halaman web, menyimpannya di database terpisah berdasarkan domain dan metode crawling, dan menggunakan algoritma pencarian berbasis frekuensi kata kunci untuk menemukan informasi yang relevan. DOXXER juga menyediakan fitur visualisasi rute yang menunjukkan jalur navigasi dari seed URL ke halaman target.

## Algoritma Utama yang Digunakan

### 1. Breadth-First Search (BFS)

#### Implementasi
BFS diimplementasikan untuk melakukan crawling pada website organisasi dengan menelusuri halaman web secara level by level.

```python
def bfs_crawl(seed_url, max_pages=100):
    # Inisialisasi
    visited = set()
    queue = deque([seed_url])
    
    while queue and len(visited) < max_pages:
        url = queue.popleft()  # Ambil URL dari depan antrian
        
        # Proses halaman
        # ...
        
        # Tambahkan semua link yang belum dikunjungi ke queue
        for link_url, link_text in links:
            if link_url not in visited and link_url not in queue:
                queue.append(link_url)
```

#### Analisis Kompleksitas
- **Waktu**: O(V + E) di mana V adalah jumlah node (halaman web) dan E adalah jumlah edge (link antar halaman).
  - Setiap node dikunjungi tepat sekali: O(V)
  - Setiap edge diperiksa tepat sekali: O(E)
- **Ruang**: O(V) untuk menyimpan visited set dan queue.
  - Dalam kasus terburuk, semua node bisa ada dalam antrian.

### 2. Depth-First Search (DFS)

#### Implementasi
DFS diimplementasikan untuk melakukan crawling dengan mengeksplorasi jalur terjauh terlebih dahulu sebelum backtracking.

```python
def dfs_crawl(seed_url, max_pages=100):
    # Inisialisasi
    visited = set()
    stack = [seed_url]
    
    while stack and len(visited) < max_pages:
        url = stack.pop()  # Ambil URL dari atas stack
        
        # Proses halaman
        # ...
        
        # Tambahkan link yang belum dikunjungi ke stack (terbalik untuk mempertahankan urutan)
        for link_url, link_text in reversed(links):
            if link_url not in visited and link_url not in stack:
                stack.append(link_url)
```

#### Analisis Kompleksitas
- **Waktu**: O(V + E) di mana V adalah jumlah node (halaman web) dan E adalah jumlah edge (link antar halaman).
- **Ruang**: O(V) untuk menyimpan visited set dan stack.
  - Dalam kasus terburuk (graf linear), stack bisa berisi semua node.

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
- **Waktu**: O(D) di mana D adalah kedalaman/jarak dari target URL ke seed URL dalam grafik crawling.
  - Dalam kasus terburuk, jika target adalah daun terdalam, kompleksitasnya bisa menjadi O(V) di mana V adalah jumlah node.
- **Ruang**: O(D) untuk menyimpan path, atau O(V) dalam kasus terburuk.
  - Path berisi node-node yang membentuk jalur dari seed URL ke target URL.

### 4. Algoritma Pencarian Berdasarkan Frekuensi Kata Kunci

#### Implementasi
Sistem menggunakan algoritma pencarian teks sederhana berdasarkan frekuensi kata kunci dalam konten halaman web, yang memungkinkan pengurutan hasil berdasarkan relevansi.

```python
def search_keyword(data, keyword):
    keyword_lower = keyword.lower()
    results = []

    for url, page in data.items():
        if keyword_lower in page['text'].lower():
            # Simple relevance score based on keyword frequency
            relevance = page['text'].lower().count(keyword_lower)
            results.append({
                'url': url, 
                'title': page.get('title', url),
                'score': relevance
            })
    
    # Sort by relevance score in descending order
    results.sort(key=lambda x: x.get('score', 0), reverse=True)
    return results
```

#### Analisis Kompleksitas
- **Waktu**: 
  - Pencarian kata kunci: O(N * M) di mana N adalah jumlah halaman dan M adalah rata-rata panjang teks per halaman
  - Pengurutan hasil berdasarkan relevansi: O(K log K) di mana K adalah jumlah hasil yang cocok
  - Total kompleksitas waktu: O(N * M + K log K)
- **Ruang**: O(K) di mana K adalah jumlah hasil yang cocok

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
5. **Validasi URL**: Sistem hanya menjelajahi URL yang valid dan termasuk dalam domain yang sama.
6. **Penanganan Error**: Sistem menangani error saat crawling untuk mencegah kegagalan proses keseluruhan.
7. **Relevance Scoring**: Pengurutan hasil pencarian berdasarkan frekuensi kemunculan kata kunci untuk meningkatkan relevansi hasil.

## Kesimpulan
Pemilihan algoritma BFS atau DFS untuk web crawling bergantung pada karakteristik situs web dan tujuan crawling. Untuk pencarian informasi umum dan menemukan jalur terpendek, BFS lebih disarankan. Untuk eksplorasi mendalam pada situs web dengan struktur hierarkis yang dalam, DFS bisa menjadi pilihan yang lebih baik.

Kompleksitas waktu untuk kedua algoritma crawling adalah O(V + E), tetapi BFS umumnya membutuhkan lebih banyak memori dibandingkan DFS. Dalam implementasi nyata, pembatasan jumlah halaman, pembatasan kedalaman, dan teknik pelacakan parent sangat penting untuk menjaga efisiensi sistem dan memudahkan visualisasi rute.

Algoritma pencarian berdasarkan frekuensi kata kunci memberikan hasil yang lebih relevan daripada pencarian teks sederhana, dengan kompleksitas waktu O(N * M + K log K) yang masih efisien untuk ukuran database website organisasi umumnya.