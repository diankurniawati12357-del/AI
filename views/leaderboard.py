"""BIOVA Leaderboard View
Displays global rankings of real registered users with tier indicators and star totals.
"""

import streamlit as st
from components.theme import apply_theme
from components.header import render_header
from components.navigation import navigate_to, render_back_button, render_bottom_nav
from services.leaderboard_service import get_leaderboard
from services.config import COLOR_PRIMARY, COLOR_SECONDARY, COLOR_CARD, COLOR_BORDER, COLOR_HIGHLIGHT


def render_leaderboard():
    """Renders the full leaderboard screen."""
    apply_theme()

    user = st.session_state.get("authenticated_user")
    if not user:
        navigate_to("login")
        return

    render_header(show_stars=True)

    st.markdown(
        f"""
        <div style="text-align: center; margin-bottom: 20px;">
            <div style="font-size: 32px; margin-bottom: 4px;">🏆</div>
            <h2 style="font-size: 22px; font-weight: 800; color: {COLOR_PRIMARY}; margin: 0;">
                Papan Peringkat
            </h2>
            <p style="font-size: 13px; color: #555555; margin-top: 4px;">
                Petualang alam dengan perolehan bintang terbanyak di BIOVA:
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    leaders = get_leaderboard(limit=50)

    if not leaders:
        st.info("Belum ada data petualang di papan peringkat.")
    else:
        st.markdown('<div class="biova-card" style="padding: 12px 14px;">', unsafe_allow_html=True)
        for row in leaders:
            is_me = row["user_id"] == user["id"]
            card_style = "background-color: #CFDFA6; border-radius: 12px; padding: 10px 12px; margin-bottom: 6px;" if is_me else "padding: 8px 12px; margin-bottom: 4px; border-bottom: 1px solid rgba(0,0,0,0.05);"
            
            rank_badge = f"#{row['rank']}"
            if row["rank"] == 1:
                rank_badge = "🥇 #1"
            elif row["rank"] == 2:
                rank_badge = "🥈 #2"
            elif row["rank"] == 3:
                rank_badge = "🥉 #3"

            st.markdown(
                f"""
                <div style="display: flex; justify-content: space-between; align-items: center; {card_style}">
                    <div style="display: flex; align-items: center; gap: 10px;">
                        <span style="font-weight: 800; font-size: 14px; min-width: 36px; color: {COLOR_PRIMARY};">
                            {rank_badge}
                        </span>
                        <div>
                            <div style="font-size: 14px; font-weight: {'800' if is_me else '700'}; color: {COLOR_PRIMARY};">
                                {row['username']} {'(Kamu)' if is_me else ''}
                            </div>
                            <div style="font-size: 11px; color: #666666;">
                                {row['tier_icon']} Tier {row['tier']}
                            </div>
                        </div>
                    </div>
                    <div style="font-weight: 800; color: #D4AF37; font-size: 15px;">
                        {row['stars']} ⭐
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        st.markdown("</div>", unsafe_allow_html=True)

    render_bottom_nav(current_active="leaderboard")
