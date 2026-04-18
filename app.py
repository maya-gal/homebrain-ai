import os
import time
import streamlit as st
import pandas as pd
from dotenv import load_dotenv
from demo_data import MOCK_RECEIPT_RESPONSE, MOCK_RECIPES, MOCK_VOICE_TEXT_ITEMS
import shopping_list as shopping_list_page

from styles import get_css
from database import (
    init_db, insert_items, get_all_items, search_items,
    get_expiring_items, get_categories, get_stats, delete_item,
    add_to_shopping_list, get_smart_predictions, get_inventory_predictions,
    get_staple_list, add_staple, remove_staple, get_missing_staples,
)
from product_images import get_product_image
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

PAGES = [
    ("🫙", "Pantry"),
    ("🛒", "Shopping List"),
    ("🍳", "Meal Planner"),
    ("⚠️", "Running Low"),
]


# ── OpenAI API key ────────────────────────────────────────────
@st.cache_resource
def get_api_key() -> str:
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        try:
            key = st.secrets.get("OPENAI_API_KEY", "")
        except Exception:
            key = ""
    return key or ""


def is_demo() -> bool:
    return not get_api_key()


# ── Sidebar ───────────────────────────────────────────────────
def render_sidebar() -> tuple[str, str]:
    with st.sidebar:
        st.markdown('<div class="sidebar-brand">🏠 HomeBrain AI</div>', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-tagline">Your household, managed.</div>', unsafe_allow_html=True)
        st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)

        if "page" not in st.session_state:
            st.session_state.page = "Pantry"

        for icon, label in PAGES:
            active = st.session_state.page == label
            if st.button(f"{icon}  {label}", key=f"nav_{label}",
                         use_container_width=True,
                         type="primary" if active else "secondary"):
                st.session_state.page = label
                st.rerun()

        st.markdown("---")

        stats = get_stats()
        st.markdown('<div style="font-size:0.7rem;font-weight:700;letter-spacing:1px;color:#475569;text-transform:uppercase;margin-bottom:8px">Pantry Stats</div>', unsafe_allow_html=True)

        warn_color = "danger" if stats["expiring_soon"] > 0 else ""
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
            with st.spinner("🔍 GPT-4o Vision analyzing receipt…"):
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


# ── Page: Pantry (Shelf View) ────────────────────────────────

CATEGORY_ICONS = {
    "Produce":      "🥬", "Dairy":        "🥛", "Meat & Fish":  "🥩",
    "Bakery":       "🍞", "Frozen":       "🧊", "Pantry":       "🫙",
    "Beverages":    "🧃", "Snacks":       "🍪", "Household":    "🧹",
    "Personal Care":"🧴", "Other":        "📦",
}

def _render_items_preview(items: list[dict], cache_key: str, user: str, store: str = None) -> None:
    """Shared preview table + save button for all 3 input modes."""
    if not items:
        st.warning("No items detected — please try again.")
        return
    st.markdown(f"**{len(items)} items detected** — review and save:")
    cols_map = {"product_name": "Product", "category": "Category", "quantity": "Quantity", "shelf_life_days": "Shelf Life (days)"}
    df = pd.DataFrame(items)[[c for c in cols_map if c in pd.DataFrame(items).columns]]
    df = df.rename(columns=cols_map)
    edited = st.data_editor(df, use_container_width=True, hide_index=True, key=f"preview_{cache_key}")
    if st.button("✅ Add to Pantry", type="primary", key=f"save_preview_{cache_key}"):
        rev = {v: k for k, v in cols_map.items()}
        save = edited.rename(columns=rev).to_dict("records")
        for s in save:
            s.setdefault("confidence", "high")
        cnt = insert_items(save, added_by=user, store_name=store)
        st.toast(f"🎉 {cnt} items added to Pantry!", icon="✅")
        st.balloons()
        for k in [cache_key, "mazava_text_items", "mazava_audio_items"]:
            st.session_state.pop(k, None)
        st.rerun()


def page_mazava(user: str) -> None:
    page_header("🫙 Pantry", "All your products — organised on the shelf, updated in real time.")
    demo_banner(is_demo())

    # ── Add products panel — 3 modes ─────────────────────────
    _has_items = bool(get_all_items())
    with st.expander("📸  Scan Receipt / Add Products", expanded=not _has_items):
        tab_receipt, tab_text, tab_voice = st.tabs(["📸 Receipt", "✍️ Free Text", "🎤 Voice Recording"])

        # ── TAB 1: Receipt image ──────────────────────────────
        with tab_receipt:
            receipt_file = st.file_uploader("Receipt", type=["jpg","jpeg","png","webp"],
                                             label_visibility="collapsed", key="mazava_upload")
            if is_demo():
                if st.button("🎬 Load Demo Receipt", key="mazava_demo"):
                    st.session_state["mazava_receipt_key"] = "receipt_demo"
                    st.session_state["receipt_demo"] = MOCK_RECEIPT_RESPONSE

            rkey = None
            if receipt_file:
                rkey = f"mazava_img_{receipt_file.name}_{receipt_file.size}"
                if rkey not in st.session_state:
                    with st.spinner("🔍 GPT-4o Vision analysing receipt..."):
                        if is_demo():
                            time.sleep(1); st.session_state[rkey] = MOCK_RECEIPT_RESPONSE
                        else:
                            from vision import analyze_receipt
                            try: st.session_state[rkey] = analyze_receipt(receipt_file.getvalue(), get_api_key())
                            except Exception as e: st.error(f"Error: {e}")
            elif "receipt_demo" in st.session_state:
                rkey = "receipt_demo"

            if rkey and rkey in st.session_state:
                _render_items_preview(st.session_state[rkey].get("items",[]), rkey, user,
                                      store=st.session_state[rkey].get("store_name"))

        # ── TAB 2: Free text ──────────────────────────────────
        with tab_text:
            st.markdown('<div style="font-size:0.82rem;color:#A07850;margin-bottom:8px">Write freely — in Hebrew or English, with quantities or without</div>', unsafe_allow_html=True)
            example = "e.g. milk 2 liters, bread, 6 eggs, tomatoes, olive oil"
            text_input = st.text_area("Product list", placeholder=example,
                                       height=100, label_visibility="collapsed", key="mazava_text")
            c1, c2 = st.columns([2,1])
            parse_text = c1.button("🔍 Parse Text", type="primary", key="parse_text_btn", use_container_width=True)
            if is_demo():
                c2.button("🎬 Demo", key="text_demo_btn", on_click=lambda: st.session_state.update({"mazava_text_items": MOCK_VOICE_TEXT_ITEMS}))

            if parse_text and text_input.strip():
                with st.spinner("Parsing..."):
                    if is_demo():
                        time.sleep(0.8); st.session_state["mazava_text_items"] = MOCK_VOICE_TEXT_ITEMS
                    else:
                        from vision import parse_text_to_items
                        try: st.session_state["mazava_text_items"] = parse_text_to_items(text_input, get_api_key())
                        except Exception as e: st.error(f"Error: {e}")

            if st.session_state.get("mazava_text_items"):
                _render_items_preview(st.session_state["mazava_text_items"], "text_items", user)

        # ── TAB 3: Voice ──────────────────────────────────────
        with tab_voice:
            st.markdown('<div style="font-size:0.82rem;color:#A07850;margin-bottom:12px">Click the microphone, say your products aloud, click again to stop</div>', unsafe_allow_html=True)

            try:
                from audio_recorder_streamlit import audio_recorder
                audio_bytes = audio_recorder(
                    text="", icon_size="2x",
                    recording_color="#C8945A", neutral_color="#5C3820",
                    key="mazava_audio",
                )
            except Exception:
                audio_bytes = None
                st.info("Recording component unavailable — try refreshing the page.")

            if is_demo():
                if st.button("🎬 Demo Recording", key="audio_demo_btn"):
                    st.session_state["mazava_audio_items"] = MOCK_VOICE_TEXT_ITEMS

            if audio_bytes and len(audio_bytes) > 1000:
                with st.spinner("🎤 Processing recording..."):
                    if is_demo():
                        time.sleep(1); st.session_state["mazava_audio_items"] = MOCK_VOICE_TEXT_ITEMS
                    else:
                        from vision import parse_audio_to_items
                        try: st.session_state["mazava_audio_items"] = parse_audio_to_items(audio_bytes, get_api_key())
                        except Exception as e: st.error(f"Recording error: {e}")

            if st.session_state.get("mazava_audio_items"):
                _render_items_preview(st.session_state["mazava_audio_items"], "audio_items", user)

    # ── Stats strip ───────────────────────────────────────────
    all_items = get_all_items()
    if not all_items:
        st.markdown("""
        <div style="text-align:center;padding:4rem 1rem">
            <div style="font-size:3rem;margin-bottom:16px">🫙</div>
            <div style="font-size:1.1rem;font-weight:700;color:#C8945A">Your pantry is empty</div>
            <div style="font-size:0.85rem;color:#7A5228;margin-top:8px">Upload a receipt above to get started</div>
        </div>
        """, unsafe_allow_html=True)
        return

    stats = get_stats()
    missing_staples = get_missing_staples()
    hero_cards(stats, missing=len(missing_staples))

    # ── Staple List ───────────────────────────────────────────
    with st.expander(f"✅  Must Have  {'🔴 ' + str(len(missing_staples)) + ' missing' if missing_staples else '✅ all stocked'}", expanded=bool(missing_staples)):
        if missing_staples:
            section_title(f"MISSING FROM PANTRY — {len(missing_staples)} ITEMS")
            for s in missing_staples:
                c1, c2, c3 = st.columns([4, 1.5, 1.5])
                img_url = get_product_image(s["product_name"], s["category"])
                img_tag = f'<img src="{img_url}" style="width:32px;height:32px;border-radius:8px;object-fit:cover;vertical-align:middle;margin-right:8px" onerror="this.style.display=\'none\'">' if img_url else ""
                c1.markdown(f'{img_tag}<span style="font-weight:700">{s["product_name"]}</span> <span style="color:#6B7280;font-size:0.8rem">{s["category"]}</span>', unsafe_allow_html=True)
                if c2.button("🛒 Add to list", key=f"staple_shop_{s['id']}", use_container_width=True):
                    add_to_shopping_list(s["product_name"], s["category"])
                    st.toast(f"'{s['product_name']}' added to shopping list!", icon="🛒")
                if c3.button("Remove", key=f"staple_rm_{s['id']}", use_container_width=True):
                    remove_staple(s["id"])
                    st.rerun()
            st.markdown("---")

        all_staples = get_staple_list()
        in_stock = [s for s in all_staples if s["product_name"].lower() not in {x["product_name"].lower() for x in missing_staples}]
        if in_stock:
            section_title(f"IN STOCK — {len(in_stock)} MUST HAVE ITEMS")
            cols = st.columns(4)
            for i, s in enumerate(in_stock):
                with cols[i % 4]:
                    img_url = get_product_image(s["product_name"], s["category"])
                    img_tag = f'<img src="{img_url}" style="width:28px;height:28px;border-radius:6px;object-fit:cover;vertical-align:middle;margin-right:6px" onerror="this.style.display=\'none\'">' if img_url else ""
                    st.markdown(f'<div style="font-size:0.8rem;font-weight:600;margin-bottom:4px">{img_tag}{s["product_name"]}</div>', unsafe_allow_html=True)
                    if st.button("✕", key=f"staple_del_{s['id']}", use_container_width=True):
                        remove_staple(s["id"])
                        st.rerun()

        with st.form("add_staple_form", clear_on_submit=True):
            section_title("ADD TO MUST HAVE")
            sc1, sc2, sc3 = st.columns([3, 2, 1])
            s_name = sc1.text_input("Product", placeholder="e.g. Milk, Eggs, Bread…", label_visibility="collapsed")
            s_cat  = sc2.selectbox("Category", ["Produce","Dairy","Meat & Fish","Bakery","Frozen","Pantry","Beverages","Snacks","Household","Personal Care","Other"], label_visibility="collapsed")
            if sc3.form_submit_button("➕ Add", use_container_width=True, type="primary") and s_name.strip():
                added = add_staple(s_name.strip(), s_cat)
                st.toast(f"'{s_name}' added to Must Have!" if added else f"'{s_name}' is already in Must Have.", icon="✅")
                st.rerun()

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

    # Separate in-stock vs zero-quantity items
    def _is_zero_qty(qty: str) -> bool:
        try:
            return float(qty.split()[0]) == 0
        except (ValueError, IndexError):
            return qty.strip() == "0"

    in_stock_items  = [it for it in items if not _is_zero_qty(it["quantity"])]
    out_of_stock    = [it for it in items if _is_zero_qty(it["quantity"])]

    # Fetch AI predictions for inline display
    predictions = get_inventory_predictions()

    section_title(f"FOOD — {len(in_stock_items)} ITEMS")
    cols = st.columns(3)
    for i, item in enumerate(in_stock_items):
        with cols[i % 3]:
            pred = predictions.get(item["product_name"].lower(), "")
            st.markdown(item_card_html(item, prediction=pred), unsafe_allow_html=True)
            if st.button("Remove", key=f"del_{item['id']}", use_container_width=True):
                delete_item(item["id"])
                st.rerun()

    # ── Out of Stock ──────────────────────────────────────────
    if out_of_stock:
        st.markdown("<br>", unsafe_allow_html=True)
        section_title(f"OUT OF STOCK — {len(out_of_stock)} ITEMS")
        st.markdown("""
        <div style="font-size:0.8rem;color:#6B7280;margin-bottom:12px">
            Items with quantity set to 0 — add them to your shopping list.
        </div>
        """, unsafe_allow_html=True)
        oos_cols = st.columns(3)
        for i, item in enumerate(out_of_stock):
            with oos_cols[i % 3]:
                img_url = get_product_image(item["product_name"], item["category"])
                img_tag = (
                    f'<img src="{img_url}" style="width:36px;height:36px;border-radius:8px;'
                    f'object-fit:cover;vertical-align:middle;margin-right:8px;opacity:0.5" '
                    f'onerror="this.style.display=\'none\'">'
                    if img_url else ""
                )
                st.markdown(f"""
                <div style="background:#F9FAFB;border:1.5px dashed #D1D5DB;border-radius:12px;
                            padding:12px 14px;margin-bottom:10px;opacity:0.85">
                    <div style="display:flex;align-items:center;margin-bottom:6px">
                        {img_tag}
                        <div>
                            <div style="font-weight:700;font-size:0.9rem;color:#374151">{item['product_name']}</div>
                            <div style="font-size:0.75rem;color:#9CA3AF">{item['category']}</div>
                        </div>
                    </div>
                    <span class="badge badge-gray">Out of Stock</span>
                </div>
                """, unsafe_allow_html=True)
                c1, c2 = st.columns(2)
                if c1.button("🛒 Add to List", key=f"oos_shop_{item['id']}", use_container_width=True):
                    add_to_shopping_list(item["product_name"], item["category"])
                    st.toast(f"'{item['product_name']}' added to shopping list!", icon="🛒")
                if c2.button("Remove", key=f"oos_del_{item['id']}", use_container_width=True):
                    delete_item(item["id"])
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
        if st.button(f"⭐ Save Recipe {i}", key=f"fav_{i}", type="secondary"):
            favs = st.session_state.get("favourites", [])
            if r not in favs:
                favs.append(r)
                st.session_state["favourites"] = favs
            st.toast(f"'{r['name']}' saved to favourites!", icon="⭐")

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
                st.toast(f"'{item['product_name']}' marked as used.", icon="✅")
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

    high   = [p for p in predictions if p["urgency"] == "High"]
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
            if st.button(f"🛒 Add to List", key=f"pred_med_{pred['product_name']}"):
                add_to_shopping_list(pred["product_name"], pred["category"])
                st.toast(f"Added!", icon="🛒")

    st.markdown("---")
    section_title("YOUR SHOPPING PATTERNS")
    rows = [
        {
            "Product":             p["product_name"],
            "Category":            p["category"],
            "Avg. Buy Interval":   f"Every {p['avg_gap_days']} days",
            "Days Since Last Buy": p["days_since_last"],
            "Priority":            p["urgency"],
        }
        for p in predictions
    ]
    if rows:
        df = pd.DataFrame(rows)
        def colour_priority(val):
            return "background:#FEE2E2;color:#991B1B" if val == "High" else "background:#FEF3C7;color:#92400E"
        st.dataframe(df.style.map(colour_priority, subset=["Priority"]),
                     use_container_width=True, hide_index=True)


# ── Main Router ───────────────────────────────────────────────
def main() -> None:
    page, user = render_sidebar()

    if page == "Pantry":
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
