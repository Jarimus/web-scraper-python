import unittest
from crawl import normalize_url


class TestCrawl(unittest.TestCase):

    def test_normalize_url1(self):
        url = "https://blog.boot.dev/path/"
        actual = normalize_url(url)
        expected = "blog.boot.dev/path"
        self.assertEqual(actual, expected)
    
    def test_normalize_url2(self):
        url = "https://blog.boot.dev/path"
        actual = normalize_url(url)
        expected = "blog.boot.dev/path"
        self.assertEqual(actual, expected)

    def test_normalize_url3(self):
        url = "http://blog.boot.dev/path/"
        actual = normalize_url(url)
        expected = "blog.boot.dev/path"
        self.assertEqual(actual, expected)

    def test_normalize_url4(self):
        url = "http://blog.boot.dev/path"
        actual = normalize_url(url)
        expected = "blog.boot.dev/path"
        self.assertEqual(actual, expected)

    def test_normalize_url5(self):
        url = "http://blog.boot.dev/path/index.html"
        actual = normalize_url(url)
        expected = "blog.boot.dev/path"
        self.assertEqual(actual, expected)

    def test_normalize_url6(self):
        url = "http://bLog.bOOt.dEv/path/index.html"
        actual = normalize_url(url)
        expected = "blog.boot.dev/path"
        self.assertEqual(actual, expected)

if __name__ == "__main__":
    unittest.main()