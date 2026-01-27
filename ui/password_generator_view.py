import tkinter as tk
from tkinter import messagebox
from modules.password_generator import generate_secure_password, hash_password
from utils.file_handler import save_password_to_log
from utils.constants import *


class ModernEntry(tk.Entry):
    """Custom styled entry widget"""

    def __init__(self, parent, **kwargs):
        super().__init__(parent,
                        bg=COLORS['input_bg'],
                        fg=COLORS['input_text'],
                        insertbackground=COLORS['accent_primary'],
                        relief=tk.FLAT,
                        highlightthickness=1,
                        highlightbackground=COLORS['input_border'],
                        highlightcolor=COLORS['input_focus'],
                        **kwargs)


class PasswordGeneratorView:

    def __init__(self, parent):
        self.parent = parent
        self.create_view()

    def create_view(self):
        """Create the password generator interface"""
        # Header section
        header_frame = tk.Frame(self.parent, bg=COLORS['bg_primary'])
        header_frame.pack(fill=tk.X, pady=(0, 20))

        title = tk.Label(header_frame, text="Password Generator",
                        font=FONTS.get('heading', FONT_FALLBACKS['heading']),
                        bg=COLORS['bg_primary'],
                        fg=COLORS['text_primary'])
        title.pack(anchor=tk.W, side=tk.LEFT)

        # Status indicator
        status_badge = tk.Label(header_frame, text="● READY",
                               font=FONTS.get('small', FONT_FALLBACKS['small']),
                               bg=COLORS['bg_tertiary'],
                               fg=COLORS['success'],
                               padx=10, pady=4)
        status_badge.pack(side=tk.RIGHT)

        desc = tk.Label(self.parent,
                       text="Generate strong, secure passwords using cryptographic SHA-256 hashing.",
                       font=FONTS.get('small', FONT_FALLBACKS['small']),
                       bg=COLORS['bg_primary'],
                       fg=COLORS['text_tertiary'])
        desc.pack(anchor=tk.W, pady=(0, 25))

        # Settings card
        settings_card = self.create_card(self.parent, "Configuration")

        # Length selector with modern slider look
        length_frame = tk.Frame(settings_card, bg=COLORS['bg_secondary'])
        length_frame.pack(fill=tk.X, pady=15)

        length_label_frame = tk.Frame(length_frame, bg=COLORS['bg_secondary'])
        length_label_frame.pack(fill=tk.X, pady=(0, 10))

        tk.Label(length_label_frame, text="Password Length",
                font=FONTS.get('body', FONT_FALLBACKS['body']),
                bg=COLORS['bg_secondary'],
                fg=COLORS['text_secondary']).pack(side=tk.LEFT)

        tk.Label(length_label_frame,
                text=f"({PASSWORD_MIN_LENGTH}-{PASSWORD_MAX_LENGTH} CHARACTERS)",
                font=FONTS.get('small', FONT_FALLBACKS['small']),
                bg=COLORS['bg_secondary'],
                fg=COLORS['text_muted']).pack(side=tk.RIGHT)

        # Length input
        length_input_frame = tk.Frame(length_frame, bg=COLORS['bg_secondary'])
        length_input_frame.pack(fill=tk.X)

        self.length_var = tk.StringVar(value=str(PASSWORD_DEFAULT_LENGTH))
        length_entry = ModernEntry(length_input_frame,
                                  textvariable=self.length_var,
                                  font=FONTS.get('body', FONT_FALLBACKS['body']),
                                  width=10)
        length_entry.pack(side=tk.LEFT, ipady=6)

        # Generate button
        gen_btn = self.create_button(settings_card, "Generate Password",
                                     self.generate_password)
        gen_btn.pack(pady=(20, 0))

        # Output card
        output_card = self.create_card(self.parent, "Generated Output")

        # Password display
        self.create_output_field(output_card, "Password", "password")

        # Hash display
        self.create_output_field(output_card, "SHA-256 Hash", "hash")

        # Action buttons
        action_frame = tk.Frame(output_card, bg=COLORS['bg_secondary'])
        action_frame.pack(fill=tk.X, pady=(15, 0))

        copy_btn = tk.Label(action_frame, text="Copy Password",
                           font=FONTS.get('small', FONT_FALLBACKS['small']),
                           bg=COLORS['bg_tertiary'],
                           fg=COLORS['text_secondary'],
                           padx=12, pady=8,
                           cursor='hand2')
        copy_btn.pack(side=tk.LEFT, padx=(0, 10))
        copy_btn.bind('<Button-1>', lambda e: self.copy_to_clipboard())

    def create_card(self, parent, title):
        """Create a card container"""
        # Card frame
        card = tk.Frame(parent, bg=COLORS['bg_secondary'])
        card.pack(fill=tk.X, pady=(0, 20))

        # Card header
        header = tk.Frame(card, bg=COLORS['bg_secondary'])
        header.pack(fill=tk.X, padx=CARD_PADDING, pady=(CARD_PADDING, 10))

        # Title with accent line
        title_label = tk.Label(header, text=title,
                              font=FONTS.get('subheading', FONT_FALLBACKS['subheading']),
                              bg=COLORS['bg_secondary'],
                              fg=COLORS['text_primary'])
        title_label.pack(side=tk.LEFT)

        # Accent line
        accent_line = tk.Frame(header, bg=COLORS['accent_primary'], height=2, width=40)
        accent_line.pack(side=tk.LEFT, padx=(10, 0))

        # Card content
        content = tk.Frame(card, bg=COLORS['bg_secondary'])
        content.pack(fill=tk.BOTH, expand=True, padx=CARD_PADDING, pady=(0, CARD_PADDING))

        return content

    def create_output_field(self, parent, label, field_type):
        """Create output display field"""
        container = tk.Frame(parent, bg=COLORS['bg_secondary'])
        container.pack(fill=tk.X, pady=(0, 15))

        # Label
        lbl = tk.Label(container, text=label,
                      font=FONTS.get('small', FONT_FALLBACKS['small']),
                      bg=COLORS['bg_secondary'],
                      fg=COLORS['text_muted'])
        lbl.pack(anchor=tk.W, pady=(0, 6))

        # Output field with modern styling
        field_frame = tk.Frame(container, bg=COLORS['bg_tertiary'])
        field_frame.pack(fill=tk.X)

        font_size = 'code' if field_type == 'password' else 'code_small'
        entry = tk.Entry(field_frame,
                        bg=COLORS['bg_tertiary'],
                        fg=COLORS['text_primary'],
                        font=FONTS.get(font_size, FONT_FALLBACKS[font_size]),
                        relief=tk.FLAT,
                        state='readonly',
                        readonlybackground=COLORS['bg_tertiary'],
                        highlightthickness=0)
        entry.pack(fill=tk.X, padx=12, pady=10)

        if field_type == 'password':
            self.password_display = entry
        else:
            self.hash_display = entry

    def create_button(self, parent, text, command):
        """Create button"""
        btn_canvas = tk.Canvas(parent, width=180, height=BUTTON_HEIGHT,
                              bg=COLORS['bg_secondary'], highlightthickness=0)

        rect = btn_canvas.create_rectangle(0, 0, 180, BUTTON_HEIGHT,
                                          fill=COLORS['accent_primary'], outline='')
        text_id = btn_canvas.create_text(90, BUTTON_HEIGHT/2,
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

    def generate_password(self):
        """Handle password generation"""
        try:
            length = int(self.length_var.get())

            if length < PASSWORD_MIN_LENGTH or length > PASSWORD_MAX_LENGTH:
                messagebox.showerror("Invalid Length",
                    f"Password length must be between {PASSWORD_MIN_LENGTH} and {PASSWORD_MAX_LENGTH}",
                    parent=self.parent)
                return

            # Generate password and hash
            password = generate_secure_password(length)
            password_hash = hash_password(password)

            # Save to log
            save_password_to_log(password, password_hash)

            # Display results
            self.password_display.configure(state='normal')
            self.password_display.delete(0, tk.END)
            self.password_display.insert(0, password)
            self.password_display.configure(state='readonly')

            self.hash_display.configure(state='normal')
            self.hash_display.delete(0, tk.END)
            self.hash_display.insert(0, password_hash)
            self.hash_display.configure(state='readonly')

            messagebox.showinfo("Success",
                              "Password generated and saved to log file!",
                              parent=self.parent)

        except ValueError:
            messagebox.showerror("Invalid Input",
                               "Please enter a valid number",
                               parent=self.parent)

    def copy_to_clipboard(self):
        """Copy password to clipboard"""
        password = self.password_display.get()
        if password:
            self.parent.clipboard_clear()
            self.parent.clipboard_append(password)
            messagebox.showinfo("Copied", "Password copied to clipboard!",
                              parent=self.parent)