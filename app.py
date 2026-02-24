import traceback
import streamlit as st

from backend.run_pipeline import run_pipeline

@st.cache_data(ttl=3600)
def get_articles():
    articles_list = run_pipeline()
    
    return articles_list

def main():
    st.title("What's going on in the world today?")

    st.subheader("Find what international press news top the covers.")
    news_fetcher = st.button(label="Fetch news!")
    st.divider()

    if news_fetcher:        
        try:
            articles = get_articles()
        except Exception as e:
            st.error("No se pudieron cargar las noticias. Comprueba tu conexión y que Ollama esté en marcha.")
            st.code(str(e), language=None)
            with st.expander("Detalles del error (traceback)"):
                st.code(traceback.format_exc(), language="text")
            articles = []
        st.session_state.articles = articles
        
        for article in articles:
            if not isinstance(article, dict):
                raise TypeError("El artículo no contiene el tipo de datos esperado")

            with st.container():
               
                st.subheader(article.get("title", ""))
                st.write(article.get("summary", ""))

                st.caption(f"**Fuente:** {article.get("source", "")}")
                st.caption(f"**URL:** {article.get("link", "")}")
                fecha = article.get("date", None)
                if fecha is not None:

                    st.caption(f"**Fecha:** {fecha.strftime('%d/%m/%Y %H:%M')}")
                st.divider()

if __name__ == "__main__":
    main()