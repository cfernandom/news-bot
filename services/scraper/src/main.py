from services.scraper.src.extractors.www_breastcancer_org import scraper__www_breast_cancer_org
from services.shared.models.article import Article

async def scrape_articles() -> list[Article]:
    articles = await scraper__www_breast_cancer_org()
    return articles