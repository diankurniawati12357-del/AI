
"""BIOVA Header Component.

Displays the user avatar, greeting, star counter,
and Indonesian/English language switcher.
"""

import base64
import html

import streamlit as st

from components.icons import render_icon
from components.i18n import t, render_language_switcher
from services.profile_service import get_profile_photo_path
from services.game_service import get_user_stats


def _render_user_information(user, username):
    """Render user avatar and greeting."""
    photo = get_profile_photo_path(user["id"]) if user else None

    if photo:
        try:
            data = base64.b64encode(photo.read_bytes()).decode("ascii")
        except OSError:
            data = ""

        avatar_html = (
            f'<img src="data:image/png;base64,{data}" '
            f'alt="{username}">'
            if data
            else render_icon(
                "pengguna",
                44,
                "biova-icon--category",
                username,
            )
        )
    else:
        avatar_html = render_icon(
            "pengguna",
            44,
            "biova-icon--category",
            username,
        )

    st.markdown(
        f"""
        <div class="biova-header-user">
            <div class="biova-header-avatar">
                {avatar_html}
            </div>
            <div class="biova-header-user-text">
                <div class="biova-header-caption">
                    {html.escape(t("header.welcome"))}
                </div>
                <div class="biova-header-name">
                    {username}
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_star_counter(stars, stars_changed):
    """Render the user's current total stars."""
    animation_class = " is-changing" if stars_changed else ""

    st.markdown(
        f"""
        <div class="biova-header-stars">
            {render_icon(
                "bintang",
                18,
                "biova-icon--reward",
                t("common.total_stars")
            )}
            <span class="biova-star-count{animation_class}">
                {stars}
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_header(show_stars: bool = True):
    """Render the authenticated user's header."""

    user = st.session_state.get("authenticated_user")

    username = html.escape(
        str(user["username"]) if user else t("auth.username")
    )

    if user:
        stats = get_user_stats(user["id"])
        stars = int(stats["stars"])

        user["stars"] = stars
        st.session_state["user_stars"] = stars
    else:
        stars = int(st.session_state.get("user_stars", 0))

    previous_stars = st.session_state.get(
        "_header_previous_stars"
    )

    stars_changed = (
        previous_stars is not None
        and stars != previous_stars
    )

    st.session_state["_header_previous_stars"] = stars

    with st.container(key="biova-header"):
        _render_user_information(user, username)

        with st.container(key="biova-header-actions"):
            if show_stars:
                _render_star_counter(stars, stars_changed)

            render_language_switcher()


def render_public_header(welcome_layout: bool = False):
    """Render the language switcher on public pages."""

    container_key = (
        "biova-welcome-header"
        if welcome_layout
        else "biova-public-header"
    )

    with st.container(key=container_key):

        spacer_col, language_col = st.columns(
            [8, 2],
            gap="small",
            vertical_alignment="center",
        )

        with language_col:
            render_language_switcher()
