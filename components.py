"""
components.py — Reusable HTML/Streamlit UI components.
All functions return HTML strings or render directly with st.markdown().
"""

import streamlit as st
from product_images import get_product_image


# ── Page Header ──────────────────────────────────────────────
def page_header(title: str, subtitle: str) -> None:
    st.markdown(f"""
    <div class="page-header">
        <div class="page-title">{title}</div>
        <div class="page-sub">{subtitle}</div>
    </div>
    """, unsafe_allow_html=True)


# ── Demo Banner ───────────────────────────────────────────────
def demo_banner(is_demo: bool) -> None:
    if is_demo:
        st.markdown("""
        <div class="demo-banner">
            🎬 <strong>Demo Mode</strong> &nbsp;—&nbsp;
            Running with mock AI data. Add <code>GEMINI_API_KEY</code> to <code>.env</code> to go live.
        </div>
        """, unsafe_allow_html=True)


# ── Hero Stat Cards ───────────────────────────────────────────
def hero_cards(stats: dict, missing: int = 0) -> None:
    cards = [
        ("primary", "🛍️", missing,                      "What's Missing"),
        ("success", "✅", stats.get("fresh", 0),         "Fresh"),
        ("warning", "⏳", stats.get("expiring_soon", 0), "Running Low"),
        ("danger",  "🗑", stats.get("expired", 0),       "Expired"),
    ]
    html = '<div class="hero-row">'
    for variant, icon, value, label in cards:
        html += f"""
        <div class="hero-card {variant}">
            <div class="hc-icon">{icon}</div>
            <div class="hc-value">{value}</div>
            <div class="hc-label">{label}</div>
        </div>"""
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)


# ── Status Badge ──────────────────────────────────────────────
def status_badge(status: str) -> str:
    mapping = {
        "Fresh":       "badge-fresh",
        "Use Soon":    "badge-soon",
        "Running Low": "badge-low",
        "Expired":     "badge-expired",
    }
    cls = mapping.get(status, "badge-gray")
    return f'<span class="badge {cls}">{status}</span>'


def category_badge(category: str) -> str:
    return f'<span class="badge badge-primary">{category}</span>'


def user_badge(user: str) -> str:
    return f'<span class="badge badge-gray">👤 {user}</span>'


# ── Shelf Life Bar ─────────────────────────────────────────────
def shelf_bar(days_remaining: int, shelf_life_days: int, status: str) -> str:
    pct = min(100, round(days_remaining / max(shelf_life_days, 1) * 100))
    cls_map = {
        "Fresh": "fresh", "Use Soon": "soon",
        "Running Low": "low", "Expired": "expired",
    }
    bar_cls = cls_map.get(status, "fresh")
    label = f"{days_remaining}d left" if days_remaining > 0 else "Expired"
    return f"""
    <div class="shelf-bar-wrap">
        <div class="shelf-bar-bg">
            <div class="shelf-bar-fill {bar_cls}" style="width:{pct}%"></div>
        </div>
        <div class="shelf-days">{label}</div>
    </div>"""


# ── Item Card ─────────────────────────────────────────────────
def item_card_html(item: dict, prediction: str = "") -> str:
    img_html = get_product_image(item['product_name'], item['category'])
    prediction_html = (
        f'<div class="item-prediction">🔮 Prediction: {prediction}</div>'
        if prediction else ""
    )
    return f"""
    <div class="item-card">
        <div class="item-card-top">
            {img_html}
            <div style="flex:1;min-width:0">
                <div class="item-name">{item['product_name']}</div>
                <div class="item-qty">{item['quantity']}</div>
            </div>
            {status_badge(item['status'])}
        </div>
        {shelf_bar(item['days_remaining'], item['shelf_life_days'], item['status'])}
        {prediction_html}
        <div class="item-meta">
            {category_badge(item['category'])}
            {user_badge(item['added_by'])}
        </div>
    </div>
    """


def _category_emoji(category: str) -> str:
    return {
        "Produce": "🥬", "Dairy": "🥛", "Meat & Fish": "🥩",
        "Bakery": "🍞", "Frozen": "🧊", "Pantry": "🫙",
        "Beverages": "🧃", "Snacks": "🍪", "Household": "🧹",
        "Personal Care": "🧴",
    }.get(category, "📦")


# ── Wizard Steps ──────────────────────────────────────────────
def wizard_steps(current: int) -> None:
    """current: 1=Upload, 2=Analyzing, 3=Review, 4=Saved"""
    steps = ["Upload", "Analyzing", "Review", "Saved"]
    html = '<div class="wizard-steps">'
    for i, label in enumerate(steps, 1):
        if i < current:
            cls = "done"
            num = "✓"
        elif i == current:
            cls = "active"
            num = str(i)
        else:
            cls = ""
            num = str(i)

        html += f"""
        <div class="wizard-step {cls}">
            <div class="step-num">{num}</div>
            <span>{label}</span>
        </div>"""
        if i < len(steps):
            html += '<div class="step-sep"></div>'
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)


# ── Recipe Card ───────────────────────────────────────────────
def recipe_card(recipe: dict, index: int) -> None:
    name  = recipe.get("name", "Recipe")
    mins  = recipe.get("prep_time_minutes", "?")
    ingrs = recipe.get("uses_ingredients", [])
    steps = recipe.get("instructions", [])
    tip   = recipe.get("tip", "")

    ingredient_badges = "".join(
        f'<span class="badge badge-primary" style="background:#EDE9FE;color:#5B21B6">{i}</span> '
        for i in ingrs
    )
    steps_html = "".join(f"<li>{s}</li>" for s in steps)
    tip_html = f'<div class="recipe-tip">💡 {tip}</div>' if tip else ""

    st.markdown(f"""
    <div class="recipe-card">
        <div class="recipe-header">
            <div class="recipe-title">🍽 Recipe {index}: {name}</div>
            <div class="recipe-time">⏱ {mins} minutes prep</div>
        </div>
        <div class="recipe-body">
            <div class="section-title">Uses from your food</div>
            <div class="recipe-ingredients">{ingredient_badges}</div>
            <div class="section-title">Instructions</div>
            <div class="recipe-steps"><ol>{steps_html}</ol></div>
            {tip_html}
        </div>
    </div>
    """, unsafe_allow_html=True)


# ── Upload Zone ───────────────────────────────────────────────
def upload_zone_hint() -> None:
    st.markdown("""
    <div class="upload-zone">
        <div class="upload-icon">📄</div>
        <div class="upload-text">Drag & drop your grocery receipt here</div>
        <div class="upload-sub">Supports JPG, PNG, WEBP — up to 10 MB</div>
        <div class="upload-sub" style="margin-top:8px">Or click "Load Demo Receipt" below ↓</div>
    </div>
    """, unsafe_allow_html=True)


# ── Alert Card (Running Low) ──────────────────────────────────
def alert_card_html(item: dict) -> str:
    is_expired = item["days_remaining"] == 0
    card_cls   = "alert-card" if is_expired else "alert-card warn"
    countdown  = "EXPIRED" if is_expired else f"{item['days_remaining']}d"
    count_cls  = "alert-countdown" if is_expired else "alert-countdown warn"
    img_url    = get_product_image(item['product_name'], item['category'])
    img_html   = (
        f'<img src="{img_url}" class="item-thumb" alt="{item["product_name"]}" '
        f'onerror="this.style.display=\'none\'">'
        if img_url else
        f'<div class="item-thumb item-thumb-emoji">{_category_emoji(item["category"])}</div>'
    )
    return f"""
    <div class="{card_cls}">
        <div style="display:flex;justify-content:space-between;align-items:center;gap:12px">
            {img_html}
            <div style="flex:1;min-width:0">
                <div class="alert-name">{item['product_name']}</div>
                <div class="alert-meta">{item['category']} · {item['quantity']} · Added by {item['added_by']}</div>
            </div>
            <div class="{count_cls}">{countdown}</div>
        </div>
    </div>"""


# ── Prediction Card ───────────────────────────────────────────
def prediction_card_html(pred: dict) -> str:
    urgency_cls = "badge-low" if pred["urgency"] == "High" else "badge-soon"
    return f"""
    <div class="item-card">
        <div class="item-card-top">
            <div>
                <div class="item-name">{pred['product_name']}</div>
                <div class="item-qty">Usually bought every {pred['avg_gap_days']} days · last bought {pred['days_since_last']} days ago</div>
            </div>
            <span class="badge {urgency_cls}">⚠ {pred['urgency']}</span>
        </div>
        <div class="item-meta">
            {category_badge(pred['category'])}
        </div>
    </div>"""


# ── Pantry Card ───────────────────────────────────────────────
def pantry_card_html(item: dict, prediction: str = "") -> str:
    img_html = get_product_image(item['product_name'], item['category'])
    days = item['days_remaining']
    if days <= 0:
        expiry_cls, expiry_text = "expired", "Expired"
    elif days <= 2:
        expiry_cls, expiry_text = "low", f"⚠ {days}d left"
    elif days <= 5:
        expiry_cls, expiry_text = "soon", f"⏳ {days}d left"
    else:
        expiry_cls, expiry_text = "fresh", f"✅ {days}d left"
    pred_html = f'<div class="pc-pred">🔮 {prediction}</div>' if prediction else ""
    return f"""
    <div class="pantry-card">
        <div class="pc-img">{img_html}</div>
        <div class="pc-name">{item['product_name']}</div>
        <div class="pc-qty">{item['quantity']}</div>
        <div class="pc-footer">
            <span class="pc-expiry {expiry_cls}">{expiry_text}</span>
            {pred_html}
        </div>
    </div>"""


# ── Section Title ─────────────────────────────────────────────
def section_title(text: str) -> None:
    st.markdown(f'<div class="section-title">{text}</div>', unsafe_allow_html=True)
