"""BIOVA Image Upload & Scanning View
Allows user to upload an image or take a photo with camera for AI classification.
"""

import streamlit as st
from PIL import Image
from components.theme import apply_theme
from components.header import render_header
from components.icons import render_icon
from components.navigation import navigate_to, render_back_button, render_bottom_nav
from services.upload_service import validate_and_process_upload
from services.model_service import classify_image, check_model_availability
from services.game_service import award_upload_star
from services.config import COLOR_PRIMARY, COLOR_SECONDARY, COLOR_CARD, COLOR_BORDER


def render_scan():
    """Renders the image upload/camera scanning interface."""
    apply_theme()

    user = st.session_state.get("authenticated_user")
    if not user:
        navigate_to("login")
        return

    render_back_button("dashboard", "Kembali ke Beranda")
    render_header(show_stars=True)

    category = st.session_state.get("selected_category", "hewan")
    cat_title = "Hewan" if category == "hewan" else "Tumbuhan"
    cat_icon = "hewan" if category == "hewan" else "tumbuhan"

    st.markdown(
        f"""
        <div style="text-align: center; margin-bottom: 18px;">
            <div style="margin-bottom: 4px;">{render_icon(cat_icon, 56, "biova-icon--heading", cat_title)}</div>
            <h2 style="font-size: 22px; font-weight: 800; color: {COLOR_PRIMARY}; margin: 0;">
                Identifikasi {cat_title}
            </h2>
            <p style="font-size: 13px; color: #555555; margin-top: 4px;">
                Unggah foto atau ambil gambar langsung untuk identifikasi.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Category Switcher
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        st.markdown(
            f'<div class="biova-icon-action">{render_icon("hewan", 28, "biova-icon--button", "Hewan")}</div>',
            unsafe_allow_html=True,
        )
        if st.button(
            "Hewan",
            key="switch_cat_hewan",
            type="primary" if category == "hewan" else "secondary",
            use_container_width=True,
        ):
            st.session_state["selected_category"] = "hewan"
            st.rerun()
    with col_c2:
        st.markdown(
            f'<div class="biova-icon-action">{render_icon("tumbuhan", 28, "biova-icon--button", "Tumbuhan")}</div>',
            unsafe_allow_html=True,
        )
        if st.button(
            "Tumbuhan",
            key="switch_cat_tumb",
            type="primary" if category == "tumbuhan" else "secondary",
            use_container_width=True,
        ):
            st.session_state["selected_category"] = "tumbuhan"
            st.rerun()

    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

    # Check model readiness status
    is_model_ready, model_msg = check_model_availability(category)
    if not is_model_ready:
        st.markdown(
            f"""
            <div class="biova-card" style="border-left: 4px solid #D4AF37; padding: 12px 14px; margin-bottom: 16px;">
                <div style="display:flex;align-items:center;gap:6px;font-weight:700;font-size:13px;color:#7B6200;">
                    {render_icon("info", 22, "biova-icon--button", "Informasi")}
                    <span>Status Model AI</span>
                </div>
                <div style="font-size: 12px; color: #555555; margin-top: 2px;">
                    {model_msg}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ------- INPUT METHOD SELECTOR -------
    if "scan_input_method" not in st.session_state:
        st.session_state["scan_input_method"] = "upload"

    col_m1, col_m2 = st.columns(2)
    with col_m1:
        is_upload = st.session_state["scan_input_method"] == "upload"
        st.markdown(
            f'<div class="biova-icon-action">{render_icon("unggah", 26, "biova-icon--button", "Unggah file")}</div>',
            unsafe_allow_html=True,
        )
        if st.button(
            "Unggah File",
            key="btn_method_upload",
            type="primary" if is_upload else "secondary",
            use_container_width=True,
        ):
            st.session_state["scan_input_method"] = "upload"
            st.rerun()
    with col_m2:
        is_camera = st.session_state["scan_input_method"] == "camera"
        st.markdown(
            f'<div class="biova-icon-action">{render_icon("kamera", 26, "biova-icon--button", "Kamera")}</div>',
            unsafe_allow_html=True,
        )
        if st.button(
            "Ambil Foto",
            key="btn_method_camera",
            type="primary" if is_camera else "secondary",
            use_container_width=True,
        ):
            st.session_state["scan_input_method"] = "camera"
            st.rerun()

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

    image_source = None  # Will hold the UploadedFile or BytesIO

    if st.session_state["scan_input_method"] == "upload":
        # ---- FILE UPLOAD ----
        st.markdown('<div class="biova-card">', unsafe_allow_html=True)
        uploaded_file = st.file_uploader(
            f"Pilih file foto {cat_title.lower()}",
            type=["jpg", "jpeg", "png"],
            key="file_uploader_scan",
            help="Format didukung: JPG, JPEG, PNG (Maks 10 MB)",
        )
        st.markdown("</div>", unsafe_allow_html=True)
        if uploaded_file is not None:
            image_source = uploaded_file

    else:
        # ---- CAMERA INPUT ----
        st.markdown(
            f"""
            <div class="biova-card" style="padding: 14px 16px;">
                <div style="font-size: 13px; color: #555555; margin-bottom: 10px;">
                    {render_icon("kamera", 22, "biova-icon--button", "Kamera")} Arahkan kamera ke objek {cat_title.lower()} dan tekan tombol untuk mengambil foto.
                </div>
                <div style="font-size: 11px; color: #888888;">
                    Catatan: Akses kamera memerlukan izin browser. Pada perangkat mobile,
                    pastikan situs diakses melalui HTTPS agar kamera dapat digunakan.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        camera_photo = st.camera_input(
            "Ambil foto untuk identifikasi",
            key="camera_input_scan",
        )
        if camera_photo is not None:
            image_source = camera_photo

        # Retake button
        if camera_photo is not None:
            st.markdown(
                f'<div class="biova-icon-action">{render_icon("restart", 22, "biova-icon--button", "Ambil ulang foto")}</div>',
                unsafe_allow_html=True,
            )
            if st.button("Ambil Ulang Foto", key="btn_retake_camera", type="secondary", use_container_width=True):
                # Clear camera by rerunning (Streamlit handles reset)
                st.rerun()

    # ------- PROCESS THE IMAGE (from either source) -------
    if image_source is not None:
        is_valid, msg, img, img_hash = validate_and_process_upload(image_source)
        if not is_valid:
            st.error(msg)
        else:
            # Display image preview
            st.markdown(
                '<div class="biova-card" style="text-align: center;">',
                unsafe_allow_html=True,
            )
            st.image(img, caption="Pratinjau Foto Terpilih", use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

            col1, col2 = st.columns([1, 1])
            with col1:
                st.markdown(
                    f'<div class="biova-icon-action">{render_icon("cari", 22, "biova-icon--button", "Identifikasi")}</div>',
                    unsafe_allow_html=True,
                )
                if st.button(
                    "Identifikasi Objek",
                    key="btn_do_identify",
                    use_container_width=True,
                ):
                    with st.spinner("Sedang memproses dan mengidentifikasi..."):
                        res = classify_image(category, img)

                        st.session_state["last_scan_image"] = img
                        st.session_state["last_scan_result"] = res
                        st.session_state["last_scan_hash"] = img_hash

                        if res.get("status") == "success":
                            awarded = award_upload_star(user["id"], img_hash)
                            st.session_state["upload_star_awarded"] = awarded

                        navigate_to("scan_result")

            with col2:
                st.markdown(
                    f'<div class="biova-icon-action">{render_icon("tutup", 22, "biova-icon--button", "Hapus foto")}</div>',
                    unsafe_allow_html=True,
                )
                if st.button(
                    "Hapus Foto",
                    key="btn_clear_scan",
                    type="secondary",
                    use_container_width=True,
                ):
                    st.rerun()

    render_bottom_nav(current_active="dashboard")
