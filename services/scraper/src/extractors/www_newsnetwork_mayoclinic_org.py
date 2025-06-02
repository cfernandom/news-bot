from services.shared.models.article import Article
from services.scraper.src.utils import get_html_with_playwright
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import datetime

async def scraper__mayoclinic() -> list[Article]:
    URL = "https://newsnetwork.mayoclinic.org/search/?search=breast"
    BASE_URL = "https://newsnetwork.mayoclinic.org"
    html = await get_html_with_playwright(URL)
    if not html:
        print(f"Failed to retrieve content from {URL}")
        return None
    soup = BeautifulSoup(html, "html.parser")
    articles = []
    
    # Buscar todas las noticias
    for result in soup.find_all("div", class_="ch-analytics-search-result"):
        # Extraer título
        title_tag = result.find("a", class_="ch-search-result-title")
        if not title_tag:
            continue
            
        title = title_tag.get_text(strip=True)
        href = title_tag["href"]
        full_url = urljoin(BASE_URL, href)
        
        # Extraer resumen
        excerpt = result.find("div", class_="ch-search-excerpt")
        summary = excerpt.get_text(strip=True) if excerpt else ""
        
        # Extraer fecha
        date_div = result.find("div", class_="ch-search-result-secondary-text", string=lambda t: "Last Updated:" in t)
        date = None
        
        if date_div:
            date_str = date_div.get_text().replace("Last Updated:", "").strip()
            try:
                date = datetime.strptime(date_str, "%B %d, %Y")
            except ValueError:
                print(f"⚠️ Formato de fecha no reconocido: {date_str} en artículo: {title}")
        
        article_obj = Article(
            title=title,
            url=full_url,
            summary=summary,
            published_at=date,
            content=""
        )
        setattr(article_obj, "article_url", full_url)  

        articles.append(article_obj)

    
    return articles