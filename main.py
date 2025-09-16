import sys, asyncio
from datetime import datetime
from async_crawl import crawl_site_async, write_csv_report
from cprint import cprint
import csv

async def main() -> None:
    # Ensure correct arg: website
    if len(sys.argv) < 2:
        print("no website provided")
        sys.exit(1)
    if len(sys.argv) not in [2, 4]:
        print("wrong number of arguments")
        sys.exit(1)
    base_url = sys.argv[1]
    cprint(f"starting crawl of: {base_url}", "BCyan")
    
    # Crawl the website
    if len(sys.argv) == 4:
        try:
            max_concurrency = int(sys.argv[2])
            max_pages = int(sys.argv[3])
        except:
            cprint("Error parsing arguments", "Red")
            sys.exit(1)
        data = await crawl_site_async(base_url, max_concurrency, max_pages)
    else:
        data = await crawl_site_async(base_url)
    if data:
        n = len(data)
        cprint("*"*20, "BYellow")
        cprint(f"Number of pages: {n}", "BYellow")
        # Write csv-file
        write_csv_report(data)
    else:
        print("Nothing retrieved.")


if __name__ == "__main__":
    start = datetime.now()
    result = asyncio.run(main())
    end = datetime.now()
    time = end - start
    cprint(f"Crawl duration: {time.total_seconds()} s", "BYellow")
