import streamlit as st
import feedparser
from gtts import gTTS
import base64

# Configuración básica
st.set_page_config(page_title="TRADING AUDIO-APP", page_icon="📈")

st.title("📈 Trading News AI")
st.caption("Filtrando: BTC, SHIB e Índices Sintéticos")

ACTIVOS = ["bitcoin", "btc", "shiba inu", "shib", "v75", "volatility", "synthetic", "crash", "boom", "deriv"]

# Usamos caché para que la app sea más estable
@st.cache_data(ttl=300)
def get_data():
    feeds = ["https://finance.yahoo.com/news/rss", "https://es.cointelegraph.com/rss"]
    items = []
    for url in feeds:
        try:
            f = feedparser.parse(url)
            for e in f.entries:
                if any(a in e.title.lower() for a in ACTIVOS):
                    items.append({"t": e.title, "l": e.link})
        except:
            continue
    return items

if st.button('ACTUALIZAR MERCADO'):
    noticias = get_data()
    if noticias:
        resumen = "Resumen de noticias. "
        for n in noticias[:10]:
            st.info(f"**{n['t']}**")
            st.write(f"[Abrir link]({n['l']})")
            resumen += n['t'] + ". "
        
        # Generar audio
        try:
            tts = gTTS(text=resumen, lang='es')
            tts.save("a.mp3")
            with open("a.mp3", "rb") as f:
                b64 = base64.b64encode(f.read()).decode()
                st.markdown(f'<audio controls style="width:100%"><source src="data:audio/mp3;base64,{b64}"></audio>', unsafe_allow_html=True)
        except:
            st.error("Error al generar el audio, pero puedes leer las noticias arriba.")
    else:
        st.write("No hay noticias nuevas en este momento.")
