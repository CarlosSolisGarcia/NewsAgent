import ollama

DEFAULT_MODEL = "llama3"

def summarize_article(title: str, content: str, model: str = DEFAULT_MODEL) -> str:
    prompt = f"""Resume, en español, el siguiente artículo de forma clara y concisa en 2-4 frases.
    Responde solo con el resumen, sin introducciones ni etiquetas.

    Título: {title}
    Contenido: {content}
    """

    try:
        response = ollama.chat(
            model=model,
            messages=[{"role": "user", "content": prompt},]
        )
        return (response.get("message", {}).get("content", "") or "").strip()
    except ollama.ResponseError as e:
        print("Modelo no encontrado.")
        raise
    except Exception as e:
        print("Ollama no está en marcha")
        raise
