"""BIOVA Dashboard View
Matches DASHBOARD.png with user greeting, star counter, Hewan and Tumbuhan category cards,
Panorama banner, and bottom navigation.
"""

import streamlit as st
from components.header import render_header
from components.navigation import navigate_to, render_bottom_nav
from components.cards import render_category_card, render_panorama_banner
from services.config import COLOR_PRIMARY
from components.i18n import t


def render_dashboard():
    """Renders the primary Dashboard screen."""
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
        <div class="biova-home-heading">
            <h2 style="color: {COLOR_PRIMARY};">
                {t("welcome.headline")}
            </h2>
            <p>
                {t("welcome.category_prompt")}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    def explore_category(category: str):
        st.session_state["selected_category"] = category
        st.session_state["learning_category"] = category
        navigate_to("learn")

    with st.container(key="biova-home-categories"):
        animal_col, plant_col = st.columns(2, gap="small")
        with animal_col:
            render_category_card(
                category_id="hewan",
                title=t("category.animals"),
                icon="maskot_BIOVA.png",
                description=t("category.animals_description"),
                action_label=t("home.explore_animals"),
                on_explore_callback=explore_category,
            )
        with plant_col:
            render_category_card(
                category_id="tumbuhan",
                title=t("category.plants"),
                icon="tumbuhan",
                description=t("category.plants_description"),
                action_label=t("home.explore_plants"),
                on_explore_callback=explore_category,
            )

    # Panorama Banner
    def on_panorama_click():
        navigate_to("panorama")

    render_panorama_banner(on_click_callback=on_panorama_click)

    # In-app Bottom Navigation
    render_bottom_nav(current_active="dashboard")
