import tkinter as tk
from tkinter import ttk, messagebox
from app.models.database import Database

class AdminView(tk.Toplevel):
    def __init__(self, parent):
        """
        Initialize the admin view
        
        Args:
            parent: The parent widget
        """
        tk.Toplevel.__init__(self, parent)
        self.title("Admin Panel")
        self.geometry("800x500")
        self.db = Database()
        
        # Create a notebook (tabbed interface)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create the users tab
        self.users_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.users_frame, text="Users")
        
        # Create the images tab
        self.images_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.images_frame, text="Images")
        
        # Set up the users tab
        self._setup_users_tab()
        
        # Set up the images tab
        self._setup_images_tab()
    
    def _setup_users_tab(self):
        """
        Set up the users tab
        """
        # Create a frame for the user list
        self.users_list_frame = ttk.Frame(self.users_frame)
        self.users_list_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        
        # Create a frame for user details and editing
        self.user_details_frame = ttk.Frame(self.users_frame)
        self.user_details_frame.pack(side="right", fill="both", expand=True, padx=5, pady=5)
        
        # Create a treeview for the user list
        columns = ("ID", "Username")
        self.users_tree = ttk.Treeview(self.users_list_frame, columns=columns, show="headings")
        
        # Set column headings
        for col in columns:
            self.users_tree.heading(col, text=col)
            self.users_tree.column(col, width=100)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.users_list_frame, orient="vertical", command=self.users_tree.yview)
        self.users_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack the treeview and scrollbar
        self.users_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind the treeview selection event
        self.users_tree.bind("<<TreeviewSelect>>", self._on_user_select)
        
        # Create the user details form
        ttk.Label(self.user_details_frame, text="User Details", font=("Helvetica", 12, "bold")).grid(row=0, column=0, columnspan=2, pady=(0, 10))
        
        ttk.Label(self.user_details_frame, text="User ID:").grid(row=1, column=0, sticky="e", padx=(0, 10), pady=5)
        self.user_id_var = tk.StringVar()
        ttk.Entry(self.user_details_frame, textvariable=self.user_id_var, state="readonly").grid(row=1, column=1, pady=5)
        
        ttk.Label(self.user_details_frame, text="Username:").grid(row=2, column=0, sticky="e", padx=(0, 10), pady=5)
        self.username_var = tk.StringVar()
        ttk.Entry(self.user_details_frame, textvariable=self.username_var).grid(row=2, column=1, pady=5)
        
        ttk.Label(self.user_details_frame, text="New Password:").grid(row=3, column=0, sticky="e", padx=(0, 10), pady=5)
        self.password_var = tk.StringVar()
        ttk.Entry(self.user_details_frame, textvariable=self.password_var, show="*").grid(row=3, column=1, pady=5)
        
        # Create buttons for user management
        button_frame = ttk.Frame(self.user_details_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="Update User", command=self._update_user).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Delete User", command=self._delete_user).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Add New User", command=self._add_user).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Refresh", command=self._load_users).pack(side="left", padx=5)
        
        # Load the users
        self._load_users()
    
    def _setup_images_tab(self):
        """
        Set up the images tab
        """
        # Create a frame for the image list
        self.images_list_frame = ttk.Frame(self.images_frame)
        self.images_list_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Create a treeview for the image list
        columns = ("ID", "User ID", "Image Path", "Result", "Timestamp")
        self.images_tree = ttk.Treeview(self.images_list_frame, columns=columns, show="headings")
        
        # Set column headings
        for col in columns:
            self.images_tree.heading(col, text=col)
            self.images_tree.column(col, width=150)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.images_list_frame, orient="vertical", command=self.images_tree.yview)
        self.images_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack the treeview and scrollbar
        self.images_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Create buttons for image management
        button_frame = ttk.Frame(self.images_frame)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="Refresh", command=self._load_images).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Delete Selected", command=self._delete_image).pack(side="left", padx=5)
        
        # Load the images
        self._load_images()
    
    def _load_users(self):
        """
        Load the users from the database
        """
        # Clear the treeview
        for item in self.users_tree.get_children():
            self.users_tree.delete(item)
        
        # Connect to the database
        conn = self.db.connect()
        cursor = conn.cursor()
        
        # Get all users
        cursor.execute("SELECT user_id, username FROM users")
        users = cursor.fetchall()
        
        # Add users to the treeview
        for user in users:
            self.users_tree.insert("", "end", values=user)
        
        # Close the connection
        self.db.close()
    
    def _load_images(self):
        """
        Load the images from the database
        """
        # Clear the treeview
        for item in self.images_tree.get_children():
            self.images_tree.delete(item)
        
        # Connect to the database
        conn = self.db.connect()
        cursor = conn.cursor()
        
        # Get all images
        cursor.execute("SELECT image_id, user_id, image_path, result, timestamp FROM images")
        images = cursor.fetchall()
        
        # Add images to the treeview
        for image in images:
            self.images_tree.insert("", "end", values=image)
        
        # Close the connection
        self.db.close()
    
    def _on_user_select(self, event):
        """
        Handle the user selection event
        """
        # Get the selected item
        selected_item = self.users_tree.selection()
        if not selected_item:
            return
        
        # Get the user ID and username
        user_id, username = self.users_tree.item(selected_item, "values")
        
        # Update the user details form
        self.user_id_var.set(user_id)
        self.username_var.set(username)
        self.password_var.set("")
    
    def _update_user(self):
        """
        Update a user
        """
        # Get the user details
        user_id = self.user_id_var.get()
        username = self.username_var.get()
        password = self.password_var.get()
        
        if not user_id:
            messagebox.showerror("Error", "Please select a user")
            return
        
        if not username:
            messagebox.showerror("Error", "Username cannot be empty")
            return
        
        # Connect to the database
        conn = self.db.connect()
        cursor = conn.cursor()
        
        try:
            # Update the user
            if password:
                cursor.execute("UPDATE users SET username = ?, password = ? WHERE user_id = ?", 
                              (username, password, user_id))
            else:
                cursor.execute("UPDATE users SET username = ? WHERE user_id = ?", 
                              (username, user_id))
            
            conn.commit()
            messagebox.showinfo("Success", "User updated successfully")
            
            # Reload the users
            self._load_users()
        except Exception as e:
            messagebox.showerror("Error", f"Error updating user: {e}")
        finally:
            # Close the connection
            self.db.close()
    
    def _delete_user(self):
        """
        Delete a user
        """
        # Get the user ID
        user_id = self.user_id_var.get()
        
        if not user_id:
            messagebox.showerror("Error", "Please select a user")
            return
        
        # Confirm deletion
        if not messagebox.askyesno("Confirm", "Are you sure you want to delete this user? This will also delete all their images."):
            return
        
        # Connect to the database
        conn = self.db.connect()
        cursor = conn.cursor()
        
        try:
            # Delete the user's images
            cursor.execute("DELETE FROM images WHERE user_id = ?", (user_id,))
            
            # Delete the user
            cursor.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
            
            conn.commit()
            messagebox.showinfo("Success", "User deleted successfully")
            
            # Clear the user details form
            self.user_id_var.set("")
            self.username_var.set("")
            self.password_var.set("")
            
            # Reload the users and images
            self._load_users()
            self._load_images()
        except Exception as e:
            messagebox.showerror("Error", f"Error deleting user: {e}")
        finally:
            # Close the connection
            self.db.close()
    
    def _add_user(self):
        """
        Add a new user
        """
        # Get the username and password
        username = self.username_var.get()
        password = self.password_var.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password")
            return
        
        # Create a temporary controller to use the register method with admin privileges
        from app.controllers.main_controller import MainController
        temp_controller = MainController()
        
        try:
            # Add the user with admin privileges (is_admin_creation=True)
            success, error_message = temp_controller.auth_controller.register(username, password, is_admin_creation=True)
            
            if success:
                messagebox.showinfo("Success", "User added successfully")
                
                # Clear the user details form
                self.user_id_var.set("")
                self.username_var.set("")
                self.password_var.set("")
                
                # Reload the users
                self._load_users()
            else:
                messagebox.showerror("Error", error_message or "Error adding user")
        except Exception as e:
            messagebox.showerror("Error", f"Error adding user: {e}")

    
    def _delete_image(self):
        """
        Delete an image
        """
        # Get the selected item
        selected_item = self.images_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select an image")
            return
        
        # Get the image ID
        image_id = self.images_tree.item(selected_item, "values")[0]
        
        # Confirm deletion
        if not messagebox.askyesno("Confirm", "Are you sure you want to delete this image?"):
            return
        
        # Connect to the database
        conn = self.db.connect()
        cursor = conn.cursor()
        
        try:
            # Delete the image
            cursor.execute("DELETE FROM images WHERE image_id = ?", (image_id,))
            
            conn.commit()
            messagebox.showinfo("Success", "Image deleted successfully")
            
            # Reload the images
            self._load_images()
        except Exception as e:
            messagebox.showerror("Error", f"Error deleting image: {e}")
        finally:
            # Close the connection
            self.db.close()
