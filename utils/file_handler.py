import os
from datetime import datetime


def save_password_to_log(password, password_hash, log_file="data/security_toolkit_log.txt"):
    """Save a password and its SHA-256 hash to a log file."""
    try:
        # Create data directory if it doesn't exist
        os.makedirs(os.path.dirname(log_file), exist_ok=True)

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(log_file, "a") as file:
            file.write(f"Timestamp: {timestamp}\n")
            file.write(f"Password: {password}\n")
            file.write(f"Hash: {password_hash}\n")
            file.write("-" * 80 + "\n")

        return True
    except Exception as e:
        print(f"Error saving to file: {e}")
        return False


def load_password_history(log_file="data/security_toolkit_log.txt"):
    """Read the contents of a password log file."""
    try:
        with open(log_file, "r") as file:
            return file.read()
    except FileNotFoundError:
        return "No password history yet."
    except Exception as e:
        return f"Error reading file: {e}"


def save_validation_result(result_text, result_file="data/validation_results.txt"):
    """Save form validation results to a file."""
    try:
        # Create data directory if it doesn't exist
        os.makedirs(os.path.dirname(result_file), exist_ok=True)

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(result_file, "a") as file:
            file.write(f"\n{'=' * 80}\n")
            file.write(f"Validation Run: {timestamp}\n")
            file.write(f"{'=' * 80}\n")
            file.write(result_text)
            file.write(f"\n{'=' * 80}\n")

        return True
    except Exception as e:
        print(f"Error saving validation results: {e}")
        return False