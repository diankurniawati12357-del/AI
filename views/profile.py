"""BIOVA User Profile View
Displays account information, tier progression, collected stars, and logout controls.
"""

import streamlit as st
import base64
import html
from components.header import render_header
from components.icons import render_icon
from components.navigation import navigate_to, render_bottom_nav
from services.game_service import get_user_stats
from components.i18n import t
from services.profile_service import get_profile_photo_path, validate_and_save_profile_photo, remove_profile_photo


_TIER_MEDALS = {
    "Platinum": "medali_gold",
    "Gold": "medali_gold",
    "Silver": "medali_silver",
    "Bronze": "medali_bronze",
}


def render_profile():
    """Renders the User Profile screen."""
    user = st.session_state.get("authenticated_user")
    if not user:
        navigate_to("login")
        return

    render_header(show_stars=True)

    stats = get_user_stats(user["id"])

    username = html.escape(str(user["username"]), quote=True)
    email = html.escape(str(user["email"]), quote=True)
    tier_label = html.escape(str(stats["tier"]))
    photo = get_profile_photo_path(user["id"])
    if photo:
        photo_data = base64.b64encode(photo.read_bytes()).decode("ascii")
        avatar_html = (
            f'<img class="biova-profile-avatar__image" src="data:image/png;base64,{photo_data}" '
            f'alt="{username}">'
        )
    else:
        avatar_html = render_icon(
            "pengguna",
            112,
            "biova-icon--category",
            t("profile.edit_photo"),
        )

    with st.container(key="biova-profile-card"):
        st.markdown(
            f"""
            <div class="biova-profile-main">
                <div class="biova-profile-avatar-wrap">
                    <div class="biova-profile-avatar">{avatar_html}</div>
                    <span class="biova-profile-edit-dot">✎</span>
                </div>
                <h2>{username}</h2>
                <p class="biova-profile-email">{email}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        with st.container(key="biova-profile-photo-toggle"):
            if st.button(
                t("profile.edit_photo"),
                key="profile_photo_edit_toggle",
                use_container_width=False,
                type="secondary",
            ):
                st.session_state["profile_photo_edit_open"] = not st.session_state.get(
                    "profile_photo_edit_open",
                    False,
                )

        if st.session_state.get("profile_photo_edit_open", False):
            with st.container(key="biova-profile-photo-editor"):
                uploaded_photo = st.file_uploader(
                    t("profile.edit_photo"),
                    type=["jpg", "jpeg", "png", "webp"],
                    accept_multiple_files=False,
                    key="profile_photo_upload",
                )
                if uploaded_photo:
                    preview = uploaded_photo.read()
                    uploaded_photo.seek(0)
                    st.image(preview, width=256, caption=t("profile.edit_photo"))
                    save_col, cancel_col, remove_col = st.columns(3)
                    with save_col:
                        if st.button(t("profile.save_photo"), key="save_profile_photo", use_container_width=True):
                            success, message, _ = validate_and_save_profile_photo(user["id"], uploaded_photo)
                            if success:
                                st.success(message)
                                st.session_state["profile_photo_edit_open"] = False
                                st.rerun()
                            else:
                                st.error(message)
                    with cancel_col:
                        if st.button(t("profile.cancel"), key="cancel_profile_photo", type="secondary", use_container_width=True):
                            st.session_state["profile_photo_edit_open"] = False
                            st.rerun()
                    with remove_col:
                        if st.button(t("profile.remove_photo"), key="remove_profile_photo", type="secondary", use_container_width=True):
                            success, message = remove_profile_photo(user["id"])
                            if success:
                                st.success(message)
                                st.rerun()
                            else:
                                st.error(message)

    st.markdown(
        f"""
        <section class="biova-profile-stats">
            <div class="biova-profile-stat-grid">
                <div class="biova-profile-stat">
                    <div class="biova-profile-stat__icon">
                        {render_icon("bintang", 40, "biova-icon--reward", t("common.total_stars"))}
                    </div>
                    <div class="biova-profile-stat__copy">
                        <span>{t("common.total_stars")}</span>
                        <strong>{stats["stars"]}</strong>
                    </div>
                </div>
                <div class="biova-profile-stat">
                    <div class="biova-profile-stat__icon">
                        {render_icon(_TIER_MEDALS.get(stats["tier"], "bintang"), 40, "biova-icon--reward", t("profile.tier"))}
                    </div>
                    <div class="biova-profile-stat__copy">
                        <span>{t("profile.tier")}</span>
                        <strong>{tier_label}</strong>
                    </div>
                </div>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )

    progress_message = (
        t("profile.next_tier").format(stars=stats["stars_needed"])
        if stats["stars_needed"] > 0
        else t("profile.top_tier")
    )
    st.markdown(
        f"""
        <section class="biova-profile-activity">
            <div class="biova-profile-activity__heading">
                {render_icon("ensiklopedia", 26, "biova-icon--button", t("profile.activity"))}
                <h3>{t("profile.activity")}</h3>
            </div>
            <div class="biova-profile-activity__items">
                <div class="biova-profile-activity__item">
                    {render_icon("ensiklopedia", 28, "biova-icon--button", t("profile.quizzes_taken"))}
                    <span>{t("profile.quizzes_taken")}</span>
                    <strong>{stats["quiz_count"]}</strong>
                </div>
                <div class="biova-profile-activity__item">
                    {render_icon("gambar", 28, "biova-icon--button", t("profile.verified_photos"))}
                    <span>{t("profile.verified_photos")}</span>
                    <strong>{stats["upload_count"]}</strong>
                </div>
                <div class="biova-profile-activity__item">
                    {render_icon("cek", 28, "biova-icon--button", t("profile.completed_material"))}
                    <span>{t("profile.completed_material")}</span>
                    <strong>{stats["completed_material"]}</strong>
                </div>
            </div>
            <p class="biova-profile-activity__progress">{html.escape(progress_message)}</p>
        </section>
        """,
        unsafe_allow_html=True,
    )

    # Logout Button
    logout_icon, logout_button = st.columns([0.7, 9.3])
    with logout_icon:
        st.markdown(
            f'<div class="biova-icon-action">{render_icon("keluar", 24, "biova-icon--button", "Keluar")}</div>',
            unsafe_allow_html=True,
        )
    with logout_button:
        if st.button(t("profile.logout"), key="btn_logout", type="secondary", use_container_width=True):
            if getattr(st.user, "is_logged_in", False):
                st.logout()
                return
            st.session_state["authenticated_user"] = None
            st.session_state["is_authenticated"] = False
            st.session_state["user_stars"] = 0
            # Preserve the page-independent language preference on logout.
            language = st.session_state.get("language", "id")
            for key in list(st.session_state.keys()):
                if key not in {"language"}:
                    del st.session_state[key]
            st.session_state["language"] = language
            st.session_state["authenticated_user"] = None
            st.session_state["is_authenticated"] = False
            st.session_state["current_page"] = "welcome"
            navigate_to("welcome")

    render_bottom_nav(current_active="profile")
