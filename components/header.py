"""BIOVA Header Component
Displays top user status, avatar, greeting, and star indicator.
"""

import streamlit as st
from services.config import COLOR_PRIMARY, COLOR_SECONDARY, COLOR_CARD, COLOR_BORDER


def render_header(show_stars: bool = True):
    """Renders the top bar containing user greeting and current star counter."""
    user = st.session_state.get("authenticated_user", None)
    username = user["username"] if user else "Petualang"
    stars = user.get("stars", 0) if user else st.session_state.get("user_stars", 0)

    col1, col2 = st.columns([7, 3])
    with col1:
        st.markdown(
            f"""
            <div style="display: flex; align-items: center; gap: 10px;">
                <div style="width: 40px; height: 40px; border-radius: 50%; background-color: {COLOR_PRIMARY}; color: #FFFFFF; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 16px;">
                    {username[0].upper()}
                </div>
                <div>
                    <div style="font-size: 12px; color: #555555; line-height: 1.1;">Selamat Datang Kembali,</div>
                    <div style="font-size: 16px; font-weight: 800; color: {COLOR_PRIMARY};">{username}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col2:
        if show_stars:
            st.markdown(
                f"""
                <div style="display: flex; justify-content: flex-end; align-items: center; height: 100%;">
                    <div style="background-color: {COLOR_CARD}; border: 1.5px solid {COLOR_BORDER}; border-radius: 18px; padding: 4px 12px; display: flex; align-items: center; gap: 5px; font-weight: 800; color: {COLOR_PRIMARY}; font-size: 14px;">
                        <span style="color: #E5A823; font-size: 16px;">⭐</span>
                        <span>{stars}</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
    st.markdown("<div style='margin-bottom: 16px;'></div>", unsafe_allow_html=True)
