from .database import db
from datetime import datetime
import json

class CrawledPage(db.Model):
    __tablename__ = 'crawled_pages'

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String, unique=True, nullable=False)
    title = db.Column(db.String, nullable=True)
    text = db.Column(db.Text, nullable=True)
    links_json = db.Column(db.Text, nullable=True)  # Simpan links sebagai JSON string
    crawled_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_links(self, links):
        # links = list of tuples (url, anchor_text)
        self.links_json = json.dumps(links)

    def get_links(self):
        if self.links_json:
            return json.loads(self.links_json)
        return []

class SearchResult(db.Model):
    __tablename__ = 'search_results'

    id = db.Column(db.Integer, primary_key=True)
    keyword = db.Column(db.String, nullable=False)
    results_json = db.Column(db.Text, nullable=False)  # Simpan hasil pencarian sebagai JSON
    searched_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_results(self, results):
        # results = list of dicts {'url':..., 'title':...}
        self.results_json = json.dumps(results)

    def get_results(self):
        if self.results_json:
            return json.loads(self.results_json)
        return []
