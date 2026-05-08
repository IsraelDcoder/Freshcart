import streamlit as st
from utils.db import create_order
from utils.auth import validate_phone, validate_address
from utils.helpers import cart_total, cart_count, render_back_button


def show(navigate):
    render_back_button(navigate, "home")
    cart = st.session_state.get("cart", [])
    summary = st.session_state.get("checkout_summary", {})

    if not cart:
        st.info("Your cart is empty. Add some items first!")
        if st.button("Go to Shop"):
            navigate("shop")
        return

    st.markdown('<p class="section-title">💳 Checkout</p>', unsafe_allow_html=True)
    st.markdown('<p class="section-sub">Almost there — just a few more details</p>', unsafe_allow_html=True)

    col_form, col_order = st.columns([3, 2])

    with col_form:
        st.markdown("""
        <div class="glass-card">
            <p style="font-size:16px;font-weight:700;color:#1a1a2e;margin:0 0 20px;">🏠 Delivery Details</p>
        </div>
        """, unsafe_allow_html=True)

        with st.form("checkout_form"):
            st.markdown('<p style="font-size:13px;font-weight:600;color:#555;margin:0 0 8px;">DELIVERY ADDRESS</p>', unsafe_allow_html=True)
            address = st.text_area("Address", placeholder="123 Main Street, Apt 4B\nSan Francisco, CA 94103", height=100, label_visibility="collapsed")

            st.markdown('<p style="font-size:13px;font-weight:600;color:#555;margin:12px 0 8px;">PHONE NUMBER</p>', unsafe_allow_html=True)
            phone = st.text_input("Phone", placeholder="+1 (555) 000-0000", label_visibility="collapsed")

            st.markdown('<p style="font-size:13px;font-weight:600;color:#555;margin:12px 0 8px;">DELIVERY INSTRUCTIONS (optional)</p>', unsafe_allow_html=True)
            notes = st.text_area("Notes", placeholder="Leave at door, ring bell, etc.", height=80, label_visibility="collapsed")

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("""
            <div style="background:rgba(46,125,50,0.06);border-radius:12px;padding:14px 16px;margin-bottom:16px;">
                <div style="font-size:13px;font-weight:600;color:#2E7D32;margin-bottom:6px;">🔒 Secure Checkout</div>
                <div style="font-size:12px;color:#666;">Your payment information is encrypted and never stored on our servers.</div>
            </div>
            """, unsafe_allow_html=True)

            place_order = st.form_submit_button("Place Order →", use_container_width=True, type="primary")

        if place_order:
            # Validate inputs
            addr_valid, addr_msg = validate_address(address)
            phone_valid, phone_msg = validate_phone(phone)

            errors = []
            if not addr_valid:
                errors.append(addr_msg)
            if not phone_valid:
                errors.append(phone_msg)

            if errors:
                for err in errors:
                    st.error(err)
            else:
                user = st.session_state.get("user")
                grand_total = summary.get("grand_total", cart_total(cart))

                try:
                    with st.spinner("Placing your order..."):
                        order_id = create_order(
                            user_id=user["id"],
                            cart=cart,
                            total_price=grand_total,
                            delivery_address=address.strip(),
                            phone=phone.strip()
                        )

                    st.session_state.cart = []
                    st.session_state.last_order_id = order_id
                    st.success("Order placed successfully! 🎉")
                    navigate("order_success")
                except Exception as e:
                    st.error(f"Failed to place order: {str(e)}")
                    st.info("Please try again or contact support if the problem persists.")

    with col_order:
        grand_total = summary.get("grand_total", cart_total(cart))
        delivery_fee = summary.get("delivery_fee", 3.99)
        tax = summary.get("tax", cart_total(cart) * 0.08)

        summary_header_html = """<div class="glass-card">
<p style="font-size:16px;font-weight:700;color:#1a1a2e;margin:0 0 16px;">Order Summary</p>"""
        st.markdown(summary_header_html, unsafe_allow_html=True)

        for item in cart:
            item_html = f"""<div style="display:flex;justify-content:space-between;align-items:center;padding:8px 0;border-bottom:1px solid rgba(0,0,0,0.05);">
<div>
<div style="font-size:14px;font-weight:500;color:#1a1a2e;">{item['name']}</div>
<div style="font-size:12px;color:#888;">×{item['quantity']}</div>
</div>
<div style="font-size:14px;font-weight:600;color:#1a1a2e;">${item['price'] * item['quantity']:.2f}</div>
</div>"""
            st.markdown(item_html, unsafe_allow_html=True)

        summary_html = f"""<div style="margin-top:16px;">
<div style="display:flex;justify-content:space-between;margin-bottom:8px;">
<span style="color:#666;font-size:13px;">Subtotal</span>
<span style="font-size:13px;font-weight:600;">${summary.get('subtotal', cart_total(cart)):.2f}</span>
</div>
<div style="display:flex;justify-content:space-between;margin-bottom:8px;">
<span style="color:#666;font-size:13px;">Delivery</span>
<span style="font-size:13px;font-weight:600;color:{'#2E7D32' if delivery_fee == 0 else '#1a1a2e'};">{'FREE' if delivery_fee == 0 else f'${delivery_fee:.2f}'}</span>
</div>
<div style="display:flex;justify-content:space-between;margin-bottom:16px;">
<span style="color:#666;font-size:13px;">Tax</span>
<span style="font-size:13px;font-weight:600;">${tax:.2f}</span>
</div>
<hr style="border-top:1px solid rgba(0,0,0,0.08);">
<div style="display:flex;justify-content:space-between;margin-top:12px;">
<span style="font-size:17px;font-weight:700;color:#1a1a2e;">Total</span>
<span style="font-size:22px;font-weight:800;color:#2E7D32;">${grand_total:.2f}</span>
</div>
</div>
</div>"""
        st.markdown(summary_html, unsafe_allow_html=True)

        st.markdown("""
        <div style="background:rgba(46,125,50,0.06);border-radius:14px;padding:16px 18px;margin-top:16px;">
            <div style="font-size:14px;font-weight:600;color:#1a1a2e;margin-bottom:8px;">🚚 Delivery estimate</div>
            <div style="font-size:13px;color:#555;">Today, within 45–60 minutes of order confirmation</div>
        </div>
        """, unsafe_allow_html=True)

    if st.button("← Back to Cart"):
        navigate("cart")
