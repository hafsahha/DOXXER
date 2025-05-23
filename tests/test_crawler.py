import unittest
from app.crawler.bfs import bfs_crawl

class TestCrawler(unittest.TestCase):

    def test_crawl_seed(self):
        seed_url = 'https://www.example.com'
        # Crawl dengan max 2 halaman supaya cepat
        result = bfs_crawl(seed_url, max_pages=2)
        self.assertIsInstance(result, dict)
        self.assertTrue(seed_url in result)

    def test_crawl_limit(self):
        seed_url = 'https://www.example.com'
        max_pages = 1
        result = bfs_crawl(seed_url, max_pages=max_pages)
        self.assertLessEqual(len(result), max_pages)

if __name__ == '__main__':
    unittest.main()
