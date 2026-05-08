import streamlit as st
from utils.db import create_user
from utils.auth import hash_password, validate_email, validate_password
from utils.helpers import render_back_button


def show(navigate):
    render_back_button(navigate, "landing")
    st.markdown("""
    <div style="text-align:center;margin-bottom:36px;">
        <div style="font-size:48px;margin-bottom:10px;">✨</div>
        <h1 style="font-size:32px;font-weight:900;color:#0f172a;margin:0 0 8px;letter-spacing:-1px;">
            Create your account
        </h1>
        <p style="color:#64748b;font-size:15px;margin:0;">Join 50,000+ happy FreshCart customers</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2.2, 1])
    with col2:
        st.markdown('<div class="glass" style="padding:32px 28px;">', unsafe_allow_html=True)

        with st.form("signup_form", clear_on_submit=False):
            st.markdown('<p style="font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:1px;color:#94a3b8;margin:0 0 8px;">Full Name</p>', unsafe_allow_html=True)
            name = st.text_input("Full Name", placeholder="Alex Johnson", label_visibility="collapsed")

            st.markdown('<p style="font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:1px;color:#94a3b8;margin:14px 0 8px;">Email Address</p>', unsafe_allow_html=True)
            email = st.text_input("Email", placeholder="you@example.com", label_visibility="collapsed")

            st.markdown('<p style="font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:1px;color:#94a3b8;margin:14px 0 8px;">Password</p>', unsafe_allow_html=True)
            password = st.text_input("Password", type="password", placeholder="Min. 8 chars with a number", label_visibility="collapsed")

            st.markdown('<p style="font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:1px;color:#94a3b8;margin:14px 0 8px;">Confirm Password</p>', unsafe_allow_html=True)
            confirm_password = st.text_input("Confirm Password", type="password", placeholder="Repeat your password", label_visibility="collapsed")

            st.markdown("""
            <div style="margin:18px 0 4px;padding:12px 16px;background:rgba(22,163,74,0.05);
                        border:1px solid rgba(22,163,74,0.1);border-radius:12px;">
                <p style="margin:0;font-size:12px;color:#64748b;line-height:1.6;">
                    By creating an account you agree to our
                    <strong style="color:#16a34a;">Terms of Service</strong> and
                    <strong style="color:#16a34a;">Privacy Policy</strong>.
                </p>
            </div>
            """, unsafe_allow_html=True)

            submitted = st.form_submit_button("Create Account →", use_container_width=True, type="primary")

        st.markdown('</div>', unsafe_allow_html=True)

        if submitted:
            errors = []
            if not name.strip():
                errors.append("Please enter your full name.")
            if not validate_email(email.strip()):
                errors.append("Please enter a valid email address.")
            valid_pwd, pwd_msg = validate_password(password)
            if not valid_pwd:
                errors.append(pwd_msg)
            if password != confirm_password:
                errors.append("Passwords do not match.")

            if errors:
                for err in errors:
                    st.error(err)
            else:
                with st.spinner("Creating your account..."):
                    password_hash = hash_password(password)
                    success, message = create_user(name.strip(), email.strip().lower(), password_hash)
                    if success:
                        st.success("Account created! Redirecting to sign in… 🎉")
                        st.balloons()
                        import time; time.sleep(1.5)
                        navigate("login")
                    else:
                        st.error(message)

        st.markdown("""
        <div style="text-align:center;margin-top:20px;">
            <p style="color:#94a3b8;font-size:14px;margin:0;">Already have an account?</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<div style='height:4px;'></div>", unsafe_allow_html=True)
        if st.button("Sign in instead →", use_container_width=True):
            navigate("login")
