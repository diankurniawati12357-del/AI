"""BIOVA User Profile View
Displays account information, tier progression, collected stars, and logout controls.
"""

import streamlit as st
from components.theme import apply_theme
from components.header import render_header
from components.navigation import navigate_to, render_back_button, render_bottom_nav
from services.game_service import get_user_stats
from services.config import COLOR_PRIMARY, COLOR_SECONDARY, COLOR_CARD, COLOR_BORDER, COLOR_HIGHLIGHT, COLOR_ERROR


def render_profile():
    """Renders the User Profile screen."""
    apply_theme()

    user = st.session_state.get("authenticated_user")
    if not user:
        navigate_to("login")
        return

    render_header(show_stars=True)

    stats = get_user_stats(user["id"])

    st.markdown(
        f"""
        <div style="text-align: center; margin-bottom: 18px;">
            <div style="width: 72px; height: 72px; border-radius: 50%; background-color: {COLOR_PRIMARY}; color: #FFFFFF; display: flex; align-items: center; justify-content: center; font-weight: 900; font-size: 28px; margin: 0 auto 10px auto; border: 3px solid {COLOR_HIGHLIGHT};">
                {user['username'][0].upper()}
            </div>
            <h2 style="font-size: 22px; font-weight: 800; color: {COLOR_PRIMARY}; margin: 0;">
                {user['username']}
            </h2>
            <div style="font-size: 13px; color: #666666; margin-top: 2px;">
                {user['email']}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Tier and Stars Banner
    st.markdown(
        f"""
        <div class="biova-card" style="text-align: center; padding: 18px 16px;">
            <div style="font-size: 13px; color: #666666; text-transform: uppercase; font-weight: 700; letter-spacing: 0.5px;">
                Tingkat Petualang
            </div>
            <div style="font-size: 24px; font-weight: 900; color: {stats['tier_color']}; margin: 4px 0 6px 0;">
                {stats['tier_icon']} {stats['tier']}
            </div>
            <div style="font-size: 18px; font-weight: 800; color: #D4AF37;">
                {stats['stars']} ⭐ Total Bintang
            </div>
            {f"<div style='font-size: 11px; color: #777777; margin-top: 6px;'>Kumpulkan {stats['stars_needed']} bintang lagi untuk naik tier!</div>" if stats['stars_needed'] > 0 else "<div style='font-size: 11px; color: #198754; margin-top: 6px; font-weight: 700;'>Kamu sudah mencapai tier tertinggi!</div>"}
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Activity Statistics Card
    st.markdown(
        f"""
        <div class="biova-card">
            <div style="font-weight: 800; font-size: 14px; color: {COLOR_PRIMARY}; margin-bottom: 10px;">
                Aktivitas Eksplorasi
            </div>
            <div style="display: flex; justify-content: space-between; padding: 6px 0; border-bottom: 1px solid rgba(0,0,0,0.05); font-size: 13px;">
                <span>📸 Foto Berhasil Terverifikasi:</span>
                <strong>{stats['upload_count']} foto</strong>
            </div>
            <div style="display: flex; justify-content: space-between; padding: 6px 0; font-size: 13px;">
                <span>✏️ Kuis Dikerjakan:</span>
                <strong>{stats['quiz_count']} kali</strong>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

    # Logout Button
    if st.button("🚪 Keluar dari Akun (Logout)", key="btn_logout", type="secondary", use_container_width=True):
        st.session_state.clear()
        navigate_to("welcome")

    render_bottom_nav(current_active="profile")
