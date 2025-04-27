# Fruit Ripeness Detection Application

A desktop application for fruit ripeness detection built with Python, Tkinter, and Google Gemini AI.

## Features

- User Management (Registration and Login)
- Image Upload and Display
- AI-Powered Fruit Ripeness Analysis using Google Gemini API
- Automatic Fruit Type Detection
- Image History Tracking
- SQLite Database for Data Storage
- Modern UI with Responsive Design

## Project Structure

```
Fruit_ripeness_APP/
├── app/                   # Application core components
│   ├── controllers/       # Application controllers
│   ├── models/            # Database models
│   └── views/             # UI components
├── data/                  # Data storage
│   ├── images/            # Uploaded images
│   └── fruit_app.db       # SQLite database
├── logs/                  # Application logs
├── resources/             # Static resources
├── utils/                 # Utility modules
├── main.py                # Application entry point
├── README.md              # Project documentation
└── requirements.txt       # Dependencies
```

## Installation

### Setting up a Virtual Environment (Recommended)

1. Clone the repository
2. Navigate to the project directory
3. On Debian/Ubuntu systems, you may need to install the python3-venv package first:

```bash
sudo apt install python3-venv
# Or for a specific Python version
sudo apt install python3.10-venv
```

4. Create a virtual environment:

```bash
# For Windows
python -m venv venv

# For macOS/Linux
python3 -m venv venv
```

4. Activate the virtual environment:

```bash
# For Windows
venv\Scripts\activate

# For macOS/Linux
source venv/bin/activate
```

5. Install the required dependencies:

```bash
pip install -r requirements.txt
```

### System Requirements

This application requires Python 3.6 or higher. On Linux systems, you may need to install additional system packages:

```bash
# For Tkinter
sudo apt-get install python3-tk

# For PIL ImageTk
sudo apt-get install python3-pil.imagetk
```

## API Configuration

This application uses the Google Gemini API for fruit ripeness detection. You need to set up an API key to use this feature:

1. Get a Google Gemini API key from [Google AI Studio](https://ai.google.dev/)
2. Create a `.env` file in the project root directory
3. Add your API key to the `.env` file:

```
GEMINI_API_KEY=your_api_key_here
```

If you don't have an API key, the application will fall back to random selection for ripeness detection.

## Usage

1. Run the application:

```bash
python main.py
```

2. Register a new account or log in with an existing account
3. Upload a fruit image using the 'Upload Image' button
4. Click 'Analyze Image' to detect the fruit type and ripeness level
5. View your analysis history with the 'View History' button

## Admin Access

To access the admin panel:
1. Register with the username 'admin'
2. The admin panel button will appear on the main screen after login

## Future Enhancements

- Support for more fruit types and conditions
- Advanced image preprocessing for better analysis
- Offline analysis mode with local ML models
- User profile management and preferences
- Export functionality for analysis results and reports
- Mobile application version

## Dependencies

- Python 3.6+
- Tkinter (GUI library)
- Pillow (PIL) for image processing
- OpenCV for computer vision tasks
- NumPy for numerical operations
- Google Generative AI library for Gemini API integration
- python-dotenv for environment variable management
- Matplotlib for visualization
- Pandas for data manipulation
- SQLite for database operations
