import streamlit as st
from services.ai_chat import chat_with_ai
from utils.helpers import inject_css

st.set_page_config(page_title="AI Companion")
inject_css()
st.title("🤖 AI Companion")

if "messages" not in st.session_state: st.session_state.messages = []
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]): st.markdown(msg["content"])

if prompt := st.chat_input("Ask a question (e.g., 'Explain Surah Al-Asr 2:255')"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)
    with st.chat_message("assistant"):
        with st.spinner("Consulting authenticated sources..."):
            response = chat_with_ai(prompt)
            st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
