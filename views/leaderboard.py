"""BIOVA Leaderboard View
Displays global rankings of real registered users with tier indicators and star totals.
"""

import streamlit as st
import html
from components.header import render_header
from components.icons import render_icon
from components.navigation import navigate_to, render_bottom_nav
from services.leaderboard_service import get_leaderboard
from services.config import COLOR_PRIMARY
from components.i18n import t


_PAGE_SIZE = 10


def render_leaderboard():
    """Renders the full leaderboard screen."""
    user = st.session_state.get("authenticated_user")
    if not user:
        navigate_to("login")
        return

    render_header(show_stars=True)

    st.markdown(
        f"""
        <div class="biova-leaderboard-heading">
            <div class="biova-leaderboard-heading__icon">
                {render_icon("piala", 56, "biova-icon--heading", "Piala peringkat")}
            </div>
            <h2 style="color: {COLOR_PRIMARY};">
                {t("leaderboard.title")}
            </h2>
            <p>
                {t("leaderboard.subtitle")}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    leaders = get_leaderboard(limit=None)

    if not leaders:
        st.info(t("leaderboard.empty"))
    else:
        page_count = (len(leaders) + _PAGE_SIZE - 1) // _PAGE_SIZE
        current_rank = next(
            (index for index, row in enumerate(leaders) if row["user_id"] == user["id"]),
            None,
        )
        if "leaderboard_page" not in st.session_state:
            st.session_state["leaderboard_page"] = 0
        page = min(max(int(st.session_state["leaderboard_page"]), 0), page_count - 1)
        st.session_state["leaderboard_page"] = page
        start = page * _PAGE_SIZE

        for page_index, row in enumerate(leaders[start:start + _PAGE_SIZE]):
            is_me = row["user_id"] == user["id"]
            rank = row["rank"]
            medal = {
                1: "medali_gold",
                2: "medali_silver",
                3: "medali_bronze",
            }.get(rank)
            rank_badge = (
                f'{render_icon(medal, 32, "biova-icon--reward", f"Peringkat {rank}")}'
                if medal
                else f"#{rank}"
            )
            row_class = "biova-leaderboard-row biova-leaderboard-row--top3" if rank <= 3 else "biova-leaderboard-row"
            if page_index % 2:
                row_class += " biova-leaderboard-row--alternate"
            if is_me:
                row_class += " biova-leaderboard-row--me"

            st.markdown(
                f"""
                <div class="{row_class}">
                    <span class="biova-leaderboard-rank">{rank_badge}</span>
                    <span class="biova-leaderboard-name">
                        {html.escape(str(row['username']))} {t("leaderboard.you") if is_me else ''}
                    </span>
                    <div class="biova-leaderboard-stars">
                        {render_icon("bintang", 22, "biova-icon--reward", "Bintang")}
                        <span>{row['stars']}</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        if current_rank is not None and not start <= current_rank < start + _PAGE_SIZE:
            row = leaders[current_rank]
            st.markdown(
                f"""
                <div class="biova-leaderboard-my-rank">
                    <span>{t("leaderboard.my_rank")}</span>
                    <strong>#{row['rank']} · {html.escape(str(row['username']))}</strong>
                    <span class="biova-leaderboard-my-stars">
                        {render_icon("bintang", 22, "biova-icon--reward", "Bintang")}
                        {row['stars']}
                    </span>
                </div>
                """,
                unsafe_allow_html=True,
            )

        previous_col, page_col, next_col = st.columns([1, 2, 1], vertical_alignment="center")
        with previous_col:
            if st.button(
                t("leaderboard.previous", "Sebelumnya"),
                key="leaderboard_previous",
                disabled=page == 0,
                use_container_width=True,
            ):
                st.session_state["leaderboard_page"] = page - 1
                st.rerun()
        with page_col:
            st.markdown(
                f'<div class="biova-leaderboard-page">{page + 1} / {page_count}</div>',
                unsafe_allow_html=True,
            )
        with next_col:
            if st.button(
                t("leaderboard.next", "Berikutnya"),
                key="leaderboard_next",
                disabled=page >= page_count - 1,
                use_container_width=True,
            ):
                st.session_state["leaderboard_page"] = page + 1
                st.rerun()

    render_bottom_nav(current_active="leaderboard")
