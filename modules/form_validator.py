import re


class FormValidator:
    """Validates web form inputs against security and format requirements"""

    # Validation patterns - Strict and comprehensive
    FULL_NAME_PATTERN = re.compile(r"^[a-zA-Z](?:[a-zA-Z\s\-'])*[a-zA-Z]$")
    USERNAME_PATTERN = re.compile(r"^[a-zA-Z_][a-zA-Z0-9_]{3,15}$")
    EMAIL_PATTERN = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9._-]*@[a-zA-Z0-9][a-zA-Z0-9.-]*\.[a-zA-Z]{2,}$")

    # Security threat patterns
    SQL_KEYWORDS = [
        'SELECT', 'DROP', 'INSERT', 'DELETE', 'UPDATE',
        'UNION', 'EXEC', 'EXECUTE', 'ALTER', 'CREATE', 'TABLE'
    ]
    SCRIPT_PATTERN = re.compile(r'<script[^>]*>.*?</script>', re.IGNORECASE | re.DOTALL)
    IMG_SUSPICIOUS_PATTERN = re.compile(r'<img[^>]*(onerror|onload|onclick)[^>]*>', re.IGNORECASE)

    @staticmethod
    def validate_full_name(name):
        """Validate a full name allowing only letters, spaces, hyphens, and apostrophes."""
        # Check if empty or None
        if not name:
            return False, "Full name is required"

        # Trim whitespace
        name = name.strip()

        # Check minimum length
        if len(name) < 2:
            return False, "Full name must be at least 2 characters long"

        # Check for numbers
        if any(char.isdigit() for char in name):
            return False, "Full name cannot contain numbers"

        # Check for invalid special characters
        if not FormValidator.FULL_NAME_PATTERN.match(name):
            return False, "Full name contains invalid special characters (only spaces, hyphens, and apostrophes allowed)"

        return True, None

    @staticmethod
    def validate_email(email):
        """Validate an email address for proper format and allowed characters."""
        # Check if empty or None
        if not email:
            return False, "Email address is required"

        # Trim whitespace
        email = email.strip()

        # Check for spaces
        if ' ' in email:
            return False, "Email address cannot contain spaces"

        # Check for @ symbol
        if '@' not in email:
            return False, "Email address must contain '@' symbol"

        # Check if starts with special character
        if email[0] in '!@#$%^&*()+=[]{}|\\;:\'",<>?/':
            return False, "Email address cannot start with a special character"

        # Split email into local and domain parts
        parts = email.split('@')
        if len(parts) != 2:
            return False, "Email address must contain exactly one '@' symbol"

        local_part, domain_part = parts

        # Check if local part is empty
        if not local_part:
            return False, "Email address must have a username before '@'"

        # Check if domain part is empty
        if not domain_part:
            return False, "Email address must have a domain after '@'"

        # Check for domain extension
        if '.' not in domain_part:
            return False, "Email address missing domain extension (e.g., .com, .org)"

        # Check if domain ends with extension
        domain_parts = domain_part.split('.')
        if len(domain_parts[-1]) < 2:
            return False, "Email address has invalid domain extension"

        # Full pattern validation
        if not FormValidator.EMAIL_PATTERN.match(email):
            return False, "Invalid email format"

        return True, None

    @staticmethod
    def validate_username(username):
        """Validate a username allowing letters, numbers, and underscores with length and format rules."""
        # Check if empty or None
        if not username:
            return False, "Username is required"

        # Trim whitespace
        username = username.strip()

        # Check minimum length
        if len(username) < 4:
            return False, "Username must be at least 4 characters long"

        # Check maximum length
        if len(username) > 16:
            return False, "Username cannot exceed 16 characters"

        # Check if starts with a number
        if username[0].isdigit():
            return False, "Username cannot start with a number"

        # Check for invalid characters
        if not FormValidator.USERNAME_PATTERN.match(username):
            return False, "Username can only contain letters, numbers, and underscores"

        return True, None

    @staticmethod
    def validate_message(message):
        """Validate a message ensuring length limits and absence of harmful patterns."""
        # Check if empty or None
        if not message:
            return False, "Message cannot be empty"

        # Trim whitespace
        message = message.strip()

        # Check if empty after trimming
        if not message:
            return False, "Message cannot be empty"

        # Check maximum length
        if len(message) > 250:
            return False, "Message cannot exceed 250 characters"

        # Check for script tags
        if FormValidator.SCRIPT_PATTERN.search(message):
            return False, "Message contains prohibited script tags"

        # Check for suspicious img tags
        if FormValidator.IMG_SUSPICIOUS_PATTERN.search(message):
            return False, "Message contains prohibited HTML tags with suspicious attributes"

        # Check for SQL injection keywords
        message_upper = message.upper()
        for keyword in FormValidator.SQL_KEYWORDS:
            # Use word boundaries to avoid false positives
            if re.search(r'\b' + keyword + r'\b', message_upper):
                return False, f"Message contains prohibited SQL keyword: {keyword}"

        return True, None

    @staticmethod
    def validate_all(form_data):
        """Validate all form fields in a dictionary at once."""
        results = {}

        # Validate each field
        if 'full_name' in form_data:
            results['full_name'] = FormValidator.validate_full_name(form_data['full_name'])
        else:
            results['full_name'] = (False, "Full name field is missing")

        if 'email' in form_data:
            results['email'] = FormValidator.validate_email(form_data['email'])
        else:
            results['email'] = (False, "Email field is missing")

        if 'username' in form_data:
            results['username'] = FormValidator.validate_username(form_data['username'])
        else:
            results['username'] = (False, "Username field is missing")

        if 'message' in form_data:
            results['message'] = FormValidator.validate_message(form_data['message'])
        else:
            results['message'] = (False, "Message field is missing")

        return results