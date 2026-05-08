# 🛒 FreshCart - Premium Grocery Delivery App

A modern, full-featured grocery delivery application built with Streamlit and Python.

## 🚀 Quick Start

### For Everyone (Lecturers, Testers, Users)

**One command to run the entire app:**

```bash
python run.py
```

That's it! The app will:
- ✅ Check Python version
- ✅ Install Streamlit automatically (if needed)
- ✅ Initialize the database
- ✅ Start the server on port 5000

Then open your browser to: **http://localhost:5000**

---

## 📋 System Requirements

- **Python**: 3.8 or higher
- **OS**: Windows, macOS, or Linux
- **Browser**: Chrome, Firefox, Safari, or Edge (any modern browser)
- **Internet**: Not required (runs locally)

---

## 🎯 Features

### 🛍️ Shopping
- Browse 24+ products across 9 categories
- Search products by name
- Filter by category
- Sort by price and name
- Add items to cart with quantity selection

### 🛒 Cart Management
- View cart with product details
- Update quantities
- Remove items
- Calculate totals with tax and delivery fees
- Free delivery on orders over $50

### 💳 Checkout
- Enter delivery address
- Enter phone number
- Add delivery instructions (optional)
- Secure order creation
- Order confirmation with ID

### 📦 Order History
- View all past orders
- See order items and totals
- Check delivery status
- Estimated delivery times

### 👤 User Account
- Create account with email verification
- Update profile information
- Change password
- View member status
- Track spending

---

## 🏪 Test Credentials

You can create your own account, or use this demo:
- **Email**: test@example.com
- **Password**: TestPassword123

(Feel free to create multiple accounts to test the app)

---

## 📁 Project Structure

```
freshcart/
├── app.py                 # Main Streamlit app
├── run.py                 # Entry point (use this to run!)
├── freshcart.db          # SQLite database
├── .streamlit/
│   └── config.toml       # Streamlit configuration
├── utils/
│   ├── db.py             # Database operations
│   ├── auth.py           # Authentication & validation
│   └── helpers.py        # UI components & utilities
└── views/
    ├── landing.py        # Landing page
    ├── login.py          # Login form
    ├── signup.py         # Registration form
    ├── home.py           # Dashboard
    ├── shop.py           # Product browsing
    ├── cart.py           # Shopping cart
    ├── checkout.py       # Order checkout
    ├── orders.py         # Order history
    ├── profile.py        # User profile
    └── order_success.py  # Confirmation page
```

---

## 💻 Installation (If run.py doesn't work)

### Manual Setup

1. **Install Python 3.8+** from [python.org](https://www.python.org/)

2. **Install Streamlit**:
   ```bash
   pip install streamlit
   ```

3. **Run the app**:
   ```bash
   streamlit run app.py --server.port=5000
   ```

4. **Open in browser**: http://localhost:5000

---

## 🔧 Technology Stack

- **Frontend**: Streamlit (Python web framework)
- **Backend**: Python 3.8+
- **Database**: SQLite3
- **Authentication**: SHA256 password hashing with salt
- **Styling**: Custom CSS with glass-morphism design
- **Icons**: Emoji UI elements

---

## 🎨 Design Highlights

- **Modern UI**: Glass-morphism design with gradient backgrounds
- **Green Theme**: Professional grocery store branding (#0aaa54)
- **Responsive**: Works on desktop and tablet
- **Fast**: Instant product updates and navigation
- **Secure**: Encrypted passwords, validated forms

---

## 🧪 Testing Workflow

### Suggested Test Path

1. **Landing Page** → View features and call-to-action
2. **Sign Up** → Create a new account
3. **Home** → View welcome dashboard
4. **Shop** → Browse and search products
5. **Add to Cart** → Add 3-5 items with different quantities
6. **Cart** → Review items, update quantities, remove items
7. **Checkout** → Enter delivery details and place order
8. **Order Success** → View confirmation with order ID
9. **Orders** → See order in order history
10. **Profile** → Update name and password

---

## 🐛 Troubleshooting

### App won't start
```bash
# Make sure you're in the right directory
cd freshcart

# Try running with Python explicitly
python run.py
```

### Streamlit not installed
```bash
# Install it manually
pip install streamlit
```

### Port 5000 already in use
```bash
# Edit run.py and change port number, or use:
streamlit run app.py --server.port=5001
```

### Database errors
- The app creates `freshcart.db` automatically
- If corrupted, delete it and restart - it will regenerate

---

## 📊 Database

The app uses **SQLite3** (built-in with Python):

**Tables:**
- `users` - User accounts with password hashes
- `products` - 24 grocery products with images
- `orders` - Order history per user
- `order_items` - Items in each order

**Sample Products:**
- Fruits: Bananas, Apples, Strawberries, Avocados
- Dairy: Milk, Yogurt, Cheese, Eggs
- Vegetables: Broccoli, Tomatoes, Spinach
- Meat: Chicken, Salmon
- And more...

---

## 🔒 Security

- Passwords hashed with SHA256 + salt
- Email validation on signup
- Form validation on all inputs
- Address and phone number validation
- SQL injection protection via parameterized queries
- Session-based authentication

---

## 📈 Future Enhancements

- Payment gateway integration
- Real-time order tracking
- Customer reviews and ratings
- Wishlist/favorites
- Promo codes
- Admin dashboard
- Mobile app
- SMS notifications
- Analytics

---

## 📝 Notes for Lecturer

This app demonstrates:
- ✅ Full-stack web development with Python
- ✅ Database design and SQL operations
- ✅ User authentication and security
- ✅ Form validation and error handling
- ✅ Modern UI/UX with Streamlit
- ✅ Session state management
- ✅ Professional code organization

**Easy to test**: Just run `python run.py` - everything is pre-configured!

---

## 🎓 Learning Outcomes

This project covers:
1. Web application architecture
2. Database design (SQLite)
3. Authentication & security
4. Form validation
5. Error handling
6. UI/UX design
7. Session management
8. Python best practices

---

## 📞 Support

If anything doesn't work:
1. Make sure Python 3.8+ is installed
2. Run `python run.py` from the `freshcart` directory
3. Check that port 5000 is available
4. Delete `freshcart.db` if you get database errors
5. Clear browser cache if UI looks broken

---

## ✨ Happy Shopping!

Enjoy testing FreshCart! 🛒

NAME: ISRAEL ONYEKACHI THOMPSON
MAT NO: FPS/CSC/24/86060
STUDENT ID: E1153191
COURSE: CSC 206
