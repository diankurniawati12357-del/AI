"""BIOVA quiz completion screen with score, rewards, and leaderboard preview."""

import html

import streamlit as st

from components.header import render_header
from components.i18n import t
from components.icons import render_icon
from components.navigation import navigate_to, render_bottom_nav
from components.theme import apply_theme
from services.config import COLOR_PRIMARY
from services.leaderboard_service import get_leaderboard, get_user_rank
from services.quiz_service import initialize_quiz_session


def render_quiz_result():
    apply_theme()

    user = st.session_state.get("authenticated_user")
    if not user:
        navigate_to("login")
        return
    render_header(show_stars=True)

    category = st.session_state.get("quiz_category", "hewan")
    category_title = t("category.animals") if category == "hewan" else t("category.plants")
    score = int(st.session_state.get("last_quiz_final_score", 0))
    total_questions = int(st.session_state.get("last_quiz_total_questions", 5))
    stars_won = int(st.session_state.get("last_quiz_stars_won", 0))
    final_score = round(score * 100 / total_questions) if total_questions else 0

    st.markdown(
        f'<div style="text-align:center;margin:8px 0 12px;">'
        f'{render_icon("bintang", 64, "biova-icon--heading", t("quiz.completed").format(category=category_title))}</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f"""
        <div style="text-align:center;margin-bottom:18px;">
            <h1 style="font-size:26px;font-weight:900;color:{COLOR_PRIMARY};margin-bottom:4px;">
                {t("quiz.great")}
            </h1>
            <p style="font-size:14px;color:#555555;margin:0;">
                {t("quiz.completed").format(category=category_title)}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            f"""
            <div class="biova-card" style="text-align:center;padding:14px;">
                <div style="font-size:12px;color:#666666;">{t("quiz.correct_answers")}</div>
                <div style="font-size:26px;font-weight:900;color:{COLOR_PRIMARY};margin:4px 0;">
                    {score} / {total_questions}
                </div>
                <div style="font-size:12px;color:#666666;font-weight:700;">
                    {t("quiz.final_score")}: {final_score} / 100
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            f"""
            <div class="biova-card" style="text-align:center;padding:14px;">
                <div style="font-size:12px;color:#666666;">{t("quiz.stars_won")}</div>
                <div style="font-size:26px;font-weight:900;color:#D4AF37;margin:4px 0;">
                    {render_icon("bintang", 28, "biova-icon--reward", t("common.total_stars"))}
                    +{stars_won}
                </div>
                <div style="font-size:11px;color:#666666;">
                    {t("quiz.perfect_bonus") if score == total_questions else t("quiz.keep_improving")}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    user_rank = get_user_rank(user["id"])
    rank_text = f"{t('leaderboard.title')} #{user_rank}" if user_rank else t("leaderboard.empty")
    st.markdown(
        f"""
        <div class="biova-card" style="text-align:center;padding:12px;margin-top:6px;">
            <div style="font-size:13px;color:#555555;">{t("quiz.current_rank")}</div>
            <div style="font-size:20px;font-weight:900;color:{COLOR_PRIMARY};margin-top:2px;">
                {render_icon("piala", 28, "biova-icon--reward", t("leaderboard.title"))}
                {html.escape(rank_text)}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f'<div style="margin-top:14px;margin-bottom:8px;">'
        f'<div style="font-size:14px;font-weight:800;color:{COLOR_PRIMARY};">{t("quiz.top_leaderboard")}</div></div>',
        unsafe_allow_html=True,
    )
    top_leaders = get_leaderboard(limit=5)
    if top_leaders:
        st.markdown('<div class="biova-card" style="padding:10px 14px;">', unsafe_allow_html=True)
        for leader in top_leaders:
            is_me = leader["user_id"] == user["id"]
            highlight = "background:#CFDFA6;font-weight:800;" if is_me else ""
            medal = {
                1: "medali_gold",
                2: "medali_silver",
                3: "medali_bronze",
            }.get(leader["rank"])
            rank_mark = (
                render_icon(medal, 24, "biova-icon--reward", f"Peringkat {leader['rank']}")
                if medal
                else f"#{leader['rank']}"
            )
            st.markdown(
                f"""
                <div style="display:flex;justify-content:space-between;align-items:center;padding:6px 8px;border-radius:8px;margin-bottom:2px;{highlight}">
                    <div style="display:flex;align-items:center;gap:8px;">
                        <span style="display:inline-flex;align-items:center;font-weight:800;min-width:24px;color:{COLOR_PRIMARY};">{rank_mark}</span>
                        <span style="font-size:13px;">{html.escape(str(leader['username']))}</span>
                        <span style="font-size:11px;color:#777777;">({html.escape(str(leader['tier']))})</span>
                    </div>
                    <div style="display:flex;align-items:center;font-weight:800;color:{COLOR_PRIMARY};font-size:13px;">
                        {render_icon("bintang", 22, "biova-icon--reward", t("common.total_stars"))}
                        <span>{leader['stars']}</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        st.markdown("</div>", unsafe_allow_html=True)

    col_material, col_repeat = st.columns(2)
    with col_material:
        st.markdown(
            f'<div class="biova-icon-action">{render_icon("ensiklopedia", 22, "biova-icon--button", t("quiz.back_material"))}</div>',
            unsafe_allow_html=True,
        )
        if st.button(t("quiz.back_material"), key="btn_res_material", use_container_width=True):
            st.session_state["learning_category"] = category
            st.session_state["lesson_detail_mode"] = False
            st.session_state["current_card_index"] = 0
            navigate_to("lesson")
    with col_repeat:
        st.markdown(
            f'<div class="biova-icon-action">{render_icon("restart", 22, "biova-icon--button", t("quiz.repeat"))}</div>',
            unsafe_allow_html=True,
        )
        if st.button(t("quiz.repeat"), key="btn_res_repeat", type="secondary", use_container_width=True):
            initialize_quiz_session(category, st.session_state)
            navigate_to("quiz")

    render_bottom_nav(current_active="learn")
