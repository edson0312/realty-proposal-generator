#!/bin/bash
# Quick setup script for PythonAnywhere
# Run this in the PythonAnywhere Bash console after cloning/uploading your code

echo "=========================================="
echo "Moldex Realty App - PythonAnywhere Setup"
echo "=========================================="
echo ""

# Navigate to project directory
cd ~/Sample-Computation || { echo "Error: Project directory not found!"; exit 1; }

echo "✓ In project directory: $(pwd)"
echo ""

# Create virtual environment
echo "Creating virtual environment..."
python3.10 -m venv venv
echo "✓ Virtual environment created"
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"
echo ""

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip
echo "✓ pip upgraded"
echo ""

# Install dependencies
echo "Installing dependencies from requirements.txt..."
pip install -r requirements.txt
echo "✓ Dependencies installed"
echo ""

# Create necessary directories
echo "Creating required directories..."
mkdir -p uploads
mkdir -p logs
chmod 755 uploads
chmod 755 logs
echo "✓ Directories created (uploads, logs)"
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠ WARNING: .env file not found!"
    echo "Creating template .env file..."
    cat > .env << 'EOF'
SECRET_KEY=CHANGE-THIS-TO-A-RANDOM-SECRET-KEY
FLASK_ENV=production
MAX_CONTENT_LENGTH=16777216
EOF
    echo "✓ Template .env created"
    echo ""
    echo "⚠ IMPORTANT: Edit .env and set a secure SECRET_KEY!"
    echo "   Generate one with: python -c \"import secrets; print(secrets.token_hex(32))\""
    echo ""
else
    echo "✓ .env file exists"
    echo ""
fi

# Test import
echo "Testing Flask app import..."
python -c "from app import create_app; app = create_app('production'); print('✓ Flask app import successful!')" || {
    echo "✗ Error: Flask app import failed!"
    echo "Please check the error messages above."
    exit 1
}
echo ""

# Display next steps
echo "=========================================="
echo "Setup Complete! ✓"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Edit .env file and set a secure SECRET_KEY"
echo "2. Go to PythonAnywhere Web tab"
echo "3. Configure WSGI file (see DEPLOYMENT_GUIDE.md)"
echo "4. Set virtualenv path: $(pwd)/venv"
echo "5. Reload your web app"
echo ""
echo "Your app will be available at:"
echo "https://YOUR_USERNAME.pythonanywhere.com"
echo ""
echo "For detailed instructions, see DEPLOYMENT_GUIDE.md"
echo "=========================================="

