import streamlit as st
from utils.db import get_user_by_email
from utils.auth import verify_password
from utils.helpers import render_back_button


def show(navigate):
    render_back_button(navigate, "landing")
    st.markdown("""
    <div style="max-width:480px;margin:32px auto 0;">
        <div style="text-align:center;margin-bottom:36px;">
            <div style="font-size:48px;margin-bottom:10px;">🛒</div>
            <h1 style="font-size:32px;font-weight:900;color:#0f172a;margin:0 0 8px;letter-spacing:-1px;">
                Welcome back
            </h1>
            <p style="color:#64748b;font-size:15px;margin:0;">Sign in to your FreshCart account</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2.2, 1])
    with col2:
        st.markdown('<div class="glass" style="padding:32px 28px;">', unsafe_allow_html=True)

        with st.form("login_form", clear_on_submit=False):
            st.markdown('<p style="font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:1px;color:#94a3b8;margin:0 0 8px;">Email Address</p>', unsafe_allow_html=True)
            email = st.text_input("Email", placeholder="you@example.com", label_visibility="collapsed")

            st.markdown('<p style="font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:1px;color:#94a3b8;margin:14px 0 8px;">Password</p>', unsafe_allow_html=True)
            password = st.text_input("Password", type="password", placeholder="Enter your password", label_visibility="collapsed")

            st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
            submitted = st.form_submit_button("Sign In →", use_container_width=True, type="primary")

        st.markdown('</div>', unsafe_allow_html=True)

        if submitted:
            if not email or not password:
                st.error("Please fill in all fields.")
            else:
                with st.spinner("Signing you in..."):
                    user = get_user_by_email(email.strip().lower())
                    if user and verify_password(password, user["password_hash"]):
                        st.session_state.user = user
                        st.session_state.cart = []
                        st.success(f"Welcome back, {user['name']}! 🎉")
                        st.session_state.page = "home"
                        st.rerun()
                    else:
                        st.error("Invalid email or password. Please try again.")

        st.markdown("""
        <div style="text-align:center;margin-top:20px;">
            <p style="color:#94a3b8;font-size:14px;margin:0;">Don't have an account yet?</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<div style='height:4px;'></div>", unsafe_allow_html=True)
        if st.button("Create a free account →", use_container_width=True):
            navigate("signup")
