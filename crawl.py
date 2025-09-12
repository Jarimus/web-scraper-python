from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup,Tag

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
    
def get_urls_from_html(html: str, base_url: str) -> list[str]:
    soup = BeautifulSoup(html, 'html.parser')

    # Parse the urls and turn relative urls to absolute urls
    result = []
    links = soup.find_all("a")
    for link in links:
        if type(link) == Tag:
            href = link.get('href')
            if type(href) == str:
                if base_url not in href:
                    result.append(urljoin(base_url, href))
                else:
                    result.append(href)
        else:
            continue

    return result

def get_images_from_html(html: str, base_url: str) -> list[str]:
    result: list[str] = []
    soup = BeautifulSoup(html, 'html.parser')

    links = soup.find_all("img")
    for link in links:
        if type(link) == Tag:
            href = link.get('src')
            if type(href) == str:
                if base_url not in href:
                    result.append(urljoin(base_url, href))
                else:
                    result.append(href)
        else:
            continue

    return result
    

if __name__ == '__main__':
    input_url = "https://blog.boot.dev"
    input_body = """
        <html>
            <body>
                <a href="https://blog.boot.dev">
                    <span>Boot.dev</span>
                </a>
                <a href="/post_1">
                    <span>Boot.dev</span>
                </a>
                <a href="/post_2">
                    <span>Boot.dev</span>
                </a>
            </body
        ></html>"""
    actual = get_urls_from_html(input_body, input_url)

    print(actual)