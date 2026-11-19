"""BIOVA Dashboard View
Matches DASHBOARD.png with user greeting, star counter, Hewan and Tumbuhan category cards,
Panorama banner, and bottom navigation.
"""

import streamlit as st
from components.theme import apply_theme
from components.header import render_header
from components.navigation import navigate_to, render_bottom_nav
from components.cards import render_category_card, render_panorama_banner
from services.config import COLOR_PRIMARY, COLOR_SECONDARY


def render_dashboard():
    """Renders the primary Dashboard screen."""
    apply_theme()

    # Route protection
    user = st.session_state.get("authenticated_user")
    if not user:
        navigate_to("login")
        return

    # Top header with user greeting and live star counter
    render_header(show_stars=True)

    # Main Headline
    st.markdown(
        f"""
        <div style="margin-bottom: 18px;">
            <h2 style="font-size: 22px; font-weight: 800; color: {COLOR_PRIMARY}; margin: 0;">
                Yuk, Jelajahi Sekitarmu!
            </h2>
            <p style="font-size: 13px; color: #555555; margin-top: 4px;">
                Pilih kategori untuk mengenali flora dan fauna di kampus UNESA:
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    def on_category_click(cat: str):
        st.session_state["selected_category"] = cat
        navigate_to("scan")

    # Category 1: HEWAN
    render_category_card(
        category_id="hewan",
        title="Hewan",
        icon="🐾",
        description="Kenali berbagai jenis hewan di sekitarmu melalui foto satwa.",
        on_click_callback=on_category_click,
    )

    st.markdown("<div style='height: 6px;'></div>", unsafe_allow_html=True)

    # Category 2: TUMBUHAN
    render_category_card(
        category_id="tumbuhan",
        title="Tumbuhan",
        icon="🌿",
        description="Kenali keanekaragaman tumbuhan di sekitarmu melalui foto daun atau pohon.",
        on_click_callback=on_category_click,
    )

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

    # Panorama Banner
    def on_panorama_click():
        navigate_to("panorama")

    render_panorama_banner(on_click_callback=on_panorama_click)

    # In-app Bottom Navigation
    render_bottom_nav(current_active="dashboard")
