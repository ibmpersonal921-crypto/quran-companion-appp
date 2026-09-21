import streamlit as st, os
from utils.helpers import inject_css
from config import DB_PATH

st.set_page_config(page_title="Settings")
inject_css()
st.title("⚙️ Settings")
if st.button("Clear Local Database"):
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        st.success("Database cleared! Refresh the page.")
