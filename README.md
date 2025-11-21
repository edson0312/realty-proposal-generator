# Moldex Realty Proposal Generator

A Flask-based web application for generating professional property proposals and sample computations for Moldex Realty clients.

## Features

- **Client Information Management**: Capture client details including name, email, and contact information
- **Project Details**: Support for both Vertical (High-rise/Mid-rise) and Horizontal (Lot/House and Lot) properties
- **Multiple Payment Terms**:
  - Spot Cash
  - Deferred Payment
  - Spot Down Payment
  - 20/80 Payment Terms
  - 80% Balance Terms with various interest rates
- **Automatic Computations**: Real-time calculation of monthly amortizations, registration fees, and move-in fees
- **PDF Generation**: Professional PDF proposals with company branding
- **Image Upload**: Support for property images in proposals

## Technology Stack

- **Backend**: Python 3.10+ with Flask
- **PDF Generation**: ReportLab
- **Image Processing**: Pillow (PIL)
- **Frontend**: HTML5, CSS3, JavaScript
- **Configuration**: python-dotenv

## Local Development Setup

### Prerequisites

- Python 3.10 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd Sample-Computation
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create `.env` file:**
   ```bash
   SECRET_KEY=your-secret-key-here
   FLASK_ENV=development
   ```

5. **Run the application:**
   ```bash
   python run.py
   ```

6. **Open your browser:**
   ```
   http://localhost:5000
   ```

## Project Structure

```
Sample-Computation/
├── app/
│   ├── __init__.py           # Flask app factory
│   ├── routes/
│   │   ├── __init__.py
│   │   └── main.py           # Main routes
│   ├── services/
│   │   ├── __init__.py
│   │   ├── computation_service.py  # Business logic
│   │   └── pdf_service.py          # PDF generation
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css
│   │   ├── js/
│   │   │   └── script.js
│   │   └── img/
│   │       └── Moldex_Page_Header.jpg
│   ├── templates/
│   │   └── index.html
│   └── utils/
│       └── __init__.py
├── uploads/                  # Generated PDFs and uploaded images
├── logs/                     # Application logs (production)
├── config.py                 # Configuration settings
├── run.py                    # Application entry point
├── wsgi.py                   # WSGI configuration for deployment
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables (not in git)
├── .gitignore               # Git ignore rules
├── DEPLOYMENT_GUIDE.md      # PythonAnywhere deployment guide
└── README.md                # This file
```

## Usage

1. **Fill in Client Details**: Enter client name, email, and contact number
2. **Select Product Type**: Choose between Vertical or Horizontal property
3. **Enter Project Details**: Fill in property information based on type
4. **Upload Property Image**: Add a property photo (optional)
5. **Enter Contract Details**: Input Total Contract Price and fee percentages
6. **Configure Payment Terms**: Set discounts and payment terms as needed
7. **Generate Proposal**: Click "Generate Proposal" to create PDF
8. **Download**: PDF will automatically download

## Payment Term Calculations

### Spot Cash
- Net TCP = TCP - Discount Amount
- TLP = Net TCP ÷ 1.12 (or Net TCP if TCP ≤ ₱3,600,000)
- Registration Fee = TLP × Reg Fee % (or Net TCP × Reg Fee % if toggle disabled)
- Move-in Fee = TLP × Move-in Fee %

### Deferred Payment
- Monthly Amortization = (TCP - Discount - Reservation Fee) ÷ Months
- Includes variations with Reg Fee and Move-in Fee

### 20/80 Payment Terms
- 20% Down Payment with monthly amortization options
- 80% Balance with bank/in-house financing

### 80% Balance Terms
- Fixed terms: 5 years (10%), 7 years (13%), 10 years (15%)
- Uses factor rates for accurate amortization calculation

## Deployment

See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for detailed instructions on deploying to PythonAnywhere.

## Configuration

### Environment Variables

- `SECRET_KEY`: Flask secret key for session management
- `FLASK_ENV`: Environment (development/production)
- `MAX_CONTENT_LENGTH`: Maximum file upload size (default: 16MB)

### Factor Rates (80% Balance)

- 1-5 years: 0.0212470447
- 6-7 years: 0.0181919633
- 8-10 years: 0.0161334957

## Security Features

- CSRF protection on all forms
- File upload validation
- Secure session management
- Input sanitization
- XSS protection

## Browser Support

- Chrome (recommended)
- Firefox
- Safari
- Edge

## License

Proprietary - Moldex Realty

## Support

For issues or questions, please contact the development team.

---

**Version:** 1.0.0  
**Last Updated:** November 2025
