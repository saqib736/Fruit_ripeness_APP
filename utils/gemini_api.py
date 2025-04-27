import os
import base64
import google.generativeai as genai
from dotenv import load_dotenv
from PIL import Image

# Load environment variables from .env file
load_dotenv()

def initialize_gemini_api():
    """
    Initialize the Gemini API with the API key from environment variables
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable is not set")
    
    genai.configure(api_key=api_key)

def analyze_fruit_image(image_path):
    """
    Analyze a fruit image using Google Gemini API to determine ripeness
    
    Args:
        image_path (str): Path to the fruit image
        
    Returns:
        dict: A dictionary containing ripeness status and detailed analysis
    """
    try:
        # Initialize the API
        initialize_gemini_api()
        
        # Load the image
        image = Image.open(image_path)
        
        # Set up the model
        model = genai.GenerativeModel('gemini-2.5-pro-exp-03-25')
        
        # Create the prompt
        prompt = """
        Analyze this fruit image and determine its ripeness level. 
        Classify it as one of the following: 'Ripe', 'Unripe', or 'Overripe'.
        
        Provide a brief explanation for your classification based on visual cues like color, texture, and any visible defects.
        
        Format your response as a JSON-like structure with the following fields:
        - ripeness: The classification ('Ripe', 'Unripe', or 'Overripe')
        - confidence: A percentage (0-100) indicating your confidence in this classification
        - explanation: A brief explanation of why you classified it this way
        - visual_cues: A list of visual cues that led to this classification
        """
        
        # Generate the response
        response = model.generate_content([prompt, image])
        
        # Parse the response
        response_text = response.text
        
        # Extract the ripeness classification
        if "Ripe" in response_text and not "Unripe" in response_text:
            ripeness = "Ripe"
        elif "Unripe" in response_text:
            ripeness = "Unripe"
        elif "Overripe" in response_text:
            ripeness = "Overripe"
        else:
            ripeness = "Unknown"
        
        # Return the result
        return {
            "ripeness": ripeness,
            "full_analysis": response_text
        }
    
    except Exception as e:
        print(f"Error analyzing image with Gemini API: {e}")
        return {
            "ripeness": "Unknown",
            "full_analysis": f"Error: {str(e)}"
        }
