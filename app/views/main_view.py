import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import os
from utils.theme import ThemeManager

class MainView(tk.Frame):
    def __init__(self, parent, controller):
        """
        Initialize the main view
        
        Args:
            parent: The parent widget
            controller: The main controller
        """
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.parent = parent
        self.current_image_path = None
        self.photo_image = None  # Keep a reference to prevent garbage collection
        
        # Configure the main view
        self.configure(background=ThemeManager.COLORS["background"])
        
        # Create the main frame
        self.main_frame = ttk.Frame(self, padding=20)
        self.main_frame.pack(fill="both", expand=True)
        
        # Header with welcome message and logout button
        self.header_frame = ttk.Frame(self.main_frame)
        self.header_frame.pack(fill="x", pady=(0, 20))
        
        # App title and welcome message
        self.title_frame = ttk.Frame(self.header_frame)
        self.title_frame.pack(side="left")
        
        self.app_title = ThemeManager.create_header_label(self.title_frame, text="Fruit Ripeness Detection")
        self.app_title.pack(anchor="w")
        
        self.welcome_label = ThemeManager.create_subheader_label(self.title_frame, text="Welcome")
        self.welcome_label.pack(anchor="w")
        
        # User controls
        self.user_controls = ttk.Frame(self.header_frame)
        self.user_controls.pack(side="right", padx=10, pady=10)
        
        self.logout_button = ThemeManager.create_rounded_button(
            self.user_controls, 
            text="Logout", 
            command=self.logout,
            bg_color=ThemeManager.COLORS["primary"]
        )
        self.logout_button.pack(side="right")
        
        # Create a frame for the image and controls
        self.content_frame = ttk.Frame(self.main_frame)
        self.content_frame.pack(fill="both", expand=True)
        
        # Left side - Image upload and display
        self.left_frame = ThemeManager.create_card_frame(self.content_frame)
        self.left_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        
        # Image section title
        self.image_title = ThemeManager.create_subheader_label(
            self.left_frame, 
            text="Image Upload",
            background=ThemeManager.COLORS["card"]
        )
        self.image_title.pack(anchor="w", pady=(0, 10))
        
        # Upload button with icon if available
        self.upload_button = ThemeManager.create_rounded_button(
            self.left_frame, 
            text="Upload Image", 
            command=self.upload_image,
            bg_color=ThemeManager.COLORS["secondary"]
        )
        self.upload_button.pack(pady=(0, 15))
        
        # Image display area - with a border and better styling
        self.image_frame = ttk.Frame(self.left_frame, style="Card.TFrame", width=400, height=300)
        self.image_frame.pack(fill="both", expand=True)
        self.image_frame.pack_propagate(False)  # Prevent frame from shrinking
        
        self.image_label = ttk.Label(
            self.image_frame, 
            text="No image uploaded\n\nClick 'Upload Image' to select a fruit image",
            background=ThemeManager.COLORS["card"],
            foreground=ThemeManager.COLORS["text_secondary"],
            anchor="center",
            justify="center"
        )
        self.image_label.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Right side - Analysis and results
        self.right_frame = ThemeManager.create_card_frame(self.content_frame)
        self.right_frame.pack(side="right", fill="both", padx=10, pady=10, expand=True)
        
        # Analysis section title
        self.analysis_title = ThemeManager.create_subheader_label(
            self.right_frame, 
            text="Analysis Tools",
            background=ThemeManager.COLORS["card"]
        )
        self.analysis_title.pack(anchor="w", pady=(0, 15))
        
        # Analyze button with a different color
        self.analyze_button = ThemeManager.create_rounded_button(
            self.right_frame, 
            text="Analyze Image", 
            command=self.analyze_image,
            bg_color=ThemeManager.COLORS["accent"],
            state="disabled"
        )
        self.analyze_button.pack(pady=(0, 20))
        
        # Results section with card styling
        self.results_title = ThemeManager.create_subheader_label(
            self.right_frame, 
            text="Results",
            background=ThemeManager.COLORS["card"]
        )
        self.results_title.pack(anchor="w", pady=(0, 10))
        
        self.results_frame = ttk.Frame(self.right_frame, style="Card.TFrame")
        self.results_frame.pack(fill="both", expand=True, pady=(0, 20))
        
        # Create a styled result frame
        self.result_box = ttk.Frame(
            self.results_frame,
            style="Card.TFrame",
            padding=15
        )
        self.result_box.pack(fill="x", pady=10)
        
        # Result label with better styling
        self.result_label = ttk.Label(
            self.result_box, 
            text="No analysis performed yet",
            background=ThemeManager.COLORS["card"],
            foreground=ThemeManager.COLORS["text_secondary"],
            font=("Helvetica", 16, "bold"),
            padding=10
        )
        self.result_label.pack(expand=True, fill="both")
        
        # Configure the result_box to center its content
        self.result_box.columnconfigure(0, weight=1)
        self.result_box.rowconfigure(0, weight=1)
        
        # Buttons container
        self.buttons_container = ttk.Frame(self.right_frame, style="Card.TFrame")
        self.buttons_container.pack(fill="x", pady=10)
        
        # History button
        self.history_button = ThemeManager.create_rounded_button(
            self.buttons_container, 
            text="View History", 
            command=self.show_history,
            bg_color=ThemeManager.COLORS["primary"]
        )
        self.history_button.pack(side="left", padx=5)
        
        # Admin panel button (only shown for admin users)
        self.admin_button = ThemeManager.create_rounded_button(
            self.buttons_container, 
            text="Admin Panel", 
            command=self.show_admin_panel,
            bg_color=ThemeManager.COLORS["warning"],
            fg_color=ThemeManager.COLORS["text"]
        )
        # Initially hide the admin button - will be shown only for admin users
        # self.admin_button.pack(side="left", padx=5)
    
    def update_welcome_message(self):
        """
        Update the welcome message with the current username
        """
        username = self.controller.get_current_username()
        if username:
            self.welcome_label.config(text=f"Welcome, {username}!")
            
            # Show admin button for admin users (in this case, just for 'admin' username)
            if username.lower() == 'admin':
                self.admin_button.pack(side="left", padx=5)
            else:
                self.admin_button.pack_forget()
    
    def logout(self):
        """
        Handle the logout button click
        """
        self.controller.logout_user()
        self.reset_view()
        
        # Handle different parent types
        if hasattr(self.parent, 'show_auth_view'):
            self.parent.show_auth_view()
        else:
            # If we're in the app_view, we need to access the parent differently
            self.parent.master.show_auth_view()
            
            # Reset admin button state
            if hasattr(self, 'admin_button'):
                self.admin_button.pack_forget()
    
    def reset_view(self):
        """
        Reset the view to its initial state
        """
        self.current_image_path = None
        self.photo_image = None
        self.image_label.config(text="No image uploaded", image="")
        self.analyze_button.config(state="disabled")
        self.result_label.config(text="No analysis performed yet")
    
    def upload_image(self):
        """
        Handle the upload image button click
        """
        file_path = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")]
        )
        
        if file_path:
            self.current_image_path = file_path
            self.display_image(file_path)
            self.analyze_button.config(state="normal")
    
    def display_image(self, image_path):
        """
        Display an image in the image label
        
        Args:
            image_path (str): The path to the image file
        """
        try:
            # Open the image and resize it to fit the frame
            image = Image.open(image_path)
            image = self.resize_image(image, 380, 300)
            
            # Convert to PhotoImage and display
            self.photo_image = ImageTk.PhotoImage(image)
            self.image_label.config(text="", image=self.photo_image)
        except Exception as e:
            messagebox.showerror("Error", f"Error displaying image: {e}")
    
    def resize_image(self, image, max_width, max_height):
        """
        Resize an image to fit within the specified dimensions while maintaining aspect ratio
        
        Args:
            image (PIL.Image): The image to resize
            max_width (int): The maximum width
            max_height (int): The maximum height
            
        Returns:
            PIL.Image: The resized image
        """
        width, height = image.size
        ratio = min(max_width / width, max_height / height)
        new_width = int(width * ratio)
        new_height = int(height * ratio)
        return image.resize((new_width, new_height), Image.LANCZOS)
    
    def analyze_image(self):
        """
        Handle the analyze image button click
        """
        if not self.current_image_path:
            messagebox.showerror("Error", "Please upload an image first")
            return
        
        try:
            # Save and analyze the image
            saved_path, result, analysis_details = self.controller.save_and_analyze_image(self.current_image_path)
            
            # Extract fruit name and condition from analysis_details if available
            fruit_name = "Fruit"  # Default value
            if analysis_details:
                # Try to extract the fruit name from the analysis
                lower_analysis = analysis_details.lower()
                common_fruits = ["apple", "banana", "orange", "strawberry", "mango", "pear", "grape", "pineapple", "kiwi", "avocado", "watermelon", "peach", "plum", "cherry", "lemon", "lime", "blueberry", "raspberry"]
                
                for fruit in common_fruits:
                    if fruit in lower_analysis:
                        fruit_name = fruit.capitalize()
                        break
            
            # Update the result label with styled text including fruit name
            self.result_label.config(text=f"{fruit_name}: {result}", anchor="center", justify="center")
            
            # We'll hide the detailed analysis as requested
            # If we previously had an analysis frame, hide it
            if hasattr(self, 'analysis_frame'):
                self.analysis_frame.pack_forget()
            if hasattr(self, 'analysis_title'):
                self.analysis_title.pack_forget()
            
            # Change the color based on the result
            if result == "Ripe":
                self.result_label.config(foreground=ThemeManager.COLORS["success"], font=("Helvetica", 12, "bold"))
            elif result == "Unripe":
                self.result_label.config(foreground=ThemeManager.COLORS["warning"], font=("Helvetica", 12, "bold"))
            elif result == "Overripe":
                self.result_label.config(foreground=ThemeManager.COLORS["error"], font=("Helvetica", 12, "bold"))
            
            messagebox.showinfo("Analysis Complete", f"The {fruit_name.lower()} is {result.lower()}")
        except Exception as e:
            messagebox.showerror("Error", f"Error analyzing image: {e}")
    
    def show_admin_panel(self):
        """
        Show the admin panel
        """
        try:
            from app.views.admin_view import AdminView
            admin_view = AdminView(self)
        except Exception as e:
            messagebox.showerror("Error", f"Error showing admin panel: {e}")
    
    def show_analysis_details(self, result, analysis_details):
        """
        Display detailed analysis from the Gemini API in a new window
        
        Args:
            result (str): The ripeness classification result
            analysis_details (str): The detailed analysis from the Gemini API
        """
        # Create a new top-level window
        details_window = tk.Toplevel(self)
        details_window.title(f"Detailed Analysis - {result}")
        details_window.geometry("600x500")
        details_window.configure(background=ThemeManager.COLORS["background"])
        
        # Create a frame for the content
        content_frame = ThemeManager.create_card_frame(details_window)
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Add a title
        title_label = ThemeManager.create_header_label(
            content_frame, 
            text=f"AI Analysis Result: {result}",
            background=ThemeManager.COLORS["card"]
        )
        title_label.pack(pady=(10, 20), anchor="w")
        
        # Add a subtitle
        subtitle_label = ThemeManager.create_subheader_label(
            content_frame,
            text="Powered by Google Gemini AI",
            background=ThemeManager.COLORS["card"],
            foreground=ThemeManager.COLORS["text_secondary"]
        )
        subtitle_label.pack(pady=(0, 20), anchor="w")
        
        # Create a frame for the analysis text with scrollbars
        text_frame = ttk.Frame(content_frame)
        text_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Add scrollbars
        scrollbar_y = ttk.Scrollbar(text_frame, orient="vertical")
        scrollbar_y.pack(side="right", fill="y")
        
        scrollbar_x = ttk.Scrollbar(text_frame, orient="horizontal")
        scrollbar_x.pack(side="bottom", fill="x")
        
        # Add a text widget for the analysis
        analysis_text = tk.Text(
            text_frame,
            wrap="word",
            bg=ThemeManager.COLORS["card_secondary"],
            fg=ThemeManager.COLORS["text"],
            font=("Helvetica", 10),
            padx=10,
            pady=10,
            height=15,
            width=70
        )
        analysis_text.pack(fill="both", expand=True)
        
        # Connect the scrollbars
        analysis_text.config(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        scrollbar_y.config(command=analysis_text.yview)
        scrollbar_x.config(command=analysis_text.xview)
        
        # Insert the analysis text
        analysis_text.insert("1.0", analysis_details)
        analysis_text.config(state="disabled")  # Make it read-only
        
        # Add a close button
        close_button = ThemeManager.create_rounded_button(
            details_window,
            text="Close",
            command=details_window.destroy,
            bg_color=ThemeManager.COLORS["primary"]
        )
        close_button.pack(pady=15)
    
    def show_history(self):
        """
        Show the user's image history
        """
        try:
            images = self.controller.get_user_images()
            if not images:
                messagebox.showinfo("History", "No images found in history")
                return
            
            # Create a new window for the history
            history_window = tk.Toplevel(self)
            history_window.title("Image History")
            history_window.geometry("600x400")
            
            # Create a treeview to display the history
            columns = ("ID", "Image", "Result", "Timestamp")
            tree = ttk.Treeview(history_window, columns=columns, show="headings")
            
            # Set column headings
            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=100)
            
            # Add data to the treeview
            for image_id, image_path, result, timestamp in images:
                tree.insert("", "end", values=(image_id, os.path.basename(image_path), result, timestamp))
            
            # Add scrollbar
            scrollbar = ttk.Scrollbar(history_window, orient="vertical", command=tree.yview)
            tree.configure(yscrollcommand=scrollbar.set)
            
            # Pack the treeview and scrollbar
            tree.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            
            # Add a button to close the window
            close_button = tk.Button(history_window, text="Close", command=history_window.destroy)
            close_button.pack(pady=10)
        except Exception as e:
            messagebox.showerror("Error", f"Error showing history: {e}")
