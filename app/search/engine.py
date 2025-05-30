from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import CrawledPage, Base
import os
import re

def search_keyword(data, keyword):
    """
    Mencari keyword dalam data yang diberikan
    """

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

def get_available_databases():
    """
    Get a list of available databases in the instance folder
    Returns a list of database names
    """
    databases = []
    db_dir = 'instance'
    if os.path.exists(db_dir):
        for db_file in os.listdir(db_dir):
            if db_file.endswith('.db'):
                db = {
                    'val': db_file,
                    'name': db_file.replace('.db', '').split('-')[1] if '-' in db_file else db_file.replace('.db', ''),
                    'method': db_file.upper().split('-')[0] if '-' in db_file else None
                }
                databases.append(db)
    return databases

def parse_database_name(db_name):
    """Parse database name to extract method and domain"""
    pattern = r'^(bfs|dfs)-(.+)\.db$'
    match = re.match(pattern, db_name)
    if match:
        return match.group(1), match.group(2)  # method, domain
    
    # If not in method-domain.db format, try to parse just domain
    domain = db_name.replace('.db', '')
    return None, domain

def load_data_from_db(database_name=None):
    """
    Load data from the specified database or all databases
    Returns a dictionary of data
    """
    data = {}
    
    if database_name:
        # Load data from the specified database
        db_path = os.path.join('instance', database_name)
        if os.path.exists(db_path):
            try:
                engine = create_engine(f'sqlite:///{db_path}')
                Session = sessionmaker(bind=engine)
                session = Session()
                Base.metadata.create_all(engine)
                
                pages = session.query(CrawledPage).all()
                for p in pages:
                    data[p.url] = {
                        'title': p.title or p.url,
                        'text': p.text or '',
                        'parent': p.parent,
                        'links': p.get_links(),
                        'database': database_name
                    }
                
                session.close()
                print(f"Loaded {len(pages)} pages from database {database_name}")
            except Exception as e:
                print(f"Error loading database {database_name}: {str(e)}")
    else:
        # Load data from all available databases
        for db_file in get_available_databases():
            try:
                db_path = os.path.join('instance', db_file)
                engine = create_engine(f'sqlite:///{db_path}')
                Session = sessionmaker(bind=engine)
                session = Session()
                Base.metadata.create_all(engine)
                
                pages = session.query(CrawledPage).all()
                for p in pages:
                    data[p.url] = {
                        'title': p.title or p.url,
                        'text': p.text or '',
                        'parent': p.parent,
                        'links': p.get_links(),
                        'database': db_file
                    }
                
                session.close()
                print(f"Loaded {len(pages)} pages from database {db_file}")
            except Exception as e:
                print(f"Error loading database {db_file}: {str(e)}")
    
    return data
