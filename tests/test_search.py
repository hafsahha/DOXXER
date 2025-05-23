import unittest
from app.search.engine import search_keyword

class TestSearchEngine(unittest.TestCase):

    def setUp(self):
        self.data = {
            'http://site.com/page1': {'title': 'Page One', 'text': 'This is a test page about Python.'},
            'http://site.com/page2': {'title': 'Page Two', 'text': 'Another page discussing Java and coding.'},
        }

    def test_search_found(self):
        results = search_keyword(self.data, 'python')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['url'], 'http://site.com/page1')

    def test_search_not_found(self):
        results = search_keyword(self.data, 'golang')
        self.assertEqual(len(results), 0)

if __name__ == '__main__':
    unittest.main()
