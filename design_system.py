"""
Design System for HomeBrain AI

This file contains the design system components and styles for the HomeBrain AI application.
"""

# Import necessary libraries
import streamlit as st

# Define the design system components
def page_header(title: str, subtitle: str):
    st.markdown(f"<h1 class='text-4xl font-extrabold text-primary'>{title}</h1>", unsafe_allow_html=True)
    st.markdown(f"<p class='text-on-surface-variant font-medium'>{subtitle}</p>", unsafe_allow_html=True)
    st.markdown(f"<p class='text-on-surface-variant font-medium'>{subtitle}</p>", unsafe_allow_html=True)
    st.markdown(f"<p class='text-on-surface-variant font-medium'>{subtitle}</p>", unsafe_allow_html=True)

def item_card(product_name: str, quantity: int, status: str, expiry_date: str):
    status_classes = {
        "in_stock": "bg-primary",
        "low_stock": "bg-tertiary",
        "out_of_stock": "bg-error",
        "expiring_soon": "bg-warning"
    }
    status_class = status_classes.get(status, "bg-surface-container-lowest")
    status_class = status_classes.get(status, "bg-surface-container-lowest")
    status_class = status_classes.get(status, "bg-surface-container-lowest")
    st.markdown(f"""
    <div class="item-card {status_class}">
        <h3 class="font-bold text-on-surface">{product_name}</h3>
        <p class="text-xs text-on-surface-variant">{quantity} units</p>
        <p class="text-[11px] text-on-surface-variant">Expiry: {expiry_date}</p>
    </div>
    """, unsafe_allow_html=True)

# Additional components can be defined here...