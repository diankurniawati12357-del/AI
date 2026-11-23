"""BIOVA category quiz with session-stable randomized questions and options."""

import html

import streamlit as st

from components.header import render_header
from components.i18n import localize_quiz_question, t
from components.icons import render_icon
from components.navigation import navigate_to, render_back_button, render_bottom_nav
from components.theme import apply_theme
from services.config import COLOR_ERROR, COLOR_PRIMARY
from services.game_service import award_quiz_rewards
from services.quiz_service import (
    check_answer,
    get_question_by_id,
    initialize_quiz_session,
)


def _save_quiz_session(category: str, quiz_session: dict) -> None:
    sessions = dict(st.session_state.get("quiz_sessions", {}))
    sessions[category] = quiz_session
    st.session_state["quiz_sessions"] = sessions


def render_quiz():
    apply_theme()

    user = st.session_state.get("authenticated_user")
    if not user:
        navigate_to("login")
        return

    category = st.session_state.get("quiz_category", "hewan")
    if category not in ("hewan", "tumbuhan"):
        category = "hewan"
    sessions = st.session_state.get("quiz_sessions", {})
    quiz_session = sessions.get(category)
    if not quiz_session:
        if st.session_state.get("quiz_start_error") or not initialize_quiz_session(
            category, st.session_state
        ):
            render_header(show_stars=True)
            st.error(t("quiz.unavailable"))
            render_bottom_nav(current_active="learn")
            return
        quiz_session = st.session_state["quiz_sessions"][category]

    render_back_button("learn", t("quiz.exit"))
    render_header(show_stars=True)

    question_ids = quiz_session["question_ids"]
    total_questions = len(question_ids)
    question_index = int(st.session_state.get("quiz_q_index", 0))
    if question_index >= total_questions:
        navigate_to("quiz_result")
        return

    question_id = question_ids[question_index]
    question = get_question_by_id(category, question_id)
    if question is None:
        st.error(t("quiz.unavailable"))
        render_bottom_nav(current_active="learn")
        return

    display_question = localize_quiz_question(question)
    language = st.session_state.get("language", "id")
    category_title = t("category.animals") if category == "hewan" else t("category.plants")

    st.markdown(
        f"""
        <div style="text-align:center;margin-bottom:12px;">
            <h2 style="font-size:22px;font-weight:800;color:{COLOR_PRIMARY};margin:0;">
                {html.escape(t("quiz.title").format(category=category_title))}
            </h2>
            <div style="font-size:12px;color:#555555;margin-top:2px;">
                {t("quiz.question").format(current=question_index + 1, total=total_questions)}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    dots_html = '<div class="quiz-dot-row">'
    for index in range(total_questions):
        dot_class = "quiz-dot"
        if index == question_index:
            dot_class += " active"
        elif index < question_index:
            dot_class += " done"
        dots_html += f'<div class="{dot_class}">{index + 1}</div>'
    st.markdown(dots_html + "</div>", unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class="biova-card" style="margin-bottom:14px;">
            <div style="font-size:16px;font-weight:800;color:{COLOR_PRIMARY};line-height:1.4;">
                {html.escape(display_question["question"])}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    answers = dict(quiz_session.get("answers", {}))
    checked_ids = set(quiz_session.get("checked_ids", []))
    is_checked = question_id in checked_ids
    option_order = quiz_session["option_orders"][question_id]
    displayed_options = display_question["options"]
    option_labels = {
        option_id: f"{option_id}. {text}"
        for option_id, text in displayed_options.items()
    }
    widget_key = f"quiz_{quiz_session['session_id']}_{question_id}"
    selected_option_id = st.radio(
        t("quiz.choose"),
        option_order,
        format_func=lambda option_id: option_labels[option_id],
        key=widget_key,
        index=option_order.index(answers[question_id])
        if question_id in answers and answers[question_id] in option_order
        else None,
        disabled=is_checked,
        label_visibility="collapsed",
    )
    st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)

    if not is_checked:
        st.markdown(
            f'<div class="biova-icon-action">{render_icon("cek", 22, "biova-icon--button", t("quiz.check"))}</div>',
            unsafe_allow_html=True,
        )
        if st.button(t("quiz.check"), key=f"btn_check_{widget_key}", use_container_width=True):
            if selected_option_id is None:
                st.warning(t("quiz.choose_warning"))
            else:
                answers[question_id] = selected_option_id
                checked_ids.add(question_id)
                quiz_session["answers"] = answers
                quiz_session["checked_ids"] = list(checked_ids)
                _save_quiz_session(category, quiz_session)
                st.rerun()
    else:
        selected_answer = answers[question_id]
        is_correct, correct_option_id, explanation = check_answer(
            category, question_id, selected_answer
        )
        explanation_text = explanation.get(language, explanation.get("id", ""))
        if is_correct:
            st.markdown(
                f"""
                <div style="background:#D1E7DD;border-left:4px solid #198754;border-radius:10px;padding:10px 14px;margin-bottom:12px;font-weight:700;color:#0F5132;font-size:14px;">
                    {render_icon("cek", 22, "biova-icon--button", t("quiz.correct"))} {t("quiz.correct")}
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            correct_text = html.escape(option_labels[correct_option_id])
            st.markdown(
                f"""
                <div style="background:#F8D7DA;border-left:4px solid {COLOR_ERROR};border-radius:10px;padding:10px 14px;margin-bottom:12px;font-weight:700;color:#842029;font-size:14px;">
                    {render_icon("info", 22, "biova-icon--button", t("quiz.incorrect"))}
                    {t("quiz.incorrect")} {t("quiz.correct_answer")} <strong>{correct_text}</strong>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown(
            f"""
            <div class="discussion-box">
                <div style="font-weight:800;font-size:14px;color:{COLOR_PRIMARY};margin-bottom:4px;">
                    {render_icon("info", 22, "biova-icon--button", t("quiz.discussion"))} {t("quiz.discussion")}
                </div>
                <div style="font-size:13px;color:#2E332F;line-height:1.5;">
                    {html.escape(explanation_text)}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        is_final_question = question_index + 1 == total_questions
        next_label = t("quiz.result") if is_final_question else t("quiz.next")
        if is_final_question:
            st.markdown(
                f'<div class="biova-icon-action">{render_icon("piala", 24, "biova-icon--button", t("quiz.result"))}</div>',
                unsafe_allow_html=True,
            )
        if st.button(next_label, key=f"btn_next_{widget_key}", use_container_width=True):
            if not is_final_question:
                st.session_state["quiz_q_index"] = question_index + 1
                st.rerun()
            else:
                correct_question_ids = [
                    selected_id
                    for selected_id in question_ids
                    if check_answer(category, selected_id, answers[selected_id])[0]
                ]
                score = len(correct_question_ids)
                stars_won = award_quiz_rewards(
                    user["id"],
                    category,
                    score=score,
                    max_questions=total_questions,
                    question_ids=correct_question_ids,
                )
                st.session_state["last_quiz_stars_won"] = stars_won
                st.session_state["last_quiz_final_score"] = score
                st.session_state["last_quiz_total_questions"] = total_questions
                navigate_to("quiz_result")

    render_bottom_nav(current_active="learn")
