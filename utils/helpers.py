import streamlit as st
from datetime import datetime, timedelta
from config import STYLE_CSS_PATH

def inject_css():
    with open(STYLE_CSS_PATH, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def page_header(title, subtitle, emoji="📖"):
    st.markdown(f"""
    <div class="qsc-header">
        <span class="emoji">{emoji}</span>
        <div>
            <h1 style="margin:0;">{title}</h1>
            <p>{subtitle}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

def compute_streak(dates):
    if not dates: return 0
    unique_dates = sorted(set(datetime.strptime(d, "%Y-%m-%d").date() for d in dates), reverse=True)
    streak = 1
    today = datetime.now().date()
    if unique_dates[0] < today - timedelta(days=1):
        return 0
    for i in range(len(unique_dates) - 1):
        if unique_dates[i] - unique_dates[i+1] == timedelta(days=1):
            streak += 1
        else:
            break
    return streak
