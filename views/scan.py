"""BIOVA Image Upload & Scanning View
Allows user to upload an image of an animal or plant and initiate AI classification.
"""

import streamlit as st
from PIL import Image
from components.theme import apply_theme
from components.header import render_header
from components.navigation import navigate_to, render_back_button, render_bottom_nav
from services.upload_service import validate_and_process_upload
from services.model_service import classify_image, check_model_availability
from services.game_service import award_upload_star
from services.config import COLOR_PRIMARY, COLOR_SECONDARY, COLOR_CARD, COLOR_BORDER


def render_scan():
    """Renders the image upload and scanning interface."""
    apply_theme()

    user = st.session_state.get("authenticated_user")
    if not user:
        navigate_to("login")
        return

    render_back_button("dashboard", "← Kembali ke Beranda")

    category = st.session_state.get("selected_category", "hewan")
    cat_title = "Hewan" if category == "hewan" else "Tumbuhan"
    cat_icon = "🐾" if category == "hewan" else "🌿"

    st.markdown(
        f"""
        <div style="text-align: center; margin-bottom: 18px;">
            <div style="font-size: 32px; margin-bottom: 4px;">{cat_icon}</div>
            <h2 style="font-size: 22px; font-weight: 800; color: {COLOR_PRIMARY}; margin: 0;">
                Identifikasi {cat_title}
            </h2>
            <p style="font-size: 13px; color: #555555; margin-top: 4px;">
                Unggah foto {cat_title.lower()} yang ingin kamu ketahui informasinya.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Category Switcher Pills
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        if st.button("🐾 Hewan", key="switch_cat_hewan", type="primary" if category == "hewan" else "secondary", use_container_width=True):
            st.session_state["selected_category"] = "hewan"
            st.rerun()
    with col_c2:
        if st.button("🌿 Tumbuhan", key="switch_cat_tumb", type="primary" if category == "tumbuhan" else "secondary", use_container_width=True):
            st.session_state["selected_category"] = "tumbuhan"
            st.rerun()

    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

    # Check model readiness status
    is_model_ready, model_msg = check_model_availability(category)
    if not is_model_ready:
        st.markdown(
            f"""
            <div class="biova-card" style="border-left: 4px solid #D4AF37; padding: 12px 14px; margin-bottom: 16px;">
                <div style="font-weight: 700; font-size: 13px; color: #7B6200;">ℹ️ Status Model AI</div>
                <div style="font-size: 12px; color: #555555; margin-top: 2px;">
                    {model_msg}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # File uploader container
    st.markdown('<div class="biova-card">', unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        f"Pilih file foto {cat_title.lower()}",
        type=["jpg", "jpeg", "png"],
        key="file_uploader_scan",
        help="Format didukung: JPG, JPEG, PNG (Maks 10 MB)",
    )
    st.markdown("</div>", unsafe_allow_html=True)

    if uploaded_file is not None:
        # Validate upload
        is_valid, msg, img, img_hash = validate_and_process_upload(uploaded_file)
        if not is_valid:
            st.error(msg)
        else:
            # Display image preview
            st.markdown('<div class="biova-card" style="text-align: center;">', unsafe_allow_html=True)
            st.image(img, caption="Pratinjau Foto Terpilih", use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button("🔍 Identifikasi Objek", key="btn_do_identify", use_container_width=True):
                    with st.spinner("Sedang memproses dan mengidentifikasi..."):
                        # Execute classification
                        res = classify_image(category, img)
                        
                        # Store in session state
                        st.session_state["last_scan_image"] = img
                        st.session_state["last_scan_result"] = res
                        st.session_state["last_scan_hash"] = img_hash

                        # Award star if classification succeeds
                        if res.get("status") == "success":
                            awarded = award_upload_star(user["id"], img_hash)
                            st.session_state["upload_star_awarded"] = awarded

                        navigate_to("scan_result")

            with col2:
                if st.button("🗑️ Hapus Foto", key="btn_clear_scan", type="secondary", use_container_width=True):
                    st.rerun()

    render_bottom_nav(current_active="dashboard")
