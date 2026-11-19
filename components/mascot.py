"""BIOVA Mascot Component
Handles rendering the frog mascot across different emotions and contexts.
"""

from pathlib import Path
import streamlit as st
import base64
from services.config import MASCOT_DIR


def get_image_base64(path: Path) -> str:
    """Reads an image file and converts it to a base64 string for embedding."""
    if not path.exists():
        return ""
    with open(path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode("utf-8")


def render_mascot(mood: str = "happy", width: int = 140, center: bool = True):
    """Renders the mascot based on requested mood (happy, sad, celebrate, welcome)."""
    file_map = {
        "happy": MASCOT_DIR / "frog_success.png",
        "success": MASCOT_DIR / "frog_success.png",
        "sad": MASCOT_DIR / "frog_sad.png",
        "celebrate": MASCOT_DIR / "frog_celebrate.png",
        "welcome": MASCOT_DIR / "mascot_home_bottom.png",
    }

    img_path = file_map.get(mood, MASCOT_DIR / "frog_success.png")
    
    if img_path.exists():
        b64 = get_image_base64(img_path)
        align_style = "justify-content: center;" if center else ""
        html = f"""
        <div style="display: flex; {align_style} margin: 8px 0 14px 0;">
            <img src="data:image/png;base64,{b64}" width="{width}" style="max-width: 100%; height: auto; object-fit: contain;" alt="Mascot BIOVA ({mood})" />
        </div>
        """
        st.markdown(html, unsafe_allow_html=True)
    else:
        # High quality inline SVG Fallback
        color = "#416848" if mood != "sad" else "#5A7A60"
        eye_expression = "●   ●" if mood != "sad" else "╥   ╥"
        mouth = "◡" if mood != "sad" else "︵"
        svg = f"""
        <div style="display: flex; justify-content: center; margin: 10px 0;">
            <svg width="{width}" height="{width*0.8}" viewBox="0 0 100 80" xmlns="http://www.w3.org/2000/svg">
                <!-- Body -->
                <ellipse cx="50" cy="50" rx="35" ry="25" fill="{color}" />
                <!-- Eyes -->
                <circle cx="32" cy="30" r="12" fill="{color}" />
                <circle cx="68" cy="30" r="12" fill="{color}" />
                <circle cx="32" cy="30" r="9" fill="#FFFFFF" />
                <circle cx="68" cy="30" r="9" fill="#FFFFFF" />
                <circle cx="33" cy="31" r="5" fill="#263C2B" />
                <circle cx="67" cy="31" r="5" fill="#263C2B" />
                <!-- Cheeks -->
                <circle cx="28" cy="52" r="5" fill="#EFAAA0" opacity="0.6" />
                <circle cx="72" cy="52" r="5" fill="#EFAAA0" opacity="0.6" />
                <!-- Smile/Frown -->
                <path d="{'M 38 52 Q 50 64 62 52' if mood != 'sad' else 'M 38 60 Q 50 50 62 60'}" stroke="#263C2B" stroke-width="2.5" fill="none" stroke-linecap="round"/>
            </svg>
        </div>
        """
        st.markdown(svg, unsafe_allow_html=True)
