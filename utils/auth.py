import hashlib
import os
import re


def hash_password(password: str) -> str:
    salt = os.urandom(16).hex()
    hashed = hashlib.sha256((salt + password).encode()).hexdigest()
    return f"{salt}:{hashed}"


def verify_password(password: str, password_hash: str) -> bool:
    try:
        salt, hashed = password_hash.split(":")
        return hashlib.sha256((salt + password).encode()).hexdigest() == hashed
    except Exception:
        return False


def validate_email(email: str) -> bool:
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w{2,}$"
    return bool(re.match(pattern, email))


def validate_password(password: str) -> tuple[bool, str]:
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    if not any(c.isdigit() for c in password):
        return False, "Password must contain at least one number."
    return True, ""


def validate_phone(phone: str) -> tuple[bool, str]:
    """Validate phone number format. Accepts multiple formats."""
    phone = phone.strip()
    if not phone:
        return False, "Phone number is required."
    # Remove common formatting characters
    cleaned = "".join(c for c in phone if c.isdigit() or c in "+-() ")
    # Extract just digits
    digits = "".join(c for c in cleaned if c.isdigit())
    if len(digits) < 10:
        return False, "Phone number must be at least 10 digits."
    if len(digits) > 15:
        return False, "Phone number is too long."
    return True, ""


def validate_address(address: str) -> tuple[bool, str]:
    """Validate delivery address."""
    address = address.strip()
    if not address:
        return False, "Delivery address is required."
    if len(address) < 10:
        return False, "Please enter a more complete address (at least 10 characters)."
    if len(address) > 200:
        return False, "Address is too long."
    return True, ""
