"""BIOVA Learning Selection View
Matches GAMIFIKASI.png with 'Ayo, Belajar Bersama!', Hewan & Tumbuhan cards, and Mater/Quiz buttons.
"""

import streamlit as st
from components.header import render_header
from components.navigation import navigate_to, render_back_button, render_bottom_nav
from components.cards import render_learning_category_card
from services.quiz_service import initialize_quiz_session
from components.i18n import t


def render_learn():
    """Renders the Learning selection hub."""
    user = st.session_state.get("authenticated_user")
    if not user:
        navigate_to("login")
        return

    render_header(show_stars=True)
    render_back_button(
        "dashboard",
        compact=True,
        key="btn_back_learn_home",
    )

    st.markdown(
        f"""
        <div class="biova-page-heading">
            <h2>{t("learn.title")}</h2>
            <p>{t("learn.subtitle")}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    selected_category = st.session_state.get(
        "selected_category",
        st.session_state.get("learning_category", "hewan"),
    )
    selected_title = t("category.plants") if selected_category == "tumbuhan" else t("category.animals")
    st.markdown(
        f'<div class="biova-selection-pill">'
        f'{t("learn.selected_category").format(category=selected_title)}</div>',
        unsafe_allow_html=True,
    )

    # Function to start lesson or quiz
    def start_learning(category: str, mode: str):
        if mode == "materi":
            st.session_state["learning_category"] = category
            st.session_state["selected_category"] = category
            st.session_state["current_card_index"] = 0
            st.session_state["lesson_detail_mode"] = False
            navigate_to("lesson")
        elif mode == "kuis":
            initialize_quiz_session(category, st.session_state)
            navigate_to("quiz")
        else:
            st.session_state["selected_category"] = category
            navigate_to("scan")

    with st.container(key="biova-learning-categories"):
        animal_column, plant_column = st.columns(2, gap="small")
        with animal_column:
            render_learning_category_card(
                category_id="hewan",
                title=t("category.animals"),
                icon="maskot_BIOVA.png",
                description=t("learn.animal_description"),
                actions=(
                    ("ensiklopedia", t("learn.animal_material"), "btn_materi_hewan", lambda: start_learning("hewan", "materi")),
                    ("cek", t("learn.animal_quiz"), "btn_kuis_hewan", lambda: start_learning("hewan", "kuis")),
                    ("riset", t("scan.identify"), "btn_identify_hewan", lambda: start_learning("hewan", "identify")),
                ),
            )
        with plant_column:
            render_learning_category_card(
                category_id="tumbuhan",
                title=t("category.plants"),
                icon="tumbuhan",
                description=t("learn.plant_description"),
                actions=(
                    ("ensiklopedia", t("learn.plant_material"), "btn_materi_tumbuhan", lambda: start_learning("tumbuhan", "materi")),
                    ("cek", t("learn.plant_quiz"), "btn_kuis_tumbuhan", lambda: start_learning("tumbuhan", "kuis")),
                    ("riset", t("scan.identify"), "btn_identify_tumbuhan", lambda: start_learning("tumbuhan", "identify")),
                ),
            )

    render_bottom_nav(current_active="learn")
