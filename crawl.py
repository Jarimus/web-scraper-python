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

def extract_page_data(html: str, page_url: str) -> dict[str, str | list[str]]:
    h1 = get_h1_from_html(html)
    first_paragraph = get_first_paragraph_from_html(html)
    links = get_urls_from_html(html, page_url)
    img_urls = get_images_from_html(html, page_url)

    return {
        "url": page_url,
        "h1": h1,
        "first_paragraph": first_paragraph,
        "outgoing_links": links,
        "image_urls": img_urls
    }
    
def get_html(url: str) -> tuple[str, Exception | None]:
    res = requests.get(
        url=url,
        headers={
            "User-Agent": "BootCrawler/1.0"
        }
    )
    # Check status code
    if res.status_code >= 400:
        return "", ConnectionError(f"Error connecting to server: {res.status_code}")
    # Make sure the response is text/html
    content_type = res.headers.get("Content-Type")
    if content_type and content_type.find("text/html") == -1:
        return "", ConnectionError(f"page is not text/html (is {content_type})")
    # Attempt to read the content
    try:
        return res.content.decode(), None
    except Exception as err:
        return "", err
    
def crawl_page(base_url: str, current_url=None, page_data: dict={}, checked_urls: set[str]=set()):
    # For first page, current_url is base_url
    if current_url is None:
        current_url = base_url
    
    # Make sure current_url is in the same domain
    if not current_url.startswith(base_url):
        return

    # Get normalized version of current_url. Add it to checked urls
    normalized_url = normalize_url(current_url)
    checked_urls.add(normalized_url)

    # Get html from the url. Print statement to keep track of the crawl.
    print(f"Getting html for {current_url}")
    html, err = get_html(current_url)
    if err:
        print(f"Invalid page: {err}")
        return
    # extract_page_data() to get rich data from the page, add to page_data[normalized_url] = rich_data
    rich_data = extract_page_data(html, current_url)
    page_data[normalized_url] = rich_data
    # Get all outgoing links from current page
    urls = rich_data.get("outgoing_links", [])
    # Recursively call each of them
    for url in urls:
        url_normalized = normalize_url(url)
        if url_normalized in checked_urls:
            continue
        checked_urls.add(url_normalized)
        crawl_page(base_url, url, page_data, checked_urls)
    return page_data