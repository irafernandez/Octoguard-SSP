import tkinter as tk
from tkinter import scrolledtext
from modules.form_validator import FormValidator
from modules.form_sanitizer import FormSanitizer
from utils.constants import *


class FormValidatorView:
    """Form input validator interface"""

    def __init__(self, parent):
        self.parent = parent
        self.create_view()

    def create_view(self):
        """Create the form validator interface"""
        # Header section
        header_frame = tk.Frame(self.parent, bg=COLORS['bg_primary'])
        header_frame.pack(fill=tk.X, pady=(0, 20))

        title = tk.Label(header_frame, text="Form Input Validator",
                        font=FONTS.get('heading', FONT_FALLBACKS['heading']),
                        bg=COLORS['bg_primary'],
                        fg=COLORS['text_primary'])
        title.pack(anchor=tk.W, side=tk.LEFT)

        # Status indicator
        status_badge = tk.Label(header_frame, text="● VALIDATING",
                               font=FONTS.get('small', FONT_FALLBACKS['small']),
                               bg=COLORS['bg_tertiary'],
                               fg=COLORS['warning'],
                               padx=10, pady=4)
        status_badge.pack(side=tk.RIGHT)

        desc = tk.Label(self.parent,
                       text="Advanced input validation with XSS and SQL injection detection",
                       font=FONTS.get('small', FONT_FALLBACKS['small']),
                       bg=COLORS['bg_primary'],
                       fg=COLORS['text_tertiary'])
        desc.pack(anchor=tk.W, pady=(0, 25))

        # Main container with two columns
        main_container = tk.Frame(self.parent, bg=COLORS['bg_primary'])
        main_container.pack(fill=tk.BOTH, expand=True)

        # Left column - Input
        left_column = tk.Frame(main_container, bg=COLORS['bg_primary'])
        left_column.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        # Right column - Results
        right_column = tk.Frame(main_container, bg=COLORS['bg_primary'])
        right_column.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0))

        # Input card
        input_card = self.create_card(left_column, "Form Inputs")

        # Form fields
        self.name_entry = self.create_input_field(input_card, "Full Name",
                                                  "John Doe")

        self.email_entry = self.create_input_field(input_card, "Email Address",
                                                   "john@example.com")

        self.username_entry = self.create_input_field(input_card, "Username",
                                                      "johndoe123")

        # Message field (larger)
        msg_label = tk.Label(input_card, text="Message",
                            font=FONTS.get('small', FONT_FALLBACKS['small']),
                            bg=COLORS['bg_secondary'],
                            fg=COLORS['text_muted'])
        msg_label.pack(anchor=tk.W, pady=(15, 6))

        msg_frame = tk.Frame(input_card, bg=COLORS['bg_tertiary'])
        msg_frame.pack(fill=tk.X, pady=(0, 20))

        self.message_entry = tk.Text(msg_frame,
                                     bg=COLORS['bg_tertiary'],
                                     fg=COLORS['input_text'],
                                     font=FONTS.get('body', FONT_FALLBACKS['body']),
                                     relief=tk.FLAT,
                                     height=4,
                                     insertbackground=COLORS['accent_primary'],
                                     wrap=tk.WORD)
        self.message_entry.pack(fill=tk.X, padx=12, pady=10)
        self.message_entry.insert("1.0", "Hello, I would like to...")

        # Validate button
        validate_btn = self.create_button(input_card, "Validate & Sanitize",
                                         self.validate_form)
        validate_btn.pack(pady=(0, 0))

        # Results card
        results_card = self.create_card(right_column, "Validation Results")

        # Results display with modern scrolled text
        self.results_display = scrolledtext.ScrolledText(
            results_card,
            bg=COLORS['bg_tertiary'],
            fg=COLORS['text_primary'],
            font=FONTS.get('code_small', FONT_FALLBACKS['code_small']),
            relief=tk.FLAT,
            insertbackground=COLORS['accent_primary'],
            wrap=tk.WORD,
            state='disabled'
        )
        self.results_display.pack(fill=tk.BOTH, expand=True, pady=15)

        # Configure text tags for colored output
        self.results_display.tag_config('valid', foreground=COLORS['success'])
        self.results_display.tag_config('invalid', foreground=COLORS['error'])
        self.results_display.tag_config('warning', foreground=COLORS['warning'])
        self.results_display.tag_config('header', foreground=COLORS['accent_primary'],
                                       font=FONTS.get('code', FONT_FALLBACKS['code']))

    def create_card(self, parent, title):
        """Create a card container"""
        card = tk.Frame(parent, bg=COLORS['bg_secondary'])
        card.pack(fill=tk.BOTH, expand=True, pady=(0, 0))

        # Card header
        header = tk.Frame(card, bg=COLORS['bg_secondary'])
        header.pack(fill=tk.X, padx=CARD_PADDING, pady=(CARD_PADDING, 10))

        title_label = tk.Label(header, text=title,
                              font=FONTS.get('subheading', FONT_FALLBACKS['subheading']),
                              bg=COLORS['bg_secondary'],
                              fg=COLORS['text_primary'])
        title_label.pack(side=tk.LEFT)

        accent_line = tk.Frame(header, bg=COLORS['accent_primary'], height=2, width=40)
        accent_line.pack(side=tk.LEFT, padx=(10, 0))

        # Card content
        content = tk.Frame(card, bg=COLORS['bg_secondary'])
        content.pack(fill=tk.BOTH, expand=True, padx=CARD_PADDING, pady=(0, CARD_PADDING))

        return content

    def create_input_field(self, parent, label, placeholder):
        """Create input field"""
        label_widget = tk.Label(parent, text=label,
                               font=FONTS.get('small', FONT_FALLBACKS['small']),
                               bg=COLORS['bg_secondary'],
                               fg=COLORS['text_muted'])
        label_widget.pack(anchor=tk.W, pady=(15, 6))

        field_frame = tk.Frame(parent, bg=COLORS['bg_tertiary'])
        field_frame.pack(fill=tk.X, pady=(0, 0))

        entry = tk.Entry(field_frame,
                        bg=COLORS['bg_tertiary'],
                        fg=COLORS['input_text'],
                        font=FONTS.get('body', FONT_FALLBACKS['body']),
                        relief=tk.FLAT,
                        insertbackground=COLORS['accent_primary'])
        entry.pack(fill=tk.X, padx=12, pady=10)
        entry.insert(0, placeholder)

        return entry

    def create_button(self, parent, text, command):
        """Create button"""
        btn_canvas = tk.Canvas(parent, width=200, height=BUTTON_HEIGHT,
                              bg=COLORS['bg_secondary'], highlightthickness=0)

        rect = btn_canvas.create_rectangle(0, 0, 200, BUTTON_HEIGHT,
                                          fill=COLORS['accent_primary'], outline='')
        text_id = btn_canvas.create_text(100, BUTTON_HEIGHT/2,
                                        text=text,
                                        fill='#000000',
                                        font=FONTS.get('button', FONT_FALLBACKS['button']))

        def on_click(e):
            command()

        def on_enter(e):
            btn_canvas.itemconfig(rect, fill=COLORS['accent_primary_hover'])
            btn_canvas.config(cursor='hand2')

        def on_leave(e):
            btn_canvas.itemconfig(rect, fill=COLORS['accent_primary'])
            btn_canvas.config(cursor='')

        btn_canvas.bind('<Button-1>', on_click)
        btn_canvas.bind('<Enter>', on_enter)
        btn_canvas.bind('<Leave>', on_leave)

        return btn_canvas

    def validate_form(self):
        """Handle form validation with comprehensive feedback"""
        # Get input values
        full_name = self.name_entry.get()
        email = self.email_entry.get()
        username = self.username_entry.get()
        message = self.message_entry.get("1.0", tk.END).strip()

        # Create form data dictionary
        form_data = {
            'full_name': full_name,
            'email': email,
            'username': username,
            'message': message
        }

        # Validate all fields
        validation_results = FormValidator.validate_all(form_data)

        # Sanitize all fields
        sanitization_results = FormSanitizer.sanitize_all(form_data)

        # Clear previous results
        self.results_display.configure(state='normal')
        self.results_display.delete("1.0", tk.END)

        # Display validation results
        self.results_display.insert(tk.END, "VALIDATION RESULTS\n", 'header')
        self.results_display.insert(tk.END, "─" * 60 + "\n\n")

        # Full Name
        is_valid, error_msg = validation_results['full_name']
        self.results_display.insert(tk.END, "Full Name: ")
        if is_valid:
            self.results_display.insert(tk.END, "✓ Valid\n", 'valid')
        else:
            self.results_display.insert(tk.END, f"✗ {error_msg}\n", 'invalid')

        # Email
        is_valid, error_msg = validation_results['email']
        self.results_display.insert(tk.END, "Email: ")
        if is_valid:
            self.results_display.insert(tk.END, "✓ Valid\n", 'valid')
        else:
            self.results_display.insert(tk.END, f"✗ {error_msg}\n", 'invalid')

        # Username
        is_valid, error_msg = validation_results['username']
        self.results_display.insert(tk.END, "Username: ")
        if is_valid:
            self.results_display.insert(tk.END, "✓ Valid\n", 'valid')
        else:
            self.results_display.insert(tk.END, f"✗ {error_msg}\n", 'invalid')

        # Message
        is_valid, error_msg = validation_results['message']
        msg_sanitized = sanitization_results['message']['was_modified']
        msg_notes = sanitization_results['message']['notes']

        self.results_display.insert(tk.END, "Message: ")
        if is_valid and not msg_sanitized:
            self.results_display.insert(tk.END, "✓ Valid\n", 'valid')
        elif msg_sanitized:
            self.results_display.insert(tk.END, f"⚠ Sanitized ({', '.join(msg_notes)})\n", 'warning')
        else:
            self.results_display.insert(tk.END, f"✗ {error_msg}\n", 'invalid')

        # Display sanitized output
        self.results_display.insert(tk.END, "\n")
        self.results_display.insert(tk.END, "SANITIZED OUTPUT\n", 'header')
        self.results_display.insert(tk.END, "─" * 60 + "\n\n")

        # Full Name sanitized
        name_data = sanitization_results['full_name']
        self.results_display.insert(tk.END, f"Full Name: {name_data['sanitized']}\n")
        if name_data['was_modified']:
            self.results_display.insert(tk.END, f"  → {', '.join(name_data['notes'])}\n", 'warning')

        # Email sanitized
        email_data = sanitization_results['email']
        self.results_display.insert(tk.END, f"\nEmail: {email_data['sanitized']}\n")
        if email_data['was_modified']:
            self.results_display.insert(tk.END, f"  → {', '.join(email_data['notes'])}\n", 'warning')

        # Username sanitized
        username_data = sanitization_results['username']
        self.results_display.insert(tk.END, f"\nUsername: {username_data['sanitized']}\n")
        if username_data['was_modified']:
            self.results_display.insert(tk.END, f"  → {', '.join(username_data['notes'])}\n", 'warning')

        # Message sanitized
        message_data = sanitization_results['message']
        self.results_display.insert(tk.END, f"\nMessage: {message_data['sanitized']}\n")
        if message_data['was_modified']:
            self.results_display.insert(tk.END, f"  → {', '.join(message_data['notes'])}\n", 'warning')

        # Process complete
        self.results_display.insert(tk.END, "\n")
        self.results_display.insert(tk.END, "─" * 60 + "\n")
        self.results_display.insert(tk.END, "Process Complete.\n")

        self.results_display.configure(state='disabled')