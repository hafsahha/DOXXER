from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from config import Config
import numpy as np

class SearchEngine:
    def __init__(self, data):
        """
        data: dict {url: {'title':..., 'text':...}, ...}
        """
        self.data = data
        self.urls = list(data.keys())
        self.docs = [data[url]['text'] for url in self.urls]

        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.tfidf_matrix = self.vectorizer.fit_transform(self.docs)

    def search(self, query, top_k=Config.MAX_SEARCH_RESULTS):
        """
        Cari dokumen paling relevan dengan query.
        Returns list of dict [{'url':..., 'title':..., 'score':...}, ...]
        """
        query_vec = self.vectorizer.transform([query])
        cosine_sim = cosine_similarity(query_vec, self.tfidf_matrix).flatten()

        top_indices = np.argsort(-cosine_sim)[:top_k]

        results = []
        for idx in top_indices:
            score = cosine_sim[idx]
            if score > 0:
                results.append({
                    'url': self.urls[idx],
                    'title': self.data[self.urls[idx]].get('title', self.urls[idx]),
                    'score': score
                })
        return results
