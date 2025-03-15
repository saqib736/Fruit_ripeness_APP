from app.controllers.auth_controller import AuthController
from app.controllers.image_controller import ImageController

class MainController:
    def __init__(self):
        """
        Initialize the main controller
        """
        self.auth_controller = AuthController()
        self.image_controller = ImageController()
        self.current_user_id = None
        self.current_username = None
    
    def register_user(self, username, password):
        """
        Register a new user
        
        Args:
            username (str): The username for the new account
            password (str): The password for the new account
            
        Returns:
            tuple: (success, error_message) where success is a boolean indicating if
                  registration was successful, and error_message is a string with an
                  error message if registration failed, or None if successful
        """
        return self.auth_controller.register(username, password)
        
    def create_admin_user(self, admin_key, username, password):
        """
        Create an admin user with a special admin key
        
        Args:
            admin_key (str): The admin key to authorize admin creation
            username (str): The username for the admin account
            password (str): The password for the admin account
            
        Returns:
            tuple: (success, error_message) where success is a boolean indicating if
                  admin creation was successful, and error_message is a string with an
                  error message if creation failed, or None if successful
        """
        return self.auth_controller.create_admin_user(admin_key, username, password)
    
    def login_user(self, username, password):
        """
        Authenticate a user
        
        Args:
            username (str): The username to authenticate
            password (str): The password to authenticate
            
        Returns:
            bool: True if authentication was successful, False otherwise
        """
        user_id = self.auth_controller.login(username, password)
        if user_id:
            self.current_user_id = user_id
            self.current_username = username
            self.image_controller.set_user_id(user_id)
            return True
        return False
    
    def logout_user(self):
        """
        Log out the current user
        """
        self.current_user_id = None
        self.current_username = None
        self.image_controller.set_user_id(None)
    
    def save_and_analyze_image(self, image_path):
        """
        Save and analyze an image
        
        Args:
            image_path (str): The path to the image file
            
        Returns:
            tuple: (saved_path, result) where saved_path is the path where the image was saved
                  and result is the ripeness classification result
        """
        if not self.current_user_id:
            raise ValueError("User is not logged in")
        
        saved_path = self.image_controller.save_image(image_path)
        result = self.image_controller.analyze_image(saved_path)
        
        return saved_path, result
    
    def get_user_images(self):
        """
        Get all images for the current user
        
        Returns:
            list: A list of tuples containing image data
        """
        if not self.current_user_id:
            raise ValueError("User is not logged in")
        
        return self.image_controller.get_user_images()
    
    def is_logged_in(self):
        """
        Check if a user is currently logged in
        
        Returns:
            bool: True if a user is logged in, False otherwise
        """
        return self.current_user_id is not None
    
    def get_current_username(self):
        """
        Get the username of the currently logged in user
        
        Returns:
            str: The username of the current user, or None if no user is logged in
        """
        return self.current_username
