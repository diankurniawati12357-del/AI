"""BIOVA Authentication Views (Login & Register)
Matches Masuk.png and Daftar.png designs with frog mascot, rounded cards, and validation.
"""

import streamlit as st
from components.theme import apply_theme
from components.mascot import render_mascot
from components.navigation import navigate_to, render_back_button
from services.auth_service import authenticate_user, register_user
from services.config import COLOR_PRIMARY, COLOR_SECONDARY, COLOR_CARD, COLOR_BORDER


def render_login():
    """Renders the Login screen matching Masuk.png."""
    apply_theme()

    render_back_button("welcome", "← Kembali")

    # Smiling Frog Mascot at top center
    render_mascot("happy", width=120, center=True)

    # Headlines
    st.markdown(
        f"""
        <div style="text-align: center; margin-bottom: 20px;">
            <h2 style="font-size: 22px; font-weight: 800; color: {COLOR_PRIMARY}; margin-bottom: 4px;">
                Selamat Datang Kembali!
            </h2>
            <p style="font-size: 13px; color: #555555; margin: 0;">
                Lanjutkan petualanganmu bersama BIOVA
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Form card
    st.markdown('<div class="biova-card">', unsafe_allow_html=True)
    with st.form("login_form", clear_on_submit=False):
        username = st.text_input("Nama Pengguna", placeholder="Masukkan nama pengguna", key="login_user")
        password = st.text_input("Kata Sandi", type="password", placeholder="Masukkan kata sandi", key="login_pass")
        
        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
        submitted = st.form_submit_button("Masuk", use_container_width=True)

        if submitted:
            success, user_data, msg = authenticate_user(username, password)
            if success:
                st.session_state["authenticated_user"] = user_data
                st.session_state["user_stars"] = user_data.get("stars", 0)
                st.success(msg)
                navigate_to("dashboard")
            else:
                st.error(msg)

    st.markdown("</div>", unsafe_allow_html=True)

    # Link to Register
    col1, col2, col3 = st.columns([1, 8, 1])
    with col2:
        st.markdown(
            """
            <div style="text-align: center; margin-top: 14px; font-size: 13px; color: #555555;">
                Belum punya akun?
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Daftar Sekarang", key="btn_goto_register", use_container_width=True, type="secondary"):
            navigate_to("register")


def render_register():
    """Renders the Registration screen matching Daftar.png."""
    apply_theme()

    render_back_button("welcome", "← Kembali")

    # Smiling Frog Mascot
    render_mascot("happy", width=120, center=True)

    # Headlines
    st.markdown(
        f"""
        <div style="text-align: center; margin-bottom: 20px;">
            <h2 style="font-size: 22px; font-weight: 800; color: {COLOR_PRIMARY}; margin-bottom: 4px;">
                Petualanganmu dimulai di sini!
            </h2>
            <p style="font-size: 13px; color: #555555; margin: 0;">
                Yuk, ambil langkah pertamamu bersama BIOVA
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Registration Form card
    st.markdown('<div class="biova-card">', unsafe_allow_html=True)
    with st.form("register_form", clear_on_submit=False):
        email = st.text_input("Email", placeholder="contoh: nama@mhs.unesa.ac.id", key="reg_email")
        username = st.text_input("Nama Pengguna", placeholder="Pilih nama pengguna (min. 3 huruf)", key="reg_user")
        password = st.text_input("Kata Sandi", type="password", placeholder="Minimal 6 karakter", key="reg_pass")

        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
        submitted = st.form_submit_button("Daftar", use_container_width=True)

        if submitted:
            success, msg = register_user(username, email, password)
            if success:
                st.success(msg)
                navigate_to("login")
            else:
                st.error(msg)

    st.markdown("</div>", unsafe_allow_html=True)

    # Link to Login
    col1, col2, col3 = st.columns([1, 8, 1])
    with col2:
        st.markdown(
            """
            <div style="text-align: center; margin-top: 14px; font-size: 13px; color: #555555;">
                Sudah punya akun?
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Masuk ke Akunmu", key="btn_goto_login", use_container_width=True, type="secondary"):
            navigate_to("login")
