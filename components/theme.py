"""BIOVA Theme & Custom CSS Component
Provides styling matching the design system and UI reference screenshots.
"""

import streamlit as st
from services.config import (
    COLOR_BG,
    COLOR_CARD,
    COLOR_PRIMARY,
    COLOR_SECONDARY,
    COLOR_HIGHLIGHT,
    COLOR_BORDER,
    COLOR_TEXT,
    COLOR_ERROR,
    COLOR_WHITE,
)


def apply_theme():
    """Injects custom CSS to style the Streamlit app to match BIOVA UI specifications."""
    css = f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&display=swap');

    /* Global reset and font */
    html, body, [class*="css"], [class*="st-"] {{
        font-family: 'Nunito', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
        color: {COLOR_TEXT};
    }}

    /* Main background */
    .stApp {{
        background-color: {COLOR_BG} !important;
    }}

    /* Hide default Streamlit decoration, header, and footer */
    header[data-testid="stHeader"] {{
        background: transparent !important;
        height: 0px !important;
        visibility: hidden !important;
    }}
    footer {{
        visibility: hidden !important;
        display: none !important;
    }}
    #MainMenu {{
        visibility: hidden !important;
    }}

    /* Center mobile app container */
    .block-container {{
        max-width: 440px !important;
        padding-top: 1.5rem !important;
        padding-bottom: 3.5rem !important;
        padding-left: 1.25rem !important;
        padding-right: 1.25rem !important;
        margin: 0 auto !important;
    }}

    /* Standard Cards */
    .biova-card {{
        background-color: {COLOR_CARD};
        border: 1.5px solid {COLOR_BORDER};
        border-radius: 18px;
        padding: 16px 18px;
        margin-bottom: 14px;
        box-shadow: 0 2px 6px rgba(38, 60, 43, 0.05);
    }}

    .biova-card-highlight {{
        background-color: {COLOR_PRIMARY};
        color: #FFFFFF !important;
        border-radius: 20px;
        padding: 18px 20px;
        margin-bottom: 14px;
        box-shadow: 0 4px 10px rgba(38, 60, 43, 0.15);
    }}

    .biova-card-highlight h1, 
    .biova-card-highlight h2, 
    .biova-card-highlight h3, 
    .biova-card-highlight p,
    .biova-card-highlight span {{
        color: #FFFFFF !important;
    }}

    /* Button Styling */
    div.stButton > button {{
        width: 100% !important;
        background-color: {COLOR_PRIMARY} !important;
        color: #FFFFFF !important;
        border-radius: 24px !important;
        border: none !important;
        padding: 10px 24px !important;
        font-weight: 700 !important;
        font-size: 15px !important;
        transition: all 0.2s ease-in-out !important;
        box-shadow: 0 2px 5px rgba(38, 60, 43, 0.12) !important;
    }}

    div.stButton > button:hover {{
        background-color: {COLOR_SECONDARY} !important;
        color: #FFFFFF !important;
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(38, 60, 43, 0.2) !important;
    }}

    div.stButton > button:active {{
        transform: translateY(0px);
    }}

    /* Secondary / Outline Button Variant */
    div.stButton > button[kind="secondary"] {{
        background-color: {COLOR_CARD} !important;
        color: {COLOR_PRIMARY} !important;
        border: 1.8px solid {COLOR_PRIMARY} !important;
        box-shadow: none !important;
    }}

    div.stButton > button[kind="secondary"]:hover {{
        background-color: #E2E1D4 !important;
        color: {COLOR_PRIMARY} !important;
    }}

    /* Form Inputs */
    .stTextInput > div > div > input {{
        background-color: {COLOR_WHITE} !important;
        border: 1.2px solid {COLOR_BORDER} !important;
        border-radius: 14px !important;
        color: {COLOR_TEXT} !important;
        padding: 10px 14px !important;
        font-size: 14px !important;
    }}

    .stTextInput > div > div > input:focus {{
        border-color: {COLOR_SECONDARY} !important;
        box-shadow: 0 0 0 1px {COLOR_SECONDARY} !important;
    }}

    /* Top decorative circles for Welcome screen */
    .welcome-decor-container {{
        position: relative;
        height: 90px;
        margin-bottom: 10px;
        overflow: hidden;
    }}
    .circle-large {{
        position: absolute;
        width: 120px;
        height: 120px;
        background-color: {COLOR_PRIMARY};
        border-radius: 50%;
        top: -45px;
        left: -35px;
        opacity: 0.95;
    }}
    .circle-medium {{
        position: absolute;
        width: 60px;
        height: 60px;
        background-color: {COLOR_SECONDARY};
        border-radius: 50%;
        top: -15px;
        left: 45%;
        opacity: 0.85;
    }}
    .circle-small {{
        position: absolute;
        width: 85px;
        height: 85px;
        background-color: {COLOR_PRIMARY};
        border-radius: 50%;
        top: -25px;
        right: -25px;
        opacity: 0.95;
    }}

    /* Badges */
    .biova-badge {{
        display: inline-block;
        background-color: {COLOR_HIGHLIGHT};
        color: {COLOR_PRIMARY};
        font-weight: 700;
        font-size: 12px;
        padding: 4px 12px;
        border-radius: 12px;
        margin-bottom: 8px;
    }}

    /* Progress Indicators for Quiz */
    .quiz-dot-row {{
        display: flex;
        gap: 8px;
        justify-content: center;
        align-items: center;
        margin-bottom: 16px;
    }}
    .quiz-dot {{
        width: 32px;
        height: 32px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 13px;
        background-color: {COLOR_CARD};
        border: 1.5px solid {COLOR_BORDER};
        color: {COLOR_TEXT};
    }}
    .quiz-dot.active {{
        background-color: {COLOR_PRIMARY};
        border-color: {COLOR_PRIMARY};
        color: #FFFFFF;
    }}
    .quiz-dot.done {{
        background-color: {COLOR_SECONDARY};
        border-color: {COLOR_SECONDARY};
        color: #FFFFFF;
    }}

    /* Feedback Discussion Box */
    .discussion-box {{
        background-color: {COLOR_HIGHLIGHT};
        border-left: 4px solid {COLOR_PRIMARY};
        border-radius: 12px;
        padding: 14px 16px;
        margin-top: 14px;
        margin-bottom: 14px;
    }}

    /* Custom Navigation Bar */
    .biova-navbar {{
        display: flex;
        justify-content: space-around;
        background-color: {COLOR_CARD};
        border: 1.5px solid {COLOR_BORDER};
        border-radius: 20px;
        padding: 8px 12px;
        margin-top: 20px;
        margin-bottom: 10px;
    }}

    /* Mascot Containers */
    .mascot-center {{
        display: flex;
        justify-content: center;
        align-items: center;
        margin-bottom: 14px;
    }}
    .mascot-center img {{
        max-width: 130px;
        height: auto;
    }}

    /* Error text */
    .biova-error {{
        color: {COLOR_ERROR};
        font-weight: 600;
        font-size: 13px;
        margin-top: 4px;
    }}

    /* Center aligned header */
    .text-center {{
        text-align: center;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
