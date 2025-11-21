# Quick Reference Card - PythonAnywhere Deployment

## 🚀 Deploy in 5 Steps

### 1️⃣ Upload Code
```bash
# In PythonAnywhere Bash console
cd ~
git clone YOUR_REPO_URL Sample-Computation
cd Sample-Computation
```

### 2️⃣ Setup Environment
```bash
# Run the automated setup script
bash setup_pythonanywhere.sh

# OR manually:
python3.10 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
mkdir -p uploads logs
```

### 3️⃣ Configure .env
```bash
nano .env
```
Add:
```
SECRET_KEY=<run: python -c "import secrets; print(secrets.token_hex(32))">
FLASK_ENV=production
MAX_CONTENT_LENGTH=16777216
```

### 4️⃣ Configure Web App
**Web Tab → WSGI Configuration File:**
```python
import sys
import os

project_home = '/home/YOUR_USERNAME/Sample-Computation'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

activate_this = os.path.join(project_home, 'venv/bin/activate_this.py')
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

os.environ['FLASK_ENV'] = 'production'

from app import create_app
application = create_app('production')
```

**Web Tab → Virtualenv:**
```
/home/YOUR_USERNAME/Sample-Computation/venv
```

### 5️⃣ Reload & Test
- Click green "Reload" button
- Visit: `https://YOUR_USERNAME.pythonanywhere.com`

---

## 🔧 Common Commands

### Check Status
```bash
cd ~/Sample-Computation
source venv/bin/activate
python -c "from app import create_app; print('OK')"
```

### Update App
```bash
cd ~/Sample-Computation
git pull
source venv/bin/activate
pip install -r requirements.txt
# Then reload from Web tab
```

### View Logs
```bash
tail -f /var/log/YOUR_USERNAME.pythonanywhere.com.error.log
```

### Check Dependencies
```bash
source venv/bin/activate
pip list
```

---

## 📁 Important Files

| File | Purpose |
|------|---------|
| `run.py` | Local development entry point |
| `wsgi.py` | PythonAnywhere WSGI template |
| `config.py` | Configuration (dev/production) |
| `requirements.txt` | Python dependencies |
| `.env` | Environment variables (SECRET!) |
| `DEPLOYMENT_GUIDE.md` | Full instructions |
| `DEPLOYMENT_CHECKLIST.md` | Step-by-step checklist |

---

## 🆘 Troubleshooting

| Problem | Solution |
|---------|----------|
| 500 Error | Check error log on Web tab |
| Import Error | Verify WSGI config paths |
| Upload Fails | Check `uploads/` permissions |
| PDF Error | Verify ReportLab installed |
| CSS Not Loading | Add static files mapping |

---

## 🔗 URLs

- **Your App**: `https://YOUR_USERNAME.pythonanywhere.com`
- **Dashboard**: `https://www.pythonanywhere.com/user/YOUR_USERNAME/`
- **Help**: `https://help.pythonanywhere.com/`

---

## ✅ Test Checklist

- [ ] App loads
- [ ] Forms work
- [ ] Image upload
- [ ] PDF generation
- [ ] PDF download
- [ ] All calculations correct

---

**Need more details?** See `DEPLOYMENT_GUIDE.md`

