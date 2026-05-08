import streamlit as st
from utils.db import get_user_orders
from utils.helpers import render_back_button


def show(navigate):
    render_back_button(navigate, "home")
    user = st.session_state.get("user", {})

    st.markdown('<p class="sec-label">History</p>', unsafe_allow_html=True)
    st.markdown('<p class="sec-title">📦 My Orders</p>', unsafe_allow_html=True)

    with st.spinner("Loading your orders..."):
        orders = get_user_orders(user["id"])

    if not orders:
        st.markdown("""
        <div class="empty-wrap">
            <span class="empty-icon">📦</span>
            <div class="empty-title">No orders yet</div>
            <p class="empty-desc">Your purchase history will appear here after your first order</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Start Shopping →", type="primary"):
            navigate("shop")
        return

    st.markdown(f'<p class="sec-sub">You have placed <strong style="color:#16a34a;">{len(orders)}</strong> order{"s" if len(orders) != 1 else ""} total</p>', unsafe_allow_html=True)

    for order in orders:
        item_preview = ", ".join([i["name"] for i in order["items"][:2]])
        if len(order["items"]) > 2:
            item_preview += f" +{len(order['items'])-2} more"

        with st.expander(f"Order #{order['id']}  ·  {order['created_at'][:10]}  ·  {len(order['items'])} item(s)  ·  ${order['total_price']:.2f}", expanded=False):
            # Status row
            status_html = f"""<div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:12px;margin-bottom:20px;">
<div>
<div style="font-size:13px;font-weight:600;color:#94a3b8;margin-bottom:4px;">ORDER #{order['id']}</div>
<div style="font-size:14px;color:#475569;">Placed {order['created_at'][:16].replace('T', ' ')}</div>
</div>
<div style="text-align:right;">
<span class="badge badge-green" style="font-size:12px;">{order['status']}</span>
<div style="font-size:12px;color:#94a3b8;margin-top:4px;">Est. 45–60 min delivery</div>
</div>
</div>"""
            st.markdown(status_html, unsafe_allow_html=True)

            # Delivery address
            if order.get("delivery_address"):
                address_html = f"""<div style="background:rgba(22,163,74,0.05);border:1px solid rgba(22,163,74,0.1);border-radius:12px;padding:12px 16px;margin-bottom:20px;">
<div style="font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:0.8px;color:#94a3b8;margin-bottom:4px;">Delivery Address</div>
<div style="font-size:14px;color:#475569;">{order['delivery_address']}</div>
</div>"""
                st.markdown(address_html, unsafe_allow_html=True)

            # Items
            st.markdown('<div style="font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:0.8px;color:#94a3b8;margin-bottom:12px;">Items Ordered</div>', unsafe_allow_html=True)

            for item in order["items"]:
                line = item["price"] * item["quantity"]
                item_html = f"""<div style="display:flex;justify-content:space-between;align-items:center;padding:10px 0;border-bottom:1px solid rgba(0,0,0,0.05);">
<div>
<span style="font-size:14px;font-weight:600;color:#0f172a;">{item['name']}</span>
<span style="font-size:12px;color:#94a3b8;margin-left:8px;">× {item['quantity']}</span>
</div>
<span style="font-size:14px;font-weight:700;color:#0f172a;">${line:.2f}</span>
</div>"""
                st.markdown(item_html, unsafe_allow_html=True)

            total_html = f"""<div style="display:flex;justify-content:space-between;align-items:center;margin-top:16px;padding-top:14px;border-top:2px solid rgba(22,163,74,0.15);">
<span style="font-size:16px;font-weight:800;color:#0f172a;">Order Total</span>
<span style="font-size:24px;font-weight:900;color:#16a34a;">${order['total_price']:.2f}</span>
</div>"""
            st.markdown(total_html, unsafe_allow_html=True)
