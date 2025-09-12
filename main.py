import sys
from crawl import get_html

def main():
    if len(sys.argv) < 2:
        print("no website provided")
        sys.exit(1)
    if len(sys.argv) > 2:
        print("too many arguments provided")
        sys.exit(1)
    
    base_url = sys.argv[1]
    print(f"starting crawl of: {base_url}")
    content, err = get_html(base_url)
    if err:
        print(f"Error fetching website: {err}")
        sys.exit(1)
    print(content)


if __name__ == "__main__":
    main()
