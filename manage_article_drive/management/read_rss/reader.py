import feedparser
import ssl
from bs4 import BeautifulSoup

def extract_field(item, field_name):
    html = item[field_name]
    soup = BeautifulSoup(html)
    text_parts = soup.findAll(text=True)
    return ''.join(text_parts)

def read(rss_url):
    res = []
    if hasattr(ssl, '_create_unverified_context'):
        ssl._create_default_https_context = ssl._create_unverified_context
    feed = feedparser.parse(rss_url)
    for item in feed['items']:
        title = extract_field(item, 'title')
        summary = extract_field(item, 'summary')
        link = extract_field(item, 'link')
        res.append((title, summary, link))

    return res


if __name__ == "__main__":
    rss_url = "https://www.google.com/alerts/feeds/08564597941618389321/11787135276340735120"
    res = read(rss_url)
    print(res)

