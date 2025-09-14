import asyncio, aiohttp
from crawl import normalize_url, extract_page_data
from urllib.parse import urlparse

class AsyncCrawler:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.base_domain = urlparse(base_url).netloc
        self.page_data = {}
        self.lock = asyncio.Lock()
        self.max_concurrency = 3
        self.semaphore = asyncio.Semaphore(self.max_concurrency)
        self.session: aiohttp.ClientSession
        self.ignore = set()

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    async def add_page_visit(self, normalized_url):
        async with self.lock:
            if normalized_url in self.ignore:
                return False
            self.ignore.add(normalized_url)
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
                
    async def crawl_page(self, current_url=None):
        # For first page, current_url is base_url
        if current_url is None:
            current_url = self.base_url

        # Get normalized version of current_url.
        normalized_current_url = normalize_url(current_url)

        # Check whether url within initial domain
        current_url_obj = urlparse(current_url)
        if current_url_obj.netloc != self.base_domain:
            self.ignore.add(normalized_current_url)
            return
        
        # Check if the url is already visited
        if not await self.add_page_visit(normalized_current_url):
            return
        
        async with self.semaphore:
            # Get html from the url. Print statement to keep track of the crawl.
            print(f"Getting html for {current_url} (Active: {self.max_concurrency - self.semaphore._value})")
            html, err = await self.get_html(current_url)
            if err:
                print(f"Invalid page: {err}")
                return
            # extract_page_data() to get rich data from the page, add to page_data[normalized_url] = rich_data
            rich_data = extract_page_data(html, current_url)
            async with self.lock:
                self.page_data[normalized_current_url] = rich_data
            # Get all outgoing links from current page
            urls = rich_data.get("outgoing_links", [])
            # Recursively call each of them
            tasks = []
            for url in urls:
                if normalize_url(url) in self.ignore:
                    continue
                task = asyncio.create_task(self.crawl_page(url))
                tasks.append(task)
        if tasks:
            await asyncio.gather(*tasks)
        
    async def crawl(self):
        await self.crawl_page(self.base_url)
        return self.page_data
    
async def crawl_site_async(base_url: str):
    async with AsyncCrawler(base_url=base_url) as crawler:
        return await crawler.crawl()