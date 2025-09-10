from urllib.parse import urlparse
import re

def normalize_url(url: str):
    url_parsed = urlparse(url=url)
    result = url_parsed.netloc + url_parsed.path
    result = result.lower().rstrip("/").replace("/index.html", "")
    return result

def get_h1_from_html(html: str):
    re_result = re.search(r"<h1>(.*)</h1>", html)
    if re_result:
        return re_result.group(1)
    else:
        return ""
    

if __name__ == '__main__':
    html = """<html>
  <body>
    <h>Welcome to Boot.dev</h1>
    <main>
      <p>Learn to code by building real projects.</p>
      <p>This is the second paragraph.</p>
    </main>
  </body>
</html>"""

    print(get_h1_from_html(html))