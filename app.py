import streamlit as st

from backend.run_pipeline import run_pipeline

@st.cache_data(ttl=3600)
def get_articles():
    return run_pipeline()

def main():
    st.title("What's going on in the world today?")

    st.subheader("Find what international press news top the covers.")
    news_fetcher = st.button(label="Fetch news!")
    st.divider()

    ### Fetching the news:
    if news_fetcher:
        articles = get_articles()
        st.session_state.articles = articles
        
        for article in articles:
            with st.container():
                st.subheader(article["title"])
                st.write(article["summary"])
                st.caption(f"**Fuente:** {article["source"]}")
                fecha = article.get("date")
                st.caption(f"**Fecha:** {fecha.strftime('%d/%m/%Y %H:%M')}")
                st.divider()

if __name__ == "__main__":
    main()