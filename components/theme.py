"""BIOVA Theme & Custom CSS Component
Provides responsive styling matching the design system for both desktop and mobile.
Carefully scoped to avoid overriding Streamlit's internal icon fonts.
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
    """Injects custom CSS to style the Streamlit app to match BIOVA UI specifications.
    Includes responsive breakpoints for desktop (>768px) and mobile (<=768px).
    Font selectors are scoped to avoid breaking Material Icons/Symbols used by Streamlit.
    """
    css = f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Nunito+Sans:wght@400;500;600;700;800;900&display=swap');

    :root {{
        --biova-font: "Nunito Sans", "Segoe UI", sans-serif;
        --biova-forest: #203E30;
        --biova-leaf: #568967;
        --biova-sage: #BBDD9C;
        --biova-light: #EFF8DF;
        --biova-cream: #F6F5EA;
        --biova-gold: #F7C957;
        --biova-space-8: 8px;
        --biova-space-12: 12px;
        --biova-space-14: 14px;
        --biova-space-16: 16px;
        --biova-space-20: 20px;
        --biova-space-24: 24px;
        --biova-space-30: 30px;
        --biova-space-32: 32px;
        --biova-radius-card: 22px;
        --biova-radius-category-card: 26px;
        --biova-radius-small: 16px;
        --biova-radius-button: 14px;
        --biova-shadow-card: 0 6px 18px rgba(32,62,48,.08);
        --biova-page-background: linear-gradient(135deg,#F8F7EE 0%,#EDF5E6 55%,#E4F0D8 100%);
    }}

    html, body {{
        max-width:100%;
        min-width:0;
        font-family:var(--biova-font) !important;
        font-size:16px;
        line-height:1.55;
    }}
    .stApp,
    [data-testid="stAppViewContainer"] {{
        max-width:100%;
        min-width:0;
        background:var(--biova-page-background) !important;
        background-attachment:fixed;
        font-family:var(--biova-font) !important;
    }}
    .stApp div[data-testid="stMarkdownContainer"],
    [data-testid="stMarkdownContainer"] :not(span[class*="material"]):not([data-testid="stIconMaterial"]) {{
        font-family:var(--biova-font) !important;
    }}
    /* Target only specific Streamlit text containers */
    .stMarkdown, .stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3,
    .stMarkdown h4, .stMarkdown h5, .stMarkdown h6, .stMarkdown li, .stMarkdown span,
    .stText, .stCode,
    .stRadio label span,
    .stSelectbox label span,
    .stTextInput label span,
    .stTextArea label span,
    .stNumberInput label span,
    .stAlert p, .stAlert span,
    div.stButton > button,
    .stFormSubmitButton > button,
    .stDownloadButton > button {{
        font-family:var(--biova-font) !important;
    }}
    .stMarkdown h1 {{
        font-size:34px !important;
        line-height:1.2 !important;
    }}
    .stMarkdown h2 {{
        font-size:28px !important;
        line-height:1.25 !important;
    }}
    .stMarkdown h3 {{
        font-size:22px !important;
        line-height:1.25 !important;
    }}
    .stMarkdown h4 {{
        font-size:22px !important;
        line-height:1.25 !important;
    }}
    .stMarkdown p,
    .stMarkdown li {{
        font-size:16px !important;
        line-height:1.55 !important;
    }}

    /* ===== PROTECT ICON FONTS =====
       Ensure Material Icons / Symbols are never overridden.
       These selectors restore the correct icon font on internal
       Streamlit elements that render glyphs.
    */
    [data-testid="stIconMaterial"],
    span[class*="material-icons"],
    span[class*="material-symbols"],
    .material-icons,
    .material-symbols-rounded,
    .material-symbols-outlined,
    [data-testid="stFileUploader"] button span[class*="material"],
    [data-testid="stFileUploader"] button span[aria-hidden="true"],
    .stTextInput span[class*="material"],
    .stTextInput button span,
    [data-testid="stPasswordInput"] button span,
    [data-testid="baseButton-headerNoPadding"] span,
    button[kind="icon"] span {{
        font-family: 'Material Symbols Rounded', 'Material Icons', 'Material Icons Round', 'Material Symbols Outlined', sans-serif !important;
        font-style: normal !important;
        font-weight: normal !important;
        -webkit-font-feature-settings: 'liga' !important;
        font-feature-settings: 'liga' !important;
    }}

    /* ===== HIDE STREAMLIT CHROME ===== */
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
    [data-testid="stToolbar"] {{
        display: none !important;
    }}

    /* ===== RESPONSIVE CONTAINER ===== */
    /* Desktop default */
    .block-container {{
        max-width: 1160px !important;
        width: 100% !important;
        min-width: 0 !important;
        box-sizing: border-box !important;
        padding-top: 24px !important;
        padding-bottom: 48px !important;
        padding-left: 24px !important;
        padding-right: 24px !important;
        margin: 0 auto !important;
    }}

    /* Mobile (<= 768px) */
    @media (max-width: 768px) {{
        .block-container {{
            max-width: 100% !important;
            padding-top: 20px !important;
            padding-bottom: 40px !important;
            padding-left: 20px !important;
            padding-right: 20px !important;
        }}
    }}
    @media (max-width: 767px) {{
        .stMarkdown h1 {{ font-size:28px !important; }}
        .stMarkdown h2 {{ font-size:24px !important; }}
        .stMarkdown h3 {{ font-size:20px !important; }}
        .stMarkdown h4 {{ font-size:18px !important; }}
        .stMarkdown p,
        .stMarkdown li {{ font-size:15px !important; }}
    }}

    /* Large desktop (>= 1200px) */
    @media (min-width: 1200px) {{
        .block-container {{
            max-width: 1160px !important;
            padding-left: 24px !important;
            padding-right: 24px !important;
        }}
    }}

    /* ===== STANDARD CARDS ===== */
    .biova-card {{
        background-color: {COLOR_CARD};
        border: 1.5px solid {COLOR_BORDER};
        border-radius: 20px;
        padding: 20px;
        margin-bottom: 16px;
        box-shadow: 0 2px 6px rgba(38, 60, 43, 0.05);
        box-sizing: border-box;
        max-width: 100%;
        min-width: 0;
        overflow-wrap: anywhere;
        transition: transform 200ms ease, box-shadow 200ms ease, border-color 200ms ease;
    }}
    @media (hover: hover) and (pointer: fine) {{
        .biova-card:hover {{
            transform: translateY(-3px);
            border-color: #558B65;
            box-shadow: 0 8px 18px rgba(32, 62, 48, 0.10);
        }}
    }}

    .st-key-biova-panorama-banner {{
        border:1px solid rgba(187,221,156,.28);
        background:linear-gradient(115deg,var(--biova-forest) 0%,#355D45 55%,var(--biova-leaf) 100%);
        color: #FFFFFF !important;
        border-radius:var(--biova-radius-card);
        padding:24px;
        margin:16px auto;
        box-shadow:var(--biova-shadow-card);
        animation:biovaPanoramaFade 260ms ease-out;
        gap:0;
    }}
    .st-key-biova-panorama-banner [data-testid="stHorizontalBlock"] {{
        display:grid !important;
        grid-template-columns:minmax(0, 1fr) minmax(0, 0.9fr);
        align-items:center;
        gap:28px;
    }}
    .st-key-biova-panorama-banner [data-testid="stColumn"] {{
        width:auto !important;
        min-width:0 !important;
        flex:none !important;
    }}
    .st-key-biova-panorama-banner [data-testid="stColumn"]:first-child {{
        align-self:stretch;
    }}
    .stVerticalBlock.st-key-biova-panorama-copy[data-testid="stVerticalBlock"] {{
        display:flex;
        flex-direction:column;
        justify-content:center;
        align-items:flex-start;
        gap:16px;
        height:100%;
        min-width:0;
    }}
    .st-key-biova-panorama-copy [data-testid="stElementContainer"] {{
        width:100%;
    }}
    .biova-panorama-text {{
        display:flex;
        flex-direction:column;
        align-items:flex-start;
        gap:8px;
    }}
    .st-key-biova-panorama-copy .biova-panorama-title {{
        margin:0;
        color:#FFF9EB;
        font-size:24px !important;
        line-height:1.25;
        font-weight:800;
    }}
    .st-key-biova-panorama-copy .biova-panorama-description {{
        max-width:520px;
        margin:0;
        color:rgba(255,249,235,.88);
        font-size:16px !important;
        line-height:1.5;
    }}
    .st-key-biova-panorama-banner .st-key-btn_dash_panorama div.stButton > button {{
        width:max-content !important;
        max-width:100%;
        height:48px;
        min-height:48px;
        padding:0 24px !important;
        border:1px solid #F7C957 !important;
        border-radius:12px !important;
        background:#F7C957 !important;
        color:#203E30 !important;
        box-shadow:0 4px 12px rgba(164,125,34,.15);
        transition:background-color 200ms ease, box-shadow 200ms ease;
    }}
    .st-key-biova-panorama-banner .st-key-btn_dash_panorama div.stButton > button:hover {{
        border-color:#B88925 !important;
        background:#EAB83F !important;
        box-shadow:0 7px 16px rgba(164,125,34,.20);
    }}
    .st-key-biova-panorama-banner .st-key-btn_dash_panorama div.stButton > button:focus-visible {{
        outline:3px solid rgba(255,249,235,.88) !important;
        outline-offset:3px;
    }}
    .st-key-biova-panorama-banner .st-key-btn_dash_panorama {{
        width:max-content !important;
        max-width:100%;
    }}
    .biova-panorama-art {{
        position:relative;
        height:190px;
        max-height:190px;
        width:100%;
        overflow:hidden;
        border-radius:16px;
        background:linear-gradient(180deg,rgba(187,221,156,.12),rgba(255,249,235,.04));
        opacity:0.96;
        transition:opacity 200ms ease;
    }}
    .biova-panorama-art__sun {{
        position:absolute;
        top:17%;
        right:20%;
        width:34px;
        height:34px;
        border-radius:50%;
        background:#F7C957;
        box-shadow:none;
    }}
    .biova-panorama-art__ridge {{
        position:absolute;
        display:block;
        clip-path:polygon(0 100%,18% 58%,34% 72%,52% 30%,68% 58%,82% 24%,100% 100%);
    }}
    .biova-panorama-art__ridge--back {{
        right:-3%;
        bottom:26%;
        width:94%;
        height:60%;
        background:#568967;
        opacity:.82;
    }}
    .biova-panorama-art__ridge--front {{
        left:-6%;
        bottom:-10%;
        width:112%;
        height:62%;
        background:#8FB87C;
        opacity:.96;
    }}
    .biova-panorama-art__water {{
        position:absolute;
        left:10%;
        bottom:-2%;
        width:58%;
        height:20%;
        border-radius:50% 50% 0 0;
        background:rgba(232,239,227,.32);
        opacity:.72;
    }}
    @keyframes biovaPanoramaFade {{
        from {{ opacity:0; }}
        to {{ opacity:1; }}
    }}
    .biova-leaderboard {{
        max-width:760px;
        margin:0 auto;
    }}
    .biova-leaderboard-row {{
        box-sizing:border-box;
        width:100%;
        max-width:760px;
        min-height:56px;
        display:grid;
        grid-template-columns:42px minmax(0,1fr) max-content;
        align-items:center;
        gap:12px;
        margin:0 auto 6px;
        padding:8px 14px;
        border:1px solid rgba(53,93,69,.10);
        border-radius:12px;
        background:#FFFDF7;
    }}
    .biova-leaderboard-row--alternate {{
        background:#F0F5E9;
    }}
    .biova-leaderboard-row--top3 {{
        border-color:rgba(247,201,87,.48);
        background:#FFF8E3;
    }}
    .biova-leaderboard-row--me {{
        border-color:#8FB87C;
        background:#E8F0D8;
    }}
    .biova-leaderboard-stars,
    .biova-leaderboard-my-rank {{
        display:flex;
        align-items:center;
    }}
    .biova-leaderboard-rank {{
        width:42px;
        min-width:42px;
        display:flex;
        justify-content:center;
        align-items:center;
        color:#203E30;
        font-size:14px;
        font-weight:850;
    }}
    .biova-leaderboard-name {{
        min-width:0;
        overflow:hidden;
        color:#203E30;
        font-size:15px;
        font-weight:750;
        text-overflow:ellipsis;
        white-space:nowrap;
    }}
    .biova-leaderboard-stars {{
        gap:5px;
        color:#203E30;
        font-size:15px;
        font-weight:850;
        white-space:nowrap;
    }}
    .biova-leaderboard-my-rank {{
        min-height:50px;
        justify-content:space-between;
        gap:10px;
        margin:8px auto 12px;
        padding:8px 10px;
        border:1px solid #BFCFBA;
        border-radius:12px;
        background:#E8EFE3;
        color:#203E30;
        font-size:14px;
    }}
    .biova-leaderboard-heading {{
        margin:0 auto 20px;
        text-align:center;
    }}
    .biova-leaderboard-heading__icon {{
        margin-bottom:8px;
    }}
    .biova-leaderboard-heading h2 {{
        margin:0;
        font-size:24px !important;
        font-weight:800;
        line-height:1.25;
    }}
    .biova-leaderboard-heading p {{
        margin:8px 0 0;
        color:#526258;
        font-size:16px !important;
        line-height:1.5;
    }}
    .biova-leaderboard-page {{
        padding:8px;
        color:var(--biova-forest);
        font-size:14px;
        font-weight:700;
        text-align:center;
    }}
    .biova-leaderboard-my-stars {{
        display:flex;
        align-items:center;
        gap:5px;
        font-weight:850;
        white-space:nowrap;
    }}
    @media (max-width:767px) {{
        .st-key-biova-panorama-banner {{
            padding:24px;
        }}
        .st-key-biova-panorama-banner [data-testid="stHorizontalBlock"] {{
            grid-template-columns:minmax(0,1fr);
            gap:16px;
        }}
        .st-key-biova-panorama-banner [data-testid="stColumn"] {{
            width:100% !important;
        }}
        .stVerticalBlock.st-key-biova-panorama-copy[data-testid="stVerticalBlock"] {{
            height:auto;
        }}
        .biova-leaderboard-row {{
            grid-template-columns:36px minmax(0,1fr) max-content;
            gap:8px;
            padding:8px 10px;
        }}
        .biova-panorama-art {{
            height:150px;
            max-height:190px;
        }}
    }}

    /* ===== BUNDLED 3D ICONS ===== */
    .biova-icon {{
        display: inline-block;
        flex: 0 0 auto;
        object-fit: contain;
        vertical-align: middle;
    }}
    .biova-icon--nav {{ margin: 0 auto 2px; }}
    .biova-icon--category {{ margin: 0; }}
    .biova-icon--reward {{ margin-right: 5px; }}
    .biova-icon--button {{ margin-right: 6px; }}
    .biova-icon--heading {{ margin-bottom: 4px; }}
    .biova-icon-fallback {{
        display: inline-flex;
        flex: 0 0 auto;
        align-items: center;
        justify-content: center;
        border-radius: 8px;
        background: {COLOR_HIGHLIGHT};
        color: {COLOR_PRIMARY};
        font-weight: 800;
        vertical-align: middle;
    }}
    .biova-field-label {{
        display: flex;
        align-items: center;
        gap: 8px;
        margin: 0 0 6px;
        color: {COLOR_PRIMARY};
        font-size: 14px;
        font-weight: 800;
    }}
    .biova-icon-action {{
        display: flex;
        align-items: center;
        justify-content: center;
        min-height: 44px;
    }}
    .st-key-biova-content-back [data-testid="stVerticalBlock"] {{
        align-items:flex-start;
        gap:0;
    }}
    .st-key-biova-content-back [data-testid="stElementContainer"] {{
        width:max-content !important;
        flex:0 0 auto !important;
    }}
    .st-key-biova-content-back div.stButton > button {{
        width:max-content !important;
        height:40px !important;
        min-height:40px !important;
        padding:0 16px !important;
        border:1px solid #A9C4AC !important;
        border-radius:12px !important;
        background:#FFF9EB !important;
        color:#203E30 !important;
        box-shadow:none !important;
        font-size:14px !important;
        font-weight:600 !important;
        line-height:1 !important;
        transition:background-color 200ms ease, border-color 200ms ease, color 200ms ease !important;
    }}
    .st-key-biova-content-back div.stButton > button:hover {{
        border-color:#A9C4AC !important;
        background:#E4F0D8 !important;
        color:#203E30 !important;
        box-shadow:none !important;
    }}

    /* ===== BUTTON STYLING ===== */
    div.stButton > button {{
        width: 100%;
        background-color: {COLOR_PRIMARY} !important;
        color: #FFFFFF !important;
        min-height:46px !important;
        border-radius: var(--biova-radius-button) !important;
        border: none !important;
        padding: 10px 24px !important;
        font-weight: 700 !important;
        font-size: 15px !important;
        transition: all 0.2s ease-in-out !important;
        box-shadow: 0 2px 5px rgba(38, 60, 43, 0.12) !important;
        cursor: pointer !important;
    }}

    div.stButton > button:active,
    .stFormSubmitButton > button:active {{
        transform: scale(0.99) !important;
    }}
    div.stButton > button:focus-visible,
    .stFormSubmitButton > button:focus-visible {{
        outline: 3px solid rgba(241, 198, 91, 0.75) !important;
        outline-offset: 2px !important;
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

    /* Secondary / Outline Button */
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

    /* ===== FORM INPUTS ===== */
    .stTextInput [data-testid="stTextInputRootElement"] {{
        background-color: {COLOR_WHITE} !important;
        border: 1.2px solid {COLOR_BORDER} !important;
        border-radius: 14px !important;
    }}

    .stTextInput > div > div > input {{
        background-color: transparent !important;
        border: 0 !important;
        border-radius: 14px !important;
        color: {COLOR_TEXT} !important;
        padding: 10px 14px !important;
        font-size: 15px !important;
        font-family: var(--biova-font) !important;
    }}

    .stTextInput [data-testid="stTextInputRootElement"]:focus-within {{
        border-color: {COLOR_SECONDARY} !important;
        box-shadow: 0 0 0 1px {COLOR_SECONDARY} !important;
    }}

    /* ===== AUTH FORMS ===== */
    [data-testid="stForm"] {{
        box-sizing: border-box !important;
        margin-bottom: 12px;
        padding: 18px !important;
        background-color: {COLOR_CARD} !important;
        border: 1.5px solid {COLOR_BORDER} !important;
        border-radius: 18px !important;
        max-width: 480px !important;
        margin-left: auto !important;
        margin-right: auto !important;
    }}

    /* ===== PASSWORD INPUT — keep toggle icon usable ===== */
    /* Give password field extra right padding so text doesn't collide with the eye icon */
    .stTextInput input[type="password"] {{
        padding-right: 42px !important;
    }}
    /* Password visibility toggle button positioning */
    [data-testid="stPasswordInput"] button,
    .stTextInput button[kind="icon"] {{
        position: absolute !important;
        right: 4px !important;
        top: 50% !important;
        transform: translateY(-50%) !important;
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        min-height: unset !important;
        width: 36px !important;
        height: 36px !important;
        padding: 6px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }}
    [data-testid="stPasswordInput"] [data-testid="stTextInputRootElement"] {{
        position: relative;
    }}
    [data-testid="stPasswordInput"] > div,
    .stTextInput > div > div {{
        min-height: 44px;
    }}

    /* ===== FORM SUBMIT BUTTON ===== */
    .stFormSubmitButton > button {{
        width: 100% !important;
        background-color: {COLOR_PRIMARY} !important;
        color: #FFFFFF !important;
        min-height:46px !important;
        border-radius: var(--biova-radius-button) !important;
        border: none !important;
        padding: 10px 24px !important;
        font-weight: 700 !important;
        font-size: 15px !important;
        box-shadow: 0 2px 5px rgba(38, 60, 43, 0.12) !important;
    }}

    .stFormSubmitButton > button:hover {{
        background-color: {COLOR_SECONDARY} !important;
        color: #FFFFFF !important;
    }}

    /* ===== FILE UPLOADER — preserve native icons & functionality ===== */
    [data-testid="stFileUploader"] label span {{
        font-family: var(--biova-font) !important;
    }}
    /* Do NOT restyle the uploader button's internal icon span —
       let Streamlit render the upload icon with its own Material font. */
    [data-testid="stFileUploader"] section {{
        border: 1.5px dashed {COLOR_BORDER} !important;
        border-radius: 14px !important;
        padding: 14px !important;
        background-color: {COLOR_WHITE} !important;
    }}

    /* ===== CAMERA INPUT ===== */
    [data-testid="stCameraInput"] > div {{
        border-radius: 14px !important;
        overflow: hidden;
    }}

    /* ===== RADIO BUTTONS ===== */
    .stRadio > div[role="radiogroup"] > label {{
        background-color: {COLOR_CARD} !important;
        border: 1.5px solid {COLOR_BORDER} !important;
        border-radius: 12px !important;
        padding: 10px 14px !important;
        margin-bottom: 6px !important;
        cursor: pointer !important;
        transition: all 0.15s ease !important;
    }}
    .stRadio > div[role="radiogroup"] > label:hover {{
        border-color: {COLOR_SECONDARY} !important;
        background-color: #E2E1D4 !important;
    }}
    .stRadio > div[role="radiogroup"] > label[data-checked="true"] {{
        border-color: {COLOR_PRIMARY} !important;
        background-color: {COLOR_HIGHLIGHT} !important;
    }}

    /* ===== DOWNLOAD BUTTON ===== */
    .stDownloadButton > button {{
        width: 100% !important;
        background-color: {COLOR_PRIMARY} !important;
        color: #FFFFFF !important;
        border-radius: 24px !important;
        border: none !important;
        padding: 10px 24px !important;
        font-weight: 700 !important;
        font-size: 14px !important;
    }}
    .stDownloadButton > button:hover {{
        background-color: {COLOR_SECONDARY} !important;
    }}

    /* ===== WELCOME DECORATIVE CIRCLES ===== */
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

    /* ===== BADGES ===== */
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

    /* ===== QUIZ PROGRESS DOTS ===== */
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

    /* ===== DISCUSSION BOX ===== */
    .discussion-box {{
        background-color: {COLOR_HIGHLIGHT};
        border-left: 4px solid {COLOR_PRIMARY};
        border-radius: 12px;
        padding: 14px 16px;
        margin-top: 14px;
        margin-bottom: 14px;
    }}

    /* ===== BOTTOM NAVIGATION ===== */
    .st-key-biova-bottom-nav [data-testid="stHorizontalBlock"] {{
        background-color: var(--biova-cream);
        border: 1px solid var(--biova-forest);
        border-radius: var(--biova-radius-small);
        margin-top: 24px;
        margin-bottom: 10px;
        padding: 8px;
        gap: 8px !important;
        flex-wrap: nowrap !important;
        box-sizing: border-box;
    }}
    .st-key-biova-bottom-nav [data-testid="stHorizontalBlock"] [data-testid="stColumn"] {{
        min-width: 0 !important;
        flex: 1 1 0% !important;
    }}
    .st-key-biova-bottom-nav [data-testid="stHorizontalBlock"] .biova-icon--nav {{
        display: block;
        margin: 0 auto 1px;
    }}
    .st-key-biova-bottom-nav [data-testid="stHorizontalBlock"] .biova-icon-action {{
        min-height: 23px;
    }}
    .st-key-nav_dashboard div.stButton > button,
    .st-key-nav_learn div.stButton > button,
    .st-key-nav_leaderboard div.stButton > button,
    .st-key-nav_profile div.stButton > button {{
        width: 100% !important;
        min-height: 48px !important;
        padding: 6px 4px !important;
        border: 1.5px solid {COLOR_PRIMARY} !important;
        border-radius: 14px !important;
        box-shadow: none !important;
        font-size: 14px !important;
        font-weight: 700 !important;
        line-height: 1.2 !important;
        white-space: normal !important;
    }}
    .st-key-nav_dashboard div.stButton > button[kind="primary"],
    .st-key-nav_learn div.stButton > button[kind="primary"],
    .st-key-nav_leaderboard div.stButton > button[kind="primary"],
    .st-key-nav_profile div.stButton > button[kind="primary"] {{
        background-color: {COLOR_PRIMARY} !important;
        color: #FFFFFF !important;
    }}
    .st-key-nav_dashboard div.stButton > button[kind="secondary"],
    .st-key-nav_learn div.stButton > button[kind="secondary"],
    .st-key-nav_leaderboard div.stButton > button[kind="secondary"],
    .st-key-nav_profile div.stButton > button[kind="secondary"] {{
        background-color: {COLOR_CARD} !important;
        color: {COLOR_PRIMARY} !important;
    }}

    /* ===== ERROR TEXT ===== */
    .biova-error {{
        color: {COLOR_ERROR};
        font-weight: 600;
        font-size: 13px;
        margin-top: 4px;
    }}

    /* ===== UTILITY CLASSES ===== */
    .text-center {{
        text-align: center;
    }}

    /* ===== ALERTS / INFO MESSAGES ===== */
    .stAlert {{
        border-radius: 14px !important;
    }}
    .stAlert p, .stAlert span {{
        font-family: var(--biova-font) !important;
    }}
    .stCaption,
    [data-testid="stCaptionContainer"] {{
        font-family:var(--biova-font) !important;
        font-size:14px !important;
        line-height:1.4 !important;
    }}

    /* ===== TABS ===== */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 8px;
    }}
    .stTabs [data-baseweb="tab"] {{
        font-family: var(--biova-font) !important;
        font-weight: 700 !important;
        border-radius: 12px 12px 0 0 !important;
    }}

    /* ===== MOBILE RESPONSIVE TUNING ===== */
    @media (max-width: 768px) {{
        div.stButton > button {{
            padding: 10px 16px !important;
            font-size: 15px !important;
            min-height: 46px !important;
        }}

        .st-key-biova-bottom-nav [data-testid="stHorizontalBlock"] {{
            gap: 6px !important;
            padding: 6px 4px;
        }}
        .st-key-nav_dashboard div.stButton > button,
        .st-key-nav_learn div.stButton > button,
        .st-key-nav_leaderboard div.stButton > button,
        .st-key-nav_profile div.stButton > button {{
            min-height: 46px !important;
            padding: 4px 2px !important;
            font-size: 14px !important;
            white-space: normal !important;
            min-width: 0 !important;
        }}
        .st-key-biova-bottom-nav .biova-icon--nav {{
            width: 22px !important;
            height: 22px !important;
        }}

        [data-testid="stHorizontalBlock"] {{
            gap: 8px !important;
        }}

        .quiz-dot {{
            width: 28px;
            height: 28px;
            font-size: 12px;
        }}

        .welcome-decor-container {{
            height: 70px;
        }}
        .circle-large {{
            width: 100px;
            height: 100px;
            top: -40px;
            left: -30px;
        }}
        .circle-medium {{
            width: 50px;
            height: 50px;
        }}
        .circle-small {{
            width: 70px;
            height: 70px;
            top: -20px;
            right: -20px;
        }}
    }}

    /* ===== NO HORIZONTAL OVERFLOW ===== */
    .block-container,
    [data-testid="stVerticalBlock"],
    [data-testid="stHorizontalBlock"],
    [data-testid="column"],
    [data-testid="stIFrame"],
    .stMarkdown {{
        max-width: 100%;
        min-width: 0;
        box-sizing: border-box;
    }}
    .biova-icon,
    .stImage img,
    iframe, svg, model-viewer {{
        max-width: 100%;
        box-sizing: border-box;
    }}

    /* ===== REUSABLE ICON SYSTEM ===== */
    .biova-icon-input {{ width:22px !important; height:22px !important; object-fit:contain; }}
    .biova-icon-category {{ width:64px !important; height:64px !important; object-fit:contain; }}
    .biova-icon-result {{ width:104px !important; height:104px !important; object-fit:contain; }}
    .biova-icon-medal {{ width:32px !important; height:32px !important; object-fit:contain; }}
    .biova-icon--nav {{ width:22px !important; height:22px !important; object-fit:contain; }}
    .biova-mascot {{ object-fit:contain; width:300px; max-width:100%; }}
    .biova-icon-enter {{
        animation: biova-icon-enter 400ms ease-out both;
    }}
    @keyframes biova-icon-enter {{
        from {{ opacity: 0; transform: translateY(8px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}

    .biova-animal-result-icon {{
        width:104px;
        height:104px;
        margin: 0 auto 8px;
        display:flex;
        align-items:center;
        justify-content:center;
    }}

    /* ===== NATURE HERO ===== */
    .biova-welcome-copy {{
        max-width: 520px;
    }}
    .biova-welcome-copy h1 {{
        color: {COLOR_PRIMARY};
        font-size: 42px;
        line-height: 1.08;
        letter-spacing: -0.8px;
        margin: 8px 0 6px;
        font-weight: 900;
    }}
    .biova-welcome-copy h2 {{
        color: {COLOR_SECONDARY};
        font-size: 21px;
        margin: 0 0 14px;
        font-weight: 800;
    }}
    .biova-welcome-copy p {{
        color: #66776C;
        font-size: 16px;
        line-height: 1.55;
        margin: 0 0 14px;
    }}
    .biova-kicker {{
        display: inline-flex;
        align-items: center;
        gap: 6px;
        color: {COLOR_PRIMARY};
        font-size: 13px;
        font-weight: 900;
        letter-spacing: 1px;
        text-transform: uppercase;
    }}
    .biova-kicker span {{
        color: {COLOR_SECONDARY};
        font-weight: 700;
    }}
    .biova-welcome-mascot {{
        width: 300px;
        max-width: 100%;
        margin: 0 auto;
        display: flex;
        align-items: center;
        justify-content: center;
        animation: biova-float 3.6s ease-in-out infinite alternate;
    }}
    .biova-welcome-mascot img {{
        width: 300px;
        max-width: 100%;
        height: auto;
        object-fit: contain;
        display: block;
    }}
    .biova-login-mascot {{
        display:flex;
        align-items:center;
        justify-content:center;
        margin:2px 0 8px;
    }}
    .biova-login-mascot__image {{
        width:112px !important;
        height:112px !important;
        object-fit:contain;
    }}
    .biova-auth-heading {{
        margin:0 auto 14px !important;
    }}
    @keyframes biova-float {{
        from {{ transform: translateY(0); }}
        to {{ transform: translateY(-7px); }}
    }}
    @media (prefers-reduced-motion: reduce) {{
        .biova-welcome-mascot {{
            animation: none;
        }}
        .biova-icon-enter,
        [data-testid="stMainBlockContainer"],
        [data-testid="stVerticalBlock"],
        .biova-card,
        div.stButton > button,
        .stFormSubmitButton > button {{
            animation: none !important;
            transition: none !important;
        }}
    }}

    /* ===== COMPACT LANGUAGE SWITCHER ===== */
    [data-testid="stSegmentedControl"] button {{
        min-height: 36px !important;
        padding: 6px 10px !important;
    }}

    /* ===== AUTH ===== */
    .biova-login-divider {{
        max-width: 480px;
        height: 24px;
        margin: 8px auto 10px;
        display: grid;
        grid-template-columns: 1fr auto 1fr;
        align-items: center;
        gap: 10px;
        color: #66776C;
        font-size: 12px;
    }}
    .biova-login-divider span {{
        height: 1px;
        background: {COLOR_BORDER};
    }}
    .biova-google-logo {{
        height: 48px;
        display: flex;
        align-items: center;
        justify-content: center;
    }}
    .biova-header-user {{
        display:flex;
        align-items:center;
        gap:12px;
        height:48px;
        min-height:48px;
        max-height:48px;
        min-width:0;
        font-family:var(--biova-font) !important;
    }}
    .biova-header-user-text {{
        display:flex;
        flex-direction:column;
        justify-content:center;
        gap:2px;
        margin:0;
        min-width:0;
    }}
    .biova-header-avatar {{
        width:44px;
        height:44px;
        display:flex;
        align-items:center;
        justify-content:center;
        flex:0 0 44px;
    }}
    .biova-header-avatar img {{
        box-sizing:border-box;
        width:44px;
        height:44px;
        max-width:44px;
        max-height:44px;
        border-radius:50%;
        object-fit:cover;
        border:2px solid #C8E6A0;
        transition:transform 180ms ease, box-shadow 180ms ease;
    }}
    .biova-header-caption {{
        margin:0;
        font-size:13px;
        color:#66776C;
        line-height:1.3;
        white-space:nowrap;
        overflow:hidden;
        text-overflow:ellipsis;
        font-family:var(--biova-font) !important;
    }}
    .biova-header-name {{
        margin:0;
        font-size:16px;
        font-weight:800;
        color:{COLOR_PRIMARY};
        line-height:1.2;
        overflow:hidden;
        text-overflow:ellipsis;
        white-space:nowrap;
        font-family:var(--biova-font) !important;
    }}
    .st-key-biova-header {{
        width:100%;
        box-sizing:border-box;
        min-height:66px;
        margin:0 auto 16px;
        padding:9px 20px;
        border:1px solid rgba(86,137,103,.16);
        border-radius:var(--biova-radius-small);
        background:linear-gradient(120deg, rgba(255,255,255,.82), rgba(187,221,156,.20));
        box-shadow:var(--biova-shadow-card);
        backdrop-filter:blur(8px);
    }}
    .stVerticalBlock.st-key-biova-header[data-testid="stVerticalBlock"] {{
        display:flex;
        flex-direction:row;
        flex-wrap:nowrap;
        align-items:center;
        justify-content:space-between;
        gap:12px;
    }}
    .stVerticalBlock.st-key-biova-header[data-testid="stVerticalBlock"] > [data-testid="stElementContainer"]:first-child {{
        box-sizing:border-box;
        display:flex;
        flex:1 1 auto;
        align-items:center;
        width:auto;
        height:48px;
        min-height:48px;
        max-height:48px;
        min-width:0;
        margin:0;
    }}
    .stVerticalBlock.st-key-biova-header[data-testid="stVerticalBlock"] > [data-testid="stElementContainer"]:last-child {{
        box-sizing:border-box;
        display:flex;
        flex:0 0 auto;
        align-items:center;
        justify-content:flex-end;
        width:max-content;
        height:48px;
        min-height:48px;
        max-height:48px;
        max-width:100%;
        min-width:0;
        margin:0;
    }}
    .st-key-biova-public-header {{
        width:100%;
        margin:0 auto 12px;
        gap:0;
    }}
    .st-key-biova-public-header [data-testid="stHorizontalBlock"] {{
        width:100%;
        align-items:center;
        justify-content:space-between;
        flex-wrap:nowrap !important;
    }}
    .st-key-biova-public-header [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:first-child {{
        flex:1 1 0% !important;
        min-width:0 !important;
    }}
    .st-key-biova-public-header [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:last-child {{
        flex:0 0 104px !important;
        width:104px !important;
        min-width:104px !important;
        align-items:center;
    }}
    .st-key-biova-public-header [data-testid="stElementContainer"] {{
        width:max-content !important;
        height:48px;
        flex:0 0 auto !important;
        display:flex;
        align-items:center;
    }}
    .st-key-biova-public-header [data-testid="stSegmentedControl"] {{
        width:104px;
        height:48px;
    }}
    .st-key-biova-public-header [data-testid="stSegmentedControl"] button {{
        box-sizing:border-box;
        width:48px !important;
        height:48px !important;
        min-height:48px !important;
        padding:0 !important;
    }}
    .st-key-biova-public-header [class*="st-key-biova_language_control_"] {{
        min-height:0;
        width:104px;
        min-width:104px;
    }}
    @media (hover:hover) and (pointer:fine) {{
        .biova-header-avatar img:hover {{
            transform:scale(1.04);
            box-shadow:0 3px 10px rgba(32,62,48,.18);
        }}
    }}
    .stVerticalBlock.st-key-biova-header-actions[data-testid="stVerticalBlock"] {{
        width:max-content;
        max-width:100%;
        min-width:0;
        flex:0 0 auto;
        height:48px;
        min-height:48px;
        max-height:48px;
        margin:0;
        display:flex;
        flex-direction:row;
        flex-wrap:nowrap;
        align-items:center;
        justify-content:flex-end;
        gap:8px;
    }}
    .st-key-biova-header-actions [data-testid="stElementContainer"] {{
        width:auto !important;
        box-sizing:border-box;
        height:48px;
        min-height:48px;
        max-height:48px;
        margin:0;
        flex:0 0 auto !important;
        display:flex !important;
        align-items:center !important;
        justify-content:center;
    }}
    .biova-header-stars {{
        box-sizing:border-box;
        height:48px;
        min-height:48px;
        max-height:48px;
        width:max-content;
        margin:0;
        border-radius:999px;
        padding:0 14px;
        display:inline-flex;
        align-items:center;
        justify-content:center;
        vertical-align:middle;
        gap:8px;
        background:{COLOR_CARD};
        border:1px solid {COLOR_BORDER};
        box-shadow:0 2px 8px rgba(32,62,48,.05);
        font-weight:700;
        color:{COLOR_PRIMARY};
        font-size:14px;
        white-space:nowrap;
        font-family:var(--biova-font) !important;
    }}
    .biova-header-stars .biova-icon--reward {{
        width:18px !important;
        height:18px !important;
        flex:0 0 18px;
        margin-right:0;
    }}
    .biova-star-count {{
        display:inline-block;
        min-width:12px;
        text-align:center;
    }}
    .biova-star-count.is-changing {{
        animation:biovaStarPop 220ms ease-out;
    }}
    [class*="st-key-biova_language_control_"] {{
        width:104px;
        min-width:104px;
        margin-left:0;
    }}
    [class*="st-key-biova_language_control_"] [data-testid="stSegmentedControl"] {{
        width:104px;
        height:48px;
        min-height:48px;
        display:flex;
        gap:8px;
        border:0;
        border-radius:12px;
        background:transparent;
        box-shadow:none;
    }}
    [class*="st-key-biova_language_control_"] button {{
        box-sizing:border-box;
        flex:0 0 48px;
        width:48px;
        height:48px !important;
        min-height:48px !important;
        max-height:48px !important;
        padding:0 !important;
        margin:0 !important;
        border:1px solid #BFCFBA !important;
        border-radius:10px !important;
        background:#E8EFE3 !important;
        color:#203E30 !important;
        font-size:14px !important;
        font-weight:700 !important;
        line-height:1 !important;
        display:flex;
        align-items:center;
        justify-content:center;
        text-align:center !important;
        transition:
            background-color 220ms ease,
            color 220ms ease,
            border-color 220ms ease,
            box-shadow 220ms ease;
    }}
    [class*="st-key-biova_language_control_"] button[aria-pressed="true"],
    [class*="st-key-biova_language_control_"] button[aria-selected="true"],
    [class*="st-key-biova_language_control_"] button[data-selected="true"] {{
        border-color:#203E30 !important;
        background:#203E30 !important;
        color:#FFFFFF !important;
        box-shadow:none;
    }}
    [class*="st-key-biova_language_control_"] [role="radiogroup"] {{
        width:104px;
        height:48px;
        display:flex;
        gap:8px;
    }}
    [class*="st-key-biova_language_control_"] [role="radio"] {{
        box-sizing:border-box;
        flex:0 0 48px;
        width:48px;
        height:48px !important;
        min-height:48px !important;
        max-height:48px !important;
        margin:0 !important;
        display:flex !important;
        align-items:center;
        justify-content:center;
        border:1px solid #BFCFBA !important;
        border-radius:10px !important;
        background:#E8EFE3 !important;
        color:#203E30 !important;
        font-size:14px !important;
        font-weight:700 !important;
        transition:
            background-color 220ms ease,
            color 220ms ease,
            border-color 220ms ease,
            box-shadow 220ms ease;
    }}
    [class*="st-key-biova_language_control_"] [role="radio"][aria-checked="true"] {{
        border-color:#203E30 !important;
        background:#203E30 !important;
        color:#FFFFFF !important;
    }}
    [class*="st-key-biova_language_control_"] [role="radio"] p {{
        margin:0 !important;
        color:inherit !important;
        font-weight:700 !important;
        text-align:center !important;
    }}
    .st-key-biova-welcome-header {{
        width:100%;
        margin-bottom:16px;
    }}
    .st-key-biova-welcome-header [data-testid="stHorizontalBlock"] {{
        display:flex !important;
        flex-direction:row !important;
        flex-wrap:nowrap !important;
        align-items:center !important;
        justify-content:space-between;
    }}
    .st-key-biova-welcome-header [data-testid="stColumn"]:first-child {{
        flex:1 1 0% !important;
        min-width:0 !important;
    }}
    .st-key-biova-welcome-header [data-testid="stColumn"]:last-child {{
        flex:0 0 104px !important;
        width:104px !important;
        min-width:104px !important;
    }}
    @keyframes biovaStarPop {{
        0% {{ transform:scale(.88); }}
        70% {{ transform:scale(1.12); }}
        100% {{ transform:scale(1); }}
    }}
    @media (max-width:767px) {{
        .st-key-biova-header [data-testid="stHorizontalBlock"] {{
            align-items:center !important;
            gap:8px !important;
        }}
        .st-key-biova-header [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:first-child {{
            flex:1 1 auto !important;
            width:auto !important;
            min-width:0 !important;
        }}
        .st-key-biova-header [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:last-child {{
            flex:0 0 max-content !important;
            width:max-content !important;
            max-width:100% !important;
            min-width:max-content !important;
        }}
        .st-key-biova-header {{
            min-height:58px;
            margin-bottom:16px;
            padding:7px 10px;
        }}
        .biova-header-avatar,
        .biova-header-avatar img {{
            width:44px !important;
            height:44px !important;
        }}
        .biova-header-name {{ font-size:15px; }}
        .biova-header-caption {{ font-size:12px; }}
        .biova-header-stars {{
            height:48px;
            padding:0 8px;
            gap:6px;
            font-size:14px;
        }}
        [class*="st-key-biova_language_control_"] {{
            width:104px;
            min-width:104px;
        }}
        [class*="st-key-biova_language_control_"] button {{
            box-sizing:border-box;
            width:48px !important;
            height:48px !important;
            min-height:48px !important;
            padding:0 !important;
        }}
    }}
    @media (max-width:380px) {{
        .st-key-biova-header [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:last-child {{
            flex-basis:max-content !important;
            width:max-content !important;
            min-width:max-content !important;
        }}
        [class*="st-key-biova_language_control_"],
        [class*="st-key-biova_language_control_"] [data-testid="stSegmentedControl"],
        [class*="st-key-biova_language_control_"] [role="radiogroup"] {{
            width:88px;
            min-width:88px;
        }}
        [class*="st-key-biova_language_control_"] button,
        [class*="st-key-biova_language_control_"] [role="radio"] {{
            width:40px !important;
            flex-basis:40px !important;
        }}
    }}
    @media (prefers-reduced-motion: reduce) {{
        .st-key-biova-header,
        .biova-star-count,
        .biova-header-avatar img,
        .st-key-biova-profile-card,
        .biova-profile-stat,
        .biova-profile-activity,
        [class*="st-key-biova_language_control_"] button {{
            animation:none !important;
            transition:none !important;
        }}
    }}
    .biova-home-heading {{
        margin:0 0 16px;
    }}
    .biova-home-heading h2 {{
        margin:0;
        font-size:30px !important;
        font-weight:800;
        line-height:1.2;
    }}
    .biova-home-heading p {{
        margin:12px 0 0;
        color:#526258;
        font-size:16px !important;
        line-height:1.5;
    }}
    .st-key-biova-home-categories [data-testid="stHorizontalBlock"] {{
        align-items:stretch;
        gap:var(--biova-space-24) !important;
    }}
    .st-key-biova-home-categories [data-testid="stHorizontalBlock"] > [data-testid="stColumn"] {{
        min-width:0 !important;
        width:auto !important;
        flex:1 1 0% !important;
    }}
    .st-key-biova-learning-categories [data-testid="stHorizontalBlock"] {{
        align-items:stretch;
        gap:var(--biova-space-24) !important;
    }}
    .st-key-biova-learning-categories [data-testid="stHorizontalBlock"] > [data-testid="stColumn"] {{
        min-width:0 !important;
        width:50% !important;
        flex:1 1 0% !important;
    }}
    .stVerticalBlock.st-key-home-card-hewan[data-testid="stVerticalBlock"],
    .stVerticalBlock.st-key-home-card-tumbuhan[data-testid="stVerticalBlock"] {{
        box-sizing:border-box;
        display:grid;
        grid-template-rows:minmax(124px,1fr) auto;
        align-items:stretch;
        min-width:0;
        width:100%;
        height:100%;
        min-height:0;
        row-gap:var(--biova-space-24);
        padding:var(--biova-space-30);
        border:1px solid rgba(86,137,103,.30);
        border-radius:var(--biova-radius-category-card);
        box-shadow:var(--biova-shadow-card);
        animation:biovaCardEntrance 350ms ease-out both;
        transition:transform 220ms ease, box-shadow 220ms ease;
    }}
    .st-key-home-card-hewan {{
        border-color:var(--biova-sage);
        background:linear-gradient(135deg,#EFF8DF 0%,#D8EDC1 100%);
    }}
    .st-key-home-card-tumbuhan {{
        border-color:#355D45;
        background:linear-gradient(135deg,#203E30 0%,#497D56 100%);
    }}
    .st-key-home-card-tumbuhan .biova-home-card__title h3 {{
        color:#FFF9EB;
    }}
    .st-key-home-card-tumbuhan .biova-home-card__title p {{
        color:rgba(255,249,235,.90);
    }}
    .st-key-home_explore_hewan div.stButton > button,
    .st-key-home_explore_tumbuhan div.stButton > button {{
        box-sizing:border-box;
        height:48px !important;
        min-height:48px !important;
        padding:0 16px !important;
        border:1px solid rgba(143,184,124,.72) !important;
        border-radius:12px !important;
        background:#FFF9EB !important;
        color:#203E30 !important;
        font-size:15px !important;
        font-weight:800 !important;
        white-space:normal !important;
        transition:transform 200ms ease, box-shadow 200ms ease, background-color 200ms ease, border-color 200ms ease !important;
    }}
    .st-key-home_explore_hewan div.stButton > button:hover,
    .st-key-home_explore_tumbuhan div.stButton > button:hover {{
        border-color:#568967 !important;
        background:#EFF8DF !important;
        box-shadow:0 4px 12px rgba(32,62,48,.10);
    }}
    .st-key-home_explore_hewan div.stButton > button:focus-visible,
    .st-key-home_explore_tumbuhan div.stButton > button:focus-visible {{
        outline:3px solid #203E30 !important;
        outline-offset:3px;
    }}
    .stVerticalBlock.st-key-home-card-hewan[data-testid="stVerticalBlock"] > [data-testid="stElementContainer"]:first-child,
    .stVerticalBlock.st-key-home-card-tumbuhan[data-testid="stVerticalBlock"] > [data-testid="stElementContainer"]:first-child {{
        display:flex;
        align-items:center;
        min-width:0;
    }}
    .stVerticalBlock.st-key-home-card-actions-hewan[data-testid="stVerticalBlock"],
    .stVerticalBlock.st-key-home-card-actions-tumbuhan[data-testid="stVerticalBlock"] {{
        display:flex;
        flex-direction:column;
        justify-content:flex-end;
        width:100%;
        min-width:0;
    }}
    .biova-home-card__head {{
        display:grid;
        grid-template-columns:124px minmax(0,1fr);
        align-items:stretch;
        gap:20px;
        min-width:0;
    }}
    .biova-home-card__illustration {{
        width:124px;
        height:124px;
        display:flex;
        align-items:center;
        justify-content:center;
        border:1px solid rgba(143,184,124,.35);
        border-radius:18px;
        background:rgba(255,249,235,.66);
    }}
    .st-key-home-card-tumbuhan .biova-home-card__illustration {{
        border-color:rgba(255,249,235,.24);
        background:rgba(255,249,235,.10);
    }}
    .biova-home-card__illustration img {{
        width:112px !important;
        height:112px !important;
        max-width:112px;
        max-height:112px;
        object-fit:contain;
        animation:biovaFloat 4.5s ease-in-out infinite;
    }}
    .biova-home-card__title {{
        min-width:0;
        box-sizing:border-box;
        display:grid;
        grid-template-columns:minmax(0,1fr);
        align-content:start;
        row-gap:var(--biova-space-12);
        padding-top:4px;
    }}
    .biova-home-card__title h3 {{
        margin:0;
        color:{COLOR_PRIMARY};
        font-size:22px !important;
        font-weight:800;
        line-height:1.2;
    }}
    .biova-home-card__title p {{
        margin:0;
        color:#526258;
        font-size:16px !important;
        line-height:1.5;
    }}
    @media (hover:hover) and (pointer:fine) {{
        .st-key-home-card-hewan:hover,
        .st-key-home-card-tumbuhan:hover {{
            transform:translateY(-4px);
            box-shadow:0 13px 28px rgba(32,62,48,.13);
        }}
    }}
    .biova-page-heading {{
        margin:0 0 var(--biova-space-16);
    }}
    .biova-page-heading h2 {{
        margin:0;
        color:var(--biova-forest);
        font-size:28px !important;
        font-weight:800;
        line-height:1.25;
    }}
    .biova-page-heading p {{
        margin:var(--biova-space-8) 0 0;
        color:#526258;
        font-size:16px !important;
        line-height:1.55;
    }}
    .biova-selection-pill {{
        display:inline-flex;
        align-items:center;
        min-height:32px;
        margin:0 0 var(--biova-space-16);
        padding:4px 12px;
        border:1px solid rgba(86,137,103,.28);
        border-radius:999px;
        background:rgba(255,255,255,.66);
        color:var(--biova-forest);
        font-size:14px;
        font-weight:700;
        line-height:1.3;
    }}
    .stVerticalBlock.st-key-learn-card-hewan[data-testid="stVerticalBlock"],
    .stVerticalBlock.st-key-learn-card-tumbuhan[data-testid="stVerticalBlock"] {{
        box-sizing:border-box;
        display:flex;
        flex-direction:column;
        height:100%;
        min-width:0;
        min-height:0;
        gap:var(--biova-space-24);
        padding:var(--biova-space-30);
        border:1px solid rgba(86,137,103,.28);
        border-radius:var(--biova-radius-category-card);
        box-shadow:var(--biova-shadow-card);
        color:var(--biova-forest);
    }}
    .st-key-learn-card-hewan {{
        background:linear-gradient(135deg,#EFF8DF 0%,#D8EDC1 100%);
    }}
    .st-key-learn-card-tumbuhan {{
        border-color:rgba(255,249,235,.24);
        background:linear-gradient(135deg,#203E30 0%,#497D56 100%);
        color:#FFF9EB;
    }}
    .stVerticalBlock.st-key-learn-actions-hewan[data-testid="stVerticalBlock"],
    .stVerticalBlock.st-key-learn-actions-tumbuhan[data-testid="stVerticalBlock"] {{
        display:grid;
        grid-template-columns:minmax(0,1fr);
        grid-auto-rows:minmax(58px,auto);
        align-content:end;
        width:100%;
        row-gap:var(--biova-space-14);
        margin-top:auto;
    }}
    .biova-learn-card__header {{
        display:grid;
        grid-template-columns:124px minmax(0,1fr);
        align-items:center;
        gap:var(--biova-space-20);
        flex-shrink:0;
        min-height:124px;
    }}
    .biova-learn-card__illustration {{
        width:124px;
        height:124px;
        display:flex;
        align-items:center;
        justify-content:center;
        border-radius:var(--biova-radius-small);
        background:rgba(255,249,235,.72);
    }}
    .st-key-learn-card-tumbuhan .biova-learn-card__illustration {{
        background:rgba(255,249,235,.12);
    }}
    .biova-learn-card__illustration img {{
        width:112px !important;
        height:112px !important;
        object-fit:contain;
    }}
    .biova-learn-card__copy {{
        display:flex;
        flex-direction:column;
        gap:var(--biova-space-12);
        min-width:0;
        overflow-wrap:anywhere;
    }}
    .biova-learn-card__copy h3 {{
        margin:0;
        color:var(--biova-forest);
        font-size:22px !important;
        font-weight:800;
        line-height:1.25;
    }}
    .biova-learn-card__copy p {{
        margin:0;
        color:#40584A;
        font-size:15px !important;
        line-height:1.5;
    }}
    .st-key-learn-card-tumbuhan .biova-learn-card__copy h3,
    .st-key-learn-card-tumbuhan .biova-learn-card__copy p {{
        color:#FFF9EB;
    }}
    @media (min-width:768px) and (max-width:1023px) {{
        .stVerticalBlock.st-key-home-card-hewan[data-testid="stVerticalBlock"],
        .stVerticalBlock.st-key-home-card-tumbuhan[data-testid="stVerticalBlock"] {{
            grid-template-rows:minmax(112px,1fr) auto;
            padding:24px;
        }}
        .biova-home-card__head {{
            grid-template-columns:112px minmax(0,1fr);
            gap:16px;
        }}
        .biova-home-card__illustration {{
            width:112px;
            height:112px;
        }}
        .biova-home-card__illustration img {{
            width:100px !important;
            height:100px !important;
        }}
        .stVerticalBlock.st-key-learn-card-hewan[data-testid="stVerticalBlock"],
        .stVerticalBlock.st-key-learn-card-tumbuhan[data-testid="stVerticalBlock"] {{
            padding:24px;
        }}
        .biova-learn-card__header {{
            grid-template-columns:112px minmax(0,1fr);
            gap:16px;
            min-height:112px;
        }}
        .biova-learn-card__illustration {{
            width:112px;
            height:112px;
        }}
        .biova-learn-card__illustration img {{
            width:100px !important;
            height:100px !important;
        }}
    }}
    .st-key-learn-card-hewan div.stButton > button,
    .st-key-learn-card-tumbuhan div.stButton > button {{
        box-sizing:border-box;
        height:58px !important;
        min-height:58px !important;
        padding:8px 16px !important;
        border:1px solid rgba(143,184,124,.62) !important;
        border-radius:var(--biova-radius-button) !important;
        background:var(--biova-cream) !important;
        color:var(--biova-forest) !important;
        font-size:15px !important;
        font-weight:700 !important;
        line-height:1.2 !important;
        display:flex;
        align-items:center;
        justify-content:center;
        text-align:center;
        white-space:normal !important;
    }}
    .st-key-learn-card-hewan div.stButton > button:hover,
    .st-key-learn-card-tumbuhan div.stButton > button:hover {{
        border-color:var(--biova-leaf) !important;
        background:#E8F0D8 !important;
        color:var(--biova-forest) !important;
    }}
    .st-key-learn-card-hewan .st-key-btn_identify_hewan div.stButton > button,
    .st-key-learn-card-tumbuhan .st-key-btn_identify_tumbuhan div.stButton > button {{
        border-color:var(--biova-gold) !important;
        background:var(--biova-gold) !important;
    }}
    @media (max-width:767px) {{
        .biova-home-heading {{ margin:0 0 8px; }}
        .biova-home-heading h2 {{ font-size:30px !important; }}
        .biova-page-heading h2 {{ font-size:25px !important; }}
        .st-key-biova-home-categories [data-testid="stHorizontalBlock"],
        .st-key-biova-learning-categories [data-testid="stHorizontalBlock"] {{
            flex-wrap:wrap !important;
            gap:var(--biova-space-24) !important;
        }}
        .st-key-biova-home-categories [data-testid="stHorizontalBlock"] > [data-testid="stColumn"],
        .st-key-biova-learning-categories [data-testid="stHorizontalBlock"] > [data-testid="stColumn"] {{
            flex:none !important;
            width:100% !important;
        }}
        .stVerticalBlock.st-key-home-card-hewan[data-testid="stVerticalBlock"],
        .stVerticalBlock.st-key-home-card-tumbuhan[data-testid="stVerticalBlock"] {{
            grid-template-rows:minmax(100px,auto) auto;
            height:auto;
            min-height:0;
            padding:20px;
        }}
        .biova-home-card__head {{
            grid-template-columns:100px minmax(0,1fr);
            gap:16px;
        }}
        .biova-home-card__illustration {{
            width:100px;
            height:100px;
        }}
        .biova-home-card__illustration img {{
            width:92px !important;
            height:92px !important;
        }}
        .biova-home-card__title h3 {{ font-size:21px !important; }}
        .biova-home-card__title p {{ font-size:15px !important; }}
        .stVerticalBlock.st-key-learn-card-hewan[data-testid="stVerticalBlock"],
        .stVerticalBlock.st-key-learn-card-tumbuhan[data-testid="stVerticalBlock"] {{
            height:auto;
            min-height:0;
            padding:20px;
        }}
        .biova-learn-card__header {{
            grid-template-columns:100px minmax(0,1fr);
            min-height:100px;
            gap:16px;
        }}
        .biova-learn-card__illustration {{
            width:100px;
            height:100px;
        }}
        .biova-learn-card__illustration img {{
            width:92px !important;
            height:92px !important;
        }}
        .biova-learn-card__copy h3 {{ font-size:21px !important; }}
        .biova-learn-card__copy p {{ font-size:15px !important; }}
    }}
    @media (prefers-reduced-motion: reduce) {{
        .st-key-home-card-hewan,
        .st-key-home-card-tumbuhan,
        .st-key-home_explore_hewan button,
        .st-key-home_explore_tumbuhan button,
        .biova-home-card__illustration img {{
            animation:none !important;
            transition:none !important;
        }}
    }}
    .st-key-biova-profile-card {{
        box-sizing:border-box;
        max-width:860px;
        margin:0 auto var(--biova-space-16);
        padding:var(--biova-space-24);
        border:1px solid rgba(187,221,156,.52);
        border-radius:24px;
        background:
            radial-gradient(ellipse at 50% 0%,rgba(187,221,156,.20),transparent 18rem),
            linear-gradient(135deg,#203E30 0%,#315D43 58%,#497D56 100%);
        color:#FFF9EB;
        box-shadow:0 12px 28px rgba(32,62,48,.15);
        animation:biovaProfileEnter 260ms ease-out both;
        gap:var(--biova-space-16);
    }}
    .biova-profile-main {{
        text-align:center;
    }}
    .biova-profile-avatar-wrap {{
        position:relative;
        width:124px;
        height:124px;
        margin:0 auto var(--biova-space-12);
    }}
    .biova-profile-avatar {{
        box-sizing:border-box;
        width:124px;
        height:124px;
        display:flex;
        align-items:center;
        justify-content:center;
        overflow:hidden;
        border:4px solid #BBDD9C;
        border-radius:50%;
        background:#FFF9EB;
        box-shadow:0 6px 18px rgba(12,35,23,.20);
    }}
    .biova-profile-avatar img {{
        display:block;
        width:100% !important;
        height:100% !important;
        border-radius:50%;
        object-fit:cover;
    }}
    .biova-profile-edit-dot {{
        position:absolute;
        right:0;
        bottom:5px;
        width:30px;
        height:30px;
        display:flex;
        align-items:center;
        justify-content:center;
        border:2px solid #FFF9EB;
        border-radius:50%;
        background:#F7C957;
        color:#203E30;
        font-size:15px;
        font-weight:900;
        box-shadow:0 4px 10px rgba(32,62,48,.16);
    }}
    .biova-profile-main h2 {{
        margin:0;
        color:#FFF9EB;
        font-size:23px;
        line-height:1.2;
        overflow-wrap:anywhere;
    }}
    .biova-profile-email {{
        margin:2px 0 6px;
        color:rgba(255,249,235,.80);
        font-size:12px;
        overflow-wrap:anywhere;
    }}
    .st-key-biova-profile-photo-toggle {{
        display:flex;
        align-items:center;
        justify-content:center;
    }}
    .st-key-biova-profile-photo-toggle [data-testid="stElementContainer"] {{
        width:max-content !important;
        max-width:100%;
    }}
    .st-key-profile_photo_edit_toggle div.stButton > button {{
        width:max-content !important;
        max-width:100%;
        min-height:44px;
        padding:0 20px !important;
        border:1px solid rgba(187,221,156,.76) !important;
        border-radius:999px !important;
        background:#568967 !important;
        color:#FFF9EB !important;
        font-weight:800 !important;
    }}
    .st-key-biova-profile-photo-editor {{
        width:100%;
        max-width:640px;
        margin:0 auto;
        padding:var(--biova-space-16);
        border:1px solid rgba(143,184,124,.48);
        border-radius:16px;
        background:#FFF9EB;
        color:#203E30;
    }}
    .biova-profile-stats,
    .biova-profile-activity {{
        max-width:860px;
        margin:0 auto var(--biova-space-16);
    }}
    .biova-profile-stat-grid {{
        display:grid;
        grid-template-columns:repeat(2,minmax(0,1fr));
        gap:16px;
    }}
    .biova-profile-stat {{
        min-width:0;
        display:flex;
        align-items:center;
        justify-content:flex-start;
        gap:16px;
        padding:var(--biova-space-16) var(--biova-space-24);
        border:1px solid rgba(143,184,124,.56);
        border-radius:20px;
        background:#FFF9EB;
        box-shadow:0 7px 18px rgba(32,62,48,.07);
        animation:biovaProfileEnter 260ms ease-out both;
    }}
    .biova-profile-stat__icon {{
        width:58px;
        height:58px;
        flex:0 0 58px;
        display:flex;
        align-items:center;
        justify-content:center;
        border:1px solid rgba(143,184,124,.45);
        border-radius:18px;
        background:#EFF8DF;
    }}
    .biova-profile-stat__copy {{
        min-width:0;
        display:flex;
        flex-direction:column;
        gap:var(--biova-space-8);
    }}
    .biova-profile-stat__copy span {{
        color:#607465;
        font-size:12px;
        font-weight:700;
        line-height:1.35;
        overflow-wrap:anywhere;
    }}
    .biova-profile-stat__copy strong {{
        color:#203E30;
        font-size:23px;
        line-height:1.15;
        overflow-wrap:anywhere;
    }}
    .biova-profile-activity {{
        box-sizing:border-box;
        padding:16px;
        border:1px solid rgba(143,184,124,.50);
        border-radius:20px;
        background:rgba(255,249,235,.96);
        box-shadow:0 7px 18px rgba(32,62,48,.06);
        animation:biovaProfileEnter 260ms ease-out both;
    }}
    .biova-profile-activity__heading {{
        display:flex;
        align-items:center;
        gap:8px;
        margin-bottom:12px;
    }}
    .biova-profile-activity__heading h3 {{
        margin:0;
        color:#203E30;
        font-size:22px;
        font-weight:850;
    }}
    .biova-profile-activity__items {{
        display:grid;
        grid-template-columns:repeat(3,minmax(0,1fr));
        gap:var(--biova-space-8);
    }}
    .biova-profile-activity__item {{
        min-width:0;
        display:flex;
        align-items:center;
        gap:8px;
        padding:var(--biova-space-8);
        border:1px solid rgba(143,184,124,.30);
        border-radius:14px;
        background:#FFFFFF;
    }}
    .biova-profile-activity__item span {{
        min-width:0;
        flex:1 1 auto;
        color:#526258;
        font-size:13px;
        line-height:1.35;
        overflow-wrap:anywhere;
    }}
    .biova-profile-activity__item strong {{
        flex:0 0 auto;
        color:#203E30;
        font-size:14px;
    }}
    .biova-profile-activity__progress {{
        margin:var(--biova-space-12) 0 0;
        padding-top:var(--biova-space-12);
        border-top:1px solid rgba(143,184,124,.30);
        color:#607465;
        font-size:12px;
        text-align:center;
    }}
    @keyframes biovaProfileEnter {{
        from {{ opacity:0; transform:translateY(6px); }}
        to {{ opacity:1; transform:translateY(0); }}
    }}
    @media (max-width:767px) {{
        [data-testid="stHorizontalBlock"] {{
            flex-wrap:wrap;
        }}
        .st-key-biova-profile-card {{
            padding:var(--biova-space-16);
            border-radius:20px;
        }}
        .biova-profile-avatar-wrap,
        .biova-profile-avatar {{
            width:100px;
            height:100px;
        }}
        .st-key-biova-profile-photo-editor {{
            padding:10px;
        }}
        .biova-profile-stats,
        .biova-profile-activity {{
            margin-bottom:var(--biova-space-12);
        }}
        .biova-profile-stat-grid {{
            grid-template-columns:1fr;
            gap:var(--biova-space-8);
        }}
        .biova-profile-stat {{
            padding:var(--biova-space-12) var(--biova-space-16);
            border-radius:18px;
        }}
        .biova-profile-activity {{
            padding:var(--biova-space-16);
        }}
        .biova-profile-activity__items {{
            grid-template-columns:1fr;
            gap:var(--biova-space-8);
        }}
    }}
    .st-key-biova-material-collection [data-testid="stHorizontalBlock"] {{
        flex-wrap:wrap !important;
        gap:var(--biova-space-20) !important;
    }}
    .st-key-biova-material-collection [data-testid="stHorizontalBlock"] > [data-testid="stColumn"] {{
        min-width:0 !important;
    }}
    [class*="st-key-collection-card-"] > [data-testid="stVerticalBlock"] {{
        align-items:center;
        gap:8px;
    }}
    [class*="st-key-collection-card-"] [data-testid="stIFrame"] {{
        width:100% !important;
        border:0 !important;
    }}
    [class*="st-key-collection-card-"] div.stButton > button {{
        min-height:46px !important;
        padding:8px 14px !important;
        font-size:14px !important;
    }}
    @media (min-width:768px) and (max-width:1024px) {{
        .st-key-biova-material-collection [data-testid="stHorizontalBlock"] > [data-testid="stColumn"] {{
            flex:0 0 calc(50% - 10px) !important;
            width:calc(50% - 10px) !important;
        }}
        .st-key-biova-material-row-last [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:first-child,
        .st-key-biova-material-row-last [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:last-child {{
            display:none !important;
        }}
        .st-key-biova-material-row-last [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:nth-child(2),
        .st-key-biova-material-row-last [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:nth-child(3) {{
            flex:0 0 calc(50% - 10px) !important;
            width:calc(50% - 10px) !important;
        }}
    }}
    @media (max-width:767px) {{
        .st-key-biova-material-collection [data-testid="stHorizontalBlock"] > [data-testid="stColumn"] {{
            flex:0 0 100% !important;
            width:100% !important;
        }}
        .st-key-biova-material-row-last [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:first-child,
        .st-key-biova-material-row-last [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:last-child {{
            display:none !important;
        }}
        .st-key-biova-material-row-last [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:nth-child(2),
        .st-key-biova-material-row-last [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:nth-child(3) {{
            flex:0 0 100% !important;
            width:100% !important;
        }}
    }}
    .biova-nature-card {{
        min-height:210px;
        height:100%;
        box-sizing:border-box;
        text-align:center;
        padding:16px 12px;
        margin-bottom:8px;
        border:1.5px solid {COLOR_BORDER};
        border-radius:20px;
        background:linear-gradient(145deg,#FFFFFF,#F1F6E8);
        box-shadow:0 4px 12px rgba(32,62,48,.06);
        transition:transform 220ms ease, box-shadow 220ms ease, border-color 220ms ease;
    }}
    .biova-nature-card.active {{
        border-color:{COLOR_SECONDARY};
        background:linear-gradient(145deg,#FFFFFF,#EAF3DF);
    }}
    .biova-nature-card-icon {{
        height:96px;
        display:flex;
        align-items:center;
        justify-content:center;
        margin-bottom:6px;
    }}
    .biova-nature-card-title {{
        min-height:44px;
        color:{COLOR_PRIMARY};
        font-size:15px;
        font-weight:900;
        line-height:1.35;
    }}
    .biova-nature-card-badge {{
        color:#66776C;
        font-size:12px;
        margin-top:5px;
    }}
    [data-testid="stMainBlockContainer"],
    [data-testid="stVerticalBlock"] {{
        animation: biova-page-enter 300ms ease-out both;
    }}
    @keyframes biova-page-enter {{
        from {{ opacity:0; transform:translateY(8px); }}
        to {{ opacity:1; transform:translateY(0); }}
    }}
    @media (hover:hover) and (pointer:fine) {{
        .biova-nature-card:hover {{
            transform:translateY(-4px) scale(1.01);
            border-color:#568967;
            box-shadow:0 10px 22px rgba(32,62,48,.12);
        }}
    }}
    .stTextInput [data-testid="stTextInputRootElement"] {{
        min-height: 50px !important;
    }}
    .stTextInput input {{
        min-height: 48px !important;
        font-size: 15px !important;
    }}
    [data-testid="stForm"] [data-testid="InputInstructions"] {{
        display: none !important;
    }}
    .st-key-btn_google_login button {{
        position: relative !important;
        background: #FFFFFF !important;
        color: {COLOR_PRIMARY} !important;
        border: 1.5px solid {COLOR_BORDER} !important;
        border-radius: 14px !important;
        box-shadow: none !important;
        padding-left: 52px !important;
    }}
    .st-key-btn_google_login button::before {{
        content: "G";
        position: absolute;
        left: 22px;
        top: 50%;
        transform: translateY(-50%);
        width: 20px;
        height: 20px;
        display:flex;
        align-items:center;
        justify-content:center;
        border-radius:50%;
        background:
            conic-gradient(#4285F4 0 25%, #34A853 25% 50%, #FBBC05 50% 75%, #EA4335 75%);
        color:#FFFFFF;
        font-family:Arial,sans-serif;
        font-size:13px;
        font-weight:800;
        box-shadow: inset 0 0 0 5px #FFFFFF;
    }}

    .biova-lesson-heading {{
        margin: 4px 0 12px;
        text-align:center;
    }}
    .biova-lesson-heading span {{
        color:{COLOR_SECONDARY};
        font-size:12px;
        font-weight:800;
        letter-spacing:.8px;
        text-transform:uppercase;
    }}
    .biova-lesson-heading h2 {{
        margin:2px 0 0;
        color:{COLOR_PRIMARY};
        font-size:22px;
    }}
    .biova-detail-heading {{
        min-height:48px;
    }}
    .biova-detail-heading span {{
        color:{COLOR_SECONDARY};
        font-size:12px;
        font-weight:900;
        letter-spacing:.6px;
    }}
    .biova-detail-heading h2 {{
        margin:2px 0 0;
        color:{COLOR_PRIMARY};
        font-size:21px;
    }}
    .biova-detail-position {{
        height:38px;
        display:flex;
        align-items:center;
        justify-content:center;
        color:{COLOR_PRIMARY};
        font-weight:800;
    }}
    @keyframes biovaCardEntrance {{
        from {{ opacity:0; transform:translateY(8px); }}
        to {{ opacity:1; transform:translateY(0); }}
    }}
    @keyframes biovaFloat {{
        0%,100% {{ transform:translateY(0); }}
        50% {{ transform:translateY(-3px); }}
    }}
    @media (max-width: 767px) {{
        .biova-icon-input {{ width:20px !important; height:20px !important; }}
        .biova-icon-nav {{ width:24px !important; height:24px !important; }}
        .biova-icon-category {{ width:56px !important; height:56px !important; }}
        .biova-icon-result {{ width:88px !important; height:88px !important; }}
        .biova-icon-medal {{ width:28px !important; height:28px !important; }}
        .biova-mascot {{ width:180px; }}
        .block-container {{
            padding-left: 16px !important;
            padding-right: 16px !important;
        }}
        .biova-welcome-mascot {{
            width: 180px;
            margin: 4px auto 10px;
        }}
        .biova-welcome-mascot img {{
            width: 180px;
        }}
        .biova-welcome-copy {{
            text-align: center;
            margin: 0 auto;
        }}
        .biova-welcome-copy h1 {{
            font-size: 32px;
        }}
        .biova-welcome-copy h2 {{
            font-size: 18px;
        }}
        .biova-welcome-copy p {{
            font-size: 14px;
        }}
        .biova-login-mascot {{
            margin:0 0 8px;
        }}
        .biova-login-mascot__image {{
            width:92px !important;
            height:92px !important;
        }}
        .st-key-biova-welcome-content [data-testid="stHorizontalBlock"] {{
            flex-direction: column;
        }}
    }}

    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
