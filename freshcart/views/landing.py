import streamlit as st

# ------------------ SAMPLE DATA ------------------
PRODUCTS = [
    {"name":"Bananas","price":1.49,"img":"https://images.unsplash.com/photo-1571771894821-ce9b6c11b08e?w=300"},
    {"name":"Apples","price":3.99,"img":"https://images.unsplash.com/photo-1568702846914-96b305d2aaeb?w=300"},
    {"name":"Milk","price":1.89,"img":"https://images.unsplash.com/photo-1563636619-e9143da7973b?w=300"},
    {"name":"Bread","price":3.49,"img":"https://images.unsplash.com/photo-1586444248902-2f64eddc13df?w=300"},
    {"name":"Eggs","price":3.79,"img":"https://images.unsplash.com/photo-1582722872445-44dc5f7e3c8f?w=300"},
    {"name":"Juice","price":3.29,"img":"https://images.unsplash.com/photo-1600271886742-f049cd451bba?w=300"},
]

def show(navigate):
    # ------------------ STYLES ------------------
    st.markdown("""
<style>
body {font-family: Inter, sans-serif;}
.header {
    display:flex; justify-content:space-between; align-items:center;
    padding:15px 40px; background:white; border-bottom:1px solid #eee;
}
.logo {font-size:24px; font-weight:900; color:#16a34a;}
.nav {display:flex; gap:20px; color:#555;}
.search {
    flex:1; margin:0 40px; padding:10px; border-radius:25px;
    border:1px solid #ddd;
}
.hero {
    display:flex; align-items:center; justify-content:space-between;
    padding:60px 40px; background:#f0fdf4;
}
.hero h1 {font-size:48px; font-weight:900;}
.hero span {color:#16a34a;}
.hero button {
    margin-top:20px; padding:12px 20px;
    background:#16a34a; color:white; border:none;
    border-radius:8px; font-weight:700;
}
.categories {
    display:flex; gap:15px; padding:20px 40px;
}
.cat {
    padding:15px; background:white; border-radius:10px;
    border:1px solid #eee; text-align:center; flex:1;
}
.products {
    display:grid; grid-template-columns:repeat(4,1fr);
    gap:20px; padding:20px 40px;
}
.card {
    background:white; padding:15px; border-radius:12px;
    border:1px solid #eee; transition:0.2s;
}
.card:hover {transform:translateY(-5px); box-shadow:0 10px 20px rgba(0,0,0,0.1);}
.card img {width:100%; height:140px; object-fit:cover; border-radius:8px;}
.price {font-weight:800; margin-top:5px;}
.btn {
    margin-top:10px; width:100%; padding:8px;
    background:#16a34a; color:white; border:none; border-radius:6px;
}
.footer {
    background:#111827; color:white; padding:40px; text-align:center;
}
</style>
""", unsafe_allow_html=True)

    # ------------------ HEADER ------------------
    st.markdown("""
<div class='header'>
    <div class='logo'>FreshCart</div>
    <input class='search' placeholder='Search for groceries...' />
    <div class='nav'>
        <div>Deals</div>
        <div>Orders</div>
        <div>Cart 🛒</div>
    </div>
</div>
""", unsafe_allow_html=True)

    # ------------------ HERO ------------------
    st.markdown("""
<div class='hero'>
    <div>
        <h1>Fresh groceries.<br><span>Delivered fast.</span></h1>
        <p>Get everything you need in minutes.</p>
        <button>Shop Now</button>
    </div>
    <img src='https://images.unsplash.com/photo-1542838132-92c53300491e?w=600' style='width:400px; border-radius:12px;'>
</div>
""", unsafe_allow_html=True)

    # ------------------ CATEGORIES ------------------
    st.markdown("<div class='categories'>" + "".join([
        f"<div class='cat'>{c}</div>" for c in ["Fruits","Dairy","Snacks","Drinks"]
    ]) + "</div>", unsafe_allow_html=True)

    # ------------------ PRODUCTS ------------------
    products_html = "<div class='products'>"
    for p in PRODUCTS:
        products_html += f"""<div class='card'>
        <img src='{p['img']}' />
        <div>{p['name']}</div>
        <div class='price'>${p['price']}</div>
        <button class='btn'>Add</button>
    </div>"""
    products_html += "</div>"
    st.markdown(products_html, unsafe_allow_html=True)

    # ------------------ FOOTER ------------------
    st.markdown("""
<div class='footer'>
    FreshCart © 2026 - Built like a funded startup 🚀
</div>
""", unsafe_allow_html=True)
