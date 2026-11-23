"""BIOVA collectible learning cards and dedicated material detail page."""

import html
import streamlit as st

from components.theme import apply_theme
from components.header import render_header
from components.icons import render_icon, get_animal_class_icon, get_plant_topic_icon
from components.navigation import navigate_to, render_back_button, render_bottom_nav
from components.i18n import (
    get_collection_flip_copy,
    get_material_flip_copy,
    init_language,
    localize_material_card,
    t,
)
from components.material_flip_card import build_material_flip_card_html
from services.materi_service import get_all_cards


def _get_card_icon(category: str, card: dict) -> str:
    if category == "hewan":
        class_id = str(card.get("class_id") or card.get("class_name") or card.get("title") or "")
        icon_name, _ = get_animal_class_icon(class_id)
        return icon_name
    topic_id = str(card.get("topic_id") or card.get("title") or "")
    return get_plant_topic_icon(topic_id)


def _render_card_grid(category: str, cards: list, user_id: int):
    def render_collectible(col, index, original):
        localized = localize_material_card(original)
        icon_name = _get_card_icon(category, original)
        copy = get_collection_flip_copy(category, original["material_id"])
        material_id = original["material_id"]
        stable_card_id = f"{'animal' if category == 'hewan' else 'plant'}_{material_id}"
        with col:
            with st.container(key=f"collection-card-{stable_card_id}"):
                card_html = build_material_flip_card_html(
                    icon_html=render_icon(
                        icon_name,
                        160,
                        "biova-card-float",
                        str(localized.get("title", "")),
                    ),
                    card_number=f"#{index + 1:02d}",
                    title=localized.get("title", ""),
                    category_label=localized.get(
                        "class_name",
                        localized.get("topic_name", ""),
                    ),
                    description=copy["description"],
                    fun_fact=copy["fun_fact"],
                    examples=copy["examples"],
                    collection_label=t("lesson.collection_brand"),
                    number_label=t("lesson.card_number"),
                    flip_to_back_label=t("lesson.flip_to_back"),
                    flip_to_front_label=t("collection.return"),
                    did_you_know_label=t("lesson.did_you_know"),
                    fun_fact_label=t("lesson.fun_fact"),
                    examples_label=t("lesson.examples"),
                    theme="plants" if category == "tumbuhan" else "animals",
                    language=init_language(),
                    front_description=localized.get(
                        "characteristics",
                        localized.get("description", ""),
                    ),
                    overview_label=t("collection.overview"),
                    flip_indicator_label=t("collection.flip"),
                    state_key=f"biova-flip-{user_id}-{stable_card_id}",
                    mode="collection",
                )
                st.iframe(
                    card_html,
                    height=480,
                    tab_index=0,
                    alt=t("lesson.flip_card_alt").format(
                        title=localized.get("title", ""),
                    ),
                )

    with st.container(key="biova-material-collection"):
        for start in range(0, len(cards), 3):
            row_cards = cards[start:start + 3]
            row_key = "biova-material-row-last" if len(row_cards) == 2 else f"biova-material-row-{start // 3}"
            with st.container(key=row_key):
                if len(row_cards) == 3:
                    cols = st.columns(3, gap="small")
                    for offset, card in enumerate(row_cards):
                        render_collectible(cols[offset], start + offset, card)
                elif len(row_cards) == 2:
                    cols = st.columns([1, 4, 4, 1], gap="small")
                    for offset, card in enumerate(row_cards):
                        render_collectible(cols[offset + 1], start + offset, card)


def _render_detail(category: str, cards: list, card_index: int):
    original = cards[card_index]
    card = localize_material_card(original)
    icon_name = _get_card_icon(category, original)

    render_back_button(
        "lesson",
        compact=True,
        key="btn_back_to_collection",
        state_updates={"lesson_detail_mode": False},
    )
    st.markdown(
        f'<div class="biova-detail-heading"><span>{html.escape(str(card.get("class_name", card.get("topic_name", ""))))}</span>'
        f'<h2>{html.escape(str(card.get("title", "")))}</h2></div>',
        unsafe_allow_html=True,
    )

    copy = get_material_flip_copy(category, original["material_id"])
    flip_card = build_material_flip_card_html(
        icon_html=render_icon(
            icon_name,
            205,
            "biova-card-float",
            str(card.get("title", "")),
        ),
        card_number=f"#{card_index + 1:02d}",
        title=card.get("title", ""),
        category_label=card.get("class_name", card.get("topic_name", "")),
        description=copy["description"],
        fun_fact=copy["fun_fact"],
        examples=copy["examples"],
        collection_label=t("lesson.collection_brand"),
        number_label=t("lesson.card_number"),
        flip_to_back_label=t("lesson.flip_to_back"),
        flip_to_front_label=t("lesson.flip_to_front"),
        did_you_know_label=t("lesson.did_you_know"),
        fun_fact_label=t("lesson.fun_fact"),
        examples_label=t("lesson.examples"),
        overview_label=t("collection.overview"),
        theme="plants" if category == "tumbuhan" else "animals",
        language=init_language(),
        front_description=card.get(
            "characteristics",
            card.get("description", ""),
        ),
    )
    st.iframe(
        flip_card,
        height=480,
        tab_index=0,
        alt=t("lesson.flip_card_alt").format(title=card.get("title", "")),
    )

    nav = st.columns([1, 1, 1], gap="small")
    with nav[0]:
        if st.button(t("lesson.previous"), key="btn_detail_prev", use_container_width=True, disabled=card_index == 0):
            st.session_state["current_card_index"] = card_index - 1
            st.rerun()
    with nav[1]:
        st.markdown(
            f'<div class="biova-detail-position">{card_index + 1} / {len(cards)}</div>',
            unsafe_allow_html=True,
        )
    with nav[2]:
        if st.button(t("lesson.next"), key="btn_detail_next", use_container_width=True, disabled=card_index >= len(cards) - 1):
            st.session_state["current_card_index"] = card_index + 1
            st.rerun()


def render_lesson():
    apply_theme()
    user = st.session_state.get("authenticated_user")
    if not user:
        navigate_to("login")
        return

    render_header(show_stars=True)
    category = st.session_state.get("learning_category", "hewan")
    cat_title = t("category.animals") if category == "hewan" else t("category.plants")

    cards = get_all_cards(category)
    if not cards:
        st.error(t("lesson.no_data"))
        return

    detail_mode = st.session_state.get("lesson_detail_mode", False)
    current_idx = max(0, min(int(st.session_state.get("current_card_index", 0)), len(cards) - 1))
    st.session_state["current_card_index"] = current_idx

    if detail_mode:
        _render_detail(category, cards, current_idx)
    else:
        render_back_button(
            "learn",
            compact=True,
            key="btn_back_lesson_collection",
        )
        st.markdown(
            f'<div class="biova-lesson-heading"><span>{cat_title}</span>'
            f'<h2>{t("lesson.collection").format(category=cat_title)}</h2></div>',
            unsafe_allow_html=True,
        )
        _render_card_grid(category, cards, user["id"])

    render_bottom_nav(current_active="learn")
