import os
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

load_dotenv()
init_db()

st.set_page_config(
    page_title="HomeBrain AI",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(get_css(), unsafe_allow_html=True)

API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY") or os.getenv("OPENAI_API_KEY")
IS_DEMO = not bool(API_KEY)

PAGES = ["Dashboard", "Scan Receipt", "Meal Planner", "Running Low", "Shopping List"]
PAGE_ICONS = {
    "Dashboard":     "🏠",
    "Scan Receipt":  "📄",
    "Meal Planner":  "🍽",
    "Running Low":   "⚠️",
    "Shopping List": "🛒",
}


# ── Sidebar ───────────────────────────────────────────────────
def render_sidebar() -> tuple[str, str]:
    with st.sidebar:
        st.markdown('<div class="sidebar-brand">🏠 HomeBrain AI</div>', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-tagline">Your household, managed.</div>', unsafe_allow_html=True)
        st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)

        if "page" not in st.session_state:
            st.session_state.page = "Dashboard"

        for page in PAGES:
            icon = PAGE_ICONS[page]
            if st.button(f"{icon}  {page}", key=f"nav_{page}", use_container_width=True):
                st.session_state.page = page
                st.rerun()

        st.markdown("---")

        stats = get_stats()
        st.markdown(f"""
        <div class="stat-pill">
            <span class="label">Total Items</span>
            <span class="value">{stats.get("total", 0)}</span>
        </div>
        <div class="stat-pill">
            <span class="label">Running Low</span>
            <span class="value warn">{stats.get("expiring_soon", 0)}</span>
        </div>
        <div class="stat-pill">
            <span class="label">Expired</span>
            <span class="value danger">{stats.get("expired", 0)}</span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        user = st.selectbox("👤 Adding as", ["You", "Mom", "Dad", "Kids"])

    return st.session_state.page, user


# ── Dashboard Page ────────────────────────────────────────────
def render_dashboard(user: str) -> None:
    page_header("🏠 Family Dashboard", "Your household at a glance.")
    demo_banner(IS_DEMO)

    stats = get_stats()
    hero_cards(stats)

    col_search, col_cat = st.columns([3, 1])
    with col_search:
        query = st.text_input("🔍 Search items", placeholder="e.g. milk, chicken...")
    with col_cat:
        cats = ["All"] + get_categories()
        cat_filter = st.selectbox("Category", cats, label_visibility="collapsed")

    if query:
        items = search_items(query, cat_filter if cat_filter != "All" else "")
    elif cat_filter and cat_filter != "All":
        items = search_items("", cat_filter)
    else:
        items = get_all_items()

    if not items:
        st.info("No items in your food yet. Scan a receipt to get started!")
        return

    section_title(f"FOOD — {len(items)} ITEMS")
    cols = st.columns(3)
    for i, item in enumerate(items):
        with cols[i % 3]:
            st.markdown(item_card_html(item), unsafe_allow_html=True)
            if st.button("Remove", key=f"del_{item['id']}", use_container_width=True):
                delete_item(item["id"])
                st.rerun()


# ── Scan Receipt Page ─────────────────────────────────────────
def render_scan_receipt(user: str) -> None:
    page_header("📄 Scan Receipt", "Upload a grocery receipt to update your food automatically.")
    demo_banner(IS_DEMO)

    if "scan_step" not in st.session_state:
        st.session_state.scan_step = 1
    if "scan_items" not in st.session_state:
        st.session_state.scan_items = []
    if "scan_store" not in st.session_state:
        st.session_state.scan_store = ""

    wizard_steps(st.session_state.scan_step)

    # Step 1: Upload
    if st.session_state.scan_step == 1:
        upload_zone_hint()
        tab_img, tab_text = st.tabs(["📷 Receipt Image", "✏️ Type / Paste"])

        with tab_img:
            uploaded = st.file_uploader(
                "Upload receipt image", type=["jpg", "jpeg", "png", "webp"],
                label_visibility="collapsed",
            )
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🎬 Load Demo Receipt", use_container_width=True):
                    from demo_data import MOCK_RECEIPT_RESPONSE
                    st.session_state.scan_items = MOCK_RECEIPT_RESPONSE["items"]
                    st.session_state.scan_store = MOCK_RECEIPT_RESPONSE.get("store_name", "")
                    st.session_state.scan_step = 3
                    st.rerun()
            with col2:
                if uploaded and st.button("🔍 Analyze Receipt", type="primary", use_container_width=True):
                    if IS_DEMO:
                        st.warning("No API key found. Click 'Load Demo Receipt' instead.")
                    else:
                        with st.spinner("Analyzing your receipt with AI..."):
                            from vision import analyze_receipt
                            result = analyze_receipt(uploaded.read(), API_KEY)
                            st.session_state.scan_items = result.get("items", [])
                            st.session_state.scan_store = result.get("store_name", "")
                            st.session_state.scan_step = 3
                            st.rerun()

        with tab_text:
            text_input = st.text_area(
                "Type your grocery list",
                placeholder="e.g. milk x2, bread, 6 eggs, tomatoes 1kg",
                height=120,
            )
            if st.button("Parse List", type="primary", use_container_width=True) and text_input.strip():
                if IS_DEMO:
                    from demo_data import MOCK_VOICE_TEXT_ITEMS
                    st.session_state.scan_items = MOCK_VOICE_TEXT_ITEMS
                    st.session_state.scan_store = ""
                    st.session_state.scan_step = 3
                    st.rerun()
                else:
                    with st.spinner("Parsing your list..."):
                        from vision import parse_text_to_items
                        st.session_state.scan_items = parse_text_to_items(text_input, API_KEY)
                        st.session_state.scan_store = ""
                        st.session_state.scan_step = 3
                        st.rerun()

    # Step 3: Review & save
    elif st.session_state.scan_step == 3:
        import pandas as pd
        items = st.session_state.scan_items
        if st.session_state.scan_store:
            st.info(f"🏪 Store: {st.session_state.scan_store}")

        section_title(f"REVIEW — {len(items)} ITEMS DETECTED")
        df = pd.DataFrame(items)
        edited = st.data_editor(df, use_container_width=True, num_rows="dynamic", key="scan_editor")

        col_save, col_cancel = st.columns(2)
        with col_save:
            if st.button("✅ Save to food", type="primary", use_container_width=True):
                records = edited.to_dict("records")
                n = insert_items(records, user, st.session_state.scan_store)
                st.session_state.scan_step = 4
                st.session_state.saved_count = n
                st.rerun()
        with col_cancel:
            if st.button("← Start Over", use_container_width=True):
                st.session_state.scan_step = 1
                st.session_state.scan_items = []
                st.rerun()

    # Step 4: Done
    elif st.session_state.scan_step == 4:
        n = st.session_state.get("saved_count", 0)
        st.success(f"✅ {n} items saved to your food!")
        if st.button("Scan Another Receipt", type="primary"):
            st.session_state.scan_step = 1
            st.session_state.scan_items = []
            st.rerun()


# ── Meal Planner Page ─────────────────────────────────────────
def render_meal_planner() -> None:
    page_header("🍽 Chaos Meal Planner", "Recipes built from items about to expire.")
    demo_banner(IS_DEMO)

    expiring = get_expiring_items(within_days=5)

    if not expiring:
        st.info("No items expiring soon — your food is in great shape! Come back when things are getting low.")
        return

    section_title(f"USING {len(expiring)} EXPIRING ITEMS")
    badges = " ".join(f'<span class="badge badge-soon">{i["product_name"]}</span>' for i in expiring)
    st.markdown(f'<div style="margin-bottom:1rem">{badges}</div>', unsafe_allow_html=True)

    if "recipes" not in st.session_state:
        st.session_state.recipes = []

    if st.button("✨ Generate Meal Ideas", type="primary"):
        if IS_DEMO:
            from demo_data import MOCK_RECIPES
            st.session_state.recipes = MOCK_RECIPES
        else:
            with st.spinner("Thinking up delicious recipes..."):
                from planner import suggest_meals
                st.session_state.recipes = suggest_meals(expiring, API_KEY)
        st.rerun()

    for i, r in enumerate(st.session_state.recipes, 1):
        recipe_card(r, i)


# ── Running Low Page ──────────────────────────────────────────
def render_running_low() -> None:
    page_header("⚠️ Running Low", "Items expiring soon and smart restocking predictions.")
    demo_banner(IS_DEMO)

    expiring    = get_expiring_items(within_days=3)
    expired     = [i for i in get_all_items() if i["status"] == "Expired"]
    predictions = get_smart_predictions()

    col1, col2 = st.columns(2)

    with col1:
        section_title(f"EXPIRING SOON — {len(expiring)} ITEMS")
        if expiring:
            for item in expiring:
                st.markdown(alert_card_html(item), unsafe_allow_html=True)
                if st.button("Add to Shopping List", key=f"shop_{item['id']}", use_container_width=True):
                    add_to_shopping_list(item["product_name"], item["category"], item["quantity"])
                    st.toast(f"'{item['product_name']}' added to shopping list!", icon="🛒")
        else:
            st.success("Nothing expiring in the next 3 days!")

        if expired:
            st.markdown("<br>", unsafe_allow_html=True)
            section_title(f"EXPIRED — {len(expired)} ITEMS")
            for item in expired:
                st.markdown(alert_card_html(item), unsafe_allow_html=True)
                if st.button("Remove", key=f"exp_del_{item['id']}", use_container_width=True):
                    delete_item(item["id"], reason="expired")
                    st.rerun()

    with col2:
        section_title(f"SMART PREDICTIONS — {len(predictions)} ITEMS")
        if predictions:
            for pred in predictions:
                st.markdown(prediction_card_html(pred), unsafe_allow_html=True)
                if st.button("Add to List", key=f"pred_{pred['product_name']}", use_container_width=True):
                    add_to_shopping_list(pred["product_name"], pred["category"])
                    st.toast(f"'{pred['product_name']}' added to shopping list!", icon="🛒")
        else:
            st.info("Not enough purchase history for predictions yet. Scan more receipts to train your AI!")


# ── Main Router ───────────────────────────────────────────────
def main() -> None:
    page, user = render_sidebar()

    if page == "Dashboard":
        render_dashboard(user)
    elif page == "Scan Receipt":
        render_scan_receipt(user)
    elif page == "Meal Planner":
        render_meal_planner()
    elif page == "Running Low":
        render_running_low()
    elif page == "Shopping List":
        import shopping_list
        shopping_list.render(IS_DEMO)


if __name__ == "__main__":
    main()
