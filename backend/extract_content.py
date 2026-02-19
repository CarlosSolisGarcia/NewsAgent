import trafilatura

def extract_content(url):
    downloaded = trafilatura.fetch_url(url)
    content = trafilatura.extract(downloaded)
    return content