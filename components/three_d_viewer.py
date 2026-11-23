"""BIOVA 3D Viewer Component
Renders interactive 3D GLB/glTF models using Google's <model-viewer> web component.
Supports 360-degree rotation, zoom, animation playback, and clean fallbacks.
"""

from pathlib import Path
import base64
import streamlit as st
import streamlit.components.v1 as components
from components.icons import render_icon
from services.config import COLOR_CARD, COLOR_BORDER, COLOR_PRIMARY


def render_3d_viewer(
    model_path: Path = None,
    species_name: str = "Spesies",
    poster_path: Path = None,
    has_animation: bool = False,
    animation_name: str = None,
    height: int = 340,
):
    """Renders an interactive 3D viewer or fallback UI."""
    st.markdown(
        f"""
        <div style="margin-top: 14px; margin-bottom: 8px;">
            <div style="font-size: 15px; font-weight: 800; color: {COLOR_PRIMARY}; display: flex; align-items: center; gap: 6px;">
                {render_icon("kubus3d", 24, "biova-icon--button", "Objek 3D")}
                <span>Lihat dalam Bentuk 3D</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if model_path and Path(model_path).exists():
        # Read GLB and encode to base64 data URI
        with open(model_path, "rb") as f:
            glb_bytes = f.read()
        glb_b64 = base64.b64encode(glb_bytes).decode("utf-8")
        data_uri = f"data:model/gltf-binary;base64,{glb_b64}"

        anim_attrs = 'autoplay animation-name=""' if has_animation else ""
        if animation_name:
            anim_attrs = f'autoplay animation-name="{animation_name}"'

        html_code = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <script type="module" src="https://ajax.googleapis.com/ajax/libs/model-viewer/3.4.0/model-viewer.min.js"></script>
            <style>
                body {{
                    margin: 0;
                    padding: 0;
                    background-color: transparent;
                    font-family: -apple-system, sans-serif;
                }}
                .viewer-card {{
                    background: {COLOR_CARD};
                    border: 1.5px solid {COLOR_BORDER};
                    border-radius: 18px;
                    overflow: hidden;
                    box-shadow: 0 2px 6px rgba(0,0,0,0.05);
                    position: relative;
                }}
                model-viewer {{
                    width: 100%;
                    height: {height - 40}px;
                    --poster-color: transparent;
                }}
                .controls-hint {{
                    position: absolute;
                    bottom: 8px;
                    left: 0;
                    right: 0;
                    text-align: center;
                    font-size: 11px;
                    color: #555555;
                    pointer-events: none;
                    background: rgba(234, 233, 222, 0.7);
                    padding: 2px 0;
                }}
            </style>
        </head>
        <body>
            <div class="viewer-card">
                <model-viewer 
                    src="{data_uri}"
                    alt="3D model of {species_name}"
                    auto-rotate
                    camera-controls
                    shadow-intensity="1"
                    exposure="1.0"
                    interaction-prompt="auto"
                    {anim_attrs}>
                </model-viewer>
                <div class="controls-hint">
                    {render_icon("putar3d", 20, "biova-icon--button", "Rotasi 3D")}
                    Geser untuk memutar • Cubit untuk zoom
                </div>
            </div>
        </body>
        </html>
        """
        components.html(html_code, height=height)
    else:
        # Graceful fallback when 3D asset is not yet available
        st.markdown(
            f"""
            <div class="biova-card" style="text-align: center; padding: 24px 16px;">
                <div style="margin-bottom:6px;">{render_icon("kubus3d", 48, "biova-icon--heading", "Objek 3D")}</div>
                <div style="font-weight: 700; font-size: 14px; color: {COLOR_PRIMARY};">
                    Visualisasi 3D Belum Tersedia
                </div>
                <div style="font-size: 12px; color: #666666; margin-top: 4px;">
                    Model 3D (.glb) untuk <em>{species_name}</em> belum ditambahkan ke direktori aset.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
