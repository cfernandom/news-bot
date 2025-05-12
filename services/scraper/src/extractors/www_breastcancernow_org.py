from services.shared.models.article import Article
from services.scraper.src.utils import get_html_with_playwright
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import datetime
from typing import Optional

async def scraper__breast_cancer_now_org() -> list[Article]:
    URL = "https://breastcancernow.org/about-us/research-news"
    BASE_URL = "https://breastcancernow.org"
    html = await get_html_with_playwright(URL)
    soup = BeautifulSoup(html, "html.parser")
    articles = []
    
    # Buscar todos los artículos principales
    for article in soup.find_all("article", class_="m-pm-card"):
        link = article.find("a", class_="m-pm-card__inner")
        if not link:
            continue
            
        href = link.get("href")
        full_url = urljoin(BASE_URL, href)
        
        title_tag = link.find("h5", class_="m-pm-card__title")
        title = title_tag.get_text(strip=True) if title_tag else ""
        
        summary_tag = link.find("p", class_="m-pm-card__text")
        summary = summary_tag.get_text(strip=True) if summary_tag else ""
        
        date_tag = link.find("p", class_="m-pm-card__date")
        date_str = date_tag.get_text(strip=True) if date_tag else ""
        date = None
        
        if date_str:
            try:
                date = datetime.strptime(date_str, "%d %b %Y")
            except ValueError:
                pass
        
        articles.append(Article(
            title=title,
            url=full_url,
            summary=summary,
            date=date,
            content=""
        ))
    
    return articles