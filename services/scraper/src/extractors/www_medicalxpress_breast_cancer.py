from services.shared.models.article import Article
from services.scraper.src.utils import get_html_with_playwright
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import datetime, timezone
from typing import Optional
import re

async def scraper__medicalxpress_com_breast_cancer() -> list[Article]:
    URL = "https://medicalxpress.com/conditions/breast-cancer/"
    BASE_URL = "https://medicalxpress.com"
    html = await get_html_with_playwright(URL)
    soup = BeautifulSoup(html, "html.parser")
    articles = []

    # Encuentra todos los artículos con la clase específica
    article_elements = soup.find_all("article", class_="sorted-article d-flex")
    

    for i, article_elem in enumerate(article_elements):
        try:
            print(f"\n--- Procesando artículo {i+1} ---")
            
            # Extraer el título del h2 > a
            title_h2 = article_elem.find("h2", class_="mb-2")
            title = ""
            href = ""
            
            if title_h2:
                title_a = title_h2.find("a", class_="news-link")
                if title_a:
                    title = title_a.get_text(strip=True)
                    href = title_a["href"]
                    print(f"Título encontrado: '{title}'")
                    print(f"URL: {href}")
                else:
                    print("No se encontró enlace en el h2")
                    continue
            else:
                print("No se encontró h2 con título")
                continue
            
            if not title or not href:
                print("Título o URL vacíos, saltando artículo")
                continue

            # La URL ya viene completa, no necesita urljoin
            full_url = href if href.startswith("http") else urljoin(BASE_URL, href)

            # Extraer el resumen del párrafo
            summary = ""
            summary_p = article_elem.find("p", class_="mb-4")
            if summary_p:
                summary = summary_p.get_text(strip=True)
                print(f"Resumen encontrado: '{summary[:100]}...'")
            else:
                # Buscar cualquier párrafo que no sea de metadatos
                all_p = article_elem.find_all("p")
                for p in all_p:
                    text = p.get_text(strip=True)
                    # Evitar párrafos de metadatos (fechas, comentarios, etc.)
                    if (text and len(text) > 30 and 
                        not any(word in text.lower() for word in ["may", "april", "march", "comments", "shares"]) and
                        not re.match(r'^[A-Z][a-z]+ \d{1,2}, \d{4}', text)):
                        summary = text
                        print(f"Resumen alternativo encontrado: '{summary[:100]}...'")
                        break

            # Extraer la fecha - buscar en el div de información del artículo
            date = None
            info_div = article_elem.find("div", class_="article__info mt-auto")
            
            if info_div:
                # Buscar el párrafo con la fecha
                date_p = info_div.find("p", class_="text-uppercase text-low")
                if date_p:
                    date_str = date_p.get_text(strip=True)
                    print(f"Fecha encontrada: '{date_str}'")
                    date = parse_date(date_str)
                else:
                    print("No se encontró párrafo con fecha en article__info")
            
            # Si no encontramos fecha en el lugar esperado, buscar en todo el artículo
            if not date:
                all_text = article_elem.get_text()
                date_patterns = [
                    r'(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}',
                    r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2},?\s+\d{4}',
                    r'\d{1,2}[/-]\d{1,2}[/-]\d{4}',
                    r'\d{4}[/-]\d{1,2}[/-]\d{1,2}'
                ]
                
                for pattern in date_patterns:
                    match = re.search(pattern, all_text)
                    if match:
                        date_str = match.group(0)
                        print(f"Fecha encontrada con regex: '{date_str}'")
                        date = parse_date(date_str)
                        if date:
                            break

            # Extraer el tópico/categoría
            topic = ""
            topic_div = article_elem.find("div", class_="sorted-article-topic mb-2")
            if topic_div:
                topic = topic_div.get_text(strip=True)
                print(f"Tópico encontrado: '{topic}'")

            # Crear el objeto Article
            article = Article(
                title=title,
                url=full_url,
                summary=summary,
                published_at=date,
                content=""
            )

            print(f"✓ Artículo extraído exitosamente:")
            print(f"  Título: {article.title}")
            print(f"  URL: {article.url}")
            print(f"  Tópico: {topic}")
            print(f"  Resumen: {article.summary[:100]}..." if len(article.summary) > 100 else f"  Resumen: {article.summary}")
            print(f"  Fecha: {article.published_at}")

            articles.append(article)
            
        except Exception as e:
            print(f"Error al procesar artículo {i+1}: {e}")
            import traceback
            traceback.print_exc()
            continue

    return articles


def parse_date(date_str: str) -> Optional[datetime]:
    """Parsea una fecha con múltiples formatos posibles"""
    if not date_str:
        return None
        
    # Limpiar la cadena de fecha
    clean_date_str = re.sub(r'(\d+)(st|nd|rd|th)', r'\1', date_str.strip())
    
    # Formatos de fecha a intentar
    date_formats = [
        "%B %d, %Y",         # May 22, 2025
        "%B %d %Y",          # May 22 2025
        "%b %d, %Y",         # May 22, 2025
        "%b %d %Y",          # May 22 2025
        "%m/%d/%Y",          # 05/22/2025
        "%d/%m/%Y",          # 22/05/2025
        "%Y-%m-%d",          # 2025-05-22
        "%d-%m-%Y",          # 22-05-2025
        "%m-%d-%Y",          # 05-22-2025
    ]
    
    for fmt in date_formats:
        try:
            parsed_date = datetime.strptime(clean_date_str, fmt).replace(tzinfo=timezone.utc)
            print(f"Fecha parseada exitosamente con formato '{fmt}': {parsed_date}")
            return parsed_date
        except ValueError:
            continue
    
    # Intentar extraer solo números si los formatos anteriores fallan
    numbers = re.findall(r'\d+', clean_date_str)
    if len(numbers) >= 3:
        try:
            # Para dates como "May 22, 2025" ya procesadas
            # Asumir formato MM/DD/YYYY o DD/MM/YYYY basado en el tamaño del primer número
            if int(numbers[0]) > 12:  # Probablemente DD/MM/YYYY
                day, month, year = int(numbers[0]), int(numbers[1]), int(numbers[2])
            else:  # Probablemente MM/DD/YYYY
                month, day, year = int(numbers[0]), int(numbers[1]), int(numbers[2])
            
            if year < 100:  # Año de 2 dígitos
                year += 2000
                
            parsed_date = datetime(year, month, day, tzinfo=timezone.utc)
            print(f"Fecha parseada con extracción numérica: {parsed_date}")
            return parsed_date
        except (ValueError, IndexError):
            pass
    
    print(f"No se pudo parsear la fecha: '{date_str}'")
    return None