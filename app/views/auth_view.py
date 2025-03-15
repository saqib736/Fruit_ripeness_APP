import tkinter as tk
from tkinter import messagebox, ttk
from utils.theme import ThemeManager
import os
from PIL import Image, ImageTk

class AuthView(tk.Frame):
    def __init__(self, parent, controller):
        """
        Initialize the authentication view
        
        Args:
            parent: The parent widget
            controller: The main controller
        """
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.parent = parent
        
        # Main container with background color
        self.configure(background=ThemeManager.COLORS["background"])
        
        # Create a card-style frame for the authentication form
        self.auth_frame = ThemeManager.create_card_frame(self)
        self.auth_frame.pack(fill="none", expand=True, padx=50, pady=50)
        
        # Logo/Image section (if available)
        self.image_frame = ttk.Frame(self.auth_frame)
        self.image_frame.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Try to load and display a logo
        logo_path = os.path.join('resources', 'fruit_logo.png')
        if os.path.exists(logo_path):
            try:
                logo_img = Image.open(logo_path)
                logo_img = logo_img.resize((150, 150), Image.LANCZOS)
                self.logo_photo = ImageTk.PhotoImage(logo_img)
                logo_label = ttk.Label(self.image_frame, image=self.logo_photo, background=ThemeManager.COLORS["card"])
                logo_label.pack()
            except Exception as e:
                print(f"Error loading logo: {e}")
        
        # Title label
        self.title_label = ThemeManager.create_header_label(self.auth_frame, text="Fruit Ripeness Detection")
        self.title_label.grid(row=1, column=0, columnspan=2, pady=(0, 20))
        
        # Username label and entry
        self.username_label = ttk.Label(self.auth_frame, text="Username:", background=ThemeManager.COLORS["card"])
        self.username_label.grid(row=2, column=0, sticky="e", padx=(0, 10), pady=10)
        
        self.username_entry = ttk.Entry(self.auth_frame, width=30)
        self.username_entry.grid(row=2, column=1, pady=10, sticky="ew")
        
        # Password label and entry
        self.password_label = ttk.Label(self.auth_frame, text="Password:", background=ThemeManager.COLORS["card"])
        self.password_label.grid(row=3, column=0, sticky="e", padx=(0, 10), pady=10)
        
        self.password_entry = ttk.Entry(self.auth_frame, width=30, show="•")  # Using a bullet character for password
        self.password_entry.grid(row=3, column=1, pady=10, sticky="ew")
        
        # Buttons frame
        self.buttons_frame = ttk.Frame(self.auth_frame, style="Card.TFrame")
        self.buttons_frame.grid(row=4, column=0, columnspan=2, pady=(20, 10))
        
        # Login button
        self.login_button = ThemeManager.create_rounded_button(
            self.buttons_frame, 
            text="Login", 
            command=self.login,
            bg_color=ThemeManager.COLORS["primary"]
        )
        self.login_button.pack(side="left", padx=10)
        
        # Register button
        self.register_button = ThemeManager.create_rounded_button(
            self.buttons_frame, 
            text="Register", 
            command=self.register,
            bg_color=ThemeManager.COLORS["secondary"]
        )
        self.register_button.pack(side="left", padx=10)
        
        # Admin registration link
        self.admin_link = ttk.Label(
            self.auth_frame, 
            text="Register as Admin", 
            foreground=ThemeManager.COLORS["primary"],
            cursor="hand2",
            background=ThemeManager.COLORS["card"]
        )
        self.admin_link.grid(row=5, column=0, columnspan=2, pady=(15, 0))
        self.admin_link.bind("<Button-1>", lambda e: self.show_admin_register())
        
        # Add a subtle hover effect to the admin link
        self.admin_link.bind("<Enter>", lambda e: self.admin_link.configure(foreground=ThemeManager.COLORS["primary_dark"], font=("Helvetica", 9, "underline")))
        self.admin_link.bind("<Leave>", lambda e: self.admin_link.configure(foreground=ThemeManager.COLORS["primary"], font=("Helvetica", 9)))
        
        # Bind Enter key to login
        self.password_entry.bind("<Return>", lambda event: self.login())
    
    def login(self):
        """
        Handle the login button click
        """
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password")
            return
        
        if self.controller.login_user(username, password):
            # Clear the entries
            self.username_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)
            
            # Switch to the main view
            if hasattr(self.parent, 'show_main_view'):
                self.parent.show_main_view()
            else:
                # If we're in the app_view, we need to access the parent differently
                self.parent.master.show_main_view()
        else:
            messagebox.showerror("Error", "Invalid username or password")
    
    def show_admin_register(self):
        """
        Show the admin registration view
        """
        try:
            from app.views.admin_register_view import AdminRegisterView
            admin_register = AdminRegisterView(self, self.controller)
        except Exception as e:
            messagebox.showerror("Error", f"Error showing admin registration: {e}")
    
    def register(self):
        """
        Handle the register button click
        """
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password")
            return
        
        success, error_message = self.controller.register_user(username, password)
        
        if success:
            messagebox.showinfo("Success", "Registration successful! You can now login.")
            # Clear the entries
            self.username_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", error_message or "Registration failed")
