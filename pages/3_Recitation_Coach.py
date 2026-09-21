import streamlit as st
import tempfile
import os
from services.recitation_coach import transcribe_audio, compare_recitation
from utils.helpers import inject_css

st.set_page_config(page_title="Recitation Coach")
inject_css()
st.title("🎙️ Recitation Coach")

target_text = st.text_area("Paste the Arabic text you want to practice:", "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ")
audio_file = st.audio_input("Record your recitation")

if audio_file:
    with st.spinner("Transcribing and analyzing..."):
        # Save the uploaded audio to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
            tmp_file.write(audio_file.read())
            tmp_path = tmp_file.name
        
        try:
            transcribed = transcribe_audio(tmp_path)
            feedback = compare_recitation(target_text, transcribed)
            
            html_feedback = ""
            for word, status in feedback:
                css_class = f"qsc-word qsc-word-{status}"
                html_feedback += f'<span class="{css_class}">{word}</span> '
            
            st.markdown(f'<div class="qsc-card" style="text-align:center; direction:rtl;">{html_feedback}</div>', unsafe_allow_html=True)
            st.info("🟢 Green = Correct | 🔴 Red = Mispronounced | 🟡 Gold = Missing")
            
            if "Could not understand" in transcribed:
                st.warning("🔊 The AI couldn't catch that clearly. Try speaking louder or closer to the mic.")
            elif "API error" in transcribed:
                st.error("🌐 Network error. Please check your internet connection.")
        finally:
            # Clean up temp file
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
