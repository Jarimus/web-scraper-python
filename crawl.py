from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup,Tag
import requests

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
    main_section = soup.find('main')
    if main_section and type(main_section) == Tag:
        first_p = main_section.find("p")
    else:
        first_p = soup.find("p")

    return first_p.get_text(strip=True) if first_p else ""
    
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

def extract_page_data(html: str, page_url: str):
    url = get_urls_from_html(html, page_url)
    h1 = get_h1_from_html(html)
    first_paragraph = get_first_paragraph_from_html(html)
    links = get_urls_from_html(html, page_url)
    img_urls = get_images_from_html(html, page_url)

    data = {
        "url": page_url,
        "h1": h1,
        "first_paragraph": first_paragraph,
        "outgoing_links": links,
        "image_urls": img_urls
    }
    return data
    
def get_html(url: str) -> tuple[str, Exception | None]:
    res = requests.get(
        url=url,
        headers={
            "User-Agent": "BootCrawler/1.0"
        }
    )
    # Check status code
    if res.status_code >= 400:
        return "", ConnectionError("Something went wrong connecting to the server")
    # Make sure the response is text/html
    content_type = res.headers.get("Content-Type")
    if content_type and content_type.find("text/html") == -1:
        return "", ConnectionError("page is not text/html")
    # Attempt to read the content
    try:
        return res.content.decode(), None
    except Exception as err:
        return "", err