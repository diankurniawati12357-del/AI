"""BIOVA Quiz Result View
Matches HASIL KUIS (2).png with celebration frog mascot, score breakdown, stars earned,
rank positioning, and real leaderboard display.
"""

import streamlit as st
from components.theme import apply_theme
from components.mascot import render_mascot
from components.navigation import navigate_to, render_bottom_nav
from services.leaderboard_service import get_leaderboard, get_user_rank
from services.config import COLOR_PRIMARY, COLOR_SECONDARY, COLOR_CARD, COLOR_BORDER, COLOR_HIGHLIGHT


def render_quiz_result():
    """Renders the quiz completion celebration screen."""
    apply_theme()

    user = st.session_state.get("authenticated_user")
    if not user:
        navigate_to("login")
        return

    category = st.session_state.get("quiz_category", "hewan")
    chapter_id = st.session_state.get("quiz_chapter", 1)
    score = st.session_state.get("last_quiz_final_score", 0)
    stars_won = st.session_state.get("last_quiz_stars_won", 0)

    # Celebrate Mascot
    render_mascot("celebrate", width=140, center=True)

    # Headlines
    st.markdown(
        f"""
        <div style="text-align: center; margin-bottom: 18px;">
            <h1 style="font-size: 26px; font-weight: 900; color: {COLOR_PRIMARY}; margin-bottom: 4px;">
                KAMU HEBAT!
            </h1>
            <p style="font-size: 14px; color: #555555; margin: 0;">
                Kamu berhasil menyelesaikan kuis Bab {chapter_id}!
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Score Cards Row
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            f"""
            <div class="biova-card" style="text-align: center; padding: 14px;">
                <div style="font-size: 12px; color: #666666;">Jawaban Benar</div>
                <div style="font-size: 26px; font-weight: 900; color: {COLOR_PRIMARY}; margin: 4px 0;">
                    {score} / 5
                </div>
                <div style="font-size: 11px; color: {'#198754' if score >= 3 else '#C0392B'}; font-weight: 700;">
                    {'Lulus & Buka Bab Baru' if score >= 3 else 'Perlu Min. 3 Benar'}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            f"""
            <div class="biova-card" style="text-align: center; padding: 14px;">
                <div style="font-size: 12px; color: #666666;">Bintang Diperoleh</div>
                <div style="font-size: 26px; font-weight: 900; color: #D4AF37; margin: 4px 0;">
                    +{stars_won} ⭐
                </div>
                <div style="font-size: 11px; color: #666666;">
                    {'Bonus Sempurna +3' if score == 5 else 'Terus Tingkatkan!'}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # User Rank Card
    user_rank = get_user_rank(user["id"])
    rank_text = f"Peringkat #{user_rank}" if user_rank else "Belum Masuk Peringkat"
    st.markdown(
        f"""
        <div class="biova-card" style="text-align: center; padding: 12px; margin-top: 6px;">
            <div style="font-size: 13px; color: #555555;">Posisi Peringkatmu Saat Ini:</div>
            <div style="font-size: 20px; font-weight: 900; color: {COLOR_PRIMARY}; margin-top: 2px;">
                🏆 {rank_text}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Mini Leaderboard Preview matching screenshot
    st.markdown(
        f"""
        <div style="margin-top: 14px; margin-bottom: 8px;">
            <div style="font-size: 14px; font-weight: 800; color: {COLOR_PRIMARY};">
                Papan Peringkat Teratas:
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    top_leaders = get_leaderboard(limit=5)
    if top_leaders:
        st.markdown('<div class="biova-card" style="padding: 10px 14px;">', unsafe_allow_html=True)
        for leader in top_leaders:
            is_me = leader["user_id"] == user["id"]
            highlight = "background: #CFDFA6; font-weight: 800;" if is_me else ""
            st.markdown(
                f"""
                <div style="display: flex; justify-content: space-between; align-items: center; padding: 6px 8px; border-radius: 8px; margin-bottom: 2px; {highlight}">
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <span style="font-weight: 800; width: 20px; color: {COLOR_PRIMARY};">#{leader['rank']}</span>
                        <span style="font-size: 13px;">{leader['username']}</span>
                        <span style="font-size: 11px; color: #777777;">({leader['tier']})</span>
                    </div>
                    <div style="font-weight: 800; color: {COLOR_PRIMARY}; font-size: 13px;">
                        {leader['stars']} ⭐
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        st.markdown("</div>", unsafe_allow_html=True)

    # Action buttons
    col_a1, col_a2 = st.columns(2)
    with col_a1:
        if st.button("🏠 Kembali ke Beranda", key="btn_res_home", use_container_width=True):
            navigate_to("dashboard")
    with col_a2:
        if st.button("🔄 Ulangi Kuis", key="btn_res_repeat", type="secondary", use_container_width=True):
            st.session_state["quiz_q_index"] = 0
            st.session_state["quiz_answers"] = {}
            st.session_state["quiz_checked"] = False
            st.session_state["quiz_score"] = 0
            navigate_to("quiz")

    render_bottom_nav(current_active="learn")
