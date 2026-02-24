from .summarize import summarize_article
from .fetch_news import fetch_news
from .extract_content import extract_content

def run_pipeline():
    # CONTROL DE ERRORES: fetch_news() puede fallar (red, feedparser, etc.) o devolver algo
    # que no sea lista en una versión futura. Valida que news_list sea una lista antes de iterar.
    
    news_list = []

    try:
        news_list = fetch_news()

    except Exception as e:
        print(f"No se pudo obtener la lista de noticias: {e}")
        
    if news_list:

        for article in news_list:
            # CONTROL DE ERRORES: KeyError si article no tiene "link" (estructura de feed inesperada).
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