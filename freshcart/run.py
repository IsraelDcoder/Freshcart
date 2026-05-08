#!/usr/bin/env python3
"""
FreshCart - Premium Grocery Delivery App
Run this file to start the application!

Usage:
    python run.py
    
Then open your browser to: http://localhost:5000

Requirements:
- Python 3.8+
- Streamlit (auto-installed)
- SQLite3 (built-in with Python)
"""

import subprocess
import sys
import os
from pathlib import Path


def print_header():
    """Display a friendly welcome message."""
    print("\n" + "=" * 60)
    print("🛒 FreshCart - Premium Grocery Delivery".center(60))
    print("=" * 60)
    print()


def check_python_version():
    """Ensure Python version is 3.8 or higher."""
    if sys.version_info < (3, 8):
        print("❌ Error: Python 3.8 or higher is required")
        print(f"   Current version: {sys.version}")
        sys.exit(1)
    print(f"✅ Python version: {sys.version.split()[0]}")


def install_dependencies():
    """Install required packages."""
    print("\n📦 Checking dependencies...")
    
    try:
        import streamlit
        print(f"✅ Streamlit {streamlit.__version__} is installed")
    except ImportError:
        print("⏳ Installing Streamlit...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "streamlit"])
        print("✅ Streamlit installed successfully")
    
    print("✅ All dependencies ready!")


def initialize_database():
    """Initialize the SQLite database with seed data."""
    print("\n🗄️  Initializing database...")
    
    try:
        from utils.db import init_db
        init_db()
        print("✅ Database initialized with 24 products")
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        sys.exit(1)


def start_app():
    """Start the Streamlit app."""
    print("\n🚀 Starting FreshCart app...")
    print("=" * 60)
    print()
    print("📱 Access the app at: http://localhost:5000")
    print("📱 Or try:           http://127.0.0.1:5000")
    print()
    print("Press Ctrl+C to stop the server")
    print()
    print("=" * 60)
    print()
    
    try:
        subprocess.run(
            [sys.executable, "-m", "streamlit", "run", "app.py", "--server.port=5000"],
            cwd=os.path.dirname(os.path.abspath(__file__))
        )
    except KeyboardInterrupt:
        print("\n\n👋 FreshCart app stopped. See you soon!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error starting app: {e}")
        sys.exit(1)


def main():
    """Main entry point."""
    try:
        print_header()
        check_python_version()
        install_dependencies()
        initialize_database()
        start_app()
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
