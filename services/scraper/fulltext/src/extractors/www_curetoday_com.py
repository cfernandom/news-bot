from typing import Optional

import requests
from bs4 import BeautifulSoup

SELECTOR = {"main_content": "customPageFullWidthClass"}


async def extract_full_text(url: str) -> Optional[str]:
    """
    Extracts the full text from a given URL of the www.curetoday.com website.
    Args:
        url (str): The URL of the page to extract text from.
    Returns:
        Optional[str]: The extracted full text, or None if extraction fails.
    """
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses

        # Parse the HTML content using BeautifulSoup
        # Await the async function call to get the actual HTML content
        html_content = response.text
        soup = BeautifulSoup(html_content, "html.parser")

        # Find the main content area
        main_content = soup.find("div", class_=SELECTOR["main_content"]).find(
            "div", class_="py-2"
        )
        if not main_content:
            return None

        # Extract text from the main content area
        full_text = main_content.get_text(separator="\n", strip=True)
        return full_text
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None
