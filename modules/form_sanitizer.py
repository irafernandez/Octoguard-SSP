import re
import html


class FormSanitizer:
    """Sanitizes web form inputs by removing or neutralizing dangerous content"""

    # Patterns for detection and removal
    SCRIPT_PATTERN = re.compile(r'<script[^>]*>.*?</script>', re.IGNORECASE | re.DOTALL)
    HTML_TAG_PATTERN = re.compile(r'<[^>]+>')
    SQL_INJECTION_PATTERN = re.compile(
        r"(\bOR\b|\bAND\b)\s*['\"]?\d+['\"]?\s*=\s*['\"]?\d+['\"]?|'\s*OR\s*'1'\s*=\s*'1|--|\bUNION\b.*\bSELECT\b",
        re.IGNORECASE
    )

    @staticmethod
    def sanitize_full_name(name):
        """Sanitize a full name by allowing only letters, spaces, hyphens, and apostrophes."""
        if not name:
            return "", False, []

        original = name
        notes = []

        # Remove leading/trailing whitespace
        sanitized = name.strip()

        # Remove all characters except letters, spaces, hyphens, and apostrophes
        sanitized = re.sub(r"[^a-zA-Z\s\-']", "", sanitized)

        # Remove multiple consecutive spaces
        sanitized = re.sub(r'\s+', ' ', sanitized)

        # Check if modifications were made
        was_modified = (sanitized != original)

        if was_modified:
            if re.search(r'\d', original):
                notes.append("Removed numbers")
            if len(original) != len(re.sub(r"[^a-zA-Z\s\-']", "", original)):
                notes.append("Removed invalid special characters")

        return sanitized, was_modified, notes

    @staticmethod
    def sanitize_email(email):
        """Sanitize an email by trimming spaces and normalizing."""
        if not email:
            return "", False, []

        original = email
        notes = []

        # Remove all whitespace
        sanitized = email.replace(' ', '').replace('\t', '').replace('\n', '')

        # Convert to lowercase (standard practice)
        sanitized = sanitized.lower()

        # Check if modifications were made
        was_modified = (sanitized != original)

        if was_modified:
            if ' ' in original:
                notes.append("Removed spaces")
            if sanitized != original.lower():
                notes.append("Converted to lowercase")

        return sanitized, was_modified, notes

    @staticmethod
    def sanitize_username(username):
        """Sanitize a username by allowing only letters, numbers, and underscores."""
        if not username:
            return "", False, []

        original = username
        notes = []

        # Remove leading/trailing whitespace
        sanitized = username.strip()

        # Keep only letters, numbers, and underscores
        sanitized = re.sub(r"[^a-zA-Z0-9_]", "", sanitized)

        # Check if modifications were made
        was_modified = (sanitized != original)

        if was_modified:
            notes.append("Removed invalid characters")

        return sanitized, was_modified, notes

    @staticmethod
    def sanitize_message(message):
        """Sanitize a message by removing scripts, HTML tags, SQL patterns, and escaping special characters."""
        if not message:
            return "", False, []

        original = message
        sanitized = message
        notes = []

        # Step 1: Remove script tags
        if FormSanitizer.SCRIPT_PATTERN.search(sanitized):
            sanitized = FormSanitizer.SCRIPT_PATTERN.sub('', sanitized)
            notes.append("Script tags removed")

        # Step 2: Remove all HTML tags
        if FormSanitizer.HTML_TAG_PATTERN.search(sanitized):
            # Count how many tags
            tag_count = len(FormSanitizer.HTML_TAG_PATTERN.findall(sanitized))
            sanitized = FormSanitizer.HTML_TAG_PATTERN.sub('', sanitized)
            notes.append(f"HTML tags removed ({tag_count} tag(s))")

        # Step 3: Remove SQL injection patterns
        if FormSanitizer.SQL_INJECTION_PATTERN.search(sanitized):
            sanitized = FormSanitizer.SQL_INJECTION_PATTERN.sub('', sanitized)
            notes.append("SQL injection patterns removed")

        # Step 4: Escape special HTML characters
        escaped = html.escape(sanitized)
        if escaped != sanitized:
            sanitized = escaped
            notes.append("Special characters escaped")

        # Step 5: Clean up whitespace
        sanitized = re.sub(r'\s+', ' ', sanitized).strip()

        # Check if any modifications were made
        was_modified = (sanitized != original)

        return sanitized, was_modified, notes

    @staticmethod
    def sanitize_all(form_data):
        """Sanitize all form fields in a dictionary at once."""
        results = {}

        # Sanitize each field
        if 'full_name' in form_data:
            sanitized, modified, notes = FormSanitizer.sanitize_full_name(form_data['full_name'])
            results['full_name'] = {
                'original': form_data['full_name'],
                'sanitized': sanitized,
                'was_modified': modified,
                'notes': notes
            }

        if 'email' in form_data:
            sanitized, modified, notes = FormSanitizer.sanitize_email(form_data['email'])
            results['email'] = {
                'original': form_data['email'],
                'sanitized': sanitized,
                'was_modified': modified,
                'notes': notes
            }

        if 'username' in form_data:
            sanitized, modified, notes = FormSanitizer.sanitize_username(form_data['username'])
            results['username'] = {
                'original': form_data['username'],
                'sanitized': sanitized,
                'was_modified': modified,
                'notes': notes
            }

        if 'message' in form_data:
            sanitized, modified, notes = FormSanitizer.sanitize_message(form_data['message'])
            results['message'] = {
                'original': form_data['message'],
                'sanitized': sanitized,
                'was_modified': modified,
                'notes': notes
            }

        return results