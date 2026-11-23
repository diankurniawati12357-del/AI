"""BIOVA Classification Result View
Displays detection outcome with success or failure states.
Uses placeholder where mascot was previously rendered.
"""

import streamlit as st
from components.theme import apply_theme
from components.icons import render_icon, get_animal_class_icon
from components.navigation import navigate_to, render_back_button, render_bottom_nav
from components.header import render_header
from components.three_d_viewer import render_3d_viewer
from services.edukasi_service import get_education_info
from services.model3d_service import get_model3d_info
from services.config import COLOR_PRIMARY, COLOR_SECONDARY, COLOR_CARD, COLOR_BORDER, COLOR_ERROR


def render_scan_result():
    """Renders either the classification success or failure screen."""
    apply_theme()

    user = st.session_state.get("authenticated_user")
    if not user:
        navigate_to("login")
        return

    render_back_button("scan", "Kembali ke Pemindaian")
    render_header(show_stars=True)

    res = st.session_state.get("last_scan_result", None)
    img = st.session_state.get("last_scan_image", None)

    if res is None:
        st.warning("Belum ada data hasil pemindaian.")
        if st.button("Mulai Pindai", use_container_width=True):
            navigate_to("scan")
        return

    status = res.get("status", "error")
    category = res.get("category", "hewan")

    if status == "success":
        # ===== SUCCESS STATE =====
        pred_group = res.get("predicted_group", "Spesies")
        confidence = res.get("confidence", 0.0)
        edu_info = get_education_info(category, pred_group)
        animal_icon = None
        if category == "hewan":
            animal_icon, normalized_group = get_animal_class_icon(pred_group)
        else:
            normalized_group = ""

        # Star notification
        if st.session_state.get("upload_star_awarded", False):
            st.markdown(
                """
                <div style="background-color: #CFDFA6; border: 1.5px solid #416848; border-radius: 14px; padding: 8px 14px; text-align: center; margin-bottom: 12px; font-weight: 700; color: #263C2B; font-size: 13px;">
                    {render_icon("cek", 22, "biova-icon--button", "Berhasil")}
                    Selamat! Kamu mendapatkan <strong>+1 {render_icon("bintang", 22, "biova-icon--reward", "Bintang")}</strong> dari foto baru ini!
                </div>
                """,
                unsafe_allow_html=True,
            )

        # Main Container
        st.markdown('<div class="biova-card">', unsafe_allow_html=True)

        st.markdown(
            f'<div style="text-align:center;margin:8px 0 12px;">'
            f'{render_icon("cek", 56, "biova-icon--heading", "Identifikasi berhasil")}</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            f"""
            <div style="text-align: center; margin-bottom: 14px;">
                {f'<div class="biova-animal-result-icon biova-icon-enter" key="animal-{normalized_group}">{render_icon(animal_icon, 104, "biova-icon--result", pred_group)}</div>' if animal_icon else ""}
                <div style="font-size: 13px; font-weight: 700; color: {COLOR_SECONDARY}; text-transform: uppercase; letter-spacing: 0.5px;">
                    Objek Berhasil Terdeteksi!
                </div>
                <h1 style="font-size: 26px; font-weight: 900; color: {COLOR_PRIMARY}; margin: 4px 0 6px 0;">
                    {pred_group}
                </h1>
                <div class="biova-badge">
                    {edu_info.get('class_badge', f'Kelas: {pred_group}') if edu_info else f'Kelas: {pred_group}'}
                </div>
                <div style="font-size: 11px; color: #666666; margin-top: 2px;">
                    Tingkat Keyakinan Model: <strong>{confidence*100:.1f}%</strong>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Uploaded image preview
        if img:
            st.image(img, use_container_width=True)

        # Interactive 3D Model Section
        model_info = get_model3d_info(category, pred_group)
        render_3d_viewer(
            model_path=model_info.get("model_path"),
            species_name=pred_group,
            has_animation=model_info.get("has_animation", False),
            animation_name=model_info.get("animation_name"),
            height=320,
        )

        # Educational Description
        if edu_info:
            st.markdown(
                f"""
                <div style="margin-top: 14px;">
                    <div style="font-size: 14px; font-weight: 800; color: {COLOR_PRIMARY}; margin-bottom: 4px;">
                        Deskripsi Singkat:
                    </div>
                    <p style="font-size: 13px; line-height: 1.5; color: #333333; margin-bottom: 10px;">
                        {edu_info.get('description', '')}
                    </p>
                    <div style="font-size: 12px; color: #444444; background: rgba(255,255,255,0.6); border-radius: 10px; padding: 10px; margin-bottom: 8px;">
                        <strong>Ciri Fisik:</strong> {edu_info.get('characteristics', '-')}<br>
                        <strong>Habitat:</strong> {edu_info.get('habitat', '-')}<br>
                        <strong>Fakta Unik:</strong> {edu_info.get('unique_fact', '-')}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown("</div>", unsafe_allow_html=True)

        # Action Buttons
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(
                f'<div class="biova-icon-action">{render_icon("ensiklopedia", 22, "biova-icon--button", "Pelajari")}</div>',
                unsafe_allow_html=True,
            )
            if st.button("Pelajari Lebih Lanjut", key="btn_res_learn", use_container_width=True):
                st.session_state["selected_learning_category"] = category
                navigate_to("learn")
        with col2:
            st.markdown(
                f'<div class="biova-icon-action">{render_icon("gambar", 22, "biova-icon--button", "Ubah gambar")}</div>',
                unsafe_allow_html=True,
            )
            if st.button("Ubah Gambar", key="btn_res_change_succ", type="secondary", use_container_width=True):
                navigate_to("scan")

    else:
        # ===== FAILURE / UNRECOGNIZED STATE =====
        st.markdown('<div class="biova-card">', unsafe_allow_html=True)

        st.markdown(
            f'<div style="text-align:center;margin:8px 0 12px;">'
            f'{render_icon("info", 52, "biova-icon--heading", "Belum dikenali")}</div>',
            unsafe_allow_html=True,
        )

        error_title = "Objek Belum Dapat Dikenali!"
        error_msg = res.get("message", "Kami belum dapat mengenali objek pada gambar ini.")

        st.markdown(
            f"""
            <div style="text-align: center; margin-bottom: 16px;">
                <h2 style="font-size: 20px; font-weight: 800; color: {COLOR_ERROR}; margin-bottom: 8px;">
                    {error_title}
                </h2>
                <p style="font-size: 13px; color: #444444; line-height: 1.5; margin: 0 10px 14px 10px;">
                    {error_msg}
                </p>
                <div style="font-size: 12px; color: #666666; background: rgba(255,255,255,0.7); border-radius: 12px; padding: 10px; text-align: left;">
                    {render_icon("info", 22, "biova-icon--button", "Tips")} <strong>Tips foto lebih akurat:</strong>
                    <ul style="margin: 4px 0 0 18px; padding: 0;">
                        <li>Pastikan pencahayaan terang dan objek terlihat fokus.</li>
                        <li>Ambil foto dari jarak yang cukup dekat dengan objek utama.</li>
                        <li>Pastikan objek sesuai kategori yang dipilih ({category.title()}).</li>
                    </ul>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown(
            f'<div class="biova-icon-action">{render_icon("gambar", 22, "biova-icon--button", "Ubah gambar")}</div>',
            unsafe_allow_html=True,
        )
        if st.button("Ubah Gambar", key="btn_res_change_fail", use_container_width=True):
            navigate_to("scan")

    render_bottom_nav(current_active="dashboard")
