from services.scraper.src.extractors.www_breastcancer_org import scraper__www_breast_cancer_org
from services.scraper.src.extractors.www_breastcancernow_org import scraper__breast_cancer_now_org
from services.scraper.src.extractors.www_breastcancernews_features import scraper__webmd_breast_cancer
from services.scraper.src.extractors.www_scraper_sciencedaily import scraper__sciencedaily
from services.scraper.src.extractors.www_scraper__news_medical import scraper__news_medical
from services.shared.models.article import Article


async def scrape_articles() -> list[Article]:
    articles = []
    article1 = await scraper__www_breast_cancer_org()
    article2 = await scraper__breast_cancer_now_org()
    article3 = await scraper__webmd_breast_cancer()
    article5 = await scraper__sciencedaily()
    article6 = await scraper__news_medical()
    articles.extend(article1 + article2 + article3 + article5 + article6)
    return articles
