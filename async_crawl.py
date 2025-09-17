import asyncio, aiohttp
from crawl import normalize_url, extract_page_data
from urllib.parse import urlparse
from asyncio import Task
from cprint import cprint
import csv

class AsyncCrawler:
    def __init__(self, base_url: str, max_concurrency: int, max_pages: int):
        self.base_url = base_url
        self.base_domain = urlparse(base_url).netloc
        self.page_data = {}
        self.lock = asyncio.Lock()
        self.max_concurrency = max_concurrency
        self.semaphore = asyncio.Semaphore(self.max_concurrency)
        self.session: aiohttp.ClientSession
        self.ignore = set()
        self.max_pages: int = max_pages
        self.should_stop = False
        self.all_tasks: set[Task] = set()

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    async def add_page_visit(self, normalized_url: str):
        async with self.lock:
            if self.should_stop:
                return False
            if normalized_url in self.page_data or normalized_url in self.ignore:
                return False
            if len(self.page_data) >= self.max_pages:
                self.should_stop = True
                cprint("Reached maximum number of pages to crawl.", "BRed")
                for task in self.all_tasks:
                    if not task.done():
                        task.cancel()
                return False
            return True
        
    async def get_html(self, url: str):
        try:
            async with self.session.get(
                url=url,
                headers={ "User-Agent": "BootCrawler/1.0"}
            ) as res:
                # Check status code
                if res.status >= 400:
                    return "", ConnectionError(f"Error connecting to server: {res.status}")
                # Make sure the response is text/html
                content_type = res.headers.get("Content-Type", "")
                if "text/html" not in content_type:
                    return "", ConnectionError(f"page is not text/html (is {content_type})")
                # Attempt to read the content
                payload = await res.text()
                return payload, None
        except Exception as err:
            return "", err
                
    async def crawl_page(self, current_url: str):
        if self.should_stop:
            return

        # Get normalized version of current_url.
        normalized_current_url = normalize_url(current_url)

        # Check whether url within initial domain
        current_url_obj = urlparse(current_url)
        if current_url_obj.netloc != self.base_domain:
            self.ignore.add(normalized_current_url)
            return
        
        async with self.semaphore:
            if self.should_stop:
                return
            # Check if the url is already visited and whether the page limit has been reached.
            if not await self.add_page_visit(normalized_current_url):
                return
            # Get html from the url. Print statement to keep track of the crawl.
            cprint(f"Getting html for {current_url} (Active: {self.max_concurrency - self.semaphore._value})", "BGreen")
            html, err = await self.get_html(current_url)
            if err:
                cprint(f"Invalid page: {err}", "BRed")
                self.ignore.add(normalized_current_url)
                return
            else:
                cprint(f"html for {current_url} retrieved successfully", "BGreen")
            # extract_page_data() to get rich data from the page, add to page_data[normalized_url] = page_data
            page_data = extract_page_data(html, current_url)
            async with self.lock:
                self.page_data[normalized_current_url] = page_data
            # Get all outgoing links from current page
            urls = page_data.get("outgoing_link_urls", [])

        # Recursively call each of them
        tasks = []
        for url in urls:
            normal_url = normalize_url(url)
            if normal_url in self.page_data or normal_url in self.ignore:
                continue
            task = asyncio.create_task(self.crawl_page(url))
            tasks.append(task)
            self.all_tasks.add(task)

        await asyncio.gather(*tasks, return_exceptions=True)
        
    async def crawl(self):
        await self.crawl_page(self.base_url)
        return self.page_data
    
async def crawl_site_async(base_url: str, max_concurrency: int=3, max_pages: int=10):
    async with AsyncCrawler(base_url, max_concurrency, max_pages) as crawler:
        data = await crawler.crawl()
        return data
    
def write_csv_report(page_data: dict[str, dict], filename:str="report.csv"):
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=[
            "page_url",
            "h1",
            "first_paragraph",
            "outgoing_link_urls",
            "image_urls"
        ],
        delimiter=",")
        writer.writeheader()
        for data in page_data.values():
            data["outgoing_link_urls"] = ";".join(data["outgoing_link_urls"])
            data["image_urls"] = ";".join(data["image_urls"])
            writer.writerow(data)