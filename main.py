#!/usr/bin/env python3

import os
import sys
from app.views.app_view import AppView
from utils.logger import logger

def main():
    """
    Main entry point for the application
    """
    # Log application start
    logger.info("Starting Fruit Ripeness Detection Application")
    
    # Create data directories if they don't exist
    os.makedirs('data', exist_ok=True)
    os.makedirs('data/images', exist_ok=True)
    
    # Create and run the application
    app = AppView()
    app.mainloop()
    
    # Log application exit
    logger.info("Exiting Fruit Ripeness Detection Application")

if __name__ == "__main__":
    main()
