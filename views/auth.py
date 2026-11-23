"""BIOVA Authentication Views (Login & Register)
Clean form-based login and registration with validation.
"""

import streamlit as st
from components.icons import render_icon
from components.navigation import navigate_to, render_back_button
from services.auth_service import authenticate_user, register_user
from services.config import COLOR_PRIMARY, COLOR_SECONDARY, COLOR_CARD, COLOR_BORDER
from components.i18n import t, set_language
def _render_field_label(icon: str, label: str):
    st.markdown(
        f'<div class="biova-field-label">{render_icon(icon, 22, "biova-icon--button", label)}'
        f'<span>{label}</span></div>',
        unsafe_allow_html=True,
    )


def render_login():
    """Renders the Login screen."""
    if st.session_state.get("is_authenticated") and st.session_state.get("authenticated_user"):
        navigate_to("dashboard")
        return

    render_back_button("welcome", t("nav.back"))
    st.markdown(
        f'<div class="biova-login-mascot">'
        f'{render_icon("maskot_BIOVA.png", 112, "biova-login-mascot__image", "Maskot BIOVA")}</div>',
        unsafe_allow_html=True,
    )

    # Headlines
    st.markdown(
        f"""
        <div class="biova-auth-heading" style="text-align: center; margin-bottom: 14px;">
            <h2 style="font-size: 22px; font-weight: 800; color: {COLOR_PRIMARY}; margin-bottom: 4px;">
                {t("auth.welcome")}
            </h2>
            <p style="font-size: 13px; color: #555555; margin: 0;">
                {t("auth.continue")}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    google_configured = False
    try:
        auth_secrets = st.secrets.get("auth", {})
        google_secrets = auth_secrets.get("google", {}) if hasattr(auth_secrets, "get") else {}
        google_configured = bool(
            auth_secrets.get("redirect_uri")
            and auth_secrets.get("cookie_secret")
            and google_secrets.get("client_id")
            and google_secrets.get("client_secret")
        )
    except Exception:
        google_configured = False

    # Form card
    with st.form("login_form", clear_on_submit=False):
        _render_field_label("pengguna", t("auth.username"))
        username = st.text_input(
            t("auth.username"),
            placeholder=t("auth.username_placeholder"),
            key="login_user",
            label_visibility="collapsed",
        )
        _render_field_label("kunci", t("auth.password"))
        password = st.text_input(
            t("auth.password"),
            type="password",
            placeholder=t("auth.password_placeholder"),
            key="login_pass",
            label_visibility="collapsed",
        )

        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
        submitted = st.form_submit_button(t("auth.login"), use_container_width=True, key="login_submit")

        st.markdown(
            f'<div class="biova-login-divider"><span></span><b>{t("auth.or")}</b><span></span></div>',
            unsafe_allow_html=True,
        )

        google_submitted = st.form_submit_button(
            t("auth.google"),
            use_container_width=True,
            type="secondary",
            key="btn_google_login",
        )

        if submitted:
            success, user_data, msg = authenticate_user(username, password)
            if success:
                st.session_state["authenticated_user"] = user_data
                st.session_state["user_stars"] = user_data.get("stars", 0)
                selected = st.session_state.get("language")
                if not st.session_state.get("_language_explicit"):
                    selected = user_data.get("language", "id")
                set_language(selected)
                st.session_state["is_authenticated"] = True
                navigate_to("dashboard")
            else:
                st.error(msg)
        if google_submitted:
            try:
                if not google_configured:
                    st.warning(t("auth.google_not_configured"))
                else:
                    st.login("google")
            except Exception:
                st.error(t("auth.google_unavailable"))

    # Link to Register
    col1, col2, col3 = st.columns([1, 8, 1])
    with col2:
        st.markdown(
            f"""
            <div style="text-align: center; margin-top: 14px; font-size: 13px; color: #555555;">
                {t("auth.no_account")}
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button(
            t("welcome.register"),
            key="btn_goto_register",
            use_container_width=True,
            type="secondary",
        ):
            navigate_to("register")


def render_register():
    """Renders the Registration screen."""
    render_back_button("welcome", t("nav.back"))
    st.markdown(
        f'<div style="text-align:center;margin:8px 0 12px;">'
        f'{render_icon("pengguna", 52, "biova-icon--heading", t("auth.create_account"))}</div>',
        unsafe_allow_html=True,
    )

    # Headlines
    st.markdown(
        f"""
        <div style="text-align: center; margin-bottom: 20px;">
            <h2 style="font-size: 22px; font-weight: 800; color: {COLOR_PRIMARY}; margin-bottom: 4px;">
                {t("auth.register_headline")}
            </h2>
            <p style="font-size: 13px; color: #555555; margin: 0;">
                {t("auth.register_subtitle")}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Registration Form card
    with st.form("register_form", clear_on_submit=False):
        _render_field_label("file", "Email")
        email = st.text_input(
            "Email",
            placeholder=t("auth.email_placeholder"),
            key="reg_email",
            label_visibility="collapsed",
        )
        _render_field_label("pengguna", t("auth.username"))
        username = st.text_input(
            t("auth.username"),
            placeholder=t("auth.username_hint"),
            key="reg_user",
            label_visibility="collapsed",
        )
        _render_field_label("kunci", t("auth.password"))
        password = st.text_input(
            t("auth.password"),
            type="password",
            placeholder=t("auth.password_hint"),
            key="reg_pass",
            label_visibility="collapsed",
        )

        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
        submitted = st.form_submit_button(t("auth.register"), use_container_width=True)

        if submitted:
            success, msg = register_user(username, email, password)
            if success:
                st.success(msg)
                navigate_to("login")
            else:
                st.error(msg)

    # Link to Login
    col1, col2, col3 = st.columns([1, 8, 1])
    with col2:
        st.markdown(
            f"""
            <div style="text-align: center; margin-top: 14px; font-size: 13px; color: #555555;">
                {t("auth.has_account")}
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button(
            t("auth.goto_login"),
            key="btn_goto_login",
            use_container_width=True,
            type="secondary",
        ):
            navigate_to("login")
