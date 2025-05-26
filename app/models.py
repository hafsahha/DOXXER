from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
import json

Base = declarative_base()

class CrawledPage(Base):
    __tablename__ = 'crawled_pages'

    id = Column(Integer, primary_key=True)
    url = Column(String, nullable=False, unique=True, index=True)
    title = Column(String, nullable=True)
    text = Column(Text, nullable=True)
    parent = Column(String, nullable=True)
    links_json = Column(Text, nullable=True)  # Simpan links sebagai JSON string
    crawled_at = Column(DateTime, default=datetime.utcnow)

    def set_links(self, links):
        self.links_json = json.dumps(links)

    def get_links(self):
        if self.links_json:
            return json.loads(self.links_json)
        return []

class SearchResult(Base):
    __tablename__ = 'search_results'

    id = Column(Integer, primary_key=True)
    keyword = Column(String, nullable=False, index=True)
    results_json = Column(Text, nullable=False)  # Simpan hasil pencarian sebagai JSON
    searched_at = Column(DateTime, default=DateTime)

    def set_results(self, results):
        self.results_json = json.dumps(results)

    def get_results(self):
        if self.results_json:
            return json.loads(self.results_json)
        return []
