from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class SearchEngine:
    def __init__(self, data):
        """
        data: dict {url: {'title':..., 'text':..., ...}, ...}
        """
        self.urls = list(data.keys())
        self.docs = [data[url]['text'] for url in self.urls]

        # Buat TF-IDF matrix dokumen
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.tfidf_matrix = self.vectorizer.fit_transform(self.docs)

    def search(self, query, top_k=20):
        """
        Cari dokumen paling relevan dengan query menggunakan cosine similarity.

        Returns: list of dict [{'url':..., 'title':..., 'score':...}, ...]
        """
        query_vec = self.vectorizer.transform([query])
        cosine_similarities = cosine_similarity(query_vec, self.tfidf_matrix).flatten()

        # Ambil indeks dokumen dengan skor tertinggi
        top_indices = np.argsort(-cosine_similarities)[:top_k]

        results = []
        for idx in top_indices:
            score = cosine_similarities[idx]
            if score > 0:
                results.append({
                    'url': self.urls[idx],
                    'title': data[self.urls[idx]].get('title', self.urls[idx]),
                    'score': score
                })
        return results
