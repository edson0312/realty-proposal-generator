"""
WSGI configuration for PythonAnywhere deployment.

This file is used by PythonAnywhere to run your Flask application.
"""
import sys
import os

# Add your project directory to the sys.path
project_home = '/home/edson001/Sample-Computation'  # UPDATE THIS!
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Set environment variables
os.environ['FLASK_ENV'] = 'production'

# Import the Flask app
from app import create_app

application = create_app('production')

