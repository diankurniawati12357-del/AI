"""BIOVA Panorama View (Image Stitching)
Matches IMAGE STITCHING.png across three states:
1. Upload & Select Images
2. Review Selected Photos Grid
3. Panorama Output / Stitching Failure with OpenCV Stitcher
"""

import streamlit as st
from PIL import Image
from components.theme import apply_theme
from components.mascot import render_mascot
from components.navigation import navigate_to, render_back_button, render_bottom_nav
from services.upload_service import validate_and_process_upload
from services.stitching_service import stitch_images, get_image_download_bytes
from services.config import COLOR_PRIMARY, COLOR_SECONDARY, COLOR_CARD, COLOR_BORDER, COLOR_ERROR


def render_panorama():
    """Renders the three-state OpenCV image stitching workflow."""
    apply_theme()

    user = st.session_state.get("authenticated_user")
    if not user:
        navigate_to("login")
        return

    render_back_button("dashboard", "← Kembali ke Beranda")

    # Panorama state in session
    if "panorama_images" not in st.session_state:
        st.session_state["panorama_images"] = []
    if "panorama_result" not in st.session_state:
        st.session_state["panorama_result"] = None
    if "panorama_error" not in st.session_state:
        st.session_state["panorama_error"] = None

    # STATE 3: RESULT VIEW
    if st.session_state["panorama_result"] is not None:
        stitched_img = st.session_state["panorama_result"]

        st.markdown('<div class="biova-card">', unsafe_allow_html=True)
        render_mascot("success", width=120, center=True)

        st.markdown(
            f"""
            <div style="text-align: center; margin-bottom: 14px;">
                <h2 style="font-size: 22px; font-weight: 800; color: {COLOR_PRIMARY}; margin: 0;">
                    Foto Berhasil Digabungkan!
                </h2>
                <p style="font-size: 13px; color: #555555; margin-top: 4px;">
                    Panorama pemandangan alammu telah sukses dibuat dengan OpenCV.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.image(stitched_img, caption="Hasil Gambar Panorama", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # Download and Reset Buttons
        col_d1, col_d2 = st.columns(2)
        with col_d1:
            img_bytes = get_image_download_bytes(stitched_img, format="JPEG")
            st.download_button(
                label="📥 Unduh Gambar",
                data=img_bytes,
                file_name="biova_panorama.jpg",
                mime="image/jpeg",
                use_container_width=True,
            )
        with col_d2:
            if st.button("🔄 Buat Panorama Baru", key="btn_reset_panorama", type="secondary", use_container_width=True):
                st.session_state["panorama_images"] = []
                st.session_state["panorama_result"] = None
                st.session_state["panorama_error"] = None
                st.rerun()

        render_bottom_nav(current_active="dashboard")
        return

    # Heading for States 1 & 2
    st.markdown(
        f"""
        <div style="text-align: center; margin-bottom: 16px;">
            <div style="font-size: 32px; margin-bottom: 4px;">🌄</div>
            <h2 style="font-size: 22px; font-weight: 800; color: {COLOR_PRIMARY}; margin: 0;">
                Buat Panorama
            </h2>
            <p style="font-size: 13px; color: #555555; margin-top: 4px;">
                Pilih beberapa foto dengan bagian gambar yang saling tumpang tindih (overlap).
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Show stitching failure message if occurred
    if st.session_state["panorama_error"]:
        st.markdown(
            f"""
            <div class="biova-card" style="border-left: 4px solid {COLOR_ERROR}; padding: 12px 14px; margin-bottom: 14px;">
                <div style="font-weight: 800; font-size: 13px; color: {COLOR_ERROR};">
                    ⚠️ Penggabungan Belum Berhasil
                </div>
                <div style="font-size: 12px; color: #444444; margin-top: 2px;">
                    {st.session_state["panorama_error"]}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # File uploader for multiple images
    uploaded_files = st.file_uploader(
        "Pilih foto-foto yang akan digabungkan:",
        type=["jpg", "jpeg", "png"],
        accept_multiple_files=True,
        key="uploader_multi_panorama",
        help="Unggah minimal 2 foto dengan sudut bersambung",
    )

    if uploaded_files:
        valid_images = []
        for uf in uploaded_files:
            is_valid, msg, img, _ = validate_and_process_upload(uf)
            if is_valid and img:
                valid_images.append(img)
            else:
                st.warning(f"{uf.name}: {msg}")
        st.session_state["panorama_images"] = valid_images

    images = st.session_state["panorama_images"]

    # STATE 1: Empty state
    if len(images) == 0:
        st.markdown(
            f"""
            <div class="biova-card" style="text-align: center; padding: 36px 20px; border-style: dashed;">
                <div style="font-size: 40px; margin-bottom: 8px;">📷</div>
                <div style="font-weight: 700; font-size: 15px; color: {COLOR_PRIMARY};">
                    Belum ada foto dipilih
                </div>
                <div style="font-size: 12px; color: #666666; margin-top: 4px;">
                    Gunakan pemilih file di atas untuk menambahkan 2 atau lebih foto.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # STATE 2: Selected images preview grid
    else:
        st.markdown(
            f"""
            <div style="font-size: 14px; font-weight: 800; color: {COLOR_PRIMARY}; margin: 12px 0 6px 0;">
                Foto Terpilih ({len(images)} foto):
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Show thumbnail preview grid
        cols = st.columns(min(len(images), 3))
        for idx, img in enumerate(images):
            with cols[idx % 3]:
                st.image(img, caption=f"Foto {idx+1}", use_container_width=True)

        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

        col_act1, col_act2 = st.columns([6, 4])
        with col_act1:
            if st.button("✨ Gabungkan Foto", key="btn_stitch_run", use_container_width=True):
                if len(images) < 2:
                    st.warning("Silakan pilih minimal 2 foto.")
                else:
                    with st.spinner("Sedang memproses homografi dan penggabungan panorama..."):
                        success, stitched, msg = stitch_images(images)
                        if success:
                            st.session_state["panorama_result"] = stitched
                            st.session_state["panorama_error"] = None
                            st.rerun()
                        else:
                            st.session_state["panorama_error"] = msg
                            st.rerun()

        with col_act2:
            if st.button("🗑️ Reset", key="btn_stitch_clear", type="secondary", use_container_width=True):
                st.session_state["panorama_images"] = []
                st.session_state["panorama_error"] = None
                st.rerun()

    render_bottom_nav(current_active="dashboard")
