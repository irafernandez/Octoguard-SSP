"""
Main Application Window
"""

import tkinter as tk
from tkinter import ttk
from utils.constants import *
from ui.password_generator_view import PasswordGeneratorView
from ui.password_assessor_view import PasswordAssessorView
from ui.form_validator_view import FormValidatorView


class ModernButton(tk.Canvas):
    """Button widget"""

    def __init__(self, parent, text, command, **kwargs):
        self.bg_color = kwargs.get('bg_color', COLORS['accent_primary'])
        self.fg_color = kwargs.get('fg_color', '#000000')
        self.hover_color = kwargs.get('hover_color', COLORS['accent_primary_hover'])
        self.width = kwargs.get('width', 200)
        self.height = kwargs.get('height', BUTTON_HEIGHT)
        self.command = command
        self.text = text

        super().__init__(parent, width=self.width, height=self.height,
                        bg=parent['bg'], highlightthickness=0)

        self.rect = self.create_rectangle(0, 0, self.width, self.height,
                                         fill=self.bg_color, outline='')
        self.text_id = self.create_text(self.width/2, self.height/2,
                                       text=text, fill=self.fg_color,
                                       font=FONTS.get('button', FONT_FALLBACKS['button']))

        self.bind('<Button-1>', self._on_click)
        self.bind('<Enter>', self._on_enter)
        self.bind('<Leave>', self._on_leave)

    def _on_click(self, event):
        if self.command:
            self.command()

    def _on_enter(self, event):
        self.itemconfig(self.rect, fill=self.hover_color)
        self.config(cursor='hand2')

    def _on_leave(self, event):
        self.itemconfig(self.rect, fill=self.bg_color)
        self.config(cursor='')


class SecurityToolkit:
    def __init__(self, root):
        self.root = root
        self.root.title(APP_NAME)
        self.root.geometry(WINDOW_SIZE)
        self.root.configure(bg=COLORS['bg_primary'])

        # Remove default window styling
        self.root.resizable(True, True)

        # Setup styles
        self.setup_styles()

        # Create UI components
        self.create_header()
        self.create_sidebar()
        self.create_content_area()

        # Show password generator by default
        self.show_password_generator()

    def setup_styles(self):
        """Configure UI styles"""
        style = ttk.Style()
        style.theme_use('clam')

        # Configure scrollbar
        style.configure('Vertical.TScrollbar',
                       background=COLORS['bg_tertiary'],
                       troughcolor=COLORS['bg_secondary'],
                       borderwidth=0,
                       arrowcolor=COLORS['text_secondary'])

    def create_header(self):
        header = tk.Frame(self.root, bg=COLORS['bg_header'], height=HEADER_HEIGHT)
        header.pack(fill=tk.X, padx=0, pady=0)
        header.pack_propagate(False)

        # Left side - Logo and title
        left_frame = tk.Frame(header, bg=COLORS['bg_header'])
        left_frame.pack(side=tk.LEFT, padx=30, pady=0, fill=tk.Y)

        # Icon/Logo
        icon_label = tk.Label(left_frame, text="🐙",
                             font=('Segoe UI', 24),
                             bg=COLORS['bg_header'],
                             fg=COLORS['error'])
        icon_label.pack(side=tk.LEFT, padx=(0, 12))

        # Title and subtitle container
        text_frame = tk.Frame(left_frame, bg=COLORS['bg_header'])
        text_frame.pack(side=tk.LEFT)

        title_label = tk.Label(text_frame, text="OCTOGUARD",
                              font=FONTS.get('title', FONT_FALLBACKS['title']),
                              bg=COLORS['bg_header'],
                              fg=COLORS['text_primary'])
        title_label.pack(anchor=tk.W)

        subtitle = tk.Label(text_frame,
                           text="Swiss Knife Of Web Security",
                           font=FONTS.get('small', FONT_FALLBACKS['small']),
                           bg=COLORS['bg_header'],
                           fg=COLORS['text_tertiary'])
        subtitle.pack(anchor=tk.W)

        # Right side - Version badge
        version_frame = tk.Frame(header, bg=COLORS['bg_tertiary'])
        version_frame.pack(side=tk.RIGHT, padx=30, pady=20)

        version_label = tk.Label(version_frame, text=f"v{APP_VERSION}",
                                font=FONTS.get('small', FONT_FALLBACKS['small']),
                                bg=COLORS['bg_tertiary'],
                                fg=COLORS['text_secondary'],
                                padx=10, pady=4)
        version_label.pack()

    def create_sidebar(self):
        """Sidebar navigation"""
        sidebar = tk.Frame(self.root, bg=COLORS['nav_bg'], width=SIDEBAR_WIDTH)
        sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=0, pady=0)
        sidebar.pack_propagate(False)

        # Sidebar header
        nav_header = tk.Label(sidebar, text="TOOLS",
                             font=FONTS.get('small', FONT_FALLBACKS['small']),
                             bg=COLORS['nav_bg'],
                             fg=COLORS['text_muted'],
                             anchor=tk.W)
        nav_header.pack(fill=tk.X, padx=20, pady=(25, 10))

        # Navigation items
        self.nav_buttons = {}

        nav_items = [
            ("Password Generator", self.show_password_generator),
            ("Password Assessor", self.show_password_assessor),
            ("Form Validator", self.show_form_validator)
        ]

        for text, command in nav_items:
            self.create_nav_button(sidebar, text, command)

        # Footer section
        footer_frame = tk.Frame(sidebar, bg=COLORS['nav_bg'])
        footer_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=20, pady=20)

        footer_text = tk.Label(footer_frame,
                              text="© Milestone 1\n Built by Gino and Ira",
                              font=FONTS.get('small', FONT_FALLBACKS['small']),
                              bg=COLORS['nav_bg'],
                              fg=COLORS['text_muted'],
                              justify=tk.CENTER)
        footer_text.pack()

    def create_nav_button(self, parent, text, command):
        """Navigation button"""
        btn_frame = tk.Frame(parent, bg=COLORS['nav_bg'])
        btn_frame.pack(fill=tk.X, padx=15, pady=3)

        # Accent indicator (left border)
        accent = tk.Frame(btn_frame, bg=COLORS['nav_bg'], width=3)
        accent.pack(side=tk.LEFT, fill=tk.Y)

        # Button
        btn = tk.Label(btn_frame,
                      text=text,
                      font=FONTS.get('nav', FONT_FALLBACKS['nav']),
                      bg=COLORS['nav_bg'],
                      fg=COLORS['nav_text'],
                      anchor=tk.W,
                      padx=15,
                      pady=12,
                      cursor='hand2')
        btn.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Store references
        self.nav_buttons[text] = (btn_frame, btn, accent)

        # Bind events
        def on_click(e):
            command()

        def on_enter(e):
            if btn['bg'] != COLORS['nav_active_bg']:
                btn.config(bg=COLORS['nav_hover'])
                btn_frame.config(bg=COLORS['nav_hover'])

        def on_leave(e):
            if btn['bg'] != COLORS['nav_active_bg']:
                btn.config(bg=COLORS['nav_bg'])
                btn_frame.config(bg=COLORS['nav_bg'])

        btn.bind('<Button-1>', on_click)
        btn.bind('<Enter>', on_enter)
        btn.bind('<Leave>', on_leave)
        btn_frame.bind('<Button-1>', on_click)
        btn_frame.bind('<Enter>', on_enter)
        btn_frame.bind('<Leave>', on_leave)

    def create_content_area(self):
        """Main content area"""
        self.content_frame = tk.Frame(self.root, bg=COLORS['bg_primary'])
        self.content_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=25, pady=25)

    def clear_content(self):
        """Clear current content"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def update_nav_style(self, active_button):
        """Update navigation button styles"""
        for text, (frame, btn, accent) in self.nav_buttons.items():
            if text == active_button:
                frame.config(bg=COLORS['nav_active_bg'])
                btn.config(bg=COLORS['nav_active_bg'], fg=COLORS['nav_text_active'])
                accent.config(bg=COLORS['nav_active_accent'])
            else:
                frame.config(bg=COLORS['nav_bg'])
                btn.config(bg=COLORS['nav_bg'], fg=COLORS['nav_text'])
                accent.config(bg=COLORS['nav_bg'])

    def show_password_generator(self):
        """Display password generator view"""
        self.clear_content()
        self.update_nav_style("🔐 Password Generator")
        PasswordGeneratorView(self.content_frame)

    def show_password_assessor(self):
        """Display password assessor view"""
        self.clear_content()
        self.update_nav_style("📊 Password Assessor")
        PasswordAssessorView(self.content_frame)

    def show_form_validator(self):
        """Display form validator view"""
        self.clear_content()
        self.update_nav_style("✓ Form Validator")
        FormValidatorView(self.content_frame)