"""BIOVA — AI-Powered Interactive Flora & Fauna Learning Platform
Main application entry point and centralized routing controller.
"""

import streamlit as st
from components.icons import get_icon_path
from components.header import render_public_header

# Streamlit Page Configuration must be the first Streamlit command
st.set_page_config(
    page_title="BIOVA – Belajar dari Alam",
    page_icon=str(get_icon_path("hewan") or "BIOVA"),
    layout="wide",
    initial_sidebar_state="collapsed",
)

from components.theme import apply_theme
from components.i18n import init_language, set_language
from services.db import init_db
from services.auth_service import get_or_create_oauth_user
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
    init_language()

    # Apply global custom styles
    apply_theme()

    # Session State Initialization
    if "authenticated_user" not in st.session_state:
        st.session_state["authenticated_user"] = None
    if "is_authenticated" not in st.session_state:
        st.session_state["is_authenticated"] = False
    if st.session_state["authenticated_user"] is not None:
        st.session_state["is_authenticated"] = True
    if "current_page" not in st.session_state:
        st.session_state["current_page"] = "welcome"
    if "user_stars" not in st.session_state:
        st.session_state["user_stars"] = 0

    # Streamlit returns from the identity provider to the app homepage in a new
    # session, so synchronize the OIDC identity before dispatching the route.
    oauth_user = st.user
    if (
        getattr(oauth_user, "is_logged_in", False)
        and not st.session_state.get("authenticated_user")
    ):
        provider_subject = oauth_user.get("sub")
        if not provider_subject:
            st.error("Identitas Google tidak memiliki subject ID yang valid.")
            st.session_state["current_page"] = "login"
        else:
            success, user_data, message = get_or_create_oauth_user(
                "google",
                provider_subject,
                oauth_user.get("email", ""),
                oauth_user.get("name", ""),
            )
            if success:
                st.session_state["authenticated_user"] = user_data
                st.session_state["user_stars"] = user_data["stars"]
                selected_language = st.session_state.get("language")
                if not st.session_state.get("_language_explicit"):
                    selected_language = user_data.get("language", "id")
                set_language(selected_language)
                st.session_state["is_authenticated"] = True
                st.session_state["current_page"] = "dashboard"
            else:
                st.error(message)
                st.session_state["current_page"] = "login"

    current_page = st.session_state["current_page"]
    user = st.session_state["authenticated_user"]

    # Protected routes check
    public_pages = {"welcome", "login", "register"}
    if current_page not in public_pages and (
        user is None or not st.session_state.get("is_authenticated", False)
    ):
        st.session_state["current_page"] = "login"
        current_page = "login"

    # Public pages use the same reusable header position as authenticated pages.
    if current_page == "welcome":
        render_public_header(welcome_layout=True)
    elif current_page in {"login", "register"}:
        render_public_header()

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
