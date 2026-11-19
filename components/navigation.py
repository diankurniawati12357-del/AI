"""BIOVA Navigation Component
Manages routing, page switching, bottom navigation bar, and back buttons.
"""

import streamlit as st
from services.config import COLOR_PRIMARY, COLOR_SECONDARY, COLOR_CARD, COLOR_BORDER


def navigate_to(page: str, **kwargs):
    """Sets session state for routing and reruns the Streamlit application."""
    st.session_state["current_page"] = page
    for k, v in kwargs.items():
        st.session_state[k] = v
    st.rerun()


def render_back_button(target_page: str = "dashboard", label: str = "← Kembali"):
    """Renders a friendly back button."""
    col1, _ = st.columns([4, 6])
    with col1:
        if st.button(label, key=f"btn_back_to_{target_page}", use_container_width=False):
            navigate_to(target_page)
    st.markdown("<div style='margin-bottom: 8px;'></div>", unsafe_allow_html=True)


def render_bottom_nav(current_active: str = "dashboard"):
    """Renders the in-app bottom navigation bar."""
    st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        is_active = current_active == "dashboard"
        btn_label = "🏠 Home" if is_active else "🏠"
        if st.button("🏠 Home" if is_active else "🏠", key="nav_dash", use_container_width=True):
            if current_active != "dashboard":
                navigate_to("dashboard")
                
    with col2:
        is_active = current_active in ["learn", "learning", "lesson", "quiz", "quiz_result"]
        if st.button("📚 Belajar" if is_active else "📚", key="nav_learn", use_container_width=True):
            if current_active != "learn":
                navigate_to("learn")
                
    with col3:
        is_active = current_active == "leaderboard"
        if st.button("🏆 Skor" if is_active else "🏆", key="nav_lead", use_container_width=True):
            if current_active != "leaderboard":
                navigate_to("leaderboard")
                
    with col4:
        is_active = current_active == "profile"
        if st.button("👤 Profil" if is_active else "👤", key="nav_prof", use_container_width=True):
            if current_active != "profile":
                navigate_to("profile")
