import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "freshcart.db")

PRODUCTS = [
    (1, "Organic Bananas", 1.49, "Fruits", "https://images.unsplash.com/photo-1571771894821-ce9b6c11b08e?w=400&auto=format&fit=crop"),
    (2, "Red Apples (6 pack)", 3.99, "Fruits", "https://images.unsplash.com/photo-1568702846914-96b305d2aaeb?w=400&auto=format&fit=crop"),
    (3, "Strawberries 500g", 4.49, "Fruits", "https://images.unsplash.com/photo-1464965911861-746a04b4bca6?w=400&auto=format&fit=crop"),
    (4, "Avocados (3 pack)", 5.29, "Fruits", "https://images.unsplash.com/photo-1523049673857-eb18f1d7b578?w=400&auto=format&fit=crop"),
    (5, "Whole Milk 1L", 1.89, "Dairy", "https://images.unsplash.com/photo-1563636619-e9143da7973b?w=400&auto=format&fit=crop"),
    (6, "Greek Yogurt 500g", 3.29, "Dairy", "https://images.unsplash.com/photo-1488477181946-6428a0291777?w=400&auto=format&fit=crop"),
    (7, "Cheddar Cheese 200g", 4.99, "Dairy", "https://images.unsplash.com/photo-1486297678162-eb2a19b0a32d?w=400&auto=format&fit=crop"),
    (8, "Free Range Eggs (12)", 3.79, "Dairy", "https://images.unsplash.com/photo-1582722872445-44dc5f7e3c8f?w=400&auto=format&fit=crop"),
    (9, "Sourdough Bread", 3.49, "Bakery", "https://images.unsplash.com/photo-1586444248902-2f64eddc13df?w=400&auto=format&fit=crop"),
    (10, "Whole Wheat Pasta 500g", 2.19, "Grains", "https://images.unsplash.com/photo-1612927601601-6638404737ce?w=400&auto=format&fit=crop"),
    (11, "Basmati Rice 1kg", 3.99, "Grains", "https://images.unsplash.com/photo-1536304929831-ee1ca9d44906?w=400&auto=format&fit=crop"),
    (12, "Rolled Oats 1kg", 3.29, "Grains", "https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=400&auto=format&fit=crop"),
    (13, "Chicken Breast 500g", 6.99, "Meat", "https://images.unsplash.com/photo-1604503468506-a8da13d82791?w=400&auto=format&fit=crop"),
    (14, "Salmon Fillet 300g", 8.99, "Meat", "https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?w=400&auto=format&fit=crop"),
    (15, "Sparkling Water 6x500ml", 4.49, "Beverages", "https://images.unsplash.com/photo-1523362628745-0c100150b504?w=400&auto=format&fit=crop"),
    (16, "Orange Juice 1L", 3.29, "Beverages", "https://images.unsplash.com/photo-1600271886742-f049cd451bba?w=400&auto=format&fit=crop"),
    (17, "Green Tea (20 bags)", 2.99, "Beverages", "https://images.unsplash.com/photo-1556679343-c7306c1976bc?w=400&auto=format&fit=crop"),
    (18, "Broccoli 400g", 2.49, "Vegetables", "https://images.unsplash.com/photo-1459411621453-7b03977f4bfc?w=400&auto=format&fit=crop"),
    (19, "Cherry Tomatoes 250g", 2.79, "Vegetables", "https://images.unsplash.com/photo-1561136594-7f68413baa99?w=400&auto=format&fit=crop"),
    (20, "Baby Spinach 150g", 2.29, "Vegetables", "https://images.unsplash.com/photo-1576045057995-568f588f82fb?w=400&auto=format&fit=crop"),
    (21, "Dark Chocolate 85%", 3.49, "Snacks", "https://images.unsplash.com/photo-1481391319762-47dff72954d9?w=400&auto=format&fit=crop"),
    (22, "Mixed Nuts 200g", 5.99, "Snacks", "https://images.unsplash.com/photo-1599599810694-b5b37304c041?w=400&auto=format&fit=crop"),
    (23, "Olive Oil Extra Virgin 500ml", 7.99, "Pantry", "https://images.unsplash.com/photo-1474979266404-7eaacbcd87c5?w=400&auto=format&fit=crop"),
    (24, "Honey Raw 350g", 6.49, "Pantry", "https://images.unsplash.com/photo-1587049352846-4a222e784d38?w=400&auto=format&fit=crop"),
]


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            category TEXT NOT NULL,
            image_url TEXT NOT NULL
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            total_price REAL NOT NULL,
            delivery_address TEXT,
            phone TEXT,
            status TEXT DEFAULT 'Confirmed',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders(id),
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
    """)

    c.execute("SELECT COUNT(*) FROM products")
    if c.fetchone()[0] == 0:
        c.executemany(
            "INSERT OR IGNORE INTO products (id, name, price, category, image_url) VALUES (?, ?, ?, ?, ?)",
            PRODUCTS
        )

    conn.commit()
    conn.close()


def get_all_products():
    conn = get_connection()
    products = conn.execute("SELECT * FROM products ORDER BY category, name").fetchall()
    conn.close()
    return [dict(p) for p in products]


def get_product_by_id(product_id):
    conn = get_connection()
    product = conn.execute("SELECT * FROM products WHERE id = ?", (product_id,)).fetchone()
    conn.close()
    return dict(product) if product else None


def create_user(name, email, password_hash):
    conn = get_connection()
    try:
        conn.execute(
            "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
            (name, email, password_hash)
        )
        conn.commit()
        return True, "Account created successfully!"
    except sqlite3.IntegrityError:
        return False, "An account with this email already exists."
    finally:
        conn.close()


def get_user_by_email(email):
    conn = get_connection()
    user = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
    conn.close()
    return dict(user) if user else None


def get_user_by_id(user_id):
    conn = get_connection()
    user = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    conn.close()
    return dict(user) if user else None


def update_user(user_id, name, password_hash=None):
    conn = get_connection()
    if password_hash:
        conn.execute(
            "UPDATE users SET name = ?, password_hash = ? WHERE id = ?",
            (name, password_hash, user_id)
        )
    else:
        conn.execute("UPDATE users SET name = ? WHERE id = ?", (name, user_id))
    conn.commit()
    conn.close()


def create_order(user_id, cart, total_price, delivery_address, phone):
    """Create an order and its associated items. Returns order_id or raises exception."""
    if not cart:
        raise ValueError("Cannot create order with empty cart.")
    if total_price <= 0:
        raise ValueError("Order total must be positive.")
    if not delivery_address or not delivery_address.strip():
        raise ValueError("Delivery address is required.")
    if not phone or not phone.strip():
        raise ValueError("Phone number is required.")

    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO orders (user_id, total_price, delivery_address, phone) VALUES (?, ?, ?, ?)",
            (user_id, total_price, delivery_address, phone)
        )
        order_id = cursor.lastrowid
        
        for item in cart:
            if "id" not in item or "quantity" not in item or "price" not in item:
                raise ValueError(f"Invalid cart item structure: {item}")
            cursor.execute(
                "INSERT INTO order_items (order_id, product_id, quantity, price) VALUES (?, ?, ?, ?)",
                (order_id, item["id"], item["quantity"], item["price"])
            )
        
        conn.commit()
        return order_id
    except sqlite3.Error as e:
        conn.rollback()
        raise Exception(f"Database error creating order: {str(e)}")
    finally:
        conn.close()


def get_user_orders(user_id):
    """Fetch all orders for a user with their items."""
    try:
        conn = get_connection()
        orders = conn.execute(
            "SELECT * FROM orders WHERE user_id = ? ORDER BY created_at DESC",
            (user_id,)
        ).fetchall()
        result = []
        for order in orders:
            order_dict = dict(order)
            items = conn.execute(
                """
                SELECT oi.product_id as id, oi.quantity, oi.price, p.name
                FROM order_items oi
                JOIN products p ON p.id = oi.product_id
                WHERE oi.order_id = ?
                """,
                (order["id"],)
            ).fetchall()
            order_dict["items"] = [dict(i) for i in items]
            result.append(order_dict)
        conn.close()
        return result
    except sqlite3.Error as e:
        raise Exception(f"Failed to fetch orders: {str(e)}")
