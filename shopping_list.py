"""
shopping_list.py — Shopping List page renderer.
"""

import streamlit as st
from database import (
    get_shopping_list, add_to_shopping_list,
    mark_bought, unmark_bought, clear_bought, auto_populate_shopping_list,
)
from components import page_header, demo_banner, section_title, category_badge

CATEGORIES = [
    "Produce", "Dairy", "Meat & Fish", "Bakery", "Frozen",
    "מזווה", "Beverages", "Snacks", "Household", "Personal Care", "Other",
]


def render(is_demo_mode: bool) -> None:
    page_header("🛒 Shopping List", "Auto-populated from your expiring items. Add more manually.")
    demo_banner(is_demo_mode)

    # ── Auto-populate button ──────────────────────────────────
    col_auto, col_clear = st.columns([2, 1])
    with col_auto:
        if st.button("🔄  Pull from Running Low", use_container_width=True):
            added = auto_populate_shopping_list()
            if added:
                st.toast(f"Added {added} item(s) from your expiring inventory!", icon="🛒")
                st.rerun()
            else:
                st.info("Nothing new to add — list is up to date.")

    with col_clear:
        if st.button("✅  Clear Bought", use_container_width=True, type="secondary"):
            clear_bought()
            st.toast("Cleared bought items!", icon="✅")
            st.rerun()

    st.markdown("---")

    # ── Manual add form ───────────────────────────────────────
    with st.expander("➕  Add item manually"):
        with st.form("manual_add_form", clear_on_submit=True):
            c1, c2, c3 = st.columns([3, 2, 2])
            item_name = c1.text_input("Item name", placeholder="e.g. Almond Milk")
            category  = c2.selectbox("Category", CATEGORIES)
            quantity  = c3.text_input("Quantity", value="1", placeholder="e.g. 2 packs")
            submitted = st.form_submit_button("Add to List", type="primary", use_container_width=True)
            if submitted and item_name.strip():
                add_to_shopping_list(item_name.strip(), category, quantity.strip() or "1")
                st.toast(f"'{item_name}' added to shopping list!", icon="✅")
                st.rerun()

    # ── List ──────────────────────────────────────────────────
    items = get_shopping_list()
    if not items:
        st.markdown("""
        <div style="text-align:center;padding:3rem 1rem;color:#94A3B8">
            <div style="font-size:2.5rem;margin-bottom:12px">🛒</div>
            <div style="font-size:1rem;font-weight:600">Your shopping list is empty</div>
            <div style="font-size:0.85rem;margin-top:6px">
                Pull from Running Low items above, or add items manually.
            </div>
        </div>
        """, unsafe_allow_html=True)
        return

    pending = [i for i in items if not i["is_bought"]]
    bought  = [i for i in items if i["is_bought"]]

    # Pending items
    if pending:
        section_title(f"TO BUY — {len(pending)} ITEMS")
        for item in pending:
            _render_item_row(item, is_bought=False)

    # Bought items
    if bought:
        st.markdown("<br>", unsafe_allow_html=True)
        section_title(f"IN CART / BOUGHT — {len(bought)} ITEMS")
        for item in bought:
            _render_item_row(item, is_bought=True)


def _render_item_row(item: dict, is_bought: bool) -> None:
    col_check, col_info, col_action = st.columns([0.5, 5, 1.5])

    with col_check:
        checked = st.checkbox("", value=is_bought, key=f"chk_{item['id']}", label_visibility="collapsed")
        if checked != is_bought:
            if checked:
                mark_bought(item["id"])
            else:
                unmark_bought(item["id"])
            st.rerun()

    with col_info:
        opacity = "opacity:0.4;" if is_bought else ""
        st.markdown(f"""
        <div style="{opacity}transition:opacity .2s">
            <span style="font-weight:600;font-size:0.9rem">
                {'<s>' if is_bought else ''}{item['item_name']}{'</s>' if is_bought else ''}
            </span>
            &nbsp;
            <span class="badge badge-primary" style="font-size:0.7rem">{item['category']}</span>
            <span style="font-size:0.78rem;color:#94A3B8;margin-left:8px">{item['quantity']}</span>
        </div>
        """, unsafe_allow_html=True)

    with col_action:
        if st.button("Remove", key=f"rm_{item['id']}", use_container_width=True):
            from database import _conn
            with _conn() as conn:
                conn.execute("DELETE FROM shopping_list WHERE id=?", (item["id"],))
                conn.commit()
            st.rerun()
