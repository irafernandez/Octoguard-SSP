# Application Info
APP_NAME = "Octoguard"
APP_VERSION = "1.0.0"
WINDOW_SIZE = "1100x750"

#Gruvbox
COLORS = {
    # Background colors - Warm dark theme
    'bg_primary': '#1d2021',  # Dark gruvbox background
    'bg_secondary': '#282828',  # Slightly lighter background
    'bg_tertiary': '#32302f',  # Elevated elements
    'bg_header': '#1d2021',  # Header background
    'bg_sidebar': '#282828',  # Sidebar background

    # Text colors
    'text_primary': '#ebdbb2',  # Warm beige (primary text)
    'text_secondary': '#d5c4a1',  # Light beige (secondary text)
    'text_tertiary': '#a89984',  # Gray beige (tertiary text)
    'text_muted': '#7c6f64',  # Muted brown-gray

    # Accent colors - Warm orange/red
    'accent_primary': '#fe8019',  # Bright orange (primary actions)
    'accent_primary_hover': '#d65d0e',  # Darker orange (hover)
    'accent_secondary': '#fb4934',  # Red-orange (secondary actions)

    # Status colors
    'success': '#b8bb26',  # green (success)
    'warning': '#fabd2f',  # yellow (warning)
    'error': '#fb4934',  # red (error)
    'info': '#83a598',  # blue (info)

    # Navigation colors
    'nav_bg': '#282828',
    'nav_active_bg': '#32302f',
    'nav_active_accent': '#fe8019',
    'nav_text': '#a89984',
    'nav_text_active': '#ebdbb2',
    'nav_hover': '#3c3836',

    # Border colors
    'border_primary': '#504945',
    'border_secondary': '#3c3836',
    'border_accent': '#fe8019',

    # Input colors
    'input_bg': '#32302f',
    'input_border': '#504945',
    'input_focus': '#fe8019',
    'input_text': '#ebdbb2'
}

# Modern Font Settings
FONTS = {
    'title': ('Inter', 20, 'bold'),
    'heading': ('Inter', 16, 'bold'),
    'subheading': ('Inter', 11, 'bold'),
    'body': ('Inter', 10),
    'small': ('Inter', 9),
    'button': ('Inter', 10, 'bold'),
    'code': ('JetBrains Mono', 10),
    'code_small': ('JetBrains Mono', 9),
    'nav': ('Inter', 10)
}

# Fallback fonts if Inter/JetBrains Mono not available
FONT_FALLBACKS = {
    'title': ('Segoe UI', 20, 'bold'),
    'heading': ('Segoe UI', 16, 'bold'),
    'subheading': ('Segoe UI', 11, 'bold'),
    'body': ('Segoe UI', 10),
    'small': ('Segoe UI', 9),
    'button': ('Segoe UI', 10, 'bold'),
    'code': ('Consolas', 10),
    'code_small': ('Consolas', 9),
    'nav': ('Segoe UI', 10)
}

# Password Generator Settings
PASSWORD_MIN_LENGTH = 8
PASSWORD_MAX_LENGTH = 16
PASSWORD_DEFAULT_LENGTH = 12

# Form Validation Settings
USERNAME_MIN_LENGTH = 4
USERNAME_MAX_LENGTH = 16
MESSAGE_MAX_LENGTH = 250
NAME_MIN_LENGTH = 2

# File Paths
LOG_FILE = "data/security_toolkit_log.txt"
VALIDATION_RESULTS_FILE = "data/validation_results.txt"

# Security Lists
COMMON_PASSWORDS = [
    "password", "123456", "qwerty", "admin",
    "letmein", "welcome", "12345678", "password123"
]

DICTIONARY_WORDS = [
    "apple", "computer", "dragon", "monkey",
    "sunshine", "football", "baseball", "mountain"
]

SQL_KEYWORDS = [
    'SELECT', 'DROP', 'INSERT', 'DELETE',
    'UPDATE', 'UNION', 'EXEC', 'EXECUTE'
]

SPECIAL_CHARACTERS = "!@#$%^&*()_+-=[]{};:'\",.<>?/\\|"

# UI Constants
CARD_PADDING = 20
SECTION_SPACING = 15
INPUT_HEIGHT = 35
BUTTON_HEIGHT = 40
SIDEBAR_WIDTH = 220
HEADER_HEIGHT = 70