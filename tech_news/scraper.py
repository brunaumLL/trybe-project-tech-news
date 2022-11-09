import requests
import time
import parsel
from tech_news.database import create_news


# Requisito 1
def fetch(url):
    time.sleep(1)
    try:
        response = requests.get(
            url, headers={"user-agent": "Fake user-agent"}, timeout=3.0
        )
        response.raise_for_status()
    except (requests.HTTPError, requests.Timeout):
        return None
    else:
        return response.text


# Requisito 2
def scrape_novidades(html_content):
    selector = parsel.Selector(html_content)
    novidades = []

    for novidade in selector.css("div.entry-thumbnail"):
        url = novidade.css("a.cs-overlay-link::attr(href)").get()
        novidades.append(url)
    return novidades


# Requisito 3
def scrape_next_page_link(html_content):
    try:
        selector = parsel.Selector(html_content)
        next_page = selector.css("div.nav-links a.next::attr(href)").get()
        return next_page
    except not next_page:
        return None


# Requisito 4
def scrape_noticia(html_content):
    selector = parsel.Selector(html_content)
    url = selector.css("link[rel=canonical]").attrib["href"]
    title = selector.css("h1.entry-title::text").get()
    timestamp = selector.css("li.meta-date::text").get()
    writer = selector.css("span.author a.url::text").get()
    comments_text = selector.css("h5.title-blocl::text").get()
    if not comments_text:
        comments_count = 0
    else:
        comments_count = comments_text.split(' ')[0]
    summary = selector.css(
        "div.entry-content > p:first-of-type *::text").getall()
    summary = "".join(summary).strip()
    tags = selector.css(".post-tags a::text").getall()
    category = selector.css("span.label::text").get()

    noticia = {
        "url": url,
        "title": title.rstrip(),
        "timestamp": timestamp,
        "writer": writer,
        "comments_count": comments_count,
        "summary": summary,
        "tags": tags,
        "category": category,
        }
    return noticia


# Requisito 5
def get_tech_news(amount):
    URL_BASE = "https://blog.betrybe.com/"
    list_news = []
    count_news = 0

    while count_news < amount:
        response = fetch(URL_BASE)
        news = scrape_novidades(response)

        for new in news:
            if count_news == amount:
                break
            count_news += 1
            response_new = fetch(new)
            scrape_new = scrape_noticia(response_new)
            list_news.append(scrape_new)

        URL_BASE = scrape_next_page_link(response)

    create_news(list_news)
    return list_news
