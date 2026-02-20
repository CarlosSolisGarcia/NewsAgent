import trafilatura

def extract_content(url):
    """
    Extrae el contenido principal de una página web dada su URL utilizando trafilatura.

    Args:
        url (str): URL de la noticia o página web a procesar.

    Returns:
        str or None: Texto extraído del cuerpo principal del artículo, o None si falla.
    """

    content = None

    try:
        downloaded = trafilatura.fetch_url(url)
        
        if downloaded is not None:
            content = trafilatura.extract(downloaded)

    except Exception as e:
        print(f"No se pudo descargar el contenido de la URL: {url} - Error: {e}")
    
    return content