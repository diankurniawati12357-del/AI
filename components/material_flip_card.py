"""HTML renderer for the interactive, self-contained lesson flip card."""

import html
import json


_ROTATE_ICON = (
    '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">'
    '<path d="M20 7v5h-5M4.7 9A7.5 7.5 0 0 1 18 6.5L20 9M4 17v-5h5m10.3 3A7.5 7.5 0 0 1 6 17.5L4 15" '
    'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>'
    "</svg>"
)
_BULB_ICON = (
    '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">'
    '<path d="M9 18h6m-5 3h4m-5.8-6.2A7 7 0 1 1 15.8 15c-.8.7-1.3 1.7-1.3 3h-5c0-1.3-.5-2.3-1.3-3.2zM12 2v2m8 6h-2M6 10H4m13.7-5.7-1.4 1.4M7.7 5.7 6.3 4.3" '
    'fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>'
    "</svg>"
)
_ANIMAL_BACK_DECORATION = (
    '<svg viewBox="0 0 180 52" aria-hidden="true" focusable="false">'
    '<path d="M0 42 Q30 28 62 40 T124 39 T180 36 V52 H0Z" fill="#568967" opacity=".42"/>'
    '<path d="M61 35q4-9 16-9h18q9 0 14 6l12 1-3 6h-8l-3 8h-3l1-9H82l-3 9h-3l1-10q-8 3-13 0z" fill="#74A474"/>'
    '<path d="m108 27-1-8-4-5 5 3 2-7 1 7 6-4-5 6 1 7m-6-4 5-5m-4 8 8-2" fill="none" stroke="#74A474" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>'
    '<path d="m28 8 2 4 4 1-4 2-2 4-2-4-4-2 4-1zm124 2 1.5 3 3.5 1-3.5 1.5-1.5 3-1.5-3-3.5-1.5 3.5-1z" fill="#F7D45C"/>'
    "</svg>"
)
_PLANT_BACK_DECORATION = (
    '<svg viewBox="0 0 180 52" aria-hidden="true" focusable="false">'
    '<path d="M0 42 Q30 28 62 40 T124 39 T180 36 V52 H0Z" fill="#568967" opacity=".42"/>'
    '<path d="M90 45V23m0 12Q76 34 71 22q14-2 19 10m0-4q2-14 16-17 1 13-14 19m-1 7q-13-1-18-12 13-3 19 8" fill="#74A474" stroke="#74A474" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>'
    '<path d="m30 9 2 4 4 1-4 2-2 4-2-4-4-2 4-1zm122 1 1.5 3 3.5 1-3.5 1.5-1.5 3-1.5-3-3.5-1.5 3.5-1z" fill="#F7D45C"/>'
    "</svg>"
)
_BACK_BOTTOM_DECORATION = (
    '<svg viewBox="0 0 320 72" preserveAspectRatio="none" aria-hidden="true" focusable="false">'
    '<path d="M0 72V53q13-20 27-25-3 17-17 26 15-12 33-11-8 15-29 17 20-5 34 5v7zm320 0V53q-13-20-27-25 3 17 17 26-15-12-33-11 8 15 29 17-20-5-34 5v7z" fill="#568967"/>'
    '<path d="M0 72V59q11-12 21-14-2 11-13 17 11-8 24-7-7 11-21 12 13-3 23 5zm320 0V59q-11-12-21-14 2 11 13 17-11-8-24-7 7 11 21 12-13-3-23 5z" fill="#74A474"/>'
    "</svg>"
)


def build_material_flip_card_html(
    *,
    icon_html: str,
    card_number: str,
    title: str,
    category_label: str,
    description: str,
    fun_fact: str,
    examples: str,
    collection_label: str,
    number_label: str,
    flip_to_back_label: str,
    flip_to_front_label: str,
    did_you_know_label: str,
    fun_fact_label: str,
    examples_label: str,
    theme: str,
    language: str,
    front_description: str = "",
    overview_label: str = "Overview",
    flip_indicator_label: str = "",
    state_key: str = "",
    mode: str = "detail",
) -> str:
    """Build the responsive, keyboard-accessible BIOVA collectible flip card."""
    if mode not in {"detail", "collection"}:
        raise ValueError(f"Unknown flip-card mode: {mode}")

    is_collection = mode == "collection"
    back_decoration = (
        _PLANT_BACK_DECORATION if theme == "plants" else _ANIMAL_BACK_DECORATION
    )
    front_hint = flip_indicator_label if is_collection else flip_to_back_label
    card_class = "collection-card" if is_collection else "detail-card"
    card_width = "min(320px, calc(100vw - 32px))"
    card_height = "460px"
    storage_key = json.dumps(state_key, ensure_ascii=True)
    safe = lambda value: html.escape(str(value), quote=True)
    front_description_html = (
        f'<p class="front-description">{safe(front_description)}</p>'
        if front_description
        else ""
    )

    return f"""<!doctype html>
<html lang="{safe(language)}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito+Sans:wght@400;500;600;700;800;900&display=swap');
* {{ box-sizing:border-box; }}
html, body {{ width:100%; height:100%; margin:0; overflow:hidden; }}
body {{ display:flex; align-items:center; justify-content:center; font-family:"Nunito Sans","Segoe UI",sans-serif; }}
.stage {{ width:100%; height:100%; display:flex; align-items:center; justify-content:center; perspective:1000px; }}
.flip-card {{
  position:relative; width:{card_width}; height:{card_height}; padding:0;
  border:0; border-radius:24px; background:transparent; color:inherit;
  cursor:pointer; text-align:center; transform-style:preserve-3d;
  transition:transform 650ms cubic-bezier(0.22, 1, 0.36, 1);
  -webkit-tap-highlight-color:transparent; touch-action:manipulation;
}}
.flip-card.is-flipped {{ transform:rotateY(180deg); }}
.flip-card:focus-visible {{ outline:3px solid #EAB83F; outline-offset:4px; }}
.side {{
  position:absolute; inset:0; display:grid; grid-template-rows:auto minmax(0,1fr) auto;
  gap:8px; overflow:hidden; padding:16px 18px 15px;
  border:1px solid rgba(32,62,48,.18); border-radius:24px;
  backface-visibility:hidden; -webkit-backface-visibility:hidden;
  box-shadow:0 12px 28px rgba(32,62,48,.15);
}}
.front {{
  color:#203E30;
  background:linear-gradient(180deg,rgba(234,243,210,.28),transparent 54%),#FFF9EB;
}}
.back {{ transform:rotateY(180deg); padding:20px; color:#FFF9EB; background:linear-gradient(145deg,#143D2A 0%,#204D36 55%,#173E2B 100%); }}
.topline {{
  width:100%; min-width:0; display:flex; align-items:center; justify-content:space-between;
  gap:8px; color:#203E30; font-size:11px; font-weight:800; letter-spacing:.45px;
  line-height:1.2; text-align:left; white-space:nowrap;
}}
.topline span:last-child {{ text-align:right; }}
.back .topline {{ position:relative; z-index:2; color:#EAF2DD; font-size:10px; letter-spacing:.6px; }}
.main {{ min-height:0; width:100%; display:flex; flex-direction:column; align-items:center; }}
.front-main {{ justify-content:center; }}
.art {{
  position:relative; flex:0 0 154px; width:100%; display:flex; align-items:center;
  justify-content:center; isolation:isolate; margin:0 0 3px;
}}
.art::before {{
  content:""; position:absolute; z-index:-1; width:148px; height:148px;
  border-radius:50%; background:#EAF3D2;
}}
.art img {{
  position:relative; z-index:1; display:block; width:min(184px,70vw) !important;
  height:154px !important; object-fit:contain; filter:drop-shadow(0 7px 7px rgba(32,62,48,.12));
}}
.leaf {{ position:absolute; z-index:0; bottom:10px; width:28px; height:13px; border-radius:100% 0 100% 0; background:#A9CA72; opacity:.72; }}
.leaf-left {{ left:calc(50% - 88px); transform:rotate(27deg); }}
.leaf-right {{ right:calc(50% - 88px); transform:rotate(-63deg); }}
h1 {{
  display:-webkit-box; max-width:100%; margin:0 0 7px; overflow:hidden;
  color:#203E30; font-size:24px; font-weight:800; line-height:1.16;
  overflow-wrap:anywhere; -webkit-box-orient:vertical; -webkit-line-clamp:2;
}}
.badge {{
  max-width:100%; border:1px solid #A9CA72; border-radius:999px;
  padding:5px 12px; color:#203E30; background:#EAF3D2; font-size:13px;
  font-weight:700; line-height:1.25; overflow-wrap:anywhere;
}}
.front-description {{
  display:-webkit-box; max-width:252px; margin:8px 0 0; overflow:hidden;
  color:#455B49; font-size:14px; font-weight:500; line-height:1.42;
  overflow-wrap:anywhere; -webkit-box-orient:vertical; -webkit-line-clamp:2;
}}
.hint {{
  justify-self:center; display:inline-flex; min-height:32px; align-items:center;
  justify-content:center; gap:7px; margin:0; padding:6px 15px;
  border:1px solid rgba(169,202,114,.8); border-radius:999px;
  color:#203E30; background:#EAF3D2; font-size:13px; font-weight:800;
  line-height:1.2; white-space:nowrap;
}}
.hint svg {{ width:16px; height:16px; flex:none; }}
.back-main {{ position:relative; z-index:1; justify-content:center; gap:8px; }}
.back-top-art {{
  position:absolute; top:0; left:0; width:100%; height:32px;
  display:flex; align-items:center; justify-content:center; pointer-events:none; opacity:.45;
}}
.back-top-art svg {{ display:block; width:132px; height:36px; overflow:visible; }}
.back h2 {{
  display:-webkit-box; max-width:100%; margin:31px 0 0; overflow:hidden;
  color:#FFF9EB; font-size:25px; font-weight:800; line-height:1.2;
  overflow-wrap:anywhere; -webkit-box-orient:vertical; -webkit-line-clamp:2;
}}
.section-divider {{
  width:100%; display:flex; align-items:center; gap:9px;
  color:#E1EDD9; font-size:11px; font-weight:800; letter-spacing:.7px;
  line-height:1.2; text-transform:uppercase;
}}
.section-divider::before,
.section-divider::after {{ content:""; flex:1 1 auto; height:1px; background:rgba(225,237,217,.35); }}
.fact-block {{ display:block; width:100%; margin:0; text-align:center; }}
.fact-block p {{ margin:0; color:#FFF9EB; font-size:14px; line-height:1.45; overflow-wrap:anywhere; }}
.overview p {{
  display:-webkit-box; overflow:hidden; color:#FFF9EB; font-size:14px;
  line-height:1.4; -webkit-box-orient:vertical; -webkit-line-clamp:3;
}}
.fun-fact {{
  padding:12px; border:1px solid rgba(247,212,92,.5); border-radius:14px;
  background:rgba(255,255,255,.08); box-shadow:0 3px 12px rgba(0,0,0,.08); text-align:center;
}}
.fun-fact-label {{
  display:flex; width:max-content; max-width:100%; min-height:22px; align-items:center; justify-content:center;
  gap:5px; margin:0 auto 6px; padding:0; border-radius:999px;
  color:#F7D45C; background:transparent; font-size:12px; font-weight:800;
  line-height:1.2; text-transform:uppercase; letter-spacing:.45px;
}}
.fun-fact-label svg {{ width:15px; height:15px; flex:none; }}
.fun-fact p {{
  display:-webkit-box; overflow:hidden; color:#FFF3C5; font-size:15px;
  font-weight:600; line-height:1.45; -webkit-box-orient:vertical; -webkit-line-clamp:3;
}}
.examples-heading {{ font-size:11px; }}
.examples p {{ display:-webkit-box; overflow:hidden; color:#FFF9EB; font-size:13px; line-height:1.45; -webkit-box-orient:vertical; -webkit-line-clamp:2; }}
.back-bottom-art {{
  position:absolute; z-index:0; right:0; bottom:0; left:0; height:68px;
  pointer-events:none; opacity:.24;
}}
.back-bottom-art svg {{ display:block; width:100%; height:100%; }}
.back .hint {{
  position:relative; z-index:2; width:72%; min-height:38px;
  border-color:rgba(255,255,255,.25); color:#FFF9EB;
  background:rgba(255,255,255,.1); font-size:13px; font-weight:700;
}}
@media (max-width:380px) {{
  .side {{ padding-right:15px; padding-left:15px; }}
  .topline {{ font-size:10px; letter-spacing:.3px; }}
  .front-description {{ max-width:238px; font-size:13.5px; }}
}}
@media (prefers-reduced-motion:reduce) {{ .flip-card {{ transition-duration:1ms; }} }}
</style>
</head>
<body>
<div class="stage">
  <button class="flip-card {card_class}" type="button" data-theme="{safe(theme)}" aria-label="{safe(front_hint)}" aria-pressed="false">
    <span class="side front" aria-hidden="false">
      <span class="topline"><span>{safe(collection_label)}</span><span>{safe(number_label)} {safe(card_number)}</span></span>
      <span class="main front-main">
        <span class="art"><span class="leaf leaf-left"></span><span class="leaf leaf-right"></span>{icon_html}</span>
        <h1>{safe(title)}</h1>
        <span class="badge">{safe(category_label)}</span>
        {front_description_html}
      </span>
      <span class="hint">{_ROTATE_ICON}{safe(front_hint)}</span>
    </span>
    <span class="side back" aria-hidden="true">
      <span class="back-bottom-art">{_BACK_BOTTOM_DECORATION}</span>
      <span class="topline"><span>{safe(collection_label)}</span><span>{safe(number_label)} {safe(card_number)}</span></span>
      <span class="main back-main">
        <span class="back-top-art">{back_decoration}</span>
        <h2>{safe(title)}</h2>
        <span class="section-divider overview-heading">{safe(overview_label)}</span>
        <span class="fact-block overview"><p>{safe(description)}</p></span>
        <span class="fact-block fun-fact">
          <span class="fun-fact-label">{_BULB_ICON}{safe(fun_fact_label)}</span>
          <p>{safe(fun_fact)}</p>
        </span>
        <span class="section-divider examples-heading">{safe(examples_label)}</span>
        <span class="fact-block examples"><p>{safe(examples)}</p></span>
      </span>
      <span class="hint">{_ROTATE_ICON}{safe(flip_to_front_label)}</span>
    </span>
  </button>
</div>
<script>
const card = document.querySelector(".flip-card");
const front = card.querySelector(".front");
const back = card.querySelector(".back");
const storageKey = {storage_key};
let flipped = false;
if (storageKey) {{
  try {{
    flipped = window.localStorage.getItem(storageKey) === "back";
  }} catch (error) {{
    console.warn("Flip-card state could not be restored.", error);
  }}
}}
const updateCard = () => {{
  card.classList.toggle("is-flipped", flipped);
  card.setAttribute("aria-pressed", String(flipped));
  card.setAttribute("aria-label", flipped ? "{safe(flip_to_front_label)}" : "{safe(front_hint)}");
  front.setAttribute("aria-hidden", String(flipped));
  back.setAttribute("aria-hidden", String(!flipped));
}};
updateCard();
card.addEventListener("click", () => {{
  flipped = !flipped;
  updateCard();
  if (storageKey) {{
    try {{
      window.localStorage.setItem(storageKey, flipped ? "back" : "front");
    }} catch (error) {{
      console.warn("Flip-card state could not be saved.", error);
    }}
  }}
}});
</script>
</body>
</html>"""
