from .summarize import summarize_article
from .fetch_news import fetch_news
from .extract_content import extract_content

def run_pipeline():
    news_list = fetch_news()

    for article in news_list:
        url = article["link"]
        article["content"] = extract_content(url)
        if article["content"]:
            article["summary"] = summarize_article(
                title=article["title"],
                content=article["content"]
            )
        else:
            article["summary"] = ""

    return news_list