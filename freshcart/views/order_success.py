import streamlit as st
from utils.helpers import render_back_button


def show(navigate):
    render_back_button(navigate, "home")
    order_id = st.session_state.get("last_order_id", "—")
    st.balloons()

    success_html = f"""<div style="text-align:center;padding:48px 24px 40px;">
<div style="font-size:88px;margin-bottom:20px;animation:bounce 0.6s ease;">🎉</div>
<div style="display:inline-block;background:#dcfce7;border:1px solid #bbf7d0;border-radius:100px;padding:6px 18px;font-size:12px;font-weight:700;color:#15803d;text-transform:uppercase;letter-spacing:1px;margin-bottom:16px;">Order Confirmed</div>
<h1 style="font-size:42px;font-weight:900;color:#0f172a;margin:0 0 12px;letter-spacing:-1.5px;">Your order is on its way!</h1>
<p style="font-size:17px;color:#64748b;margin:0 0 40px;max-width:460px;margin-left:auto;margin-right:auto;line-height:1.6;">Our team is picking your freshest items and your delivery partner is being dispatched right now.</p>
</div>"""
    st.markdown(success_html, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        details_html = f"""<div class="glass" style="padding:28px 32px;text-align:left;">
<div style="font-size:13px;font-weight:700;text-transform:uppercase;letter-spacing:0.8px;color:#94a3b8;margin-bottom:16px;">Order Details</div>
<div style="display:flex;justify-content:space-between;margin-bottom:12px;padding-bottom:12px;border-bottom:1px solid rgba(0,0,0,0.06);">
<span style="font-size:14px;color:#64748b;">Order ID</span>
<span style="font-size:14px;font-weight:800;color:#0f172a;">#{order_id}</span>
</div>
<div style="display:flex;justify-content:space-between;margin-bottom:12px;padding-bottom:12px;border-bottom:1px solid rgba(0,0,0,0.06);">
<span style="font-size:14px;color:#64748b;">Status</span>
<span class="badge badge-green">Confirmed ✓</span>
</div>
<div style="display:flex;justify-content:space-between;">
<span style="font-size:14px;color:#64748b;">Estimated Delivery</span>
<span style="font-size:14px;font-weight:800;color:#16a34a;">45–60 minutes</span>
</div>
</div>
<div style="background:rgba(22,163,74,0.05);border:1px solid rgba(22,163,74,0.1);border-radius:14px;padding:16px 20px;margin-top:16px;">
<div style="font-size:13px;color:#475569;line-height:1.7;">
📩 You'll receive a confirmation shortly. Our delivery partner will contact you when they're 5 minutes away.
</div>
</div>"""
        st.markdown(details_html, unsafe_allow_html=True)

    st.markdown("<div style='height:24px;'></div>", unsafe_allow_html=True)
    b1, b2, b3 = st.columns([1, 1, 2])
    with b1:
        if st.button("📦  View Orders", use_container_width=True, type="primary"):
            navigate("orders")
    with b2:
        if st.button("🛍️  Keep Shopping", use_container_width=True):
            navigate("shop")
