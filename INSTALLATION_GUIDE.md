# FreshCart - Installation Guide

## System Requirements

| Requirement | Minimum | Recommended |
|------------|---------|-------------|
| Python | 3.8 | 3.10+ |
| RAM | 512 MB | 2+ GB |
| Storage | 100 MB | 500 MB |
| OS | Windows/macOS/Linux | Any modern OS |
| Browser | Any modern browser | Chrome, Firefox, Safari, Edge |
| Internet | Not required | Recommended (for product images) |

---

## Prerequisites

### 1. Install Python

**Windows:**
- Download Python from https://www.python.org/downloads/
- Choose Python 3.8 or higher
- ✅ Check "Add Python to PATH" during installation
- Click Install

**macOS:**
```bash
# Using Homebrew
brew install python3
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install python3 python3-pip
```

### 2. Verify Python Installation

Open terminal/command prompt and run:
```bash
python --version
```

You should see: `Python 3.x.x`

---

## Installation Steps

### Step 1: Download the Project

**Option A: From GitHub**
```bash
git clone https://github.com/IsraelDcoder/Freshcart.git
cd Freshcart
```

**Option B: Download ZIP**
1. Go to https://github.com/IsraelDcoder/Freshcart
2. Click "Code" → "Download ZIP"
3. Extract the ZIP file
4. Open terminal in the extracted folder

### Step 2: Run the Application

Navigate to the project folder and run:

```bash
python run.py
```

**That's it!** The script will automatically:
- ✅ Check Python version
- ✅ Install Streamlit (if needed)
- ✅ Initialize the database
- ✅ Start the application

### Step 3: Access the Application

Once you see:
```
📱 Access the app at: http://localhost:5000
```

Open your browser and visit:
```
http://localhost:5000
```

---

## Troubleshooting

### Issue: "Python not found" or "python: command not found"

**Solution:**
- Python might not be in PATH
- Try: `python3 run.py` instead of `python run.py`
- Or reinstall Python and check "Add to PATH"

### Issue: "Permission denied" on macOS/Linux

**Solution:**
```bash
chmod +x run.py
python run.py
```

### Issue: Port 5000 already in use

**Solution:**
Edit `run.py` and change port number:
```python
# Change this line:
["python", "-m", "streamlit", "run", "app.py", "--server.port=5000"]
# To:
["python", "-m", "streamlit", "run", "app.py", "--server.port=5001"]
```

### Issue: "Module not found" errors

**Solution:**
```bash
pip install -r requirements.txt
```

(Or) Manually install Streamlit:
```bash
pip install streamlit
```

### Issue: Database errors

**Solution:**
Delete the database file and restart:
```bash
rm freshcart.db
python run.py
```

---

## Manual Setup (Alternative)

If `run.py` doesn't work, follow these steps:

### 1. Install Streamlit
```bash
pip install streamlit
```

### 2. Run the Application
```bash
streamlit run app.py --server.port 5000
```

### 3. Open Browser
```
http://localhost:5000
```

---

## Manual Database Setup

The database initializes automatically, but to manually reset it:

```bash
python -c "from utils.db import init_db; init_db()"
```

---

## Test Credentials

Use these test accounts after initial setup:

| Email | Password | Role |
|-------|----------|------|
| test@example.com | password123 | User |

Or create your own account by clicking "Sign Up"

---

## Creating Test Data

The application automatically seeds with 24 products across these categories:
- 🍎 Fruits
- 🥛 Dairy
- 🍞 Bakery
- 🌾 Grains
- 🥩 Meat
- 🥤 Beverages
- 🥬 Vegetables
- 🍫 Snacks
- 🫒 Pantry

---

## Features to Test

### 1. Authentication
- Sign up new account
- Login
- Logout

### 2. Shopping
- Browse products
- Search by name
- Filter by category
- Sort by price

### 3. Cart Management
- Add items
- Change quantities
- Remove items
- View total

### 4. Checkout
- Enter delivery address
- Enter phone number
- Review order
- Complete order

### 5. Order History
- View past orders
- Check order details

### 6. Profile
- View user information
- See account stats

---

## File Locations

```
project_folder/
├── app.py                 # Main application
├── run.py                 # Startup script ← RUN THIS
├── freshcart.db          # Database (auto-created)
├── utils/
│   ├── db.py             # Database functions
│   ├── auth.py           # Authentication
│   └── helpers.py        # UI helpers
└── views/
    ├── landing.py        # Home page
    ├── login.py          # Login page
    ├── signup.py         # Registration
    ├── home.py           # Dashboard
    ├── shop.py           # Products
    ├── cart.py           # Shopping cart
    ├── checkout.py       # Checkout
    ├── orders.py         # Order history
    ├── profile.py        # User profile
    └── order_success.py  # Confirmation
```

---

## Stopping the Application

Press `Ctrl+C` in the terminal to stop the server.

```
Press Ctrl+C to stop the server
👋 FreshCart app stopped. See you soon!
```

---

## Advanced Configuration

### Change Server Port
Edit `run.py` line with:
```python
"--server.port=YOUR_PORT_NUMBER"
```

### Enable Debug Mode
```bash
streamlit run app.py --logger.level=debug
```

### Run with Custom Settings
Edit `.streamlit/config.toml` for Streamlit configuration.

---

## Performance Tips

1. **First run may take longer** - Streamlit caches on subsequent runs
2. **Use modern browser** - Chrome recommended
3. **Disable extensions** - Some browser extensions may interfere
4. **Check internet** - Images load from Unsplash (optional)

---

## Getting Help

If issues persist:
1. Check Python version: `python --version`
2. Verify file location: `ls` or `dir`
3. Check Streamlit installation: `pip list | grep streamlit`
4. Review error message in terminal
5. Try manual setup steps above

---

## Next Steps

1. ✅ Install and run the application
2. ✅ Create an account
3. ✅ Browse products
4. ✅ Make test purchase
5. ✅ Review order history

**Enjoy FreshCart! 🛒**
