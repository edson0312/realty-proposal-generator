# PythonAnywhere Deployment Guide

## Moldex Realty Proposal Generator - Complete Deployment Instructions

**Username**: `edson001`  
**Web App URL**: `https://edson001.pythonanywhere.com`

---

## Prerequisites

1. A PythonAnywhere account (Free or Paid)
2. Your code pushed to GitHub: `https://github.com/edson0312/realty-proposal-generator`

---

## Step-by-Step Deployment

### Step 1: Log into PythonAnywhere

1. Go to https://www.pythonanywhere.com
2. Log in with username: `edson001`

### Step 2: Open a Bash Console

1. Click on the **"Consoles"** tab
2. Click **"Bash"** to start a new bash console

### Step 3: Clone Your Repository

In the bash console, run:

```bash
cd ~
git clone https://github.com/edson0312/realty-proposal-generator.git
cd realty-proposal-generator
```

### Step 4: Create Virtual Environment

```bash
python3.10 -m venv venv
source venv/bin/activate
```

### Step 5: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 6: Create Required Directories

```bash
mkdir -p uploads
mkdir -p logs
chmod 755 uploads
chmod 755 logs
```

### Step 7: Create .env File

```bash
nano .env
```

Add the following content (press Ctrl+O to save, Ctrl+X to exit):

```env
SECRET_KEY=CHANGE-THIS-TO-A-RANDOM-SECRET-KEY
FLASK_ENV=production
MAX_CONTENT_LENGTH=16777216
```

**Generate a secure SECRET_KEY:**

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Copy the output and replace `CHANGE-THIS-TO-A-RANDOM-SECRET-KEY` in your .env file.

### Step 8: Test the Application

```bash
python -c "from app import create_app; app = create_app('production'); print('Success!')"
```

If you see "Success!", continue to the next step.

---

## Step 9: Configure Web App

### 9.1: Create a New Web App

1. Go to the **"Web"** tab in PythonAnywhere
2. Click **"Add a new web app"**
3. Choose **"Manual configuration"** (NOT Flask)
4. Select **Python 3.10**

### 9.2: Configure Source Code

In the Web tab, find the **"Code"** section:

- **Source code**: `/home/edson001/realty-proposal-generator`
- **Working directory**: `/home/edson001/realty-proposal-generator`

### 9.3: Configure Virtual Environment

In the **"Virtualenv"** section:

- Enter: `/home/edson001/realty-proposal-generator/venv`
- Click the checkmark to save

### 9.4: Configure WSGI File

1. Click on the **WSGI configuration file** link (it will be something like `/var/www/edson001_pythonanywhere_com_wsgi.py`)
2. **Delete all the existing content**
3. Replace with this:

```python
"""
WSGI configuration for PythonAnywhere deployment.
"""
import sys
import os

# Add your project directory to the sys.path
project_home = '/home/edson001/realty-proposal-generator'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Set environment variables
os.environ['FLASK_ENV'] = 'production'

# Import the Flask app
from app import create_app

application = create_app('production')
```

4. Click **"Save"** (top right)

### 9.5: Configure Static Files

In the **"Static files"** section, add:

| URL | Directory |
|-----|-----------|
| `/static/` | `/home/edson001/realty-proposal-generator/app/static` |

Click the checkmark to save.

---

## Step 10: Reload Your Web App

1. Scroll to the top of the Web tab
2. Click the big green **"Reload edson001.pythonanywhere.com"** button
3. Wait for the reload to complete

---

## Step 11: Test Your Application

1. Open your browser
2. Go to: `https://edson001.pythonanywhere.com`
3. You should see the Moldex Realty Proposal Generator!

---

## Troubleshooting

### Error: "Something went wrong"

1. Check the **Error log** in the Web tab
2. Common issues:
   - Missing dependencies: Reinstall with `pip install -r requirements.txt`
   - Wrong Python version: Make sure you selected Python 3.10
   - WSGI file errors: Double-check the paths in the WSGI file

### Error: "ModuleNotFoundError"

Make sure your virtual environment is activated and all dependencies are installed:

```bash
cd ~/realty-proposal-generator
source venv/bin/activate
pip install -r requirements.txt
```

Then reload the web app.

### Error: "Permission denied" for uploads

```bash
cd ~/realty-proposal-generator
chmod 755 uploads
chmod 755 logs
```

### Static files not loading

1. Check the Static files configuration in the Web tab
2. Make sure the path is: `/home/edson001/realty-proposal-generator/app/static`
3. Reload the web app

---

## Updating Your Application

When you make changes to your code:

1. **Push changes to GitHub** (from your local machine):
   ```bash
   git add .
   git commit -m "Your commit message"
   git push origin main
   ```

2. **Pull changes on PythonAnywhere** (in bash console):
   ```bash
   cd ~/realty-proposal-generator
   git pull origin main
   ```

3. **Reload the web app** (in Web tab):
   - Click the green "Reload" button

---

## Important Notes

### Free Account Limitations

- Your app will be available at: `edson001.pythonanywhere.com`
- Limited CPU time per day
- App may sleep after inactivity (wakes up on first request)
- No custom domain (upgrade to paid plan for custom domains)

### File Uploads

- Uploaded files are stored in `/home/edson001/realty-proposal-generator/uploads`
- Free accounts have limited disk space (512MB)
- Consider cleaning up old files periodically

### Logs

- Application logs: `/home/edson001/realty-proposal-generator/logs/app.log`
- Error logs: Available in the Web tab
- Server logs: Available in the Web tab

---

## Security Checklist

- ✅ SECRET_KEY is set to a random value (not the default)
- ✅ FLASK_ENV is set to 'production'
- ✅ .env file is not committed to Git (check .gitignore)
- ✅ Debug mode is disabled in production
- ✅ CSRF protection is enabled

---

## Quick Reference Commands

### Access your app directory:
```bash
cd ~/realty-proposal-generator
```

### Activate virtual environment:
```bash
source venv/bin/activate
```

### Update dependencies:
```bash
pip install -r requirements.txt
```

### Pull latest code:
```bash
git pull origin main
```

### Check logs:
```bash
tail -f logs/app.log
```

### Generate new SECRET_KEY:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

---

## Support

- PythonAnywhere Help: https://help.pythonanywhere.com
- PythonAnywhere Forums: https://www.pythonanywhere.com/forums/
- Your GitHub Repo: https://github.com/edson0312/realty-proposal-generator

---

**Deployment Date**: November 21, 2024  
**Version**: 1.0.0  
**Python Version**: 3.10  
**Framework**: Flask

