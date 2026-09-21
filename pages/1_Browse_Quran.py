import streamlit as st
from services import quran_api
from config import RECITERS, TRANSLATION_EDITIONS
from utils.helpers import inject_css

st.set_page_config(page_title="Browse Quran", layout="wide")
inject_css()
st.title("📖 Browse Quran")

surahs = quran_api.get_surah_list()
surah_names = [f"{s['number']}. {s['englishName']}" for s in surahs]
selected_surah_name = st.selectbox("Select Surah", surah_names)
surah_number = int(selected_surah_name.split('.')[0])

col1, col2 = st.columns(2)
with col1: reciter = st.selectbox("Select Reciter", list(RECITERS.keys()))
with col2: translation = st.selectbox("Select Translation", list(TRANSLATION_EDITIONS.values()))

reciter_id = RECITERS[reciter]
trans_id = list(TRANSLATION_EDITIONS.keys())[list(TRANSLATION_EDITIONS.values()).index(translation)]
st.markdown("---")

for ayah_num in range(1, 11):
    try:
        arabic = quran_api.get_ayah_text(surah_number, ayah_num, "quran-uthmani")
        eng = quran_api.get_ayah_text(surah_number, ayah_num, trans_id)
        audio_url = quran_api.get_audio_url(surah_number, ayah_num, reciter_id)
        st.markdown(f'''<div class="qsc-card"><div style="display:flex; justify-content:space-between;"><span class="qsc-tag">Ayah {ayah_num}</span><audio controls src="{audio_url}" style="height:30px;"></audio></div><div class="arabic-text" style="font-size:1.8rem; margin:20px 0;">{arabic}</div><p style="color:#b9c9c0;">{eng}</p></div>''', unsafe_allow_html=True)
    except: break
