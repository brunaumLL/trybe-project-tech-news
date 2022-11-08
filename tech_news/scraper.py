import requests
import time
import parsel


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
    """Seu código deve vir aqui"""


# Requisito 5
def get_tech_news(amount):
    """Seu código deve vir aqui"""
