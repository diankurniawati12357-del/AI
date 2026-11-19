"""BIOVA — AI-Powered Interactive Flora & Fauna Learning Platform
Main application entry point and centralized routing controller.
"""

import streamlit as st

# Streamlit Page Configuration must be the first Streamlit command
st.set_page_config(
    page_title="BIOVA – Belajar dari Alam",
    page_icon="🐸",
    layout="centered",
    initial_sidebar_state="collapsed",
)

from components.theme import apply_theme
from services.db import init_db
from views.welcome import render_welcome
from views.auth import render_login, render_register
from views.dashboard import render_dashboard
from views.scan import render_scan
from views.scan_result import render_scan_result
from views.learn import render_learn
from views.lesson import render_lesson
from views.quiz import render_quiz
from views.quiz_result import render_quiz_result
from views.leaderboard import render_leaderboard
from views.profile import render_profile
from views.panorama import render_panorama


def main():
    """Main routing and state management loop."""
    # Ensure database is initialized
    init_db()

    # Apply global custom styles
    apply_theme()

    # Session State Initialization
    if "authenticated_user" not in st.session_state:
        st.session_state["authenticated_user"] = None
    if "current_page" not in st.session_state:
        st.session_state["current_page"] = "welcome"
    if "user_stars" not in st.session_state:
        st.session_state["user_stars"] = 0

    current_page = st.session_state["current_page"]
    user = st.session_state["authenticated_user"]

    # Protected routes check
    public_pages = {"welcome", "login", "register"}
    if current_page not in public_pages and user is None:
        st.session_state["current_page"] = "login"
        current_page = "login"

    # View Router Dispatch
    routes = {
        "welcome": render_welcome,
        "login": render_login,
        "register": render_register,
        "dashboard": render_dashboard,
        "scan": render_scan,
        "scan_result": render_scan_result,
        "learn": render_learn,
        "lesson": render_lesson,
        "quiz": render_quiz,
        "quiz_result": render_quiz_result,
        "leaderboard": render_leaderboard,
        "profile": render_profile,
        "panorama": render_panorama,
    }

    view_func = routes.get(current_page, render_welcome)
    view_func()


if __name__ == "__main__":
    main()
