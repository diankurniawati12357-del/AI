"""BIOVA Learning Selection View
Matches GAMIFIKASI.png with 'Ayo, Belajar Bersama!', Hewan & Tumbuhan cards, and Mater/Quiz buttons.
"""

import streamlit as st
from components.theme import apply_theme
from components.header import render_header
from components.navigation import navigate_to, render_back_button, render_bottom_nav
from services.game_service import get_chapter_progress
from services.config import COLOR_PRIMARY, COLOR_SECONDARY, COLOR_CARD, COLOR_BORDER, COLOR_HIGHLIGHT


def render_learn():
    """Renders the Learning selection hub."""
    apply_theme()

    user = st.session_state.get("authenticated_user")
    if not user:
        navigate_to("login")
        return

    render_header(show_stars=True)

    # Heading matching screenshot
    st.markdown(
        f"""
        <div style="margin-bottom: 20px;">
            <h2 style="font-size: 22px; font-weight: 800; color: {COLOR_PRIMARY}; margin: 0;">
                Ayo, Belajar Bersama!
            </h2>
            <p style="font-size: 13px; color: #555555; margin-top: 4px;">
                Jelajahi alam, pelajari hal baru, dan kumpulkan bintang!
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Function to start lesson or quiz
    def start_learning(category: str, mode: str):
        st.session_state["learning_category"] = category
        st.session_state["current_chapter"] = 1
        st.session_state["current_card_index"] = 0
        if mode == "materi":
            navigate_to("lesson")
        else:
            # Reset quiz state
            st.session_state["quiz_category"] = category
            st.session_state["quiz_chapter"] = 1
            st.session_state["quiz_q_index"] = 0
            st.session_state["quiz_answers"] = {}
            st.session_state["quiz_checked"] = False
            st.session_state["quiz_score"] = 0
            navigate_to("quiz")

    # CARD 1: HEWAN
    prog_hewan = get_chapter_progress(user["id"], "hewan")
    completed_hewan = sum(1 for p in prog_hewan.values() if p.get("is_completed"))

    st.markdown(
        f"""
        <div class="biova-card">
            <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 8px;">
                <div style="font-size: 26px; width: 44px; height: 44px; border-radius: 12px; background-color: {COLOR_HIGHLIGHT}; display: flex; align-items: center; justify-content: center;">
                    🐾
                </div>
                <div>
                    <h3 style="margin: 0; font-size: 18px; font-weight: 800; color: {COLOR_PRIMARY};">HEWAN</h3>
                    <div style="font-size: 11px; color: #666666;">Progress: {completed_hewan}/3 Bab Terselesaikan</div>
                </div>
            </div>
            <p style="font-size: 13px; color: #444444; margin-bottom: 12px;">
                Pelajari 6 kelompok fauna (Mamalia, Aves, Reptil, Amfibi, Pisces, Invertebrata) dan habitatnya di UNESA.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    col_h1, col_h2 = st.columns(2)
    with col_h1:
        if st.button("📖 Materi Hewan", key="btn_materi_hewan", use_container_width=True):
            start_learning("hewan", "materi")
    with col_h2:
        if st.button("✏️ Kuis Hewan", key="btn_kuis_hewan", type="secondary", use_container_width=True):
            start_learning("hewan", "kuis")

    st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

    # CARD 2: TUMBUHAN
    prog_tumbuhan = get_chapter_progress(user["id"], "tumbuhan")
    completed_tumbuhan = sum(1 for p in prog_tumbuhan.values() if p.get("is_completed"))

    st.markdown(
        f"""
        <div class="biova-card">
            <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 8px;">
                <div style="font-size: 26px; width: 44px; height: 44px; border-radius: 12px; background-color: {COLOR_HIGHLIGHT}; display: flex; align-items: center; justify-content: center;">
                    🌿
                </div>
                <div>
                    <h3 style="margin: 0; font-size: 18px; font-weight: 800; color: {COLOR_PRIMARY};">TUMBUHAN</h3>
                    <div style="font-size: 11px; color: #666666;">Progress: {completed_tumbuhan}/3 Bab Terselesaikan</div>
                </div>
            </div>
            <p style="font-size: 13px; color: #444444; margin-bottom: 12px;">
                Pelajari perbedaan Dikotil dan Monokotil, pohon peneduh kampus, serta fungsi ekologis flora UNESA.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        if st.button("📖 Materi Tumbuhan", key="btn_materi_tumbuhan", use_container_width=True):
            start_learning("tumbuhan", "materi")
    with col_t2:
        if st.button("✏️ Kuis Tumbuhan", key="btn_kuis_tumbuhan", type="secondary", use_container_width=True):
            start_learning("tumbuhan", "kuis")

    render_bottom_nav(current_active="learn")
