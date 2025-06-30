from typing import Optional
from urllib.parse import urlparse

import requests

from .registry import get_extractor_for_domain


async def scrape_full_text(url: str) -> Optional[str]:
    """
    Dado un URL, selecciona el extractor específico según el dominio
    y devuelve el texto completo en plano. Si el extractor falla o
    no existe, cae en el método genérico.
    """
    try:
        # headers = {"User-Agent": "NewsBot/1.0 (+https://preventia-wp.cfernandom.dev)"}
        # resp = requests.get(url, headers=headers, timeout=10)
        # if resp.status_code != 200:
        #     return None

        domain = urlparse(url).netloc.lower()
        extractor_fn = get_extractor_for_domain(domain)

        if extractor_fn:
            full_text = await extractor_fn(url)
            if full_text:
                return full_text
        # Si no hay extractor específico o falla, retorna None
        return None
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None
