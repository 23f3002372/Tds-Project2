from langchain_core.tools import tool
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

@tool
def get_rendered_html(url: str) -> str:
    print("\nFetching and rendering:", url)
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            # Load the page (let JS execute)
            page.goto(url, wait_until="networkidle")

            # Extract rendered HTML
            content = page.content()

            browser.close()
            return content

    except Exception as e:
        return f"Error fetching/rendering page: {str(e)}"