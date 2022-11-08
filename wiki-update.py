import json
import re

from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

from utils import user_agent
from utils import fetch_url

base_url: str = "https://luckys-tale.fandom.com"
user_agent = user_agent(base_url)


def parse_page(page: str) -> str:
    return f"{base_url}/wiki/{page}"


def soup_me(url: str):
    req = fetch_url(url)
    return BeautifulSoup(req.text, "html.parser")


all_wiki_pages: list[str] = []


def get_all_pages():
    special_all_pages = soup_me(parse_page("Special:AllPages"))
    pages_list = special_all_pages.find_all("ul", class_="mw-allpages-chunk")

    for pages in pages_list:
        # Filter all the redirects by not specifying any CSS class
        filter_available = pages.find_all("a", class_="", href=re.compile("^/wiki/"))

        for anchor in filter_available:
            get_link = anchor["href"]
            # Parse closing parentheses to clickable URL to prevent any errors
            parse_parenthesis = re.sub("\(", "%28", get_link)
            parse_parenthesis_final = re.sub("\)", "%29", parse_parenthesis)

            all_wiki_pages.append(re.sub("^/wiki/", "", parse_parenthesis_final))


def main():
    get_all_pages()

    for wiki_page in all_wiki_pages:
        page = fetch_url(parse_page(wiki_page))

        print(f"{page}: {wiki_page}")

    print(f"Total wiki pages: {len(all_wiki_pages)}")


if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=100) as e:
        e.map(main(), range(200))
