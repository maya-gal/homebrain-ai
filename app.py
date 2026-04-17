"""
HomeBrain AI — Full System
Streamlit app: Receipt → Inventory → Meal Planning → Shopping List → Smart Predictions
"""

import os
import time
import pandas as pd
import streamlit as st
from dotenv import load_dotenv

from styles import get_css
from database import (
    init_db, insert_items, get_all_items, search_items,
    get_expiring_items, get_categories, get_stats, delete_item,
    add_to_shopping_list, get_smart_predictions,
)
from components import (
    page_header, demo_banner, hero_cards, wizard_steps,
    item_card_html, recipe_card, upload_zone_hint,
    alert_card_html, prediction_card_html, section_title,
    status_badge, category_badge,
)
from demo_data import MOCK_RECEIPT_RESPONSE, MOCK_RECIPES, seed_usage_log
import shopping_list as shopping_list_page

# ── Bootstrap ─────────────────────────────────────────────────
load_dotenv()
init_db()

# Seed demo usage log on first run
from database import _conn, DB_PATH
if DB_PATH.exists():
    with _conn() as conn:
        seed_usage_log(conn)

st.set_page_config(
    page_title="HomeBrain AI",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.markdown(get_css(), unsafe_allow_html=True)

PAGES = [
    ("📸", "Scan Receipt"),
    ("🫙", "מזווה"),
    ("🛒", "Shopping List"),
    ("🍳", "Meal Planner"),
    ("⚠️", "Running Low"),
    ("🧠", "AI Predictions"),
]


# ── Gemini API key ────────────────────────────────────────────
@st.cache_resource
def get_api_key() -> str:
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        try:
            key = st.secrets.get("GEMINI_API_KEY", "")
        except Exception:
            key = ""
    return key or ""


def is_demo() -> bool:
    return not get_api_key()


# ── Sidebar ───────────────────────────────────────────────────
def render_sidebar() -> tuple[str, str]:
    with st.sidebar:
        # Brand
        st.markdown("""
        <div style="padding:0.5rem 0 0.25rem">
            <div class="sidebar-brand">🏠 HomeBrain AI</div>
            <div class="sidebar-tagline">Your family's smart pantry</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<hr class="sidebar-divider" style="border-color:#1E293B;margin:12px 0">', unsafe_allow_html=True)

        # Nav
        if "page" not in st.session_state:
            st.session_state.page = "Scan Receipt"

        for icon, label in PAGES:
            active = st.session_state.page == label
            btn_cls = "nav-btn active" if active else "nav-btn"
            # Use a real button for click handling
            if st.button(f"{icon}  {label}", key=f"nav_{label}",
                         use_container_width=True,
                         type="primary" if active else "secondary"):
                st.session_state.page = label
                st.rerun()

        st.markdown('<hr style="border-color:#1E293B;margin:12px 0">', unsafe_allow_html=True)

        # User selector
        user = st.selectbox(
            "👤 Adding as",
            ["You", "Mom", "Dad", "Kids"],
            label_visibility="visible",
        )

        st.markdown('<hr style="border-color:#1E293B;margin:12px 0">', unsafe_allow_html=True)

        # Live stats
        stats = get_stats()
        st.markdown('<div style="font-size:0.7rem;font-weight:700;letter-spacing:1px;color:#475569;text-transform:uppercase;margin-bottom:8px">Pantry Stats</div>', unsafe_allow_html=True)

        warn_color = "danger" if stats["expiring_soon"] > 0 else ""
        st.markdown(f"""
        <div class="stat-pill">
            <span class="label">Total items</span>
            <span class="value">{stats['total']}</span>
        </div>
        <div class="stat-pill">
            <span class="label">Running Low</span>
            <span class="value {'warn' if stats['expiring_soon'] > 0 else ''}">{stats['expiring_soon']}</span>
        </div>
        <div class="stat-pill">
            <span class="label">Expired</span>
            <span class="value {'danger' if stats['expired'] > 0 else ''}">{stats['expired']}</span>
        </div>
        <div class="stat-pill">
            <span class="label">Categories</span>
            <span class="value">{stats['categories']}</span>
        </div>
        """, unsafe_allow_html=True)

        if is_demo():
            st.markdown('<div style="margin-top:12px;font-size:0.72rem;color:#475569;text-align:center">🎬 Demo Mode</div>', unsafe_allow_html=True)

    return st.session_state.page, user


# ── Page: Scan Receipt ────────────────────────────────────────
def page_scan_receipt(user: str) -> None:
    page_header("📸 Scan Receipt", "Upload a grocery receipt — AI extracts your inventory automatically. Zero typing required.")
    demo_banner(is_demo())

    # Determine wizard step
    cache_key = st.session_state.get("current_receipt_key", "")
    has_data  = cache_key and cache_key in st.session_state
    step = 3 if has_data else 1

    wizard_steps(step)

    uploaded = st.file_uploader(
        "Receipt image",
        type=["jpg", "jpeg", "png", "webp"],
        label_visibility="collapsed",
    )

    use_demo = False
    if is_demo():
        use_demo = st.button("🎬  Load Demo Receipt (Whole Foods · $67.43)", type="secondary")

    if not uploaded and not use_demo:
        upload_zone_hint()
        return

    # ── Analyze ───────────────────────────────────────────────
    if uploaded:
        new_key = f"receipt_{uploaded.name}_{uploaded.size}"
    else:
        new_key = "receipt_demo"

    # Reset if a new file was uploaded
    if new_key != st.session_state.get("current_receipt_key"):
        st.session_state["current_receipt_key"] = new_key

    if new_key not in st.session_state:
        wizard_steps(2)  # Analyzing
        if is_demo() or use_demo:
            with st.spinner("🔍 GPT-4o Vision analyzing receipt…"):
                time.sleep(1.5)
            st.session_state[new_key] = MOCK_RECEIPT_RESPONSE
        else:
            from vision import analyze_receipt
            with st.spinner("🔍 Sending to Gemini Vision…"):
                try:
                    result = analyze_receipt(uploaded.getvalue(), get_api_key())
                    st.session_state[new_key] = result
                except Exception as e:
                    st.error(f"Analysis failed: {e}")
                    return

    data  = st.session_state[new_key]
    items = data.get("items", [])

    if not items:
        st.warning("No items found. Try a clearer image.")
        return

    # ── Review ────────────────────────────────────────────────
    wizard_steps(3)

    col_img, col_result = st.columns([1, 2], gap="large")

    with col_img:
        if uploaded:
            st.image(uploaded, caption="Receipt", use_container_width=True)
        else:
            st.info("🎬 Demo: Whole Foods receipt data loaded")

        # Meta chips
        st.markdown(f"""
        <div style="margin-top:12px">
            <div class="badge badge-primary" style="margin-bottom:6px;display:block;width:fit-content">
                🏪 {data.get('store_name') or 'Unknown store'}
            </div>
            <div class="badge badge-gray" style="margin-bottom:6px;display:block;width:fit-content">
                📅 {data.get('purchase_date') or '—'}
            </div>
            <div class="badge badge-gray" style="display:block;width:fit-content">
                💵 ${data.get('total_amount') or '—'}
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_result:
        # Summary
        fresh_count = sum(1 for i in items if i["shelf_life_days"] > 5)
        urgent_count = sum(1 for i in items if i["shelf_life_days"] <= 2)
        st.markdown(f"""
        <div style="display:flex;gap:12px;margin-bottom:1rem">
            <div class="hero-card success" style="flex:1;min-width:0;padding:0.75rem 1rem">
                <div class="hc-value" style="font-size:1.5rem">{fresh_count}</div>
                <div class="hc-label">Fresh items</div>
            </div>
            <div class="hero-card {'danger' if urgent_count else 'primary'}" style="flex:1;min-width:0;padding:0.75rem 1rem">
                <div class="hc-value" style="font-size:1.5rem">{urgent_count}</div>
                <div class="hc-label">Use within 2 days</div>
            </div>
            <div class="hero-card primary" style="flex:1;min-width:0;padding:0.75rem 1rem">
                <div class="hc-value" style="font-size:1.5rem">{len(items)}</div>
                <div class="hc-label">Total extracted</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        section_title("REVIEW & EDIT BEFORE SAVING")
        df = pd.DataFrame(items)[["product_name", "category", "quantity", "shelf_life_days", "confidence"]]
        df.columns = ["Product", "Category", "Quantity", "Shelf Life (days)", "Confidence"]

        edited = st.data_editor(
            df, use_container_width=True, num_rows="dynamic",
            hide_index=True, key=f"edit_{new_key}",
        )

        if st.button("✅  Save to Pantry", type="primary", use_container_width=True):
            save_items = edited.rename(columns={
                "Product": "product_name", "Category": "category",
                "Quantity": "quantity", "Shelf Life (days)": "shelf_life_days",
                "Confidence": "confidence",
            }).to_dict("records")

            count = insert_items(save_items, added_by=user, store_name=data.get("store_name"))
            wizard_steps(4)
            st.toast(f"🎉 {count} items saved to pantry by {user}!", icon="✅")
            st.balloons()
            del st.session_state[new_key]
            st.session_state["current_receipt_key"] = ""


# ── Page: מזווה (Pantry Shelf) ────────────────────────────────

CATEGORY_ICONS = {
    "Produce":      "🥬", "Dairy":        "🥛", "Meat & Fish":  "🥩",
    "Bakery":       "🍞", "Frozen":       "🧊", "Pantry":       "🫙",
    "Beverages":    "🧃", "Snacks":       "🍪", "Household":    "🧹",
    "Personal Care":"🧴", "Other":        "📦",
}

def page_mazava(user: str) -> None:
    page_header("🫙 מזווה", "כל המוצרים שלך — מסודרים על המדף, מעודכנים בזמן אמת.")
    demo_banner(is_demo())

    # ── Upload receipt panel ──────────────────────────────────
    with st.expander("📸  העלה חשבונית לעדכון מוצרים חסרים", expanded=False):
        st.markdown('<div class="receipt-panel-title">סרוק חשבונית — הפריטים יתווספו למדף אוטומטית</div>', unsafe_allow_html=True)

        up_col, hint_col = st.columns([1, 1], gap="large")
        with up_col:
            receipt_file = st.file_uploader("חשבונית", type=["jpg","jpeg","png","webp"], label_visibility="collapsed", key="mazava_upload")
            use_demo_here = False
            if is_demo():
                use_demo_here = st.button("🎬 טען חשבונית דמו", key="mazava_demo")

        with hint_col:
            st.markdown("""
            <div style="padding:1rem;background:#2A1508;border-radius:10px;border:1px dashed #5C3820;color:#A07850;font-size:0.82rem;margin-top:4px">
                📄 העלה תמונה של חשבונית<br>
                <span style="color:#6B4A30;font-size:0.75rem">JPG · PNG · WEBP</span>
            </div>
            """, unsafe_allow_html=True)

        if receipt_file or use_demo_here:
            rkey = f"mazava_{'demo' if use_demo_here else receipt_file.name + str(receipt_file.size)}"
            if rkey not in st.session_state:
                with st.spinner("🔍 מנתח חשבונית..."):
                    if is_demo() or use_demo_here:
                        time.sleep(1.2)
                        st.session_state[rkey] = MOCK_RECEIPT_RESPONSE
                    else:
                        from vision import analyze_receipt
                        try:
                            st.session_state[rkey] = analyze_receipt(receipt_file.getvalue(), get_api_key())
                        except Exception as e:
                            st.error(f"שגיאה: {e}")

            if rkey in st.session_state:
                rdata = st.session_state[rkey]
                ritems = rdata.get("items", [])
                if ritems:
                    st.markdown(f"**{len(ritems)} מוצרים זוהו** מ-{rdata.get('store_name','חנות לא ידועה')} — אשר ושמור:")
                    rdf = pd.DataFrame(ritems)[["product_name","category","quantity","shelf_life_days"]]
                    rdf.columns = ["מוצר","קטגוריה","כמות","ימי תפוגה"]
                    edited_r = st.data_editor(rdf, use_container_width=True, hide_index=True, key=f"re_{rkey}")
                    if st.button("✅ הוסף למזווה", type="primary", key=f"save_{rkey}"):
                        save = edited_r.rename(columns={"מוצר":"product_name","קטגוריה":"category","כמות":"quantity","ימי תפוגה":"shelf_life_days"}).to_dict("records")
                        for s in save:
                            s.setdefault("confidence","high")
                        cnt = insert_items(save, added_by=user, store_name=rdata.get("store_name"))
                        st.toast(f"🎉 {cnt} מוצרים נוספו למזווה!", icon="✅")
                        st.balloons()
                        del st.session_state[rkey]
                        st.rerun()

    # ── Stats strip ───────────────────────────────────────────
    all_items = get_all_items()
    if not all_items:
        st.markdown("""
        <div style="text-align:center;padding:4rem 1rem">
            <div style="font-size:3rem;margin-bottom:16px">🫙</div>
            <div style="font-size:1.1rem;font-weight:700;color:#C8945A">המזווה ריק</div>
            <div style="font-size:0.85rem;color:#7A5228;margin-top:8px">העלה חשבונית מעל כדי להתחיל</div>
        </div>
        """, unsafe_allow_html=True)
        return

    stats = get_stats()
    hero_cards(stats)

    # ── Search + filter ───────────────────────────────────────
    sc1, sc2 = st.columns([3, 2])
    query    = sc1.text_input("🔍 חיפוש", placeholder="חלב, קפואים...", label_visibility="collapsed")
    cats     = ["הכל"] + get_categories()
    cat_heb  = sc2.selectbox("קטגוריה", cats, label_visibility="collapsed")
    category = "" if cat_heb == "הכל" else cat_heb

    items = search_items(query or "", category)

    # ── Shelf ─────────────────────────────────────────────────
    by_category: dict[str, list] = {}
    for item in items:
        by_category.setdefault(item["category"], []).append(item)

    st.markdown('<div class="pantry-unit">', unsafe_allow_html=True)

    for cat, cat_items in by_category.items():
        icon = CATEGORY_ICONS.get(cat, "📦")
        st.markdown(f'<div class="shelf-category-label">{icon} &nbsp;{cat}</div>', unsafe_allow_html=True)

        # Build tiles HTML
        tiles_html = '<div class="shelf-items-row">'
        for item in cat_items:
            status_cls = {
                "Fresh": "fresh", "Use Soon": "soon",
                "Running Low": "low", "Expired": "expired",
            }.get(item["status"], "fresh")
            days_label = "פג" if item["days_remaining"] == 0 else f"{item['days_remaining']}י'"
            short_name = item["product_name"][:18] + ("…" if len(item["product_name"]) > 18 else "")
            tiles_html += f"""
            <div class="product-tile status-{status_cls}" title="{item['product_name']} · {item['quantity']}">
                <div class="pt-icon">{icon}</div>
                <div class="pt-name">{short_name}</div>
                <div class="pt-qty">{item['quantity']}</div>
                <div class="pt-days {status_cls}">{days_label}</div>
            </div>"""

        tiles_html += "</div>"
        st.markdown(tiles_html, unsafe_allow_html=True)
        st.markdown('<div class="shelf-plank"></div>', unsafe_allow_html=True)

        # Action buttons per item (below each shelf row)
        btn_cols = st.columns(min(len(cat_items), 6))
        for i, item in enumerate(cat_items[:6]):
            with btn_cols[i]:
                if st.button("🗑", key=f"sh_del_{item['id']}", help=f"הסר {item['product_name']}", use_container_width=True):
                    delete_item(item["id"], reason="used")
                    st.toast(f"'{item['product_name']}' הוסר", icon="🗑")
                    st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    # ── Manual add ────────────────────────────────────────────
    with st.expander("➕ הוסף מוצר ידנית"):
        CATS = ["Produce","Dairy","Meat & Fish","Bakery","Frozen","Pantry","Beverages","Snacks","Household","Personal Care","Other"]
        with st.form("manual_add_maz"):
            mc1, mc2, mc3, mc4 = st.columns([3, 2, 2, 2])
            name  = mc1.text_input("שם מוצר")
            cat   = mc2.selectbox("קטגוריה", CATS)
            qty   = mc3.text_input("כמות", value="1")
            shelf = mc4.number_input("ימי תפוגה", min_value=1, value=7)
            if st.form_submit_button("הוסף", type="primary"):
                if name.strip():
                    insert_items([{"product_name": name, "category": cat, "quantity": qty,
                                   "shelf_life_days": shelf, "confidence": "high"}],
                                 added_by=user, store_name=None)
                    st.toast(f"'{name}' נוסף!", icon="✓")
                    st.rerun()


# ── Page: Meal Planner ────────────────────────────────────────
def page_meal_planner() -> None:
    page_header("🍳 Chaos Meal Planner", "Zero-waste cooking. AI turns expiring ingredients into tonight's dinner.")
    demo_banner(is_demo())

    expiring = get_expiring_items(within_days=5)

    if not expiring:
        st.markdown("""
        <div style="text-align:center;padding:3rem 1rem">
            <div style="font-size:2.5rem;margin-bottom:12px">🎉</div>
            <div style="font-size:1rem;font-weight:600;color:#0F172A">Nothing expiring soon!</div>
            <div style="font-size:0.85rem;color:#64748B;margin-top:6px">Your pantry is in great shape.</div>
        </div>
        """, unsafe_allow_html=True)
        return

    section_title(f"{len(expiring)} INGREDIENTS ABOUT TO EXPIRE")
    pills = "".join(
        f'<span class="badge {"badge-low" if i["days_remaining"]<=2 else "badge-soon"}" style="margin:3px">'
        f'{i["product_name"]} · {i["days_remaining"]}d</span>'
        for i in expiring
    )
    st.markdown(f'<div style="margin-bottom:1.5rem">{pills}</div>', unsafe_allow_html=True)

    col_btn, col_fav = st.columns([2, 1])
    generate = col_btn.button("✨  Generate Meal Ideas", type="primary", use_container_width=True)

    if generate:
        with st.spinner("Chef AI is thinking…"):
            if is_demo():
                time.sleep(1.5)
                st.session_state["recipes"] = MOCK_RECIPES
            else:
                from planner import suggest_meals
                try:
                    st.session_state["recipes"] = suggest_meals(expiring, get_api_key())
                except Exception as e:
                    st.error(f"Meal planner error: {e}")
                    return
        st.toast("2 recipes ready!", icon="🍳")

    recipes = st.session_state.get("recipes", [])
    if not recipes:
        return

    st.markdown("---")
    for i, r in enumerate(recipes, 1):
        recipe_card(r, i)
        # Save to favourites (session only in demo)
        if st.button(f"⭐ Save Recipe {i}", key=f"fav_{i}", type="secondary"):
            favs = st.session_state.get("favourites", [])
            if r not in favs:
                favs.append(r)
                st.session_state["favourites"] = favs
            st.toast(f"'{r['name']}' saved to favourites!", icon="⭐")

    # Favourites
    favs = st.session_state.get("favourites", [])
    if favs:
        with st.expander(f"⭐ Saved Favourites ({len(favs)})"):
            for i, r in enumerate(favs, 1):
                recipe_card(r, i)


# ── Page: Running Low ─────────────────────────────────────────
def page_running_low() -> None:
    page_header("⚠️ Running Low", "Items expiring within 2 days. Act now to avoid waste.")
    demo_banner(is_demo())

    urgent = get_expiring_items(within_days=2)

    if not urgent:
        st.markdown("""
        <div style="text-align:center;padding:3rem 1rem">
            <div style="font-size:2.5rem;margin-bottom:12px">✅</div>
            <div style="font-size:1rem;font-weight:600;color:#0F172A">All clear!</div>
            <div style="font-size:0.85rem;color:#64748B;margin-top:6px">Nothing critical right now.</div>
        </div>
        """, unsafe_allow_html=True)
        return

    st.markdown(f'<div style="margin-bottom:1rem">{len(urgent)} item(s) need attention today</div>', unsafe_allow_html=True)

    for item in urgent:
        st.markdown(alert_card_html(item), unsafe_allow_html=True)
        col_used, col_shop = st.columns([1, 1])

        with col_used:
            if st.button("✓ Mark Used", key=f"used_{item['id']}", use_container_width=True, type="primary"):
                delete_item(item["id"], reason="used")
                st.toast(f"'{item['product_name']}' marked as used.", icon="✓")
                st.rerun()

        with col_shop:
            if st.button("🛒 Add to Shopping List", key=f"shop_low_{item['id']}", use_container_width=True):
                add_to_shopping_list(item["product_name"], item["category"], item["quantity"])
                st.toast(f"Added to shopping list!", icon="🛒")

        st.markdown("<div style='margin-bottom:4px'></div>", unsafe_allow_html=True)


# ── Page: AI Predictions ──────────────────────────────────────
def page_ai_predictions() -> None:
    page_header(
        "🧠 AI Inventory Manager",
        "Learns your shopping patterns. Predicts what you'll need before you run out.",
    )
    demo_banner(is_demo())

    # How it works explainer
    with st.expander("How does this work?", expanded=False):
        st.markdown("""
        **HomeBrain AI tracks your purchase history every time you scan a receipt.**

        It learns:
        - How often you buy each product (e.g. milk every 10 days)
        - Your last purchase date for each item

        When the gap since your last purchase approaches your average re-buy interval,
        it surfaces the item as a **prediction** — before you even notice it's missing.

        > The more receipts you scan, the smarter the predictions get.
        """)

    predictions = get_smart_predictions()

    if not predictions:
        st.markdown("""
        <div style="text-align:center;padding:3rem 1rem">
            <div style="font-size:2.5rem;margin-bottom:12px">📊</div>
            <div style="font-size:1rem;font-weight:600">Not enough data yet</div>
            <div style="font-size:0.85rem;color:#64748B;margin-top:6px">
                Scan at least 2 receipts for the same items to start seeing predictions.
            </div>
        </div>
        """, unsafe_allow_html=True)
        return

    high  = [p for p in predictions if p["urgency"] == "High"]
    medium = [p for p in predictions if p["urgency"] == "Medium"]

    if high:
        section_title(f"🔴 HIGH PRIORITY — {len(high)} ITEMS LIKELY NEEDED NOW")
        for pred in high:
            st.markdown(prediction_card_html(pred), unsafe_allow_html=True)
            if st.button(f"🛒 Add '{pred['product_name']}' to Shopping List",
                         key=f"pred_shop_{pred['product_name']}"):
                add_to_shopping_list(pred["product_name"], pred["category"])
                st.toast(f"'{pred['product_name']}' added to shopping list!", icon="🛒")

    if medium:
        st.markdown("<br>", unsafe_allow_html=True)
        section_title(f"🟡 MEDIUM PRIORITY — {len(medium)} ITEMS TO WATCH")
        for pred in medium:
            st.markdown(prediction_card_html(pred), unsafe_allow_html=True)
            if st.button(f"🛒 Add to List",
                         key=f"pred_med_{pred['product_name']}"):
                add_to_shopping_list(pred["product_name"], pred["category"])
                st.toast(f"Added!", icon="🛒")

    # Pattern summary table
    st.markdown("---")
    section_title("YOUR SHOPPING PATTERNS")
    rows = []
    for p in predictions:
        rows.append({
            "Product":              p["product_name"],
            "Category":             p["category"],
            "Avg. Buy Interval":    f"Every {p['avg_gap_days']} days",
            "Days Since Last Buy":  p["days_since_last"],
            "Priority":             p["urgency"],
        })
    if rows:
        df = pd.DataFrame(rows)
        def colour_priority(val):
            return "background:#FEE2E2;color:#991B1B" if val == "High" else "background:#FEF3C7;color:#92400E"
        st.dataframe(df.style.applymap(colour_priority, subset=["Priority"]),
                     use_container_width=True, hide_index=True)


# ── Main router ───────────────────────────────────────────────
def main():
    page, user = render_sidebar()

    if page == "Scan Receipt":
        page_scan_receipt(user)
    elif page == "מזווה":
        page_mazava(user)
    elif page == "Shopping List":
        shopping_list_page.render(is_demo())
    elif page == "Meal Planner":
        page_meal_planner()
    elif page == "Running Low":
        page_running_low()
    elif page == "AI Predictions":
        page_ai_predictions()


if __name__ == "__main__":
    main()
