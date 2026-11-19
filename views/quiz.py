"""BIOVA Quiz View
Matches KUIS.png, KUIS-1.png, and PEMBAHSAN KUIS.png with interactive questions,
instant feedback, and detailed discussion boxes.
"""

import streamlit as st
from components.theme import apply_theme
from components.header import render_header
from components.navigation import navigate_to, render_back_button, render_bottom_nav
from services.quiz_service import get_questions, check_answer
from services.game_service import award_quiz_rewards
from services.config import COLOR_PRIMARY, COLOR_SECONDARY, COLOR_CARD, COLOR_BORDER, COLOR_HIGHLIGHT, COLOR_ERROR


def render_quiz():
    """Renders the step-by-step quiz questions and discussion flow."""
    apply_theme()

    user = st.session_state.get("authenticated_user")
    if not user:
        navigate_to("login")
        return

    render_back_button("learn", "← Keluar Kuis")

    category = st.session_state.get("quiz_category", "hewan")
    chapter_id = st.session_state.get("quiz_chapter", 1)
    q_index = st.session_state.get("quiz_q_index", 0)

    cat_title = "Hewan" if category == "hewan" else "Tumbuhan"

    questions = get_questions(category, chapter_id)
    total_q = len(questions)

    if total_q == 0:
        st.info("Kuis untuk bab ini belum tersedia.")
        return

    # Check if quiz has reached beyond the last question
    if q_index >= total_q:
        navigate_to("quiz_result")
        return

    current_q = questions[q_index]

    # Heading
    st.markdown(
        f"""
        <div style="text-align: center; margin-bottom: 12px;">
            <h2 style="font-size: 22px; font-weight: 800; color: {COLOR_PRIMARY}; margin: 0;">
                Kuis {cat_title}
            </h2>
            <div style="font-size: 12px; color: #555555; margin-top: 2px;">
                Bab {chapter_id} • Soal {q_index + 1} dari {total_q}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Progress Indicator Dots (1 to 5)
    dots_html = '<div class="quiz-dot-row">'
    for i in range(total_q):
        dot_class = "quiz-dot"
        if i == q_index:
            dot_class += " active"
        elif i < q_index:
            dot_class += " done"
        dots_html += f'<div class="{dot_class}">{i + 1}</div>'
    dots_html += "</div>"
    st.markdown(dots_html, unsafe_allow_html=True)

    # Question Box
    st.markdown(
        f"""
        <div class="biova-card" style="margin-bottom: 14px;">
            <div style="font-size: 16px; font-weight: 800; color: {COLOR_PRIMARY}; line-height: 1.4;">
                {current_q.get('question', '')}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    options = current_q.get("options", [])
    q_key = f"quiz_{category}_{chapter_id}_q_{q_index}"
    checked_key = f"checked_{category}_{chapter_id}_q_{q_index}"

    is_checked = st.session_state.get(checked_key, False)

    # Radio options for multiple choice
    user_choice = st.radio(
        "Pilih jawabanmu:",
        options,
        key=f"radio_{q_key}",
        index=None if not is_checked and q_key not in st.session_state else (
            options.index(st.session_state[q_key]) if q_key in st.session_state and st.session_state[q_key] in options else None
        ),
        disabled=is_checked,
        label_visibility="collapsed",
    )

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

    # If NOT checked yet: show "Cek Jawaban"
    if not is_checked:
        if st.button("Cek Jawaban", key=f"btn_check_{q_index}", use_container_width=True):
            if not user_choice:
                st.warning("Silakan pilih salah satu jawaban terlebih dahulu.")
            else:
                st.session_state[q_key] = user_choice
                st.session_state[checked_key] = True

                # Check accuracy
                is_correct, correct_ans, explanation = check_answer(category, chapter_id, q_index, user_choice)
                if is_correct:
                    # Increment running score
                    st.session_state["quiz_score"] = st.session_state.get("quiz_score", 0) + 1

                st.rerun()

    else:
        # ALREADY CHECKED: Show feedback and discussion (Matches PEMBAHSAN KUIS.png)
        saved_answer = st.session_state.get(q_key, "")
        is_correct, correct_ans, explanation = check_answer(category, chapter_id, q_index, saved_answer)

        if is_correct:
            st.markdown(
                f"""
                <div style="background-color: #D1E7DD; border-left: 4px solid #198754; border-radius: 10px; padding: 10px 14px; margin-bottom: 12px; font-weight: 700; color: #0F5132; font-size: 14px;">
                    ✅ Jawabanmu Benar!
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"""
                <div style="background-color: #F8D7DA; border-left: 4px solid {COLOR_ERROR}; border-radius: 10px; padding: 10px 14px; margin-bottom: 12px; font-weight: 700; color: #842029; font-size: 14px;">
                    ❌ Jawabanmu Kurang Tepat. Jawaban yang benar adalah: <strong>{correct_ans}</strong>
                </div>
                """,
                unsafe_allow_html=True,
            )

        # Discussion box matching screenshot
        st.markdown(
            f"""
            <div class="discussion-box">
                <div style="font-weight: 800; font-size: 14px; color: {COLOR_PRIMARY}; margin-bottom: 4px;">
                    💡 Pembahasan:
                </div>
                <div style="font-size: 13px; color: #2E332F; line-height: 1.5;">
                    {explanation}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Button to proceed to next question or view results
        next_label = "Berikutnya →" if (q_index + 1 < total_q) else "Lihat Hasil Kuis 🏆"
        if st.button(next_label, key=f"btn_next_{q_index}", use_container_width=True):
            if q_index + 1 < total_q:
                st.session_state["quiz_q_index"] = q_index + 1
                st.rerun()
            else:
                # Final question complete -> calculate rewards and unlock chapter
                final_score = st.session_state.get("quiz_score", 0)
                stars_won = award_quiz_rewards(user["id"], category, chapter_id, final_score, total_q)
                st.session_state["last_quiz_stars_won"] = stars_won
                st.session_state["last_quiz_final_score"] = final_score
                navigate_to("quiz_result")
