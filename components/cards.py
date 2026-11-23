"""BIOVA reusable dashboard, learning, and panorama cards."""

import html
from collections.abc import Callable, Sequence

import streamlit as st

from components.icons import render_icon
from components.i18n import t


_LEARNING_BUTTON_ICONS = {
    "ensiklopedia": ":material/menu_book:",
    "cek": ":material/quiz:",
    "riset": ":material/travel_explore:",
}


def render_category_card(
    category_id: str,
    title: str,
    icon: str,
    description: str,
    action_label: str,
    on_explore_callback=None,
):
    """Render one homepage category with a single action."""

    with st.container(key=f"home-card-{category_id}"):
        st.markdown(
            f"""
            <section class="biova-home-card">
                <div class="biova-home-card__head">
                    <div class="biova-home-card__illustration">
                        {render_icon(icon, 125, "biova-icon--category", title)}
                    </div>
                    <div class="biova-home-card__title">
                        <h3>{html.escape(title)}</h3>
                        <p>{html.escape(description)}</p>
                    </div>
                </div>
            </section>
            """,
            unsafe_allow_html=True,
        )

        with st.container(key=f"home-card-actions-{category_id}"):
            if st.button(
                action_label,
                key=f"home_explore_{category_id}",
                width="stretch",
            ):
                if on_explore_callback:
                    on_explore_callback(category_id)


def render_learning_category_card(
    category_id: str,
    title: str,
    icon: str,
    description: str,
    actions: Sequence[
        tuple[str, str, str, Callable[[], None]]
    ],
):
    """Render category learning actions."""

    with st.container(key=f"learn-card-{category_id}"):
        st.markdown(
            f"""
            <div class="biova-learn-card__header">
                <div class="biova-learn-card__illustration">
                    {render_icon(icon, 112, "biova-icon--category", title)}
                </div>
                <div class="biova-learn-card__copy">
                    <h3>{html.escape(title)}</h3>
                    <p>{html.escape(description)}</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        with st.container(key=f"learn-actions-{category_id}"):
            for action_icon, label, key, callback in actions:
                icon_name = _LEARNING_BUTTON_ICONS.get(
                    action_icon,
                    ":material/arrow_forward:",
                )

                if st.button(
                    label,
                    key=key,
                    width="stretch",
                    icon=icon_name,
                ):
                    callback()


def render_panorama_banner(on_click_callback=None):
    """Render Panorama with separated copy and illustration."""

    with st.container(key="biova-panorama-banner"):
        copy_column, art_column = st.columns(
            [1, 0.9],
            gap="medium",
            vertical_alignment="center",
        )

        with copy_column:
            with st.container(key="biova-panorama-copy"):
                st.markdown(
                    f"""
                    <div class="biova-panorama-text">
                        <div
                            class="biova-panorama-title"
                            role="heading"
                            aria-level="2"
                        >
                            {html.escape(t("panorama.title"))}
                        </div>
                        <div class="biova-panorama-description">
                            {html.escape(t("panorama.description"))}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                if st.button(
                    t("panorama.start"),
                    key="btn_dash_panorama",
                    width="content",
                ):
                    if on_click_callback:
                        on_click_callback()

        with art_column:
            st.markdown(
                """
                <div class="biova-panorama-art" aria-hidden="true">
                    <span class="biova-panorama-art__sun"></span>
                    <span class="
                        biova-panorama-art__ridge
                        biova-panorama-art__ridge--back">
                    </span>
                    <span class="
                        biova-panorama-art__ridge
                        biova-panorama-art__ridge--front">
                    </span>
                    <span class="biova-panorama-art__water"></span>
                </div>
                """,
                unsafe_allow_html=True,
            )
