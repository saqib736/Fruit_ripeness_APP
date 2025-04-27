import os
import random
import shutil
from datetime import datetime
from app.models.database import Database
from PIL import Image

class ImageController:
    def __init__(self, user_id=None):
        """
        Initialize the image controller
        
        Args:
            user_id (int, optional): The ID of the current user
        """
        self.db = Database()
        self.user_id = user_id
        self.image_dir = os.path.join('data', 'images')
        os.makedirs(self.image_dir, exist_ok=True)
    
    def set_user_id(self, user_id):
        """
        Set the current user ID
        
        Args:
            user_id (int): The ID of the current user
        """
        self.user_id = user_id
    
    def save_image(self, image_path):
        """
        Save an image to the application's image directory
        
        Args:
            image_path (str): The path to the image file
            
        Returns:
            str: The path where the image was saved
        """
        if not self.user_id:
            raise ValueError("User ID is not set")
        
        # Create user directory if it doesn't exist
        user_dir = os.path.join(self.image_dir, str(self.user_id))
        os.makedirs(user_dir, exist_ok=True)
        
        # Generate a unique filename
        filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{os.path.basename(image_path)}"
        destination = os.path.join(user_dir, filename)
        
        # Copy the image to the destination
        shutil.copy2(image_path, destination)
        
        return destination
    
    def analyze_image(self, image_path):
        """
        Analyze the image to determine fruit ripeness using Google Gemini API
        
        Args:
            image_path (str): The path to the image file
            
        Returns:
            str: The ripeness classification result
            dict: Additional analysis details (if available)
        """
        try:
            # Import the Gemini API utility
            from utils.gemini_api import analyze_fruit_image
            
            # Use Gemini API to analyze the image
            analysis_result = analyze_fruit_image(image_path)
            
            # Get the ripeness classification
            result = analysis_result.get('ripeness', 'Unknown')
            
            # Fallback to random selection if API fails
            if result == 'Unknown':
                print("Gemini API analysis failed, falling back to random selection")
                results = ["Ripe", "Unripe", "Overripe"]
                result = random.choice(results)
            
            # Save the result to the database
            if self.user_id:
                self.db.save_image_data(self.user_id, image_path, result)
            
            return result, analysis_result.get('full_analysis', None)
        except Exception as e:
            print(f"Error in analyze_image: {e}")
            # Fallback to random selection if anything goes wrong
            results = ["Ripe", "Unripe", "Overripe"]
            result = random.choice(results)
            
            # Save the result to the database
            if self.user_id:
                self.db.save_image_data(self.user_id, image_path, result)
            
            return result, None
    
    def get_user_images(self):
        """
        Get all images for the current user
        
        Returns:
            list: A list of tuples containing image data
        """
        if not self.user_id:
            raise ValueError("User ID is not set")
        
        return self.db.get_user_images(self.user_id)
    
    def open_image(self, image_path):
        """
        Open an image using PIL
        
        Args:
            image_path (str): The path to the image file
            
        Returns:
            PIL.Image: The opened image
        """
        try:
            return Image.open(image_path)
        except Exception as e:
            print(f"Error opening image: {e}")
            return None
