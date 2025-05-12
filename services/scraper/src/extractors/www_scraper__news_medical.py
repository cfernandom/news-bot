from services.shared.models.article import Article
from services.scraper.src.utils import get_html_with_playwright
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import datetime

async def scraper__news_medical() -> list[Article]:
    URL = "https://www.news-medical.net/condition/Breast-Cancer"
    BASE_URL = "https://www.news-medical.net"
    html = await get_html_with_playwright(URL)
    soup = BeautifulSoup(html, "html.parser")
    articles = []
    
    for article in soup.find_all("div", class_="row"):
        
        if not article.find("h3") or "paging" in article.get("class", []):
            continue
            
        # Extraer título
        title_tag = article.find("h3").find("a")
        if not title_tag:
            continue
            
        title = title_tag.get_text(strip=True)
        href = title_tag["href"]
        full_url = urljoin(BASE_URL, href)
        
        # Extraer resumen
        summary_tag = article.find("p", class_="hidden-xs item-desc")
        summary = summary_tag.get_text(strip=True) if summary_tag else ""
        
        # Extraer fecha 
        date_row = article.find_next_sibling("div", class_="row")
        date = None
        if date_row:
            date_span = date_row.find("span", class_="article-meta-date")
            if date_span:
                date_str = date_span.get_text(strip=True)
                try:
                    date = datetime.strptime(date_str, "%d %b %Y")
                except ValueError:
                    print(f"⚠️ Formato de fecha no reconocido: {date_str} en artículo: {title}")
        
        articles.append(Article(
            title=title,
            url=full_url,
            summary=summary,
            date=date,
            content=""
        ))
    
    return articles