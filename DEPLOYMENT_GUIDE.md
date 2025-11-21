# PythonAnywhere Deployment Guide

This guide will help you deploy your Moldex Realty Proposal Generator to PythonAnywhere.

## Prerequisites

1. A PythonAnywhere account (free or paid)
   - Sign up at: https://www.pythonanywhere.com/
   - Free accounts support Python 3.10 and Flask applications

## Step-by-Step Deployment Instructions

### 1. Upload Your Code to PythonAnywhere

#### Option A: Using Git (Recommended)

1. **Push your code to GitHub:**
   ```bash
   # Initialize git repository (if not already done)
   git init
   git add .
   git commit -m "Initial commit for PythonAnywhere deployment"
   
   # Create a new repository on GitHub, then:
   git remote add origin https://github.com/edson0312/Sample-Computations.git
   git branch -M main
   git push -u origin main
   ```

2. **Clone on PythonAnywhere:**
   - Log in to PythonAnywhere
   - Go to "Consoles" → "Bash"
   - Run:
     ```bash
     cd ~
     git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git Sample-Computation
     cd Sample-Computation
     ```

#### Option B: Manual Upload

1. Go to "Files" tab in PythonAnywhere
2. Create a new directory: `Sample-Computation`
3. Upload all your project files manually

### 2. Set Up Virtual Environment

In the PythonAnywhere Bash console:

```bash
cd ~/Sample-Computation

# Create virtual environment
python3.10 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt
```

### 3. Create Required Directories

```bash
# Create uploads directory
mkdir -p uploads

# Create logs directory for production logging
mkdir -p logs

# Set proper permissions
chmod 755 uploads
chmod 755 logs
```

### 4. Configure Environment Variables

Create a `.env` file in your project directory:

```bash
nano .env
```

Add the following content (press Ctrl+X, then Y, then Enter to save):

```
SECRET_KEY=your-super-secret-key-change-this-to-random-string
FLASK_ENV=production
MAX_CONTENT_LENGTH=16777216
```

**Important:** Generate a strong SECRET_KEY. You can use this Python command:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### 5. Update WSGI Configuration

1. Go to the "Web" tab in PythonAnywhere
2. Click "Add a new web app"
3. Choose "Manual configuration" (not Flask wizard)
4. Select Python 3.10
5. Click through the setup

6. **Edit the WSGI configuration file:**
   - On the Web tab, click on the WSGI configuration file link
   - Replace ALL content with:

```python
import sys
import os

# Add your project directory to the sys.path
project_home = '/home/YOUR_PYTHONANYWHERE_USERNAME/Sample-Computation'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Activate virtual environment
activate_this = os.path.join(project_home, 'venv/bin/activate_this.py')
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

# Set environment to production
os.environ['FLASK_ENV'] = 'production'

# Import the Flask app
from app import create_app
application = create_app('production')
```

**IMPORTANT:** Replace `YOUR_PYTHONANYWHERE_USERNAME` with your actual PythonAnywhere username!

### 6. Configure Virtual Environment Path

Still on the Web tab:

1. Find the "Virtualenv" section
2. Enter the path to your virtual environment:
   ```
   /home/YOUR_PYTHONANYWHERE_USERNAME/Sample-Computation/venv
   ```
   (Replace `YOUR_PYTHONANYWHERE_USERNAME` with your username)

### 7. Configure Static Files (Optional but Recommended)

On the Web tab, scroll to "Static files" section and add:

| URL          | Directory                                                    |
|--------------|--------------------------------------------------------------|
| /static/     | /home/YOUR_USERNAME/Sample-Computation/app/static           |
| /uploads/    | /home/YOUR_USERNAME/Sample-Computation/uploads              |

### 8. Reload Your Web App

1. Scroll to the top of the Web tab
2. Click the big green "Reload" button
3. Wait for the reload to complete

### 9. Test Your Application

1. Your app will be available at: `https://YOUR_USERNAME.pythonanywhere.com`
2. Test all features:
   - Create a proposal with vertical property
   - Create a proposal with horizontal property
   - Upload images
   - Generate PDF
   - Download PDF

## Troubleshooting

### Error Logs

View error logs on the Web tab:
- Click on "Error log" link
- Check for any Python errors

### Common Issues

#### 1. "ImportError: No module named 'app'"
- Check that your WSGI file has the correct project path
- Ensure virtual environment is activated in WSGI file

#### 2. "500 Internal Server Error"
- Check the error log on the Web tab
- Verify all dependencies are installed: `pip list`
- Check file permissions: `ls -la ~/Sample-Computation`

#### 3. "File upload not working"
- Ensure uploads directory exists and has write permissions
- Check MAX_CONTENT_LENGTH in .env file

#### 4. "PDF not generating"
- Check that ReportLab is installed: `pip show reportlab`
- Verify Pillow is installed: `pip show Pillow`
- Check error logs for specific errors

#### 5. "Static files (CSS/JS) not loading"
- Verify static files mapping on Web tab
- Check that paths are correct
- Click "Reload" after changing static files configuration

### Debugging in Console

To test your app manually:

```bash
cd ~/Sample-Computation
source venv/bin/activate
python

>>> from app import create_app
>>> app = create_app('production')
>>> print(app.config['UPLOAD_FOLDER'])
```

## Updating Your Application

When you make changes to your code:

### If using Git:

```bash
cd ~/Sample-Computation
git pull origin main
source venv/bin/activate
pip install -r requirements.txt  # If dependencies changed
```

Then reload your web app from the Web tab.

### If uploading manually:

1. Upload changed files via Files tab
2. Reload your web app from the Web tab

## Free Account Limitations

PythonAnywhere free accounts have some limitations:

- Only HTTPS access to whitelisted sites (may affect external API calls)
- Limited CPU time per day
- App sleeps after inactivity (wakes up on first request)
- Custom domains not available (use USERNAME.pythonanywhere.com)

For production use with custom domain and better performance, consider upgrading to a paid plan.

## Security Recommendations

1. **Never commit `.env` file to Git** (already in .gitignore)
2. **Use a strong SECRET_KEY** in production
3. **Keep dependencies updated:**
   ```bash
   pip list --outdated
   pip install --upgrade package-name
   ```
4. **Regularly backup your data:**
   - Download generated PDFs periodically
   - Keep a backup of your code on GitHub

## Support

- PythonAnywhere Help: https://help.pythonanywhere.com/
- PythonAnywhere Forums: https://www.pythonanywhere.com/forums/
- Flask Documentation: https://flask.palletsprojects.com/

## Quick Reference Commands

```bash
# Activate virtual environment
cd ~/Sample-Computation
source venv/bin/activate

# Install/update packages
pip install -r requirements.txt

# Check installed packages
pip list

# View recent error logs
tail -f /var/log/YOUR_USERNAME.pythonanywhere.com.error.log

# Test import
python -c "from app import create_app; print('Success!')"
```

---

**Your app URL:** `https://YOUR_USERNAME.pythonanywhere.com`

Good luck with your deployment! 🚀

