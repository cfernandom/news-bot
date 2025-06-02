from bs4 import BeautifulSoup
from typing import Optional
import requests
from ....src.utils import get_html_with_playwright

SELECTOR = {
    'main_content': 'c-article-body'
}

async def extract_full_text(url: str) -> Optional[str]:
    """
    Extracts the full text from a given URL of the www.nature.com website.
    Args:
        url (str): The URL of the page to extract text from.
    Returns:
        Optional[str]: The extracted full text, or None if extraction fails.
    """
    try:
        # Await the async function call to get the actual HTML content
        html_content = await get_html_with_playwright(url)
        soup = BeautifulSoup(html_content, 'html.parser')

        # Find the main content area
        main_content = soup.find('div', class_=SELECTOR['main_content'])
        if not main_content:
            return None

        # Extract text from the main content area
        full_text = main_content.get_text(separator='\n', strip=True)
        return full_text
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None