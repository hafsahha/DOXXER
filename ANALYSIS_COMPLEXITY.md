# Analisis Kompleksitas Algoritma DOXXER

## Deskripsi Sistem
DOXXER adalah mesin pencari informasi publik organisasi berbasis penelusuran graf BFS/DFS yang memungkinkan pengguna untuk mencari informasi di situs web universitas dan organisasi lainnya. Sistem ini menggunakan algoritma penelusuran graf untuk menjelajahi halaman web dan algoritma pencarian teks untuk menemukan informasi yang relevan.

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
Algoritma BFS digunakan untuk menemukan rute/jalur dari halaman awal (seed URL) ke halaman target.

```python
def find_route(seed_url, target_url):
    visited = set()
    queue = [(seed_url, [])]  # (url, path_so_far)
    
    while queue:
        current_url, path = queue.pop(0)
        
        if current_url == target_url:
            return path
            
        if current_url in visited:
            continue
            
        visited.add(current_url)
        
        # Tambahkan semua link yang belum dikunjungi ke queue
        # beserta jalur yang telah dilalui
        for next_url, anchor_text in links:
            if next_url not in visited:
                new_path = path + [{"url": next_url, "label": anchor_text}]
                queue.append((next_url, new_path))
```

#### Analisis Kompleksitas
- **Waktu**: O(V + E) di mana V adalah jumlah node dan E adalah jumlah edge.
- **Ruang**: O(V) untuk menyimpan visited set, queue, dan path.
  - Path bisa berisi semua node dalam kasus terburuk.

### 4. Algoritma Pencarian Teks

#### Implementasi
Sistem menggunakan algoritma pencarian teks sederhana untuk menemukan kata kunci dalam konten halaman web.

```python
def search_keyword(data, keyword):
    results = []
    for page in data:
        if keyword.lower() in page.text.lower():
            results.append(page)
    return results[:MAX_RESULTS]
```

#### Analisis Kompleksitas
- **Waktu**: O(N * M) di mana N adalah jumlah halaman dan M adalah rata-rata panjang teks per halaman.
- **Ruang**: O(K) di mana K adalah jumlah hasil yang cocok.

## Perbandingan BFS vs DFS dalam Konteks Web Crawling

### BFS
- **Kelebihan**:
  - Menemukan halaman-halaman yang dekat dengan seed URL terlebih dahulu.
  - Menemukan jalur terpendek dari seed URL ke target URL.
  - Lebih sesuai untuk mencari informasi yang tersebar di berbagai bagian situs web.
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
1. **Caching Database**: Sistem menyimpan hasil crawling di database untuk mengurangi kebutuhan crawling ulang.
2. **Pembatasan Jumlah Halaman**: Parameter `max_pages` membatasi jumlah halaman yang dijelajahi.
3. **Validasi URL**: Sistem hanya menjelajahi URL yang valid dan termasuk dalam domain yang sama.
4. **Penanganan Error**: Sistem menangani error saat crawling untuk mencegah kegagalan proses keseluruhan.

## Kesimpulan
Pemilihan algoritma BFS atau DFS untuk web crawling bergantung pada karakteristik situs web dan tujuan crawling. Untuk pencarian informasi umum dan menemukan jalur terpendek, BFS lebih disarankan. Untuk eksplorasi mendalam pada situs web dengan struktur hierarkis yang dalam, DFS bisa menjadi pilihan yang lebih baik.

Kompleksitas waktu untuk kedua algoritma crawling adalah O(V + E), tetapi BFS umumnya membutuhkan lebih banyak memori dibandingkan DFS. Dalam implementasi nyata, pembatasan jumlah halaman dan teknik caching sangat penting untuk menjaga efisiensi sistem.