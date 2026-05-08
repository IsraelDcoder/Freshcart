import streamlit as st
from utils.helpers import cart_total, cart_count, render_back_button


def show(navigate):
    render_back_button(navigate, "home")
    cart = st.session_state.get("cart", [])

    st.markdown('<p class="sec-label">Review</p>', unsafe_allow_html=True)
    st.markdown('<p class="sec-title">🛒 Your Cart</p>', unsafe_allow_html=True)

    if not cart:
        st.markdown("""
        <div class="empty-wrap">
            <span class="empty-icon">🛒</span>
            <div class="empty-title">Your cart is empty</div>
            <p class="empty-desc">Add some fresh products from our shop to get started</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🛍️  Browse Products", type="primary"):
            navigate("shop")
        return

    st.markdown(f'<p class="sec-sub">{cart_count(cart)} item{"s" if cart_count(cart) != 1 else ""} ready for checkout</p>', unsafe_allow_html=True)

    col_items, col_summary = st.columns([3, 2], gap="large")

    with col_items:
        st.markdown('<p style="font-size:16px;font-weight:800;color:#0f172a;margin-bottom:16px;">Order Items</p>', unsafe_allow_html=True)

        to_remove = []
        for idx, item in enumerate(cart):
            cart_item_html = f"""<div class="cart-item">
<div style="display:flex;align-items:center;gap:16px;flex-wrap:wrap;">
<div style="position:relative;flex-shrink:0;">
<img src="{item['image_url']}" style="width:72px;height:72px;object-fit:cover;border-radius:14px;display:block;" />
</div>
<div style="flex:1;min-width:100px;">
<div style="font-size:15px;font-weight:700;color:#0f172a;">{item['name']}</div>
<div style="font-size:13px;color:#94a3b8;margin-top:2px;">${item['price']:.2f} per unit</div>
</div>
</div>
</div>"""
            st.markdown(cart_item_html, unsafe_allow_html=True)

            qcol, subtotal_col, del_col = st.columns([2, 2, 1])
            with qcol:
                new_qty = st.number_input(
                    "Quantity", min_value=1, max_value=50,
                    value=item["quantity"], key=f"cart_qty_{idx}",
                    label_visibility="visible"
                )
                if new_qty != item["quantity"]:
                    if new_qty <= 0:
                        st.error("Quantity must be at least 1.")
                    else:
                        item["quantity"] = new_qty
                        st.session_state.cart = cart
                        st.rerun()

            with subtotal_col:
                subtotal_html = f"""<div style="padding-top:28px;">
<div style="font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:0.8px;color:#94a3b8;margin-bottom:3px;">Subtotal</div>
<div style="font-size:20px;font-weight:900;color:#16a34a;">${item['price'] * item['quantity']:.2f}</div>
</div>"""
                st.markdown(subtotal_html, unsafe_allow_html=True)

            with del_col:
                st.markdown("<div style='padding-top:22px;'>", unsafe_allow_html=True)
                if st.button("🗑️", key=f"del_{idx}", help=f"Remove {item['name']}"):
                    to_remove.append(idx)
                st.markdown("</div>", unsafe_allow_html=True)

        if to_remove:
            st.session_state.cart = [item for i, item in enumerate(cart) if i not in to_remove]
            st.rerun()

    with col_summary:
        total = cart_total(cart)
        delivery_fee = 0.0 if total >= 50 else 3.99
        tax = total * 0.08
        grand_total = total + delivery_fee + tax

        free_del = delivery_fee == 0
        del_msg = (
            '<div style="background:#dcfce7;border-radius:10px;padding:10px 14px;margin-bottom:16px;font-size:12px;color:#15803d;font-weight:600;">🎉 You qualify for free delivery!</div>'
            if free_del else
            f'<div style="background:#fff7ed;border-radius:10px;padding:10px 14px;margin-bottom:16px;font-size:12px;color:#c2410c;font-weight:600;">Add ${50 - total:.2f} more for free delivery</div>'
        )

        summary_html = f"""<div class="glass" style="position:sticky;top:24px;padding:28px;">
<p style="font-size:17px;font-weight:800;color:#0f172a;margin:0 0 20px;">Order Summary</p>
<div style="display:flex;justify-content:space-between;margin-bottom:10px;">
<span style="font-size:14px;color:#64748b;">Subtotal ({cart_count(cart)} items)</span>
<span style="font-weight:700;font-size:14px;color:#0f172a;">${total:.2f}</span>
</div>
<div style="display:flex;justify-content:space-between;margin-bottom:10px;">
<span style="font-size:14px;color:#64748b;">Delivery fee</span>
<span style="font-weight:700;font-size:14px;color:{'#16a34a' if free_del else '#0f172a'};">{'FREE' if free_del else f'${delivery_fee:.2f}'}</span>
</div>
<div style="display:flex;justify-content:space-between;margin-bottom:16px;">
<span style="font-size:14px;color:#64748b;">Tax (8%)</span>
<span style="font-weight:700;font-size:14px;color:#0f172a;">${tax:.2f}</span>
</div>
{del_msg}
<hr>
<div style="display:flex;justify-content:space-between;margin-bottom:24px;">
<span style="font-size:18px;font-weight:800;color:#0f172a;">Total</span>
<span style="font-size:26px;font-weight:900;color:#16a34a;">${grand_total:.2f}</span>
</div>
<div style="background:rgba(22,163,74,0.05);border-radius:12px;padding:14px 16px;margin-top:4px;">
<div style="font-size:12px;color:#64748b;display:flex;align-items:center;gap:6px;">
🔒 <span>Secure checkout — 256-bit SSL encryption</span>
</div>
</div>
</div>"""
        st.markdown(summary_html, unsafe_allow_html=True)

        if st.button("Proceed to Checkout →", type="primary", use_container_width=True):
            st.session_state.checkout_summary = {
                "subtotal": total,
                "delivery_fee": delivery_fee,
                "tax": tax,
                "grand_total": grand_total
            }
            navigate("checkout")

        st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
        if st.button("Continue Shopping", use_container_width=True):
            navigate("shop")
        if st.button("Clear Cart", use_container_width=True, type="secondary"):
            st.session_state.cart = []
            st.toast("Cart cleared!")
            st.rerun()
