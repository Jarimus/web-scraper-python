import unittest
from crawl import normalize_url, get_h1_from_html, get_first_paragraph_from_html


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

    def test_find_h1_text1(self):
        html = """<html>
  <body>
    <h1>Welcome to Boot.dev</h1>
    <main>
      <p>Learn to code by building real projects.</p>
      <p>This is the second paragraph.</p>
    </main>
  </body>
</html>"""
        actual = get_h1_from_html(html)
        expected = "Welcome to Boot.dev"
        self.assertEqual(actual, expected)

    def test_find_h1_text2(self):
        html = """<html>
  <body>
    <h2>Welcome to Boot.dev</h2>
    <main>
      <p>Learn to code by building real projects.</p>
      <p>This is the second paragraph.</p>
    </main>
  </body>
</html>"""
        actual = get_h1_from_html(html)
        expected = ""
        self.assertEqual(actual, expected)

    def test_find_h1_text3(self):
        html = """<html>
  <body>
    <h1>Welcome to Boot.dev</h1>
    <h1>Second heading1 for reasons.</h1>
    <main>
      <p>Learn to code by building real projects.</p>
      <p>This is the second paragraph.</p>
    </main>
  </body>
</html>"""
        actual = get_h1_from_html(html)
        expected = "Welcome to Boot.dev"
        self.assertEqual(actual, expected)

    def test_find_first_para1(self):
        html = """<html>
  <body>
    <h1>Welcome to Boot.dev</h1>
    <main>
      <p>Learn to code by building real projects.</p>
      <p>This is the second paragraph.</p>
    </main>
  </body>
</html>"""
        actual = get_first_paragraph_from_html(html)
        expected = "Learn to code by building real projects."
        self.assertEqual(actual, expected)

    def test_find_first_para2(self):
        html = """<html>
  <body>
    <h1>Welcome to Boot.dev</h1>
    <main>
      <h2>Learn to code by building real projects.</h2>
      <p>This is the second paragraph.</p>
    </main>
  </body>
</html>"""
        actual = get_first_paragraph_from_html(html)
        expected = "This is the second paragraph."
        self.assertEqual(actual, expected)

    def test_find_first_para3(self):
        html = """<html>
  <body>
    <h1>Welcome to Boot.dev</h1>
    <main>
      <h2>Learn to code by building real projects.</h2>
      <h3>This is the second paragraph.</h3>
    </main>
  </body>
</html>"""
        actual = get_first_paragraph_from_html(html)
        expected = ""
        self.assertEqual(actual, expected)

if __name__ == "__main__":
    unittest.main()