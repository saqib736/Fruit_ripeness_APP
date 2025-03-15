import tkinter as tk
from tkinter import ttk
import os

class ThemeManager:
    """
    Manages the application theme and styling
    """
    # Modern color palette
    COLORS = {
        "primary": "#4a6fa5",      # Deep blue
        "primary_dark": "#3d5a8c", # Darker blue for hover effects
        "secondary": "#6fb98f",    # Mint green
        "accent": "#ff7e67",       # Coral
        "warning": "#ffd166",      # Amber
        "error": "#ef476f",        # Pink/Red
        "success": "#06d6a0",      # Teal
        "background": "#f7f9fb",   # Light gray-blue
        "card": "#ffffff",         # White
        "text": "#2d3142",         # Dark blue-gray
        "text_secondary": "#8d99ae" # Light blue-gray
    }
    
    # Font settings
    FONTS = {
        "heading": ("Helvetica", 16, "bold"),
        "subheading": ("Helvetica", 14, "bold"),
        "body": ("Helvetica", 11),
        "button": ("Helvetica", 10, "bold"),
        "small": ("Helvetica", 9)
    }
    
    @classmethod
    def setup_theme(cls):
        """
        Set up the application theme
        """
        style = ttk.Style()
        
        # Configure the base theme
        style.theme_use('clam')  # Use clam as base theme
        
        # Configure common elements
        style.configure('TFrame', background=cls.COLORS["background"])
        style.configure('TLabel', background=cls.COLORS["background"], foreground=cls.COLORS["text"])
        style.configure('TButton', 
                        background=cls.COLORS["primary"], 
                        foreground="white", 
                        font=cls.FONTS["button"],
                        borderwidth=0,
                        focusthickness=3,
                        focuscolor=cls.COLORS["primary_dark"])
        style.map('TButton',
                  background=[('active', cls.COLORS["primary_dark"])],
                  foreground=[('active', 'white')])
        
        # Entry fields
        style.configure('TEntry', 
                        fieldbackground=cls.COLORS["card"],
                        foreground=cls.COLORS["text"],
                        borderwidth=1,
                        relief="solid",
                        padding=5)
        
        # Notebook (tabs)
        style.configure('TNotebook', background=cls.COLORS["background"])
        style.configure('TNotebook.Tab', 
                        background=cls.COLORS["background"],
                        foreground=cls.COLORS["text"],
                        padding=[10, 5],
                        font=cls.FONTS["button"])
        style.map('TNotebook.Tab',
                  background=[('selected', cls.COLORS["primary"])],
                  foreground=[('selected', 'white')])
        
        # Treeview (for lists)
        style.configure('Treeview', 
                        background=cls.COLORS["card"],
                        foreground=cls.COLORS["text"],
                        rowheight=25,
                        fieldbackground=cls.COLORS["card"])
        style.configure('Treeview.Heading', 
                        background=cls.COLORS["primary"],
                        foreground="white",
                        font=cls.FONTS["button"])
        style.map('Treeview',
                  background=[('selected', cls.COLORS["primary"])],
                  foreground=[('selected', 'white')])
        
        # Custom styles
        style.configure('Card.TFrame', background=cls.COLORS["card"], relief="raised", borderwidth=1)
        style.configure('Header.TLabel', 
                        font=cls.FONTS["heading"], 
                        background=cls.COLORS["background"],
                        foreground=cls.COLORS["primary"])
        style.configure('Subheader.TLabel', 
                        font=cls.FONTS["subheading"], 
                        background=cls.COLORS["background"],
                        foreground=cls.COLORS["text"])
        
        # Success button
        style.configure('Success.TButton', 
                        background=cls.COLORS["success"], 
                        foreground="white")
        style.map('Success.TButton',
                  background=[('active', cls.COLORS["success"])])
        
        # Warning button
        style.configure('Warning.TButton', 
                        background=cls.COLORS["warning"], 
                        foreground=cls.COLORS["text"])
        style.map('Warning.TButton',
                  background=[('active', cls.COLORS["warning"])])
        
        # Danger button
        style.configure('Danger.TButton', 
                        background=cls.COLORS["error"], 
                        foreground="white")
        style.map('Danger.TButton',
                  background=[('active', cls.COLORS["error"])])
    
    @classmethod
    def apply_to_window(cls, window):
        """
        Apply theme settings to a window
        """
        window.configure(background=cls.COLORS["background"])
        
    @classmethod
    def create_custom_button(cls, parent, text, command, style="TButton", **kwargs):
        """
        Create a custom styled button
        """
        button = ttk.Button(parent, text=text, command=command, style=style, **kwargs)
        return button
    
    @classmethod
    def create_rounded_button(cls, parent, text, command, bg_color=None, fg_color="white", **kwargs):
        """
        Create a button with rounded corners (using standard tk Button as ttk doesn't support this)
        """
        if bg_color is None:
            bg_color = cls.COLORS["primary"]
            
        button = tk.Button(parent, 
                          text=text, 
                          command=command,
                          background=bg_color,
                          foreground=fg_color,
                          font=cls.FONTS["button"],
                          borderwidth=0,
                          padx=15,
                          pady=5,
                          highlightthickness=0,
                          activebackground=cls.COLORS["primary_dark"],
                          activeforeground="white",
                          **kwargs)
        return button
    
    @classmethod
    def create_header_label(cls, parent, text, **kwargs):
        """
        Create a header label
        """
        label = ttk.Label(parent, text=text, style="Header.TLabel", **kwargs)
        return label
    
    @classmethod
    def create_subheader_label(cls, parent, text, **kwargs):
        """
        Create a subheader label
        """
        label = ttk.Label(parent, text=text, style="Subheader.TLabel", **kwargs)
        return label
    
    @classmethod
    def create_card_frame(cls, parent, **kwargs):
        """
        Create a card-style frame
        """
        frame = ttk.Frame(parent, style="Card.TFrame", padding=15, **kwargs)
        return frame
