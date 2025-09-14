import sys, asyncio
from datetime import datetime
from async_crawl import crawl_site_async

async def main() -> None:
    # Ensure correct arg: website
    if len(sys.argv) < 2:
        print("no website provided")
        sys.exit(1)
    if len(sys.argv) > 2:
        print("too many arguments provided")
        sys.exit(1)
    base_url = sys.argv[1]
    print(f"starting crawl of: {base_url}")
    
    # Crawl the website
    data = await crawl_site_async(base_url)
    if data:
        n = len(data)
        print("*"*20)
        print(f"Number of pages: {n}")
    #     print("Titles:")
    #     for rich_data in data.values():
    #         print(rich_data["h1"])
    # else:
    #     print("Nothing retrieved.")


if __name__ == "__main__":
    start = datetime.now()
    result = asyncio.run(main())
    end = datetime.now()
    print(f"Time to complete: {end - start}")
