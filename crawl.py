from urllib.parse import urlparse
from bs4 import BeautifulSoup

def normalize_url(url: str):
    url_parsed = urlparse(url=url)
    result = url_parsed.netloc + url_parsed.path
    result = result.lower().rstrip("/").replace("/index.html", "")
    return result

def get_h1_from_html(html: str) -> str:
    soup: BeautifulSoup = BeautifulSoup(html, 'html.parser')
    h1 = soup.find("h1")
    if h1:
        return h1.get_text()
    else:
        return ""

def get_first_paragraph_from_html(html: str) -> str:
    soup = BeautifulSoup(html, 'html.parser')
    p = soup.find("p")
    if p:
        return p.get_text()
    else:
        return ""
    

if __name__ == '__main__':
    html = """<html>
  <body>
    <h1>Welcome to Boot.dev</h1>
    <main>
      <p>Learn to code by building real projects.</p>
      <p>This is the second paragraph.</p>
    </main>
  </body>
</html>"""

    print(get_h1_from_html(html))