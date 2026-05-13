import streamlit as st
import feedparser
from gtts import gTTS
import base64

st.set_page_config(page_title="TRADING AUDIO-APP", page_icon="📉")

st.markdown("""
<style>
    .main { background-color: #0e1117; color: white; }
    .stButton>button { background-color: #ff4b4b; color: white; width: 100%; border-radius: 20px; font-weight: bold; }
    .news-card { background-color: #161b22; padding: 15px; border-radius: 10px; border-left: 5px solid #ff4b4b; margin-bottom: 10px; }
</style>
""", unsafe_allow_html=True)

st.title("📈 Trading News AI")
st.caption("Filtrando: BTC, SHIB e Índices Sintéticos")

ACTIVOS = ["bitcoin", "btc", "shiba inu", "shib", "v75", "volatility", "synthetic", "crash", "boom", "deriv"]

def get_data():
    feeds = ["https://finance.yahoo.com/news/rss", "https://es.cointelegraph.com/rss"]
    items = []
    for url in feeds:
        f = feedparser.parse(url)
        for e in f.entries:
            if any(a in e.title.lower() for a in ACTIVOS):
                items.append({"t": e.title, "l": e.link})
    return items

if st.button('ACTUALIZAR MERCADO'):
    noticias = get_data()
    if noticias:
        resumen = "Resumen de noticias. "
        for n in noticias[:10]:
            st.markdown(f'<div class="news-card"><b>{n["t"]}</b><br><a href="{n["l"]}">Link</a></div>', unsafe_allow_html=True)
            resumen += n["t"] + ". "
        
        tts = gTTS(text=resumen, lang='es')
        tts.save("a.mp3")
        with open("a.mp3", "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
            st.markdown(f'<audio autoplay controls style="width:100%"><source src="data:audio/mp3;base64,{b64}"></audio>', unsafe_allow_html=True)
    else:
        st.write("No hay noticias nuevas.")
