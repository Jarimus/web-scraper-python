import sys
from crawl import crawl_page

def main():
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
    data = crawl_page(base_url)
    if data:
        n = len(data)
        print("*"*20)
        print(f"Number of pages: {n}")
        print("Titles:")
        for rich_data in data.values():
            print(rich_data["h1"])
    else:
        print("Nothing retrieved.")


if __name__ == "__main__":
    main()
