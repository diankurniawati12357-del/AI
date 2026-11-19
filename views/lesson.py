"""BIOVA Learning Cards View
Matches KARTU MATERI.png with structured educational cards, chapter progression, and card navigation.
"""

import streamlit as st
from components.theme import apply_theme
from components.header import render_header
from components.navigation import navigate_to, render_back_button, render_bottom_nav
from services.materi_service import get_all_chapters, get_chapter_by_id, get_card
from services.game_service import get_chapter_progress
from services.config import COLOR_PRIMARY, COLOR_SECONDARY, COLOR_CARD, COLOR_BORDER, COLOR_HIGHLIGHT


def render_lesson():
    """Renders the educational cards viewer."""
    apply_theme()

    user = st.session_state.get("authenticated_user")
    if not user:
        navigate_to("login")
        return

    render_back_button("learn", "← Kembali ke Menu Belajar")

    category = st.session_state.get("learning_category", "hewan")
    cat_title = "Hewan" if category == "hewan" else "Tumbuhan"

    # Chapter tabs / selector
    chapters = get_all_chapters(category)
    prog = get_chapter_progress(user["id"], category)

    current_ch = st.session_state.get("current_chapter", 1)
    current_idx = st.session_state.get("current_card_index", 0)

    # Chapter selector bar
    col_b1, col_b2, col_b3 = st.columns(3)
    cols = [col_b1, col_b2, col_b3]
    for i, ch in enumerate(chapters, start=1):
        is_unlocked = prog.get(ch["id"], {}).get("is_unlocked", i == 1)
        btn_title = f"Bab {i}" if is_unlocked else f"🔒 Bab {i}"
        with cols[i - 1]:
            is_active = (ch["id"] == current_ch)
            if st.button(
                btn_title,
                key=f"btn_ch_select_{i}",
                type="primary" if is_active else "secondary",
                use_container_width=True,
                disabled=not is_unlocked,
            ):
                st.session_state["current_chapter"] = ch["id"]
                st.session_state["current_card_index"] = 0
                st.rerun()

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

    # Retrieve current chapter and card
    ch_data = get_chapter_by_id(category, current_ch)
    if not ch_data:
        st.error("Data materi tidak ditemukan.")
        return

    cards = ch_data.get("cards", [])
    total_cards = len(cards)
    if total_cards == 0:
        st.info("Materi bab ini sedang disiapkan.")
        return

    card = cards[current_idx]

    # Chapter Title
    st.markdown(
        f"""
        <div style="text-align: center; margin-bottom: 12px;">
            <div style="font-size: 11px; font-weight: 700; color: {COLOR_SECONDARY}; text-transform: uppercase;">
                {cat_title.upper()} • BAB {current_ch}
            </div>
            <h3 style="font-size: 18px; font-weight: 800; color: {COLOR_PRIMARY}; margin: 2px 0 0 0;">
                {ch_data.get('title', '')}
            </h3>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Educational Card matching KARTU MATERI.png
    st.markdown('<div class="biova-card" style="padding: 20px 18px;">', unsafe_allow_html=True)
    st.markdown(
        f"""
        <div style="text-align: center; margin-bottom: 12px;">
            <div style="font-size: 42px; margin-bottom: 6px;">
                {card.get('icon', '🌱')}
            </div>
            <h3 style="font-size: 20px; font-weight: 800; color: {COLOR_PRIMARY}; margin: 0 0 6px 0;">
                {card.get('title', '')}
            </h3>
            <div class="biova-badge">
                {card.get('class_name', '')}
            </div>
        </div>
        <div style="font-size: 13.5px; line-height: 1.6; color: #2E332F; margin-bottom: 14px;">
            {card.get('description', '')}
        </div>
        <div style="background-color: rgba(255, 255, 255, 0.7); border-radius: 12px; padding: 12px; font-size: 12px; color: #333333;">
            <strong>Karakteristik & Ciri:</strong><br>
            {card.get('characteristics', '-')}
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

    # Card Navigation (Previous / Next)
    col_nav1, col_nav2, col_nav3 = st.columns([3, 4, 3])
    with col_nav1:
        if st.button("← Sebelumnya", key="btn_prev_card", disabled=(current_idx == 0), use_container_width=True):
            st.session_state["current_card_index"] = max(0, current_idx - 1)
            st.rerun()

    with col_nav2:
        st.markdown(
            f"""
            <div style="text-align: center; font-size: 13px; font-weight: 700; color: {COLOR_PRIMARY}; padding-top: 8px;">
                {current_idx + 1} dari {total_cards}
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_nav3:
        if st.button("Berikutnya →", key="btn_next_card", disabled=(current_idx >= total_cards - 1), use_container_width=True):
            st.session_state["current_card_index"] = min(total_cards - 1, current_idx + 1)
            st.rerun()

    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

    # Action to jump to Quiz for this chapter
    if st.button(f"✏️ Mulai Kuis Bab {current_ch} →", key="btn_jump_to_quiz", use_container_width=True):
        st.session_state["quiz_category"] = category
        st.session_state["quiz_chapter"] = current_ch
        st.session_state["quiz_q_index"] = 0
        st.session_state["quiz_answers"] = {}
        st.session_state["quiz_checked"] = False
        st.session_state["quiz_score"] = 0
        navigate_to("quiz")

    render_bottom_nav(current_active="learn")
