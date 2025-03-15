import tkinter as tk
from tkinter import messagebox, ttk
from utils.theme import ThemeManager, ttk

class AdminRegisterView(tk.Toplevel):
    def __init__(self, parent, controller):
        """
        Initialize the admin registration view
        
        Args:
            parent: The parent widget
            controller: The main controller
        """
        tk.Toplevel.__init__(self, parent)
        self.title("Admin Registration")
        self.geometry("600x400")
        self.controller = controller
        
        # Configure the view with background color
        self.configure(background=ThemeManager.COLORS["background"])
        
        # Create a card-style frame for the registration form
        self.register_frame = ThemeManager.create_card_frame(self)
        self.register_frame.pack(fill="none", expand=True, padx=50, pady=50)
        
        # Title label
        self.title_label = ThemeManager.create_header_label(self.register_frame, text="Admin Registration", background=ThemeManager.COLORS["card"])
        self.title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Admin key label and entry
        self.admin_key_label = ttk.Label(self.register_frame, text="Admin Key:", background=ThemeManager.COLORS["card"])
        self.admin_key_label.grid(row=1, column=0, sticky="e", padx=(0, 10), pady=10)
        
        self.admin_key_entry = ttk.Entry(self.register_frame, width=30, show="•")  # Using bullet character
        self.admin_key_entry.grid(row=1, column=1, pady=10, sticky="ew")
        
        # Username label and entry
        self.username_label = ttk.Label(self.register_frame, text="Username:", background=ThemeManager.COLORS["card"])
        self.username_label.grid(row=2, column=0, sticky="e", padx=(0, 10), pady=10)
        
        self.username_entry = ttk.Entry(self.register_frame, width=30)
        self.username_entry.grid(row=2, column=1, pady=10, sticky="ew")
        
        # Password label and entry
        self.password_label = ttk.Label(self.register_frame, text="Password:", background=ThemeManager.COLORS["card"])
        self.password_label.grid(row=3, column=0, sticky="e", padx=(0, 10), pady=10)
        
        self.password_entry = ttk.Entry(self.register_frame, width=30, show="•")  # Using bullet character
        self.password_entry.grid(row=3, column=1, pady=10, sticky="ew")
        
        # Buttons frame
        self.buttons_frame = ttk.Frame(self.register_frame, style="Card.TFrame")
        self.buttons_frame.grid(row=4, column=0, columnspan=2, pady=(20, 10))
        
        # Register button
        self.register_button = ThemeManager.create_rounded_button(
            self.buttons_frame, 
            text="Register Admin", 
            command=self.register_admin,
            bg_color=ThemeManager.COLORS["primary"]
        )
        self.register_button.pack(side="left", padx=10)
        
        # Back button
        self.back_button = ThemeManager.create_rounded_button(
            self.buttons_frame, 
            text="Back", 
            command=self.destroy,
            bg_color=ThemeManager.COLORS["secondary"]
        )
        self.back_button.pack(side="left", padx=10)
        
        # Bind Enter key to register
        self.password_entry.bind("<Return>", lambda event: self.register_admin())
    
    def register_admin(self):
        """
        Handle the register admin button click
        """
        admin_key = self.admin_key_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if not admin_key or not username or not password:
            messagebox.showerror("Error", "Please fill in all fields")
            return
        
        success, error_message = self.controller.create_admin_user(admin_key, username, password)
        
        if success:
            messagebox.showinfo("Success", "Admin registration successful! You can now login.")
            self.destroy()
        else:
            messagebox.showerror("Error", error_message or "Admin registration failed")
