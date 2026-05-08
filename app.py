import streamlit as st
from utils.db import init_db
from utils.helpers import inject_css, render_footer, render_sidebar

st.set_page_config(
    page_title="FreshCart — Fresh Grocery Delivery",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_css()
init_db()


def init_session():
    if "page" not in st.session_state:
        st.session_state.page = "landing"
    if "user" not in st.session_state:
        st.session_state.user = None
    if "cart" not in st.session_state:
        st.session_state.cart = []
    if "checkout_summary" not in st.session_state:
        st.session_state.checkout_summary = {}
    if "last_order_id" not in st.session_state:
        st.session_state.last_order_id = None


def navigate(page):
    if page == "logout":
        st.session_state.user = None
        st.session_state.cart = []
        st.session_state.page = "landing"
    else:
        st.session_state.page = page
    st.rerun()


init_session()

user = st.session_state.get("user")
cart = st.session_state.get("cart", [])

render_sidebar(user, cart, navigate)

page = st.session_state.page

PROTECTED_PAGES = {"home", "shop", "cart", "checkout", "orders", "profile", "order_success"}
if page in PROTECTED_PAGES and not user:
    st.session_state.page = "login"
    st.rerun()

if page == "landing":
    from views.landing import show
    show(navigate)
elif page == "login":
    from views.login import show
    show(navigate)
elif page == "signup":
    from views.signup import show
    show(navigate)
elif page == "home":
    from views.home import show
    show(navigate)
elif page == "shop":
    from views.shop import show
    show(navigate)
elif page == "cart":
    from views.cart import show
    show(navigate)
elif page == "checkout":
    from views.checkout import show
    show(navigate)
elif page == "orders":
    from views.orders import show
    show(navigate)
elif page == "profile":
    from views.profile import show
    show(navigate)
elif page == "order_success":
    from views.order_success import show
    show(navigate)
else:
    st.session_state.page = "landing"
    st.rerun()

render_footer()
