import tkinter as tk
from tkinter import scrolledtext
from modules.form_validator import FormValidator
from modules.form_sanitizer import FormSanitizer
from utils.constants import *


class FormValidatorView:

    def __init__(self, parent):
        self.parent = parent
        self.validation_results = {}
        self.sanitization_results = {}
        self.create_view()

    def create_view(self):
        """Create form validator interface"""
        # Header section
        header_frame = tk.Frame(self.parent, bg=COLORS['bg_primary'])
        header_frame.pack(fill=tk.X, pady=(0, 20))

        title = tk.Label(header_frame, text="Form Input Validator",
                         font=FONTS.get('heading', FONT_FALLBACKS['heading']),
                         bg=COLORS['bg_primary'],
                         fg=COLORS['text_primary'])
        title.pack(anchor=tk.W, side=tk.LEFT)

        # Status indicator
        self.status_badge = tk.Label(header_frame, text="● READY",
                                     font=FONTS.get('small', FONT_FALLBACKS['small']),
                                     bg=COLORS['bg_tertiary'],
                                     fg=COLORS['text_muted'],
                                     padx=10, pady=4)
        self.status_badge.pack(side=tk.RIGHT)

        desc = tk.Label(self.parent,
                        text="Advanced input validation with XSS and SQL injection detection",
                        font=FONTS.get('small', FONT_FALLBACKS['small']),
                        bg=COLORS['bg_primary'],
                        fg=COLORS['text_tertiary'])
        desc.pack(anchor=tk.W, pady=(0, 25))

        # Main content area
        content = tk.Frame(self.parent, bg=COLORS['bg_primary'])
        content.pack(fill=tk.BOTH, expand=True)

        # Left side - Input form
        left_panel = tk.Frame(content, bg=COLORS['bg_primary'])
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        # Right side - Results
        right_panel = tk.Frame(content, bg=COLORS['bg_primary'])
        right_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0))

        # === LEFT PANEL: INPUT FORM ===
        input_card = self.create_card(left_panel, "Form Inputs")

        # Form fields with validation indicators
        self.name_entry, self.name_indicator = self.create_input_with_indicator(
            input_card, "Full Name", "John Doe")

        self.email_entry, self.email_indicator = self.create_input_with_indicator(
            input_card, "Email Address", "john@example.com")

        self.username_entry, self.username_indicator = self.create_input_with_indicator(
            input_card, "Username", "johndoe123")

        # Message field (larger)
        msg_container = tk.Frame(input_card, bg=COLORS['bg_secondary'])
        msg_container.pack(fill=tk.X, pady=(15, 0))

        msg_header = tk.Frame(msg_container, bg=COLORS['bg_secondary'])
        msg_header.pack(fill=tk.X, pady=(0, 6))

        tk.Label(msg_header, text="Message",
                 font=FONTS.get('small', FONT_FALLBACKS['small']),
                 bg=COLORS['bg_secondary'],
                 fg=COLORS['text_muted']).pack(side=tk.LEFT)

        self.message_indicator = tk.Label(msg_header, text="●",
                                          font=('Segoe UI', 10),
                                          bg=COLORS['bg_secondary'],
                                          fg=COLORS['text_muted'])
        self.message_indicator.pack(side=tk.RIGHT)

        msg_frame = tk.Frame(msg_container, bg=COLORS['bg_tertiary'])
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
        self.message_entry.insert("1.0", "Hello, I would like to inquire...")

        # Character counter
        self.char_counter = tk.Label(msg_container,
                                     text="0/250 characters",
                                     font=FONTS.get('small', FONT_FALLBACKS['small']),
                                     bg=COLORS['bg_secondary'],
                                     fg=COLORS['text_muted'])
        self.char_counter.pack(anchor=tk.E, pady=(5, 15))
        self.message_entry.bind('<KeyRelease>', self.update_char_counter)

        # Validate button
        validate_btn = self.create_button(input_card, "Validate & Sanitize",
                                          self.validate_form)
        validate_btn.pack()

        # === RIGHT PANEL: RESULTS ===

        # Validation summary card
        summary_card = self.create_card(right_panel, "Validation Summary")

        # Summary grid
        self.summary_grid = tk.Frame(summary_card, bg=COLORS['bg_secondary'])
        self.summary_grid.pack(fill=tk.X, pady=(10, 20))

        # Create summary items (will be populated after validation)
        self.create_initial_summary()

        # Detailed results card
        results_card = self.create_card(right_panel, "Detailed Results")

        # Tabbed interface for results
        tab_frame = tk.Frame(results_card, bg=COLORS['bg_secondary'])
        tab_frame.pack(fill=tk.X, pady=(0, 10))

        self.tab_validation = self.create_tab_button(tab_frame, "Validation",
                                                     lambda: self.switch_tab('validation'), True)
        self.tab_validation.pack(side=tk.LEFT, padx=(0, 5))

        self.tab_sanitization = self.create_tab_button(tab_frame, "Sanitization",
                                                       lambda: self.switch_tab('sanitization'), False)
        self.tab_sanitization.pack(side=tk.LEFT)

        # Results display area
        self.results_container = tk.Frame(results_card, bg=COLORS['bg_secondary'])
        self.results_container.pack(fill=tk.BOTH, expand=True)

        # Validation results view
        self.validation_view = scrolledtext.ScrolledText(
            self.results_container,
            bg=COLORS['bg_tertiary'],
            fg=COLORS['text_primary'],
            font=FONTS.get('small', FONT_FALLBACKS['small']),
            relief=tk.FLAT,
            insertbackground=COLORS['accent_primary'],
            wrap=tk.WORD,
            state='disabled'
        )

        # Sanitization results view
        self.sanitization_view = scrolledtext.ScrolledText(
            self.results_container,
            bg=COLORS['bg_tertiary'],
            fg=COLORS['text_primary'],
            font=FONTS.get('small', FONT_FALLBACKS['small']),
            relief=tk.FLAT,
            insertbackground=COLORS['accent_primary'],
            wrap=tk.WORD,
            state='disabled'
        )

        # Configure text tags
        for view in [self.validation_view, self.sanitization_view]:
            view.tag_config('valid', foreground=COLORS['success'], font=FONTS.get('body', FONT_FALLBACKS['body']))
            view.tag_config('invalid', foreground=COLORS['error'], font=FONTS.get('body', FONT_FALLBACKS['body']))
            view.tag_config('warning', foreground=COLORS['warning'], font=FONTS.get('body', FONT_FALLBACKS['body']))
            view.tag_config('header', foreground=COLORS['accent_primary'],
                            font=FONTS.get('subheading', FONT_FALLBACKS['subheading']))
            view.tag_config('field', foreground=COLORS['text_primary'],
                            font=FONTS.get('body', FONT_FALLBACKS['body']))

        # Show validation view by default
        self.current_tab = 'validation'
        self.validation_view.pack(fill=tk.BOTH, expand=True)

    def create_card(self, parent, title):
        """Create a card container"""
        card = tk.Frame(parent, bg=COLORS['bg_secondary'])
        card.pack(fill=tk.BOTH, expand=True, pady=(0, 15))

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

    def create_input_with_indicator(self, parent, label, placeholder):
        """Create input field with validation indicator"""
        container = tk.Frame(parent, bg=COLORS['bg_secondary'])
        container.pack(fill=tk.X, pady=(15, 0))

        # Label with indicator
        header = tk.Frame(container, bg=COLORS['bg_secondary'])
        header.pack(fill=tk.X, pady=(0, 6))

        label_widget = tk.Label(header, text=label,
                                font=FONTS.get('small', FONT_FALLBACKS['small']),
                                bg=COLORS['bg_secondary'],
                                fg=COLORS['text_muted'])
        label_widget.pack(side=tk.LEFT)

        indicator = tk.Label(header, text="●",
                             font=('Segoe UI', 10),
                             bg=COLORS['bg_secondary'],
                             fg=COLORS['text_muted'])
        indicator.pack(side=tk.RIGHT)

        # Input field
        field_frame = tk.Frame(container, bg=COLORS['bg_tertiary'])
        field_frame.pack(fill=tk.X)

        entry = tk.Entry(field_frame,
                         bg=COLORS['bg_tertiary'],
                         fg=COLORS['input_text'],
                         font=FONTS.get('body', FONT_FALLBACKS['body']),
                         relief=tk.FLAT,
                         insertbackground=COLORS['accent_primary'])
        entry.pack(fill=tk.X, padx=12, pady=10)
        entry.insert(0, placeholder)

        return entry, indicator

    def create_tab_button(self, parent, text, command, active=False):
        """Create tab button"""
        bg = COLORS['bg_tertiary'] if active else COLORS['bg_secondary']
        fg = COLORS['text_primary'] if active else COLORS['text_secondary']

        btn = tk.Label(parent, text=text,
                       font=FONTS.get('small', FONT_FALLBACKS['small']),
                       bg=bg, fg=fg,
                       padx=15, pady=8,
                       cursor='hand2')
        btn.bind('<Button-1>', lambda e: command())

        return btn

    def switch_tab(self, tab_name):
        """Switch between validation and sanitization tabs"""
        self.current_tab = tab_name

        # Update tab styles
        if tab_name == 'validation':
            self.tab_validation.config(bg=COLORS['bg_tertiary'], fg=COLORS['text_primary'])
            self.tab_sanitization.config(bg=COLORS['bg_secondary'], fg=COLORS['text_secondary'])
            self.sanitization_view.pack_forget()
            self.validation_view.pack(fill=tk.BOTH, expand=True)
        else:
            self.tab_sanitization.config(bg=COLORS['bg_tertiary'], fg=COLORS['text_primary'])
            self.tab_validation.config(bg=COLORS['bg_secondary'], fg=COLORS['text_secondary'])
            self.validation_view.pack_forget()
            self.sanitization_view.pack(fill=tk.BOTH, expand=True)

    def create_initial_summary(self):
        """Create initial summary display"""
        fields = ['Full Name', 'Email', 'Username', 'Message']

        for i, field in enumerate(fields):
            item = tk.Frame(self.summary_grid, bg=COLORS['bg_tertiary'])
            item.pack(fill=tk.X, pady=3)

            # Field name
            tk.Label(item, text=field,
                     font=FONTS.get('small', FONT_FALLBACKS['small']),
                     bg=COLORS['bg_tertiary'],
                     fg=COLORS['text_secondary'],
                     width=12, anchor=tk.W).pack(side=tk.LEFT, padx=(10, 5), pady=8)

            # Status indicator
            status = tk.Label(item, text="Pending",
                              font=FONTS.get('small', FONT_FALLBACKS['small']),
                              bg=COLORS['bg_tertiary'],
                              fg=COLORS['text_muted'])
            status.pack(side=tk.LEFT, padx=5, pady=8)

            # Store reference
            setattr(self, f'summary_{field.lower().replace(" ", "_")}', status)

    def create_button(self, parent, text, command):
        """Create button"""
        btn_canvas = tk.Canvas(parent, width=200, height=BUTTON_HEIGHT,
                               bg=COLORS['bg_secondary'], highlightthickness=0)

        rect = btn_canvas.create_rectangle(0, 0, 200, BUTTON_HEIGHT,
                                           fill=COLORS['accent_primary'], outline='')
        text_id = btn_canvas.create_text(100, BUTTON_HEIGHT / 2,
                                         text=text,
                                         fill='#1d2021',
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

    def update_char_counter(self, event=None):
        """Update character counter for message field"""
        text = self.message_entry.get("1.0", tk.END).strip()
        char_count = len(text)

        self.char_counter.config(text=f"{char_count}/250 characters")

        if char_count > 250:
            self.char_counter.config(fg=COLORS['error'])
        elif char_count > 200:
            self.char_counter.config(fg=COLORS['warning'])
        else:
            self.char_counter.config(fg=COLORS['text_muted'])

    def validate_form(self):
        """Handle form validation with visual feedback"""
        # Update status badge
        self.status_badge.config(text="● VALIDATING", fg=COLORS['warning'])
        self.parent.update()

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
        self.validation_results = FormValidator.validate_all(form_data)

        # Sanitize all fields
        self.sanitization_results = FormSanitizer.sanitize_all(form_data)

        # Update indicators
        self.update_field_indicators()

        # Update summary
        self.update_summary()

        # Display validation results
        self.display_validation_results()

        # Display sanitization results
        self.display_sanitization_results()

        # Update status badge
        all_valid = all(result[0] for result in self.validation_results.values())
        if all_valid:
            self.status_badge.config(text="● ALL VALID", fg=COLORS['success'])
        else:
            self.status_badge.config(text="● ISSUES FOUND", fg=COLORS['error'])

    def update_field_indicators(self):
        """Update visual indicators for each field"""
        indicators = [
            (self.name_indicator, 'full_name'),
            (self.email_indicator, 'email'),
            (self.username_indicator, 'username'),
            (self.message_indicator, 'message')
        ]

        for indicator, field in indicators:
            is_valid, _ = self.validation_results[field]
            was_sanitized = self.sanitization_results[field]['was_modified']

            if is_valid and not was_sanitized:
                indicator.config(fg=COLORS['success'])
            elif was_sanitized:
                indicator.config(fg=COLORS['warning'])
            else:
                indicator.config(fg=COLORS['error'])

    def update_summary(self):
        """Update validation summary"""
        summary_map = {
            'full_name': self.summary_full_name,
            'email': self.summary_email,
            'username': self.summary_username,
            'message': self.summary_message
        }

        for field, label in summary_map.items():
            is_valid, error = self.validation_results[field]
            was_sanitized = self.sanitization_results[field]['was_modified']

            if is_valid and not was_sanitized:
                label.config(text="✓ Valid", fg=COLORS['success'])
            elif was_sanitized:
                label.config(text="⚠ Sanitized", fg=COLORS['warning'])
            else:
                label.config(text="✗ Invalid", fg=COLORS['error'])

    def display_validation_results(self):
        """Display detailed validation results"""
        self.validation_view.configure(state='normal')
        self.validation_view.delete("1.0", tk.END)

        for field_name, (is_valid, error_msg) in self.validation_results.items():
            # Field header
            display_name = field_name.replace('_', ' ').title()
            self.validation_view.insert(tk.END, f"{display_name}\n", 'header')

            if is_valid:
                self.validation_view.insert(tk.END, "  ✓ Validation passed\n", 'valid')
            else:
                self.validation_view.insert(tk.END, f"  ✗ {error_msg}\n", 'invalid')

            self.validation_view.insert(tk.END, "\n")

        self.validation_view.configure(state='disabled')

    def display_sanitization_results(self):
        """Display detailed sanitization results"""
        self.sanitization_view.configure(state='normal')
        self.sanitization_view.delete("1.0", tk.END)

        for field_name, data in self.sanitization_results.items():
            display_name = field_name.replace('_', ' ').title()
            self.sanitization_view.insert(tk.END, f"{display_name}\n", 'header')

            # Original value
            self.sanitization_view.insert(tk.END, f"  Original: {data['original']}\n", 'field')

            # Sanitized value
            if data['was_modified']:
                self.sanitization_view.insert(tk.END, f"  Sanitized: {data['sanitized']}\n", 'warning')
                self.sanitization_view.insert(tk.END, f"  Changes: {', '.join(data['notes'])}\n", 'warning')
            else:
                self.sanitization_view.insert(tk.END, f"  No changes needed\n", 'valid')

            self.sanitization_view.insert(tk.END, "\n")

        self.sanitization_view.configure(state='disabled')