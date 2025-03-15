import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from app.views.auth_view import AuthView
from app.views.main_view import MainView
from app.controllers.main_controller import MainController
from utils.theme import ThemeManager

class AppView(tk.Tk):
    def __init__(self):
        """
        Initialize the main application window
        """
        tk.Tk.__init__(self)
        
        # Set window properties
        self.title("Fruit Ripeness Detection")
        self.geometry("900x600")  # Slightly larger for better UI
        self.resizable(True, True)
        
        # Set up the theme
        ThemeManager.setup_theme()
        ThemeManager.apply_to_window(self)
        
        # Set application icon (if available)
        try:
            icon_img = Image.open('resources/app_icon.png')
            icon_photo = ImageTk.PhotoImage(icon_img)
            self.iconphoto(True, icon_photo)
        except Exception as e:
            print(f"Could not load icon: {e}")  # Icon not found, continue without it
        
        # Initialize the main controller
        self.controller = MainController()
        
        # Create a container for the frames
        self.container = ttk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True, padx=20, pady=20)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        
        # Initialize the frames dictionary
        self.frames = {}
        
        # Create the authentication view
        self.auth_view = AuthView(self.container, self.controller)
        self.auth_view.grid(row=0, column=0, sticky="nsew")
        self.frames["auth"] = self.auth_view
        
        # Create the main view
        self.main_view = MainView(self.container, self.controller)
        self.main_view.grid(row=0, column=0, sticky="nsew")
        self.frames["main"] = self.main_view
        
        # Start with the authentication view
        self.show_auth_view()
    
    def show_auth_view(self):
        """
        Show the authentication view
        """
        self.frames["auth"].tkraise()
    
    def show_main_view(self):
        """
        Show the main view
        """
        self.frames["main"].update_welcome_message()
        self.frames["main"].tkraise()
