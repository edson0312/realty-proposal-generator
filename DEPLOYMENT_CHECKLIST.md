# PythonAnywhere Deployment Checklist

Use this checklist to ensure a smooth deployment to PythonAnywhere.

## Pre-Deployment Checklist

### Local Preparation

- [ ] All code is working locally (test with `python run.py`)
- [ ] All dependencies are listed in `requirements.txt`
- [ ] `.gitignore` is configured properly
- [ ] `.env` file exists locally (but NOT committed to git)
- [ ] All sensitive data is in `.env` (not hardcoded)
- [ ] Code is pushed to GitHub (or ready for manual upload)

### PythonAnywhere Account

- [ ] PythonAnywhere account created
- [ ] Logged in to PythonAnywhere dashboard
- [ ] Know your PythonAnywhere username

## Deployment Steps

### 1. Upload Code

**If using Git:**
- [ ] Opened PythonAnywhere Bash console
- [ ] Cloned repository: `git clone <your-repo-url> Sample-Computation`
- [ ] Navigated to project: `cd Sample-Computation`

**If manual upload:**
- [ ] Created directory `Sample-Computation` in Files tab
- [ ] Uploaded all project files

### 2. Environment Setup

- [ ] Created virtual environment: `python3.10 -m venv venv`
- [ ] Activated venv: `source venv/bin/activate`
- [ ] Upgraded pip: `pip install --upgrade pip`
- [ ] Installed dependencies: `pip install -r requirements.txt`
- [ ] Verified installation: `pip list`

### 3. Directory Structure

- [ ] Created `uploads` directory: `mkdir -p uploads`
- [ ] Created `logs` directory: `mkdir -p logs`
- [ ] Set permissions: `chmod 755 uploads logs`
- [ ] Verified structure: `ls -la`

### 4. Environment Variables

- [ ] Created `.env` file: `nano .env`
- [ ] Generated SECRET_KEY: `python -c "import secrets; print(secrets.token_hex(32))"`
- [ ] Added SECRET_KEY to `.env`
- [ ] Set FLASK_ENV=production in `.env`
- [ ] Saved and closed `.env` file

### 5. Web App Configuration

- [ ] Went to "Web" tab in PythonAnywhere
- [ ] Clicked "Add a new web app"
- [ ] Selected "Manual configuration"
- [ ] Selected Python 3.10
- [ ] Completed web app creation

### 6. WSGI Configuration

- [ ] Clicked WSGI configuration file link on Web tab
- [ ] Replaced content with WSGI configuration from `wsgi.py`
- [ ] Updated `YOUR_PYTHONANYWHERE_USERNAME` with actual username
- [ ] Saved WSGI file

### 7. Virtual Environment Path

- [ ] Found "Virtualenv" section on Web tab
- [ ] Entered path: `/home/YOUR_USERNAME/Sample-Computation/venv`
- [ ] Replaced YOUR_USERNAME with actual username
- [ ] Saved configuration

### 8. Static Files (Optional)

- [ ] Added static files mapping:
  - URL: `/static/` → Directory: `/home/YOUR_USERNAME/Sample-Computation/app/static`
  - URL: `/uploads/` → Directory: `/home/YOUR_USERNAME/Sample-Computation/uploads`

### 9. First Launch

- [ ] Clicked green "Reload" button on Web tab
- [ ] Waited for reload to complete
- [ ] Checked for errors in error log

### 10. Testing

- [ ] Opened app URL: `https://YOUR_USERNAME.pythonanywhere.com`
- [ ] Tested client details form
- [ ] Tested vertical property type
- [ ] Tested horizontal property type
- [ ] Uploaded test image
- [ ] Generated test PDF
- [ ] Downloaded PDF successfully
- [ ] Verified all calculations are correct
- [ ] Tested all payment terms

## Post-Deployment

### Verification

- [ ] App loads without errors
- [ ] All forms work correctly
- [ ] Image uploads work
- [ ] PDF generation works
- [ ] PDF downloads work
- [ ] All computations are accurate
- [ ] Mobile responsive (test on phone)

### Documentation

- [ ] Saved app URL
- [ ] Documented any custom configurations
- [ ] Shared URL with stakeholders

### Monitoring

- [ ] Bookmarked error log URL
- [ ] Set up regular check schedule
- [ ] Documented how to update app

## Troubleshooting Reference

If something doesn't work:

1. **Check Error Log** (Web tab → Error log link)
2. **Verify Paths** (all paths should use your actual username)
3. **Test Import** in Bash console:
   ```bash
   cd ~/Sample-Computation
   source venv/bin/activate
   python -c "from app import create_app; print('Success!')"
   ```
4. **Check Permissions**: `ls -la ~/Sample-Computation`
5. **Reinstall Dependencies**: `pip install -r requirements.txt --force-reinstall`
6. **Reload Web App** after any changes

## Common Issues

| Issue | Solution |
|-------|----------|
| 500 Error | Check error log, verify WSGI config |
| Import Error | Check virtual environment path |
| File Upload Fails | Check uploads directory permissions |
| PDF Not Generating | Verify ReportLab and Pillow installed |
| Static Files 404 | Check static files mapping on Web tab |

## Update Procedure

When you need to update your app:

- [ ] Make changes locally and test
- [ ] Push to GitHub (if using Git)
- [ ] SSH to PythonAnywhere Bash console
- [ ] Navigate to project: `cd ~/Sample-Computation`
- [ ] Pull changes: `git pull origin main`
- [ ] Activate venv: `source venv/bin/activate`
- [ ] Update dependencies (if changed): `pip install -r requirements.txt`
- [ ] Go to Web tab
- [ ] Click "Reload" button
- [ ] Test changes

## Support Resources

- **PythonAnywhere Help**: https://help.pythonanywhere.com/
- **PythonAnywhere Forums**: https://www.pythonanywhere.com/forums/
- **Flask Docs**: https://flask.palletsprojects.com/
- **Project README**: See README.md
- **Deployment Guide**: See DEPLOYMENT_GUIDE.md

---

**Deployment Date**: _______________  
**Deployed By**: _______________  
**App URL**: https://_______________. pythonanywhere.com  
**Notes**: _______________

