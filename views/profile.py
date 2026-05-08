import streamlit as st
from utils.db import get_user_orders, update_user, get_user_by_id
from utils.auth import hash_password, verify_password, validate_password
from utils.helpers import render_stat_card, render_back_button


def show(navigate):
    render_back_button(navigate, "home")
    user = st.session_state.get("user", {})

    st.markdown('<p class="sec-label">Account</p>', unsafe_allow_html=True)
    st.markdown('<p class="sec-title">👤 My Profile</p>', unsafe_allow_html=True)
    st.markdown('<p class="sec-sub">Manage your account details and preferences</p>', unsafe_allow_html=True)

    orders = get_user_orders(user["id"])
    total_spent = sum(o["total_price"] for o in orders)

    # ── Stats ─────────────────────────────────────────────────────
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(render_stat_card("📦", str(len(orders)), "Total Orders"), unsafe_allow_html=True)
    with c2:
        st.markdown(render_stat_card("💰", f"${total_spent:.2f}", "Total Spent"), unsafe_allow_html=True)
    with c3:
        st.markdown(render_stat_card("⭐", "Gold", "Member Status"), unsafe_allow_html=True)

    st.markdown("<div style='height:32px;'></div>", unsafe_allow_html=True)

    # ── Avatar + info ─────────────────────────────────────────────
    profile_html = f"""<div class="glass" style="display:flex;align-items:center;gap:20px;margin-bottom:24px;padding:24px 28px;">
<div class="profile-avatar">{user.get('name','?')[0].upper()}</div>
<div>
<div style="font-size:22px;font-weight:800;color:#0f172a;">{user.get('name')}</div>
<div style="font-size:14px;color:#64748b;margin-top:2px;">{user.get('email')}</div>
<span class="badge badge-green" style="margin-top:8px;display:inline-block;">⭐ Gold Member</span>
</div>
</div>"""
    st.markdown(profile_html, unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["👤  Account Info", "🔐  Change Password"])

    with tab1:
        with st.form("update_profile"):
            st.markdown('<p style="font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:1px;color:#94a3b8;margin:0 0 8px;">Display Name</p>', unsafe_allow_html=True)
            new_name = st.text_input("Name", value=user.get("name", ""), label_visibility="collapsed")

            info_html = f"""<div style="margin:16px 0;padding:14px 16px;background:rgba(0,0,0,0.02);border-radius:12px;border:1px solid rgba(0,0,0,0.06);">
<div style="font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:0.8px;color:#94a3b8;margin-bottom:4px;">Email Address</div>
<div style="font-size:14px;color:#475569;font-weight:500;">{user.get('email')}</div>
</div>
<div style="margin-bottom:20px;padding:14px 16px;background:rgba(0,0,0,0.02);border-radius:12px;border:1px solid rgba(0,0,0,0.06);">
<div style="font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:0.8px;color:#94a3b8;margin-bottom:4px;">Member Since</div>
<div style="font-size:14px;color:#475569;font-weight:500;">{str(user.get('created_at',''))[:10] or 'N/A'}</div>
</div>"""
            st.markdown(info_html, unsafe_allow_html=True)

            save = st.form_submit_button("Save Changes", use_container_width=True, type="primary")

        if save:
            if not new_name.strip():
                st.error("Name cannot be empty.")
            else:
                try:
                    update_user(user["id"], new_name.strip())
                    updated = get_user_by_id(user["id"])
                    st.session_state.user = updated
                    st.success("✓ Profile updated successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Failed to update profile: {str(e)}")

    with tab2:
        with st.form("change_password"):
            st.markdown('<p style="font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:1px;color:#94a3b8;margin:0 0 8px;">Current Password</p>', unsafe_allow_html=True)
            current_pwd = st.text_input("Current", type="password", placeholder="Your current password", label_visibility="collapsed")

            st.markdown('<p style="font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:1px;color:#94a3b8;margin:14px 0 8px;">New Password</p>', unsafe_allow_html=True)
            new_pwd = st.text_input("New Password", type="password", placeholder="Min. 8 chars with a number", label_visibility="collapsed")

            st.markdown('<p style="font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:1px;color:#94a3b8;margin:14px 0 8px;">Confirm New Password</p>', unsafe_allow_html=True)
            confirm_pwd = st.text_input("Confirm", type="password", placeholder="Repeat your new password", label_visibility="collapsed")

            update_pwd = st.form_submit_button("Update Password", use_container_width=True, type="primary")

        if update_pwd:
            errors = []
            if not current_pwd:
                errors.append("Please enter your current password.")
            elif not verify_password(current_pwd, user["password_hash"]):
                errors.append("Current password is incorrect.")
            if not new_pwd:
                errors.append("Please enter a new password.")
            elif new_pwd != confirm_pwd:
                errors.append("New passwords do not match.")
            else:
                valid, msg = validate_password(new_pwd)
                if not valid:
                    errors.append(msg)

            if errors:
                for err in errors:
                    st.error(err)
            else:
                try:
                    new_hash = hash_password(new_pwd)
                    update_user(user["id"], user["name"], new_hash)
                    updated = get_user_by_id(user["id"])
                    st.session_state.user = updated
                    st.success("✓ Password updated successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Failed to update password: {str(e)}")
