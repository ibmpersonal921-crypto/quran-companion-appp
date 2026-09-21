import streamlit as st
from services.recitation_coach import transcribe_audio, compare_recitation
from utils.helpers import inject_css

st.set_page_config(page_title="Recitation Coach")
inject_css()
st.title("🎙️ Recitation Coach")

target_text = st.text_area("Paste the Arabic text you want to practice:", "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ")
audio_file = st.audio_input("Record your recitation")

if audio_file:
    with st.spinner("Transcribing and analyzing..."):
        transcribed = transcribe_audio(audio_file)
        feedback = compare_recitation(target_text, transcribed)
        html_feedback = ""
        for word, status in feedback:
            css_class = f"qsc-word qsc-word-{status}"
            html_feedback += f'<span class="{css_class}">{word}</span> '
        st.markdown(f'<div class="qsc-card" style="text-align:center; direction:rtl;">{html_feedback}</div>', unsafe_allow_html=True)
        st.info("Green = Correct, Red = Mispronounced, Gold = Missing")
