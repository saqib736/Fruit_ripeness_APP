from app.models.database import Database

class AuthController:
    def __init__(self):
        """
        Initialize the authentication controller
        """
        self.db = Database()
    
    def register(self, username, password, is_admin_creation=False):
        """
        Register a new user
        
        Args:
            username (str): The username for the new account
            password (str): The password for the new account
            is_admin_creation (bool): Whether this user is being created by an admin
            
        Returns:
            bool: True if registration was successful, False otherwise
            str: Error message if registration failed, None otherwise
        """
        # Check if trying to register as admin
        if username.lower() == 'admin' and not is_admin_creation:
            # Only allow admin registration with a special admin key or from admin panel
            return False, "The username 'admin' is reserved. Please choose another username."
            
        # In a real application, you would hash the password here
        # For simplicity, we're storing the password as plain text
        # This is NOT recommended for production applications
        success = self.db.register_user(username, password)
        return success, None if success else "Username already exists"
        
    def create_admin_user(self, admin_key, username, password):
        """
        Create an admin user with a special admin key
        
        Args:
            admin_key (str): The admin key to authorize admin creation
            username (str): The username for the admin account
            password (str): The password for the admin account
            
        Returns:
            bool: True if admin creation was successful, False otherwise
            str: Error message if creation failed, None otherwise
        """
        # In a real application, you would validate the admin key against a secure value
        # For this demo, we'll use a simple hardcoded key
        if admin_key != "fruit_admin_2025":
            return False, "Invalid admin key"
            
        return self.register(username, password, True)
    
    def login(self, username, password):
        """
        Authenticate a user
        
        Args:
            username (str): The username to authenticate
            password (str): The password to authenticate
            
        Returns:
            int or None: user_id if authentication was successful, None otherwise
        """
        # In a real application, you would verify the hashed password
        return self.db.authenticate_user(username, password)
