def assess_password_strength(password):
    """Assess password strength and provide rating, color, and feedback."""
    # Security checks
    common_passwords = ["password", "123456", "qwerty", "admin", "letmein", "welcome"]
    dictionary_words = ["apple", "computer", "dragon", "monkey"]

    # Criteria checks
    has_length = len(password) >= 12
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_num = any(c.isdigit() for c in password)

    special_chars = "!@#$%^&*()_+-=[]{};:'\",.<>?/\\|"
    has_special = any(c in special_chars for c in password)

    is_common = password.lower() in common_passwords
    has_dict_word = any(word in password.lower() for word in dictionary_words)

    # Calculate score
    score = sum([has_length, has_upper, has_lower, has_num, has_special, not is_common, not has_dict_word])

    # Generate feedback
    feedback = []
    if not has_length:
        feedback.append("- Minimum 12 characters")
    if not has_upper:
        feedback.append("- Missing uppercase letter")
    if not has_lower:
        feedback.append("- Missing lowercase letter")
    if not has_num:
        feedback.append("- Missing a number")
    if not has_special:
        feedback.append("- Missing a special character")

    # Determine rating
    if is_common or has_dict_word or score <= 4:
        rating = "WEAK"
        color = "#FF4444"
        if is_common:
            feedback.append("- Common password detected")
        if has_dict_word:
            feedback.append("- Dictionary word detected")

    elif score >= 6 and has_special:
        rating = "STRONG"
        color = "#00C853"
        feedback = ["+ Excellent security!"]

    else:
        rating = "MODERATE"
        color = "#FF9800"
        if not has_special:
            feedback.append("- Note: Missing special characters")

    return rating, color, feedback