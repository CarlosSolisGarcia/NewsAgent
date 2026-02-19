import feedparser
from datetime import datetime
from dateutil import parser as date_parser

MAX_PER_FEED = 5

RSS_FEEDS = {
    "3cat": "https://api.3cat.cat/noticies?_format=rss&origen=frontal&frontal=n324-portada-noticia&version=2.0",
    "20minutos": "https://www.20minutos.es/rss",
    "Euronews": "https://www.euronews.com/rss",
    "Xataka": "https://www.xataka.com/feedburner.xml",
    "CGTN World": "https://www.cgtn.com/subscribe/rss/section/world.xml",
    "CGTN Tech&Sci": "https://www.cgtn.com/subscribe/rss/section/tech-sci.xml",
    "Japan Times":"https://www.japantimes.co.jp/feed/",
    "NHK News": "http://www3.nhk.or.jp/rss/news/cat0.xml",
    "AlJazeera": "https://www.aljazeera.com/xml/rss/all.xml",
    "NY Times": "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml",
    "NBC": "https://feeds.nbcnews.com/nbcnews/public/news",
    "France24": "https://www.france24.com/en/europe/rss",
    "The Baltic Times": "https://feeds.feedburner.com/TheBalticTimesNews",
    "Brussels Morning": "https://brusselsmorning.com/feed/"
}

def fetch_news(max_per_feed=MAX_PER_FEED):

    all_news = []

    for source_name, url in RSS_FEEDS.items():
        feed = feedparser.parse(url, request_headers={"User-Agent": "Mozilla/5.0"})

        if not feed.entries:
            print(f"No se pudo leer feed {source_name} ({url})")
            continue

        for entry in feed.entries[:5]: # num noticias máximo por feed
            raw_date = entry.get("published", "")
            try:
                parsed_date = date_parser.parse(raw_date)
            except Exception:
                parsed_date = None
            
            news_item = {
                "title": entry.get("title", ""),
                "link": entry.get("link", ""),
                "date": parsed_date,
                "source": source_name
            }
            all_news.append(news_item)

    return all_news