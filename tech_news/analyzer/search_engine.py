from tech_news.database import search_news
from datetime import datetime


# Requisito 6
def search_by_title(title):
    query = {"title": {"$regex": title, "$options": "i"}}
    news = search_news(query)
    news_filtered = []
    for new in news:
        news_filtered.append((new["title"], new["url"]))
    return news_filtered


# Requisito 7
def search_by_date(date):
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Data inválida")
    else:
        date_format = datetime.strptime(date, "%Y-%m-%d").strftime("%d/%m/%Y")
        query = {"timestamp": date_format}
        news = search_news(query)
    news_filtered = []
    for new in news:
        news_filtered.append((new["title"], new["url"]))
    return news_filtered


# Requisito 8
def search_by_tag(tag):
    """Seu código deve vir aqui"""


# Requisito 9
def search_by_category(category):
    """Seu código deve vir aqui"""
