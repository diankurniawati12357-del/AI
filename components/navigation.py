"""BIOVA Navigation Component
Manages routing, page switching, bottom navigation bar, and back buttons.
"""

import streamlit as st
from components.icons import render_icon
from components.i18n import t


def navigate_to(page: str, **kwargs):
    """Sets session state for routing and reruns the Streamlit application."""
    st.session_state["current_page"] = page
    for k, v in kwargs.items():
        st.session_state[k] = v
    st.rerun()


def render_back_button(
    target_page: str = "dashboard",
    label: str | None = None,
    *,
    compact: bool = False,
    key: str | None = None,
    state_updates: dict[str, object] | None = None,
):
    """Renders a friendly back button."""
    label = label or t("nav.back")
    if compact:
        with st.container(key="biova-content-back"):
            if st.button(
                f"← {label}",
                key=key or f"btn_back_to_{target_page}",
                use_container_width=False,
            ):
                navigate_to(target_page, **(state_updates or {}))
        return

    icon_col, button_col, _ = st.columns([0.6, 3.4, 6])
    with icon_col:
        st.markdown(
            f'<div class="biova-icon-action">{render_icon("kembali", 24, "biova-icon--button", "Kembali")}</div>',
            unsafe_allow_html=True,
        )
    with button_col:
        if st.button(label, key=f"btn_back_to_{target_page}", use_container_width=False):
            navigate_to(target_page)
    st.markdown("<div style='margin-bottom: 8px;'></div>", unsafe_allow_html=True)


_NAV_ITEMS = [
    {
        "key": "dashboard",
        "label": "Beranda",
        "icon": "beranda",
        "page": "dashboard",
        "matches": ("dashboard",),
    },
    {
        "key": "learn",
        "label": "Belajar",
        "icon": "belajar",
        "page": "learn",
        "matches": ("learn", "learning", "lesson", "quiz", "quiz_result"),
    },
    {
        "key": "leaderboard",
        "label": "Peringkat",
        "icon": "peringkat",
        "page": "leaderboard",
        "matches": ("leaderboard",),
    },
    {
        "key": "profile",
        "label": "Profil",
        "icon": "profil",
        "page": "profile",
        "matches": ("profile",),
    },
]


def render_bottom_nav(current_active: str = "dashboard"):
    """Renders the in-app bottom navigation bar with native Streamlit buttons."""
    current_page = st.session_state.get("current_page", current_active)
    translated_labels = {
        "dashboard": t("nav.dashboard"),
        "learn": t("nav.learn"),
        "leaderboard": t("nav.leaderboard"),
        "profile": t("nav.profile"),
    }
    with st.container(key="biova-bottom-nav"):
        columns = st.columns(4, gap="small")

        for column, item in zip(columns, _NAV_ITEMS):
            with column:
                is_active = current_page in item["matches"]
                item_label = translated_labels[item["key"]]
                st.markdown(
                    f'<div class="biova-icon-action">{render_icon(item["icon"], 22, "biova-icon--nav", item_label)}</div>',
                    unsafe_allow_html=True,
                )
                if st.button(
                    item_label,
                    key=f"nav_{item['key']}",
                    type="primary" if is_active else "secondary",
                    use_container_width=True,
                ) and current_page != item["page"]:
                    navigate_to(item["page"])
