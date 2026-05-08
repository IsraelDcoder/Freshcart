# FreshCart - Project Report

## Executive Summary

**FreshCart** is a modern, full-featured grocery delivery application that enables users to browse products, manage shopping carts, place orders, and track their delivery history. The system is built with Python and Streamlit, providing a responsive, user-friendly interface for online grocery shopping.

---

## 1. Problem Statement & Objectives

### Problem
- Traditional grocery shopping requires physical store visits, consuming time and effort
- Users need a convenient way to browse, compare, and purchase groceries online
- There's a need for an integrated platform combining product browsing, cart management, and order tracking

### Objectives
1. **Product Browsing**: Enable users to browse 24+ grocery products across multiple categories
2. **Cart Management**: Provide intuitive cart functionality with quantity management
3. **Order Processing**: Implement a seamless checkout experience with delivery options
4. **User Management**: Support user authentication, registration, and profile management
5. **Order History**: Allow users to view and track their past orders
6. **User-Friendly Interface**: Create a modern, responsive UI suitable for all user types

---

## 2. Tools & Technologies

### Frontend
- **Streamlit**: Web application framework for rapid UI development
- **CSS Styling**: Custom CSS for enhanced visual design and branding
- **Session Management**: Streamlit session state for state persistence

### Backend
- **Python 3.8+**: Core programming language
- **SQLite3**: Lightweight relational database
- **Password Hashing**: bcrypt library for secure password storage

### Database
- **SQLite**: Built-in database with no external dependencies
- **4 Main Tables**: Users, Products, Orders, Order Items

### Development & Deployment
- **Git**: Version control
- **GitHub**: Remote repository hosting

---

## 3. Design & Architecture

### Application Structure

```
freshcart/
├── app.py                 # Main Streamlit application
├── run.py                 # Startup script with environment setup
├── utils/
│   ├── __init__.py
│   ├── db.py              # Database initialization and queries
│   ├── auth.py            # User authentication logic
│   └── helpers.py         # CSS styling and UI utilities
└── views/
    ├── landing.py         # Landing page
    ├── login.py           # Login form
    ├── signup.py          # Registration form
    ├── home.py            # Dashboard (protected)
    ├── shop.py            # Product browsing
    ├── cart.py            # Cart management
    ├── checkout.py        # Order checkout
    ├── order_success.py   # Order confirmation
    ├── orders.py          # Order history
    └── profile.py         # User profile
```

### Database Schema

#### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

#### Products Table
```sql
CREATE TABLE products (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    price REAL NOT NULL,
    category TEXT NOT NULL,
    image_url TEXT NOT NULL
)
```

#### Orders Table
```sql
CREATE TABLE orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    total_price REAL NOT NULL,
    delivery_address TEXT,
    phone TEXT,
    status TEXT DEFAULT 'Confirmed',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
)
```

#### Order Items Table
```sql
CREATE TABLE order_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    price REAL NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
)
```

### Key Features

#### 1. Authentication System
- User registration with email validation
- Secure password hashing using bcrypt
- Session-based authentication
- Protected pages requiring login

#### 2. Product Catalog
- 24 pre-loaded products across 9 categories
- Product images from Unsplash API
- Category filtering and search functionality
- Price sorting

#### 3. Shopping Cart
- Add/remove products dynamically
- Quantity management
- Real-time price calculation
- Tax calculation (10%)
- Free delivery on orders > $50

#### 4. Checkout Process
- Delivery address collection
- Phone number validation
- Order summary with itemized breakdown
- Order confirmation

#### 5. Order History
- View past orders with details
- Order status tracking
- Order timestamps

#### 6. User Profile
- View profile information
- Display user statistics
- Account management

---

## 4. Implementation Details

### Core Modules

#### utils/db.py
- Database initialization and schema creation
- Product seeding with 24 items
- CRUD operations for products, users, and orders
- Connection management

#### utils/auth.py
- User registration and password hashing
- Login verification
- Email validation
- Secure authentication

#### utils/helpers.py
- Custom CSS injection for styling
- UI component rendering
- Sidebar navigation
- Footer rendering

#### views/* (Page modules)
Each view module implements a specific page:
- Landing page for new users
- Login/Signup authentication pages
- Protected pages (Home, Shop, Cart, Checkout, Orders, Profile)
- Order confirmation page

### Session State Management
The application uses Streamlit's `st.session_state` for:
- Current user information
- Shopping cart contents
- Page navigation
- Checkout summary
- Last order ID

---

## 5. Testing & Validation

### User Testing Scenarios

#### Scenario 1: New User Registration
1. Click "Sign Up" button
2. Enter name, email, and password
3. Submit registration form
4. Verify account creation

#### Scenario 2: Product Browsing
1. Login with valid credentials
2. Navigate to Shop
3. Test category filtering
4. Test product search
5. Test price sorting

#### Scenario 3: Cart Operations
1. Add multiple products with varying quantities
2. Update product quantities
3. Remove items from cart
4. Verify total calculations

#### Scenario 4: Checkout Process
1. Click "Proceed to Checkout"
2. Enter delivery address and phone
3. Review order summary
4. Submit order
5. Verify order confirmation

#### Scenario 5: Order History
1. Navigate to Orders page
2. View all past orders
3. Verify order details and timestamps

### Testing Checklist
- ✅ User registration and login functionality
- ✅ Product display and search
- ✅ Cart add/remove/update operations
- ✅ Price calculations (tax, delivery fees)
- ✅ Checkout process
- ✅ Order persistence in database
- ✅ Order history retrieval
- ✅ Session management and page protection
- ✅ Responsive UI across browsers

---

## 6. Key Achievements

1. **Complete E-commerce System**: Full-featured grocery shopping platform
2. **Secure Authentication**: Password hashing and session management
3. **Responsive Design**: Works seamlessly across devices and browsers
4. **Database Persistence**: All data stored securely in SQLite
5. **Intuitive UX**: Clean, modern interface with easy navigation
6. **Production Ready**: Easy single-command startup
7. **Scalability**: Modular architecture for future enhancements

---

## 7. Future Enhancements

1. **Payment Integration**: Add Stripe/PayPal for real payments
2. **Delivery Tracking**: Real-time order tracking with GPS
3. **Reviews & Ratings**: Product reviews from customers
4. **Recommendations**: ML-based product recommendations
5. **Admin Dashboard**: Inventory and order management
6. **Notifications**: Email/SMS order updates
7. **Multi-language Support**: Support multiple languages
8. **Mobile App**: Native iOS/Android applications
9. **Analytics**: User behavior and sales analytics
10. **Advanced Filtering**: Price range, brand, organic filters

---

## 8. Conclusion

FreshCart successfully demonstrates a complete e-commerce web application with modern web technologies. The project showcases:
- Full-stack development capabilities
- Database design and management
- User authentication and security
- Responsive UI/UX design
- Clean, maintainable code architecture

The application is production-ready, thoroughly tested, and provides a solid foundation for a real-world grocery delivery service.

---

## Installation & Running

See `INSTALLATION_GUIDE.md` for detailed setup instructions.

---

## Files Included

- `app.py` - Main Streamlit application
- `run.py` - Startup script
- `utils/` - Utility modules (auth, database, helpers)
- `views/` - Page components
- `freshcart.db` - SQLite database
- `README.md` - Quick start guide
- `PROJECT_REPORT.md` - This file
- `INSTALLATION_GUIDE.md` - Detailed setup instructions
- `DATABASE_SCHEMA.md` - Database documentation
