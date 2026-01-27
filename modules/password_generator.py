import hashlib
import random
import string


def generate_secure_password(length):
    """Generate a password containing uppercase, lowercase, digits, and special characters."""
    # Define character sets
    uppercase = string.ascii_uppercase
    lowercase = string.ascii_lowercase
    digits = string.digits
    special = "!@#$%^&*()_-+={};:,.?"

    all_characters = uppercase + lowercase + digits + special

    # Keep trying until we get a valid password
    while True:
        password = ''.join(random.choice(all_characters) for i in range(length))

        # Check all requirements are met
        has_uppercase = any(char in uppercase for char in password)
        has_lowercase = any(char in lowercase for char in password)
        has_digit = any(char in digits for char in password)
        has_special = any(char in special for char in password)

        if has_uppercase and has_lowercase and has_digit and has_special:
            return password


def hash_password(password):
    """Return the SHA-256 hash of a password."""
    password_bytes = password.encode('utf-8')
    hash_object = hashlib.sha256(password_bytes)
    return hash_object.hexdigest()