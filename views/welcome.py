"""BIOVA welcome and nature explorer landing screen."""

import streamlit as st
from components.icons import render_icon
from components.navigation import navigate_to
from components.i18n import t
from pathlib import Path
import base64
from services.config import COLOR_PRIMARY, COLOR_SECONDARY, COLOR_CARD, COLOR_TEXT


def render_welcome():
    """Renders the landing Welcome screen."""
    # If already logged in, redirect to dashboard
    if st.session_state.get("authenticated_user"):
        navigate_to("dashboard")
        return

    mascot_path = Path(__file__).resolve().parent.parent / "icon" / "maskot_BIOVA.png"
    mascot_data = base64.b64encode(mascot_path.read_bytes()).decode("ascii") if mascot_path.is_file() else ""

    with st.container(key="biova-welcome-content"):
        left, right = st.columns([0.92, 1.08], gap="large", vertical_alignment="center")
        with left:
            if mascot_data:
                st.markdown(
                    f'<div class="biova-welcome-mascot"><img src="data:image/png;base64,{mascot_data}" '
                    'alt="Maskot kodok BIOVA"></div>',
                    unsafe_allow_html=True,
                )
        with right:
            st.markdown(
                f"""
                <div class="biova-welcome-copy">
                    <div class="biova-kicker">BIOVA <span>Nature Explorer</span></div>
                    <h1>{t("welcome.headline")}</h1>
                    <h2>{t("welcome.subtitle")}</h2>
                    <p>{t("welcome.description")}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button(t("welcome.start"), key="btn_welcome_login", use_container_width=True):
                navigate_to("login")
            if st.button(t("welcome.register"), key="btn_welcome_register", use_container_width=True, type="secondary"):
                navigate_to("register")
