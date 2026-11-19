"""BIOVA Welcome View
Matches the Welcome/Home screenshot with warm grey background, dark green circles, and bottom frog mascot.
"""

import streamlit as st
from components.theme import apply_theme
from components.mascot import render_mascot
from components.navigation import navigate_to
from services.config import COLOR_PRIMARY, COLOR_SECONDARY, COLOR_CARD, COLOR_TEXT


def render_welcome():
    """Renders the landing Welcome screen."""
    apply_theme()

    # If already logged in, redirect to dashboard
    if st.session_state.get("authenticated_user"):
        navigate_to("dashboard")
        return

    # Top decorative circles matching screenshot
    st.markdown(
        """
        <div class="welcome-decor-container">
            <div class="circle-large"></div>
            <div class="circle-medium"></div>
            <div class="circle-small"></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Main headlines
    st.markdown(
        f"""
        <div style="text-align: center; margin-top: 10px; margin-bottom: 24px;">
            <h1 style="font-size: 26px; font-weight: 900; color: {COLOR_PRIMARY}; margin-bottom: 4px; line-height: 1.2;">
                Jelajahi sekitarmu!
            </h1>
            <h2 style="font-size: 20px; font-weight: 800; color: {COLOR_SECONDARY}; margin-top: 0; margin-bottom: 12px;">
                Temukan, kenali, & pelajari.
            </h2>
            <p style="font-size: 14px; color: #555555; margin: 0;">
                Selamat datang di <strong>BIOVA</strong>!
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Action Buttons
    col1, col2, col3 = st.columns([1, 8, 1])
    with col2:
        if st.button("Masuk", key="btn_welcome_login", use_container_width=True):
            navigate_to("login")

        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

        # Daftar uses secondary outline styling
        if st.button("Daftar", key="btn_welcome_register", use_container_width=True, type="secondary"):
            navigate_to("register")

    # Bottom Mascot Illustration matching reference screenshot
    st.markdown("<div style='margin-top: 25px;'></div>", unsafe_allow_html=True)
    render_mascot("welcome", width=340, center=True)
