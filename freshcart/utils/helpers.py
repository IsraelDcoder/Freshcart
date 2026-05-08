import streamlit as st

CATEGORIES = ["All", "Fruits", "Vegetables", "Dairy", "Bakery", "Grains", "Meat", "Beverages", "Snacks", "Pantry"]

HERO_FEATURES = [
    ("🚀", "Ultra-Fast Delivery", "Fresh groceries at your door in under 60 minutes"),
    ("🥦", "Premium Quality", "Handpicked produce from trusted local farms"),
    ("🔒", "Secure Checkout", "256-bit encryption for all your transactions"),
    ("♻️", "Eco Packaging", "Sustainable packaging — good for you and the planet"),
]


def inject_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* ─── Hide Streamlit chrome ─── */
    #MainMenu, footer, header { visibility: hidden; }
    .stDeployButton { display: none; }
    [data-testid="stToolbar"] { display: none; }

    /* ─── App background ─── */
    .stApp {
        background: linear-gradient(145deg, #f0f9f4 0%, #e8f5ed 30%, #f5f8ff 70%, #eef2f7 100%);
        min-height: 100vh;
    }

    /* ─── Main content padding ─── */
    .main .block-container {
        padding: 2rem 2.5rem 4rem !important;
        max-width: 1400px !important;
    }

    /* ─── Sidebar ─── */
    [data-testid="stSidebar"] {
        background: rgba(255,255,255,0.96) !important;
        backdrop-filter: blur(24px) !important;
        -webkit-backdrop-filter: blur(24px) !important;
        border-right: 1px solid rgba(10,170,84,0.1) !important;
        box-shadow: 4px 0 32px rgba(0,0,0,0.06) !important;
    }
    [data-testid="stSidebar"] > div:first-child {
        padding-top: 1.5rem !important;
    }

    /* ─── SECTION HEADERS ─── */
    .sec-label {
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 2px;
        color: #0aaa54;
        margin: 0 0 8px;
    }
    .sec-title {
        font-size: 30px;
        font-weight: 800;
        color: #0f172a;
        letter-spacing: -0.8px;
        margin: 0 0 6px;
        line-height: 1.2;
    }
    .sec-sub {
        font-size: 15px;
        color: #64748b;
        margin: 0 0 32px;
        font-weight: 400;
    }

    /* ─── STAT CARDS ─── */
    .stat-glass {
        background: rgba(255,255,255,0.8);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255,255,255,0.6);
        border-radius: 20px;
        padding: 24px 20px 20px;
        text-align: center;
        box-shadow: 0 4px 24px rgba(0,0,0,0.06), 0 1px 4px rgba(0,0,0,0.04);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .stat-glass:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 40px rgba(10,170,84,0.14), 0 4px 12px rgba(0,0,0,0.06);
    }
    .stat-icon { font-size: 28px; margin-bottom: 10px; display: block; }
    .stat-value {
        font-size: 34px;
        font-weight: 900;
        color: #0f172a;
        letter-spacing: -1px;
        line-height: 1;
        margin: 0 0 6px;
    }
    .stat-label {
        font-size: 12px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        color: #94a3b8;
        margin: 0;
    }

    /* ─── PROMO BANNER ─── */
    .promo-wrap {
        background: linear-gradient(135deg, #ea580c 0%, #f97316 50%, #fb923c 100%);
        border-radius: 16px;
        padding: 22px 28px;
        color: white;
        display: flex;
        align-items: center;
        gap: 18px;
        box-shadow: 0 8px 32px rgba(234,88,12,0.25);
        margin-bottom: 36px;
        position: relative;
        overflow: hidden;
    }
    .promo-wrap::after {
        content: '🎁';
        position: absolute; right: 24px;
        font-size: 56px; opacity: 0.15;
    }
    .promo-title { font-size: 17px; font-weight: 800; margin: 0 0 3px; }
    .promo-desc { font-size: 13px; opacity: 0.9; margin: 0; }
    .promo-code {
        display: inline-block;
        background: rgba(255,255,255,0.2);
        border: 1px dashed rgba(255,255,255,0.5);
        border-radius: 6px;
        padding: 1px 8px;
        font-family: monospace;
        font-size: 14px;
        font-weight: 700;
        letter-spacing: 1px;
    }

    /* ─── PRODUCT CARDS ─── */
    .pcard {
        background: rgba(255,255,255,0.9);
        border: 1px solid rgba(255,255,255,0.7);
        border-radius: 16px;
        overflow: hidden;
        box-shadow: 0 4px 20px rgba(0,0,0,0.07);
        transition: all 0.25s cubic-bezier(0.25,0.46,0.45,0.94);
        margin-bottom: 8px;
    }
    .pcard:hover {
        transform: translateY(-5px);
        box-shadow: 0 16px 48px rgba(10,170,84,0.15);
        border-color: rgba(10,170,84,0.2);
    }
    .pcard-img-wrap { position: relative; overflow: hidden; height: 176px; }
    .pcard-img {
        width: 100%; height: 176px;
        object-fit: cover; display: block;
        transition: transform 0.4s ease;
    }
    .pcard:hover .pcard-img { transform: scale(1.06); }
    .pcard-badge {
        position: absolute; top: 10px; left: 10px;
        background: rgba(255,255,255,0.93);
        backdrop-filter: blur(8px);
        border-radius: 100px;
        padding: 3px 10px;
        font-size: 10px; font-weight: 700;
        color: #0aaa54;
        text-transform: uppercase; letter-spacing: 0.6px;
        border: 1px solid rgba(10,170,84,0.15);
    }
    .pcard-featured {
        position: absolute; top: 10px; right: 10px;
        background: linear-gradient(135deg,#ea580c,#f97316);
        border-radius: 100px;
        padding: 3px 10px;
        font-size: 10px; font-weight: 700;
        color: white; letter-spacing: 0.5px;
    }
    .pcard-body { padding: 14px 16px 12px; }
    .pcard-cat {
        font-size: 10px; font-weight: 700;
        text-transform: uppercase; letter-spacing: 1px;
        color: #0aaa54; margin: 0 0 6px;
    }
    .pcard-name {
        font-size: 15px; font-weight: 700;
        color: #0f172a; margin: 0 0 10px;
        line-height: 1.3; min-height: 38px;
    }
    .pcard-price {
        font-size: 22px; font-weight: 900;
        color: #0f172a; letter-spacing: -0.5px; line-height: 1;
    }
    .pcard-price sub { font-size:12px; font-weight:500; color:#94a3b8; }

    /* ─── GLASS CARD ─── */
    .glass {
        background: rgba(255,255,255,0.78);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255,255,255,0.55);
        border-radius: 20px;
        padding: 28px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.07);
        margin-bottom: 20px;
    }

    /* ─── FEATURE CARDS ─── */
    .feat-card {
        background: rgba(255,255,255,0.78);
        border: 1px solid rgba(255,255,255,0.55);
        border-radius: 20px;
        padding: 28px 20px;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0,0,0,0.06);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .feat-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 40px rgba(10,170,84,0.12);
    }
    .feat-icon { font-size: 38px; margin-bottom: 14px; display: block; }
    .feat-title { font-size: 16px; font-weight: 700; color: #0f172a; margin: 0 0 8px; }
    .feat-desc { font-size: 13px; color: #64748b; line-height: 1.6; margin: 0; }

    /* ─── BUTTONS ─── */
    .stButton > button {
        border-radius: 100px !important;
        font-weight: 700 !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 14px !important;
        transition: all 0.2s ease !important;
        border: none !important;
        letter-spacing: 0.2px !important;
    }
    .stButton > button[kind="primary"] {
        background: #0aaa54 !important;
        box-shadow: 0 4px 14px rgba(10,170,84,0.3) !important;
    }
    .stButton > button[kind="primary"]:hover {
        background: #059845 !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 24px rgba(10,170,84,0.4) !important;
    }
    .stButton > button:not([kind="primary"]):hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 16px rgba(0,0,0,0.1) !important;
    }

    /* ─── INPUTS ─── */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div {
        border-radius: 14px !important;
        border: 1.5px solid #e2e8f0 !important;
        background: rgba(255,255,255,0.9) !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 14px !important;
        color: #0f172a !important;
        transition: border-color 0.2s ease !important;
    }
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #0aaa54 !important;
        box-shadow: 0 0 0 3px rgba(10,170,84,0.12) !important;
    }

    /* ─── TABS ─── */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background: rgba(241,245,249,0.8);
        border-radius: 14px;
        padding: 4px;
        border: none !important;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        color: #64748b !important;
        border: none !important;
    }
    .stTabs [aria-selected="true"] {
        background: white !important;
        color: #0f172a !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08) !important;
    }

    /* ─── ORDER CARD ─── */
    .order-card {
        background: rgba(255,255,255,0.9);
        border: 1px solid rgba(10,170,84,0.1);
        border-radius: 16px;
        padding: 20px 24px;
        margin-bottom: 12px;
        box-shadow: 0 2px 14px rgba(0,0,0,0.05);
        transition: box-shadow 0.2s ease;
    }
    .order-card:hover { box-shadow: 0 8px 32px rgba(10,170,84,0.1); }

    /* ─── CART ITEM ─── */
    .cart-item {
        background: rgba(255,255,255,0.9);
        border: 1px solid rgba(0,0,0,0.06);
        border-radius: 16px;
        padding: 16px 20px;
        margin-bottom: 12px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.04);
    }

    /* ─── BADGES ─── */
    .badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 100px;
        font-size: 11px; font-weight: 700; letter-spacing: 0.4px;
    }
    .badge-green { background: #dcfce7; color: #15803d; }
    .badge-orange { background: #ffedd5; color: #c2410c; }
    .badge-blue { background: #dbeafe; color: #1d4ed8; }

    /* ─── EMPTY STATE ─── */
    .empty-wrap { text-align: center; padding: 80px 24px; }
    .empty-icon { font-size: 72px; margin-bottom: 20px; display: block; }
    .empty-title { font-size: 22px; font-weight: 800; color: #334155; margin: 0 0 8px; }
    .empty-desc { font-size: 15px; color: #94a3b8; margin: 0 0 28px; }

    /* ─── PROFILE AVATAR ─── */
    .profile-avatar {
        width: 72px; height: 72px; border-radius: 50%;
        background: linear-gradient(135deg,#0aaa54,#4ade80);
        display: flex; align-items: center; justify-content: center;
        font-size: 28px; font-weight: 900; color: white; flex-shrink: 0;
        box-shadow: 0 4px 16px rgba(10,170,84,0.3);
    }

    /* ─── DIVIDER ─── */
    hr { border: none; border-top: 1px solid rgba(0,0,0,0.07); margin: 24px 0; }

    /* ─── SCROLLBAR ─── */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: rgba(10,170,84,0.2); border-radius: 3px; }

    .section-gap { margin-top: 52px; }
    </style>
    """, unsafe_allow_html=True)


def render_footer():
    pass  # landing page has its own footer


def cart_count(cart):
    return sum(item["quantity"] for item in cart)


def cart_total(cart):
    return sum(item["price"] * item["quantity"] for item in cart)


def render_stat_card(icon, value, label):
    return f"""
    <div class="stat-glass">
        <span class="stat-icon">{icon}</span>
        <p class="stat-value">{value}</p>
        <p class="stat-label">{label}</p>
    </div>
    """


def render_product_card(product, featured=False):
    feat = '<span class="pcard-featured">⭐ Featured</span>' if featured else ""
    return f"""
    <div class="pcard">
        <div class="pcard-img-wrap">
            <img src="{product['image_url']}" class="pcard-img" alt="{product['name']}" />
            <span class="pcard-badge">{product['category']}</span>
            {feat}
        </div>
        <div class="pcard-body">
            <p class="pcard-cat">{product['category']}</p>
            <p class="pcard-name">{product['name']}</p>
            <div class="pcard-price">${product['price']:.2f} <sub>/ unit</sub></div>
        </div>
    </div>
    """


def render_back_button(navigate_fn, destination="landing"):
    st.markdown("""
    <style>
    .back-btn-wrap { margin: 0 0 12px; }
    .back-btn-wrap .stButton > button {
        background: #fff !important;
        border: 1.5px solid #e2e8f0 !important;
        color: #374151 !important;
        font-size: 12px !important;
        font-weight: 700 !important;
        padding: 0.3rem 0.9rem !important;
        border-radius: 6px !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.06) !important;
        transition: all 0.15s !important;
    }
    .back-btn-wrap .stButton > button:hover {
        border-color: #0aaa54 !important;
        color: #0aaa54 !important;
        background: #f0fdf4 !important;
    }
    </style>
    <div class="back-btn-wrap">
    """, unsafe_allow_html=True)
    if st.button("← Back to Homepage", key=f"back_{destination}"):
        navigate_fn(destination)
    st.markdown("</div>", unsafe_allow_html=True)


def render_sidebar(user, cart, navigate_fn):
    with st.sidebar:
        st.markdown("""
        <div style="padding:4px 0 24px;">
            <div style="font-size:22px;font-weight:900;color:#0aaa54;letter-spacing:-0.8px;line-height:1;">
                🛒 FreshCart
            </div>
            <div style="font-size:10px;font-weight:700;color:#94a3b8;margin-top:3px;
                        text-transform:uppercase;letter-spacing:1.2px;">
                Premium Grocery Delivery
            </div>
        </div>
        """, unsafe_allow_html=True)

        if user:
            first = user.get('name', '?')[0].upper()
            user_card_html = f"""<div style="background:linear-gradient(135deg,rgba(10,170,84,0.08),rgba(10,170,84,0.04));border:1px solid rgba(10,170,84,0.12);border-radius:14px;padding:12px 16px;margin-bottom:18px;display:flex;align-items:center;gap:12px;">
<div style="width:38px;height:38px;border-radius:50%;flex-shrink:0;background:linear-gradient(135deg,#0aaa54,#4ade80);display:flex;align-items:center;justify-content:center;font-size:15px;font-weight:800;color:white;">
{first}
</div>
<div>
<div style="font-size:14px;font-weight:700;color:#0f172a;line-height:1.2;">{user['name']}</div>
<div style="font-size:11px;color:#94a3b8;margin-top:1px;">Gold Member ⭐</div>
</div>
</div>"""
            st.markdown(user_card_html, unsafe_allow_html=True)

            cnt = cart_count(cart)
            nav_items = [
                ("🏠", "Home", "home"),
                ("🛍️", "Shop", "shop"),
                ("🛒", f"Cart  {f'({cnt})' if cnt else ''}", "cart"),
                ("📦", "My Orders", "orders"),
                ("👤", "Profile", "profile"),
            ]
            for icon, label, page in nav_items:
                if st.button(f"{icon}  {label}", key=f"nav_{page}", use_container_width=True):
                    navigate_fn(page)

            st.markdown("<hr>", unsafe_allow_html=True)
            if st.button("🚪  Sign Out", use_container_width=True, type="secondary"):
                navigate_fn("logout")
        else:
            if st.button("🔑  Sign In", use_container_width=True, type="primary"):
                navigate_fn("login")
            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
            if st.button("✨  Create Account", use_container_width=True):
                navigate_fn("signup")

        st.markdown("""
        <div style="margin-top:24px;">
            <div style="background:rgba(10,170,84,0.06);border-radius:12px;
                        padding:12px 14px;text-align:center;">
                <div style="font-size:11px;font-weight:700;color:#0aaa54;margin-bottom:2px;">
                    🚀 60-min Delivery
                </div>
                <div style="font-size:10px;color:#94a3b8;">24/7 Customer Support</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
