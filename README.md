# Fruit Ripeness Detection Application

A simple desktop application for fruit ripeness detection built with Python and Tkinter.

## Features

- User Management (Registration and Login)
- Image Upload and Display
- Basic Fruit Ripeness Analysis (currently a placeholder)
- Image History Tracking
- SQLite Database for Data Storage

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

## Usage

Run the application using:

```bash
python main.py
```

## Future Enhancements

- Integration with an actual AI model for fruit ripeness detection
- Advanced image preprocessing
- More detailed analysis results
- User profile management
- Export functionality for analysis results

## Dependencies

- Python 3.6+
- Tkinter (GUI library)
- Pillow (PIL) for image processing
- OpenCV for computer vision tasks
- NumPy for numerical operations
- Matplotlib for visualization
- Pandas for data manipulation
- SQLite for database operations
