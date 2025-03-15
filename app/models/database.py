import sqlite3
import os
import datetime

class Database:
    def __init__(self, db_path='data/fruit_app.db'):
        """
        Initialize the database connection
        """
        # Ensure the directory exists
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        self.db_path = db_path
        self.conn = None
        self.create_tables()
    
    def connect(self):
        """
        Create a connection to the SQLite database
        """
        self.conn = sqlite3.connect(self.db_path)
        return self.conn
    
    def close(self):
        """
        Close the database connection
        """
        if self.conn:
            self.conn.close()
    
    def create_tables(self):
        """
        Create the necessary tables if they don't exist
        """
        conn = self.connect()
        cursor = conn.cursor()
        
        # Create users table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
        ''')
        
        # Create images table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS images (
            image_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            image_path TEXT NOT NULL,
            result TEXT,
            timestamp TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
        ''')
        
        conn.commit()
        self.close()
    
    def register_user(self, username, password):
        """
        Register a new user
        """
        conn = self.connect()
        cursor = conn.cursor()
        
        try:
            cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', 
                          (username, password))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            # Username already exists
            return False
        finally:
            self.close()
    
    def authenticate_user(self, username, password):
        """
        Authenticate a user
        """
        conn = self.connect()
        cursor = conn.cursor()
        
        cursor.execute('SELECT user_id FROM users WHERE username = ? AND password = ?', 
                      (username, password))
        user = cursor.fetchone()
        self.close()
        
        if user:
            return user[0]  # Return user_id
        return None
    
    def save_image_data(self, user_id, image_path, result):
        """
        Save image data to the database
        """
        conn = self.connect()
        cursor = conn.cursor()
        
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        cursor.execute('INSERT INTO images (user_id, image_path, result, timestamp) VALUES (?, ?, ?, ?)', 
                      (user_id, image_path, result, timestamp))
        conn.commit()
        self.close()
        
    def get_user_images(self, user_id):
        """
        Get all images for a specific user
        """
        conn = self.connect()
        cursor = conn.cursor()
        
        cursor.execute('SELECT image_id, image_path, result, timestamp FROM images WHERE user_id = ? ORDER BY timestamp DESC', 
                      (user_id,))
        images = cursor.fetchall()
        self.close()
        
        return images
