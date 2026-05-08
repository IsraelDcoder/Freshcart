import streamlit as st
from utils.db import get_all_products
from utils.helpers import CATEGORIES, render_back_button

DEALS = [
    ("Buy 1, get 1 free", "#fef08a", "#854d0e"),
    ("Save 20%",          "#bbf7d0", "#166534"),
    ("2 for $7",          "#fed7aa", "#9a3412"),
    ("Save $1.00",        "#dbeafe", "#1e40af"),
    ("",                  "",        ""),
]
QUALITY = {
    "Fruits":    "Organic",
    "Vegetables":"Non GMO",
    "Dairy":     "Farm fresh",
    "Meat":      "Free range",
    "Snacks":    "Low calorie",
    "Bakery":    "Freshly baked",
    "Grains":    "Whole grain",
    "Beverages": "No preservatives",
    "Pantry":    "All natural",
}


def _stars(pid):
    base = 3.5 + (pid * 7 % 15) / 10
    val  = round(base * 2) / 2
    full = int(val)
    half = 1 if val != full else 0
    empty = 5 - full - half
    return "★" * full + ("½" if half else "") + "☆" * empty, 18 + (pid * 13 % 200)


def _deal(pid):
    return DEALS[pid % len(DEALS)]


def _stock(pid):
    return ("Low stock", "#f59e0b") if pid % 9 == 0 else ("Many in stock", "#16a34a")


def _pcard_html(p):
    quality   = QUALITY.get(p["category"], "Fresh")
    deal_txt, deal_bg, deal_fg = _deal(p["id"])
    stars_str, review_cnt      = _stars(p["id"])
    stock_txt, stock_color     = _stock(p["id"])

    deal_html = (f'<div class="ic-deal-badge" style="background:{deal_bg};color:{deal_fg};">'
                 f'{deal_txt}</div>') if deal_txt else "<div style='height:18px;'></div>"

    return f"""
    <div class="ic-pcard">
        <div class="ic-img-wrap">
            <img src="{p['image_url']}" class="ic-pcard-img" alt="{p['name']}" />
            <span class="ic-quality-badge">{quality}</span>
        </div>
        <div class="ic-body">
            <div class="ic-price">${p['price']:.2f}</div>
            {deal_html}
            <div class="ic-stars">{stars_str} <span class="ic-review-cnt">({review_cnt})</span></div>
            <div class="ic-name">{p['name']}</div>
            <div class="ic-stock" style="color:{stock_color};">&#10003; {stock_txt}</div>
        </div>
    </div>
    """


def _add_to_cart(product, qty=1):
    cart = st.session_state.get("cart", [])
    for item in cart:
        if item["id"] == product["id"]:
            item["quantity"] += qty
            st.session_state.cart = cart
            return
    cart.append({"id": product["id"], "name": product["name"],
                 "price": product["price"], "image_url": product["image_url"],
                 "quantity": qty})
    st.session_state.cart = cart


def show(navigate):
    render_back_button(navigate, "home")
    _inject_css()

    # ── Filter bar ────────────────────────────────────────────────
    st.markdown("""
    <div class="shop-header">
        <h1 class="shop-title">Shop</h1>
    </div>
    """, unsafe_allow_html=True)

    fc1, fc2, fc3 = st.columns([3, 2, 2])
    with fc1:
        search = st.text_input("Search", placeholder="🔍  Search products (e.g. banana, milk, bread)…",
                               label_visibility="collapsed")
    with fc2:
        category = st.selectbox("Category", CATEGORIES, label_visibility="collapsed")
    with fc3:
        sort_by = st.selectbox("Sort", ["Default", "Price: Low to High", "Price: High to Low", "Name A–Z"],
                               label_visibility="collapsed")

    # ── Filter pill row ───────────────────────────────────────────
    filter_cats = ["All", "Fruits", "Vegetables", "Dairy", "Meat", "Bakery", "Beverages", "Snacks", "Pantry"]
    pill_cols = st.columns(len(filter_cats))
    for col, cat in zip(pill_cols, filter_cats):
        with col:
            active = category == cat
            pill_html = f"""<div class="shop-pill {'shop-pill-active' if active else ''}">
{cat}
</div>"""
            st.markdown(pill_html, unsafe_allow_html=True)

    st.markdown('<div class="shop-divider"></div>', unsafe_allow_html=True)

    # ── Apply filters ─────────────────────────────────────────────
    products = get_all_products()
    if search:
        products = [p for p in products if search.lower() in p["name"].lower()
                    or search.lower() in p["category"].lower()]
    if category != "All":
        products = [p for p in products if p["category"] == category]
    if sort_by == "Price: Low to High":
        products = sorted(products, key=lambda x: x["price"])
    elif sort_by == "Price: High to Low":
        products = sorted(products, key=lambda x: x["price"], reverse=True)
    elif sort_by == "Name A–Z":
        products = sorted(products, key=lambda x: x["name"])

    # ── Results header ────────────────────────────────────────────
    if not products:
        st.markdown("""
        <div class="ic-empty">
            <div class="ic-empty-icon">🔍</div>
            <div class="ic-empty-title">No products found</div>
            <p class="ic-empty-desc">Try a different search term or category filter</p>
        </div>
        """, unsafe_allow_html=True)
        return

    cat_label = f' in <strong>{category}</strong>' if category != "All" else ""
    st.markdown(f'<p class="shop-result-count">Showing <strong>{len(products)}</strong> products{cat_label}</p>',
                unsafe_allow_html=True)

    # ── Product grid — 5 columns ──────────────────────────────────
    cols = st.columns(5)
    for i, product in enumerate(products):
        with cols[i % 5]:
            st.markdown(_pcard_html(product), unsafe_allow_html=True)

            qty_key = f"shop_qty_{product['id']}"
            if qty_key not in st.session_state:
                st.session_state[qty_key] = 1

            qa, qb = st.columns([1, 2])
            with qa:
                qty = st.number_input("Qty", min_value=1, max_value=20,
                                      value=st.session_state[qty_key],
                                      key=qty_key, label_visibility="collapsed")
            with qb:
                if st.button("＋ Add", key=f"shop_add_{product['id']}",
                             use_container_width=True, type="primary"):
                    _add_to_cart(product, qty)
                    st.toast(f"Added {qty}× {product['name']}")

            st.markdown("<div style='height:18px;'></div>", unsafe_allow_html=True)

    # ── Cart sticky summary ───────────────────────────────────────
    cart = st.session_state.get("cart", [])
    if cart:
        total = sum(i["price"] * i["quantity"] for i in cart)
        count = sum(i["quantity"] for i in cart)
        cart_bar_html = f"""<div class="shop-cart-bar">
<div>
<div style="font-size:15px;font-weight:800;color:#0f172a;">
🛒 {count} item{'s' if count != 1 else ''} in your cart
</div>
<div style="font-size:13px;color:#64748b;margin-top:2px;">
Subtotal: <strong style="color:#0aaa54;">${total:.2f}</strong>
</div>
</div>
</div>"""
        st.markdown(cart_bar_html, unsafe_allow_html=True)
        if st.button("View Cart & Checkout →", type="primary"):
            navigate("cart")


def _inject_css():
    st.markdown("""
    <style>
    .stApp { background: #ffffff !important; }
    .main .block-container {
        padding: 0 1.5rem 0 !important;
        max-width: 1300px !important;
    }

    .shop-header { padding: 16px 0 8px; border-bottom: 1px solid #e2e8f0; margin-bottom: 14px; }
    .shop-title { font-size: 24px; font-weight: 900; color: #0f172a; letter-spacing: -0.5px; margin: 0; }

    .shop-pill {
        text-align: center;
        padding: 6px 4px;
        border-radius: 100px;
        font-size: 11px;
        font-weight: 600;
        color: #475569;
        background: #f1f5f9;
        border: 1px solid #e2e8f0;
        cursor: pointer;
    }
    .shop-pill-active {
        background: #0f172a;
        color: #ffffff;
        border-color: #0f172a;
    }
    .shop-divider { height: 1px; background: #e2e8f0; margin: 14px 0 18px; }
    .shop-result-count { font-size: 13px; color: #64748b; margin: 0 0 16px; }

    /* Product card — same as home */
    .ic-pcard {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        overflow: hidden;
        transition: box-shadow 0.18s ease;
        margin-bottom: 4px;
    }
    .ic-pcard:hover { box-shadow: 0 4px 16px rgba(0,0,0,0.10); }
    .ic-img-wrap {
        background: #f8fafc;
        position: relative;
        height: 150px;
        overflow: hidden;
    }
    .ic-pcard-img {
        width: 100%; height: 150px; object-fit: cover; display: block;
        transition: transform 0.3s ease;
    }
    .ic-pcard:hover .ic-pcard-img { transform: scale(1.04); }
    .ic-quality-badge {
        position: absolute; bottom: 7px; left: 7px;
        background: rgba(255,255,255,0.93);
        border: 1px solid #e2e8f0;
        border-radius: 4px;
        font-size: 9px; font-weight: 700; color: #475569;
        padding: 2px 6px;
        text-transform: uppercase; letter-spacing: 0.4px;
    }
    .ic-body { padding: 9px 10px 10px; }
    .ic-price { font-size: 19px; font-weight: 900; color: #0f172a; letter-spacing: -0.5px; margin: 0 0 3px; }
    .ic-deal-badge {
        display: inline-block; border-radius: 3px;
        font-size: 10px; font-weight: 800; padding: 2px 6px; margin-bottom: 4px;
    }
    .ic-stars { font-size: 11px; color: #f59e0b; margin-bottom: 4px; }
    .ic-review-cnt { color: #94a3b8; font-size: 10px; }
    .ic-name {
        font-size: 12px; font-weight: 500; color: #1e293b; line-height: 1.35;
        margin-bottom: 4px; display: -webkit-box; -webkit-line-clamp: 2;
        -webkit-box-orient: vertical; overflow: hidden; min-height: 32px;
    }
    .ic-stock { font-size: 11px; font-weight: 600; margin-top: 2px; }
    .ic-empty { text-align: center; padding: 60px 24px; }
    .ic-empty-icon { font-size: 56px; margin-bottom: 14px; }
    .ic-empty-title { font-size: 20px; font-weight: 800; color: #334155; margin-bottom: 6px; }
    .ic-empty-desc { font-size: 14px; color: #94a3b8; }

    .shop-cart-bar {
        background: #f0fdf4; border: 1px solid #bbf7d0;
        border-radius: 12px; padding: 16px 20px; margin: 24px 0 12px;
    }

    /* Buttons */
    .stButton > button[kind="primary"] {
        background: #003d1a !important;
        background-image: none !important;
        border: none !important;
        border-radius: 6px !important;
        font-size: 13px !important;
        font-weight: 700 !important;
        padding: 0.35rem 0.8rem !important;
        box-shadow: none !important;
    }
    .stButton > button[kind="primary"]:hover {
        background: #0aaa54 !important;
        box-shadow: 0 2px 8px rgba(10,170,84,0.3) !important;
    }
    .stButton > button:not([kind="primary"]) {
        border: 1px solid #d1d5db !important;
        border-radius: 6px !important;
        background: #ffffff !important;
        color: #374151 !important;
        font-size: 12px !important;
        font-weight: 600 !important;
        padding: 0.3rem 0.6rem !important;
        box-shadow: none !important;
    }
    </style>
    """, unsafe_allow_html=True)
