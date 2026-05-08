import streamlit as st
from utils.db import get_all_products, get_user_orders
from utils.helpers import render_back_button

# ── Deal & quality label lookups ──────────────────────────────
DEALS = [
    ("Buy 1, get 1 free", "#fef08a", "#854d0e"),
    ("Save 20%",          "#bbf7d0", "#166534"),
    ("2 for $7",          "#fed7aa", "#9a3412"),
    ("Save $1.00",        "#dbeafe", "#1e40af"),
    ("",                  "",        ""),          # no deal
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
CATEGORY_ICONS = [
    ("Produce",      "https://images.unsplash.com/photo-1540420773420-3366772f4999?w=80&auto=format&fit=crop"),
    ("Meat & Seafood","https://images.unsplash.com/photo-1604503468506-a8da13d82791?w=80&auto=format&fit=crop"),
    ("Dairy & Eggs", "https://images.unsplash.com/photo-1563636619-e9143da7973b?w=80&auto=format&fit=crop"),
    ("Bakery",       "https://images.unsplash.com/photo-1549931319-a545dcf3bc73?w=80&auto=format&fit=crop"),
    ("Snacks",       "https://images.unsplash.com/photo-1599599810694-b5b37304c041?w=80&auto=format&fit=crop"),
    ("Beverages",    "https://images.unsplash.com/photo-1600271886742-f049cd451bba?w=80&auto=format&fit=crop"),
    ("Frozen",       "https://images.unsplash.com/photo-1584277261846-c6a1672ed979?w=80&auto=format&fit=crop"),
    ("Pantry",       "https://images.unsplash.com/photo-1506484381205-f7945653044d?w=80&auto=format&fit=crop"),
    ("Household",    "https://images.unsplash.com/photo-1583947581924-860bda6a26df?w=80&auto=format&fit=crop"),
    ("Recipes",      "https://images.unsplash.com/photo-1466637574441-749b8f19452f?w=80&auto=format&fit=crop"),
]


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
    quality    = QUALITY.get(p["category"], "Fresh")
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


def _product_row(section_key, products, navigate):
    """Render 5 products in a row with Instacart-style cards + add buttons."""
    cols = st.columns(5)
    for i, (col, p) in enumerate(zip(cols, products)):
        with col:
            st.markdown(_pcard_html(p), unsafe_allow_html=True)
            qty_key = f"qty_{section_key}_{p['id']}"
            if qty_key not in st.session_state:
                st.session_state[qty_key] = 1
            if st.button("＋ Add", key=f"add_{section_key}_{p['id']}",
                         use_container_width=True, type="primary"):
                _add_to_cart(p, st.session_state[qty_key])
                st.toast(f"Added {p['name']} to cart")


def _section_header(title, section_key, navigate):
    c1, c2 = st.columns([5, 1])
    with c1:
        st.markdown(f'<h2 class="ic-section-title">{title}</h2>', unsafe_allow_html=True)
    with c2:
        if st.button("View more →", key=f"more_{section_key}", use_container_width=True):
            navigate("shop")


def show(navigate):
    render_back_button(navigate, "landing")
    _inject_css()

    user   = st.session_state.get("user", {})
    cart   = st.session_state.get("cart", [])
    orders = get_user_orders(user["id"])
    fname  = user.get("name", "there").split()[0]

    products = get_all_products()

    # ── Delivery / greeting bar ────────────────────────────────────
    cart_count = sum(i["quantity"] for i in cart)
    cart_total = sum(i["price"] * i["quantity"] for i in cart)

    top_bar_html = f"""<div class="ic-top-bar">
<div class="ic-greeting">
<span class="ic-flash">⚡</span>
<div>
<div class="ic-delivery-time">Delivery by 10:38 – 10:58am</div>
<div class="ic-delivery-addr">👋 Welcome back, {fname}</div>
</div>
</div>
<div class="ic-cart-pill">
🛒&nbsp; {cart_count} item{'s' if cart_count != 1 else ''}
&nbsp;·&nbsp;
<strong>${cart_total:.2f}</strong>
</div>
</div>"""
    st.markdown(top_bar_html, unsafe_allow_html=True)

    # ── Inline search ──────────────────────────────────────────────
    sc1, sc2 = st.columns([5, 1])
    with sc1:
        search = st.text_input("search", placeholder='🔍  Try "organic bananas" or "milk"…',
                               label_visibility="collapsed")
    with sc2:
        if st.button("Browse all", use_container_width=True):
            navigate("shop")

    # ── Category icon row ──────────────────────────────────────────
    cat_cols = st.columns(len(CATEGORY_ICONS))
    for col, (name, img) in zip(cat_cols, CATEGORY_ICONS):
        with col:
            cat_html = f"""<div class="ic-cat-chip">
<img src="{img}" class="ic-cat-img" alt="{name}" />
<span class="ic-cat-label">{name}</span>
</div>"""
            st.markdown(cat_html, unsafe_allow_html=True)

    st.markdown('<div class="ic-cat-divider"></div>', unsafe_allow_html=True)

    # If searching, show filtered results instead of sections
    if search:
        filtered = [p for p in products if search.lower() in p["name"].lower()
                    or search.lower() in p["category"].lower()]
        if filtered:
            st.markdown(f'<p class="ic-result-count">{len(filtered)} results for "<strong>{search}</strong>"</p>',
                        unsafe_allow_html=True)
            for chunk_start in range(0, len(filtered), 5):
                chunk = filtered[chunk_start:chunk_start + 5]
                _product_row(f"search_{chunk_start}", chunk, navigate)
                st.markdown('<div style="height:16px;"></div>', unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="ic-empty">
                <div class="ic-empty-icon">🔍</div>
                <div class="ic-empty-title">No results found</div>
                <p class="ic-empty-desc">Try a different search term</p>
            </div>
            """, unsafe_allow_html=True)
        return

    # ── BOGO / Deals section ───────────────────────────────────────
    deal_products = [p for p in products if _deal(p["id"])[0]][:5]
    if deal_products:
        st.markdown('<div style="height:8px;"></div>', unsafe_allow_html=True)
        _section_header("🏷️ BOGO and more", "deals", navigate)
        _product_row("deals", deal_products, navigate)
        st.markdown("""
        <p class="ic-eligible-link">See eligible items &rsaquo;</p>
        """, unsafe_allow_html=True)

    # ── Fresh produce ──────────────────────────────────────────────
    produce = [p for p in products if p["category"] in ("Fruits", "Vegetables")][:5]
    if produce:
        st.markdown('<div class="ic-section-gap"></div>', unsafe_allow_html=True)
        _section_header("🥦 Fresh produce", "produce", navigate)
        _product_row("produce", produce, navigate)

    # ── Dairy & Eggs ──────────────────────────────────────────────
    dairy = [p for p in products if p["category"] == "Dairy"][:5]
    if dairy:
        st.markdown('<div class="ic-section-gap"></div>', unsafe_allow_html=True)
        _section_header("🥛 Dairy & Eggs", "dairy", navigate)
        _product_row("dairy", dairy, navigate)

    # ── Meat & Seafood ────────────────────────────────────────────
    meat = [p for p in products if p["category"] == "Meat"][:5]
    if meat:
        st.markdown('<div class="ic-section-gap"></div>', unsafe_allow_html=True)
        _section_header("🥩 Meat & Seafood", "meat", navigate)
        _product_row("meat", meat, navigate)

    # ── Pantry staples ────────────────────────────────────────────
    pantry = [p for p in products if p["category"] in ("Pantry", "Grains", "Snacks", "Beverages")][:5]
    if pantry:
        st.markdown('<div class="ic-section-gap"></div>', unsafe_allow_html=True)
        _section_header("🫙 Pantry staples", "pantry", navigate)
        _product_row("pantry", pantry, navigate)

    # ── Buy it again (recent orders) ──────────────────────────────
    if orders:
        all_prev_ids = []
        for o in orders[:3]:
            for item in o.get("items", []):
                if item["id"] not in all_prev_ids:
                    all_prev_ids.append(item["id"])

        prev_products = [p for p in products if p["id"] in all_prev_ids][:5]
        if prev_products:
            st.markdown('<div class="ic-section-gap"></div>', unsafe_allow_html=True)
            _section_header("🔄 Buy it again", "buyagain", navigate)
            _product_row("buyagain", prev_products, navigate)

    # ── Bottom CTA strip ──────────────────────────────────────────
    st.markdown('<div class="ic-section-gap"></div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="ic-bottom-strip">
        <div>
            <div class="ic-bottom-title">Browse all aisles</div>
            <p class="ic-bottom-sub">200+ products across every category — from farm to door in 60 min.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    bc1, bc2, bc3 = st.columns([1.2, 1, 3])
    with bc1:
        if st.button("🛍️  Shop all products", use_container_width=True, type="primary"):
            navigate("shop")
    with bc2:
        if st.button("📦  My orders", use_container_width=True):
            navigate("orders")

    st.markdown('<div style="height:48px;"></div>', unsafe_allow_html=True)


def _inject_css():
    st.markdown("""
    <style>
    /* ── White canvas for store view ── */
    .stApp { background: #ffffff !important; }
    .main .block-container {
        padding: 0 1.5rem 0 !important;
        max-width: 1300px !important;
    }

    /* ── Top delivery bar ── */
    .ic-top-bar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 14px 0 10px;
        border-bottom: 1px solid #e2e8f0;
        margin-bottom: 14px;
    }
    .ic-greeting { display: flex; align-items: center; gap: 12px; }
    .ic-flash { font-size: 24px; }
    .ic-delivery-time {
        font-size: 15px; font-weight: 800; color: #0f172a;
        letter-spacing: -0.3px;
    }
    .ic-delivery-addr { font-size: 12px; color: #64748b; margin-top: 1px; }
    .ic-cart-pill {
        background: #f0fdf4;
        border: 1px solid #bbf7d0;
        border-radius: 100px;
        padding: 7px 18px;
        font-size: 13px;
        color: #0f172a;
    }

    /* ── Category chips ── */
    .ic-cat-chip {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 6px;
        padding: 8px 4px 10px;
        border-radius: 10px;
        cursor: pointer;
        transition: background 0.15s;
    }
    .ic-cat-chip:hover { background: #f1f5f9; }
    .ic-cat-img {
        width: 100%;
        max-width: 64px;
        height: 56px;
        object-fit: cover;
        border-radius: 8px;
        display: block;
        margin: 0 auto;
    }
    .ic-cat-label {
        font-size: 10px;
        font-weight: 600;
        color: #334155;
        text-align: center;
        line-height: 1.2;
    }
    .ic-cat-divider {
        height: 1px;
        background: #e2e8f0;
        margin: 12px 0 24px;
    }

    /* ── Section headers ── */
    .ic-section-title {
        font-size: 20px;
        font-weight: 800;
        color: #0f172a;
        letter-spacing: -0.4px;
        margin: 0;
    }
    .ic-section-gap { height: 36px; }

    /* ── Product card ── */
    .ic-pcard {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        overflow: hidden;
        transition: box-shadow 0.18s ease;
        margin-bottom: 4px;
    }
    .ic-pcard:hover {
        box-shadow: 0 4px 16px rgba(0,0,0,0.10);
    }
    .ic-img-wrap {
        background: #f8fafc;
        position: relative;
        height: 150px;
        overflow: hidden;
    }
    .ic-pcard-img {
        width: 100%;
        height: 150px;
        object-fit: cover;
        display: block;
        transition: transform 0.3s ease;
    }
    .ic-pcard:hover .ic-pcard-img { transform: scale(1.04); }
    .ic-quality-badge {
        position: absolute;
        bottom: 7px;
        left: 7px;
        background: rgba(255,255,255,0.93);
        border: 1px solid #e2e8f0;
        border-radius: 4px;
        font-size: 9px;
        font-weight: 700;
        color: #475569;
        padding: 2px 6px;
        text-transform: uppercase;
        letter-spacing: 0.4px;
    }
    .ic-body { padding: 9px 10px 10px; }
    .ic-price {
        font-size: 19px;
        font-weight: 900;
        color: #0f172a;
        letter-spacing: -0.5px;
        margin: 0 0 3px;
    }
    .ic-deal-badge {
        display: inline-block;
        border-radius: 3px;
        font-size: 10px;
        font-weight: 800;
        padding: 2px 6px;
        margin-bottom: 4px;
        letter-spacing: 0.2px;
    }
    .ic-stars {
        font-size: 11px;
        color: #f59e0b;
        margin-bottom: 4px;
        line-height: 1;
    }
    .ic-review-cnt { color: #94a3b8; font-size: 10px; }
    .ic-name {
        font-size: 12px;
        font-weight: 500;
        color: #1e293b;
        line-height: 1.35;
        margin-bottom: 4px;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        overflow: hidden;
        min-height: 32px;
    }
    .ic-stock {
        font-size: 11px;
        font-weight: 600;
        margin-top: 2px;
    }

    /* ── View more / eligible links ── */
    .ic-eligible-link {
        font-size: 12px;
        color: #0aaa54;
        font-weight: 600;
        margin: 6px 0 0;
        cursor: pointer;
    }
    .ic-result-count {
        font-size: 14px;
        color: #64748b;
        margin: 0 0 16px;
    }

    /* ── Bottom CTA ── */
    .ic-bottom-strip {
        background: #f0fdf4;
        border: 1px solid #bbf7d0;
        border-radius: 14px;
        padding: 24px 28px;
        margin-bottom: 16px;
    }
    .ic-bottom-title {
        font-size: 18px; font-weight: 800; color: #0f172a; margin-bottom: 3px;
    }
    .ic-bottom-sub { font-size: 13px; color: #64748b; margin: 0; }

    /* ── Empty state ── */
    .ic-empty {
        text-align: center; padding: 60px 24px;
    }
    .ic-empty-icon { font-size: 56px; margin-bottom: 14px; }
    .ic-empty-title { font-size: 20px; font-weight: 800; color: #334155; margin-bottom: 6px; }
    .ic-empty-desc { font-size: 14px; color: #94a3b8; }

    /* ── Buttons — compact add button ── */
    .stButton > button[kind="primary"] {
        background: #003d1a !important;
        background-image: none !important;
        border: none !important;
        border-radius: 6px !important;
        font-size: 13px !important;
        font-weight: 700 !important;
        padding: 0.35rem 0.8rem !important;
        box-shadow: none !important;
        letter-spacing: 0.3px !important;
    }
    .stButton > button[kind="primary"]:hover {
        background: #0aaa54 !important;
        transform: none !important;
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
