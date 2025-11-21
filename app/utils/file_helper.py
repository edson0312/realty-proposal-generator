"""Helper functions for file operations."""
import os
from typing import Optional
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage


def allowed_file(filename: str, allowed_extensions: set) -> bool:
    """
    Check if file has an allowed extension.
    
    Args:
        filename: Name of the file to check
        allowed_extensions: Set of allowed file extensions
        
    Returns:
        True if file extension is allowed, False otherwise
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions


def save_uploaded_file(file: FileStorage, upload_folder: str, allowed_extensions: set) -> Optional[str]:
    """
    Save an uploaded file securely.
    
    Args:
        file: Uploaded file object
        upload_folder: Directory to save the file
        allowed_extensions: Set of allowed file extensions
        
    Returns:
        Path to saved file or None if save failed
    """
    if file and file.filename and allowed_file(file.filename, allowed_extensions):
        filename = secure_filename(file.filename)
        
        # Add timestamp to filename to avoid collisions
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        name, ext = os.path.splitext(filename)
        filename = f"{name}_{timestamp}{ext}"
        
        filepath = os.path.join(upload_folder, filename)
        file.save(filepath)
        return filepath
    
    return None


def format_currency(amount: float) -> str:
    """
    Format amount as Philippine Peso currency.
    
    Args:
        amount: Amount to format
        
    Returns:
        Formatted currency string
    """
    return f"₱{amount:,.2f}"

