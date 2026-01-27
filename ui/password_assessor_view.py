import tkinter as tk
from tkinter import messagebox
from modules.password_assessor import assess_password_strength
from utils.constants import *


class PasswordAssessorView:
    """Password strength assessor interface"""

    def __init__(self, parent):
        self.parent = parent
        self.create_view()

    def create_view(self):
        """Create the password assessor interface"""
        # Header section
        header_frame = tk.Frame(self.parent, bg=COLORS['bg_primary'])
        header_frame.pack(fill=tk.X, pady=(0, 20))

        title = tk.Label(header_frame, text="Password Strength Assessor",
                        font=FONTS.get('heading', FONT_FALLBACKS['heading']),
                        bg=COLORS['bg_primary'],
                        fg=COLORS['text_primary'])
        title.pack(anchor=tk.W, side=tk.LEFT)

        # Status indicator
        status_badge = tk.Label(header_frame, text="● ANALYZING",
                               font=FONTS.get('small', FONT_FALLBACKS['small']),
                               bg=COLORS['bg_tertiary'],
                               fg=COLORS['info'],
                               padx=10, pady=4)
        status_badge.pack(side=tk.RIGHT)

        desc = tk.Label(self.parent,
                       text="Real-time password security analysis with comprehensive feedback",
                       font=FONTS.get('small', FONT_FALLBACKS['small']),
                       bg=COLORS['bg_primary'],
                       fg=COLORS['text_tertiary'])
        desc.pack(anchor=tk.W, pady=(0, 25))

        # Input card
        input_card = self.create_card(self.parent, "Input Password")

        # Password input with show/hide toggle
        input_container = tk.Frame(input_card, bg=COLORS['bg_secondary'])
        input_container.pack(fill=tk.X, pady=15)

        tk.Label(input_container, text="Enter Password to Analyze",
                font=FONTS.get('small', FONT_FALLBACKS['small']),
                bg=COLORS['bg_secondary'],
                fg=COLORS['text_muted']).pack(anchor=tk.W, pady=(0, 8))

        # Input field with modern styling
        input_frame = tk.Frame(input_container, bg=COLORS['bg_tertiary'])
        input_frame.pack(fill=tk.X)

        self.password_entry = tk.Entry(input_frame,
                                       bg=COLORS['bg_tertiary'],
                                       fg=COLORS['input_text'],
                                       font=FONTS.get('body', FONT_FALLBACKS['body']),
                                       relief=tk.FLAT,
                                       show="●",
                                       insertbackground=COLORS['accent_primary'])
        self.password_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=12, pady=12)
        self.password_entry.bind('<KeyRelease>', lambda e: self.analyze_password())

        # Toggle visibility button
        self.show_password = False
        self.toggle_btn = tk.Label(input_frame, text="👁",
                                   font=('Segoe UI', 12),
                                   bg=COLORS['bg_tertiary'],
                                   fg=COLORS['text_muted'],
                                   cursor='hand2',
                                   padx=12)
        self.toggle_btn.pack(side=tk.RIGHT)
        self.toggle_btn.bind('<Button-1>', self.toggle_password_visibility)

        # Analyze button
        analyze_btn = self.create_button(input_card, "Analyze Strength",
                                        self.analyze_password)
        analyze_btn.pack(pady=(20, 0))

        # Results card
        results_card = self.create_card(self.parent, "Security Analysis")

        # Strength meter
        meter_frame = tk.Frame(results_card, bg=COLORS['bg_secondary'])
        meter_frame.pack(fill=tk.X, pady=(15, 20))

        self.strength_canvas = tk.Canvas(meter_frame,
                                        height=8,
                                        bg=COLORS['bg_secondary'],
                                        highlightthickness=0)
        self.strength_canvas.pack(fill=tk.X)

        # Rating display
        self.rating_frame = tk.Frame(results_card, bg=COLORS['bg_tertiary'])
        self.rating_frame.pack(fill=tk.X, pady=(0, 20))

        self.rating_label = tk.Label(self.rating_frame,
                                     text="",
                                     font=('Inter', 24, 'bold'),
                                     bg=COLORS['bg_tertiary'],
                                     pady=20)
        self.rating_label.pack()

        # Feedback section
        feedback_header = tk.Label(results_card, text="Security Recommendations",
                                   font=FONTS.get('subheading', FONT_FALLBACKS['subheading']),
                                   bg=COLORS['bg_secondary'],
                                   fg=COLORS['text_secondary'])
        feedback_header.pack(anchor=tk.W, pady=(10, 10))

        self.feedback_frame = tk.Frame(results_card, bg=COLORS['bg_secondary'])
        self.feedback_frame.pack(fill=tk.BOTH, expand=True)

    def create_card(self, parent, title):
        """Create a card container"""
        card = tk.Frame(parent, bg=COLORS['bg_secondary'])
        card.pack(fill=tk.BOTH, expand=True, pady=(0, 20))

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

    def toggle_password_visibility(self, event=None):
        """Toggle password visibility"""
        self.show_password = not self.show_password
        if self.show_password:
            self.password_entry.config(show="")
            self.toggle_btn.config(fg=COLORS['accent_primary'])
        else:
            self.password_entry.config(show="●")
            self.toggle_btn.config(fg=COLORS['text_muted'])

    def update_strength_meter(self, strength_percent, color):
        """Update visual strength meter"""
        self.strength_canvas.delete('all')
        width = self.strength_canvas.winfo_width()
        if width < 2:
            width = 400

        # Background bar
        self.strength_canvas.create_rectangle(0, 0, width, 8,
                                             fill=COLORS['bg_tertiary'], outline='')

        # Strength bar
        filled_width = int(width * strength_percent / 100)
        if filled_width > 0:
            self.strength_canvas.create_rectangle(0, 0, filled_width, 8,
                                                 fill=color, outline='')

    def analyze_password(self):
        """Handle password analysis"""
        password = self.password_entry.get()

        if not password:
            self.rating_label.config(text="", fg=COLORS['text_secondary'])
            self.update_strength_meter(0, COLORS['bg_tertiary'])
            for widget in self.feedback_frame.winfo_children():
                widget.destroy()
            return

        # Assess password strength
        rating, color, feedback = assess_password_strength(password)

        # Map rating to strength percentage
        strength_map = {"WEAK": 33, "MODERATE": 66, "STRONG": 100}
        strength_percent = strength_map.get(rating, 0)

        # Update meter
        self.update_strength_meter(strength_percent, color)

        # Update rating display
        self.rating_label.config(text=f"{rating}", fg=color)

        # Update feedback
        for widget in self.feedback_frame.winfo_children():
            widget.destroy()

        for item in feedback:
            self.create_feedback_item(item)

    def create_feedback_item(self, text):
        """Create a feedback list item"""
        item_frame = tk.Frame(self.feedback_frame, bg=COLORS['bg_tertiary'])
        item_frame.pack(fill=tk.X, pady=3)

        # Icon based on feedback type
        icon = "✓" if text.startswith("+") else "•" if text.startswith("-") else "!"
        icon_color = COLORS['success'] if text.startswith("+") else COLORS['text_tertiary']

        icon_label = tk.Label(item_frame, text=icon,
                             font=FONTS.get('body', FONT_FALLBACKS['body']),
                             bg=COLORS['bg_tertiary'],
                             fg=icon_color,
                             width=3)
        icon_label.pack(side=tk.LEFT, padx=(10, 5), pady=8)

        text_label = tk.Label(item_frame, text=text,
                             font=FONTS.get('small', FONT_FALLBACKS['small']),
                             bg=COLORS['bg_tertiary'],
                             fg=COLORS['text_secondary'],
                             anchor=tk.W)
        text_label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10), pady=8)