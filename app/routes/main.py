"""Main routes for the application."""
from flask import Blueprint, render_template, request, jsonify, send_file, current_app
from werkzeug.utils import secure_filename
import os
from typing import Dict, Any

from app.services.computation_service import ComputationService
from app.services.pdf_service import PDFService
from app.utils.file_helper import save_uploaded_file, format_currency

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """Render the main form page."""
    return render_template('index.html')


@main_bp.route('/generate-proposal', methods=['POST'])
def generate_proposal():
    """
    Handle form submission and generate PDF proposal.
    
    Returns:
        JSON response with PDF download URL or error message
    """
    try:
        # Extract form data
        form_data = request.form.to_dict()
        
        # Handle file upload
        picture_path = None
        if 'picture' in request.files:
            file = request.files['picture']
            if file and file.filename:
                picture_path = save_uploaded_file(
                    file,
                    current_app.config['UPLOAD_FOLDER'],
                    current_app.config['ALLOWED_EXTENSIONS']
                )
        
        # Convert numeric fields
        tcp = float(form_data.get('tcp', 0))
        reservation_fee = float(form_data.get('reservation_fee', 0))
        registration_fee_percent = float(form_data.get('registration_fee_percent', 0))
        move_in_fee_percent = float(form_data.get('move_in_fee_percent', 0))
        use_tlp_toggle = form_data.get('use_tlp_toggle') == 'on'  # Checkbox value
        
        # Initialize computation service
        comp_service = ComputationService()
        
        # Prepare data dictionary
        data = {
            'client_name': form_data.get('client_name'),
            'email': form_data.get('email'),
            'contact_no': form_data.get('contact_no', ''),
            'product_type': form_data.get('product_type'),
            'project_type': form_data.get('project_type', ''),
            'brand': form_data.get('brand', ''),
            'address': form_data.get('address', ''),
            'tcp': tcp,
            'reservation_fee': reservation_fee,
            'registration_fee_percent': registration_fee_percent,
            'move_in_fee_percent': move_in_fee_percent,
            'picture_path': picture_path
        }
        
        # Add product-specific fields
        if form_data.get('product_type') == 'Vertical':
            data.update({
                'property_details': form_data.get('property_details_vertical', ''),
                'tower_building': form_data.get('tower_building', ''),
                'floor_unit': form_data.get('floor_unit', ''),
                'floor_area': form_data.get('floor_area', ''),
                'project_advantages': form_data.get('project_advantages', '')
            })
        else:  # Horizontal
            data.update({
                'phase': form_data.get('phase', ''),
                'block_lot': form_data.get('block_lot', ''),
                'project_advantages': form_data.get('project_advantages_horiz', '')
            })
            
            if form_data.get('project_type') == 'House and Lot':
                data.update({
                    'house_model': form_data.get('house_model', ''),
                    'property_details': form_data.get('property_details', ''),
                    'lot_area': form_data.get('lot_area', ''),
                    'floor_area': form_data.get('floor_area', '')
                })
            else:  # Lot
                data['lot_area'] = form_data.get('lot_area', '')
        
        # Compute Spot Cash if discount provided
        if form_data.get('spot_cash_discount'):
            discount = float(form_data.get('spot_cash_discount', 0))
            spot_cash_data = comp_service.compute_spot_cash(
                tcp, discount, reservation_fee,
                registration_fee_percent, move_in_fee_percent,
                use_tlp_toggle
            )
            data['spot_cash_data'] = spot_cash_data
        
        # Compute Deferred Payment if terms provided
        deferred_terms = []
        if form_data.get('deferred_term1'):
            deferred_terms.append(int(form_data.get('deferred_term1')))
        if form_data.get('deferred_term2'):
            deferred_terms.append(int(form_data.get('deferred_term2')))
        if form_data.get('deferred_term3'):
            deferred_terms.append(int(form_data.get('deferred_term3')))
        
        if deferred_terms:
            deferred_data = comp_service.compute_deferred_payment(
                tcp, reservation_fee,
                registration_fee_percent, move_in_fee_percent,
                deferred_terms,
                use_tlp_toggle
            )
            data['deferred_payment_data'] = deferred_data
        
        # Compute Spot Down Payment if discount provided
        if form_data.get('spot_down_discount'):
            discount = float(form_data.get('spot_down_discount', 0))
            spot_down_data = comp_service.compute_spot_down_payment(
                tcp, discount, reservation_fee,
                registration_fee_percent, move_in_fee_percent,
                use_tlp_toggle
            )
            data['spot_down_payment_data'] = spot_down_data
        
        # Compute 20/80 Payment if terms provided
        payment_20_80_terms = []
        if form_data.get('payment_20_80_term1'):
            payment_20_80_terms.append(int(form_data.get('payment_20_80_term1')))
        if form_data.get('payment_20_80_term2'):
            payment_20_80_terms.append(int(form_data.get('payment_20_80_term2')))
        if form_data.get('payment_20_80_term3'):
            payment_20_80_terms.append(int(form_data.get('payment_20_80_term3')))
        
        if payment_20_80_terms:
            payment_20_80_data = comp_service.compute_20_80_payment(
                tcp, reservation_fee,
                registration_fee_percent, move_in_fee_percent,
                payment_20_80_terms,
                use_tlp_toggle
            )
            data['payment_20_80_data'] = payment_20_80_data
        
        # Compute 80% balance amortizations with static terms and factor rates
        # Static terms: 5 years (10%), 7 years (13%), 10 years (15%)
        balance_80_amortizations = []
        
        # Calculate registration fee for 80% balance
        if tcp <= 3600000:
            tlp = tcp
        else:
            tlp = tcp / 1.12
        
        if use_tlp_toggle:
            reg_fee_for_80 = tlp * (registration_fee_percent / 100)
        else:
            reg_fee_for_80 = tcp * (registration_fee_percent / 100)
        
        # Static terms with factor rates
        static_terms = [
            {'years': 5, 'rate': 10},
            {'years': 7, 'rate': 13},
            {'years': 10, 'rate': 15}
        ]
        
        for term in static_terms:
            amort = comp_service.compute_80_balance_amortization(
                tcp, term['years'], term['rate'], reg_fee_for_80
            )
            balance_80_amortizations.append(amort)
        
        # Add 80% balance amortizations to whichever payment method is being used
        if balance_80_amortizations:
            if data.get('spot_down_payment_data'):
                data['spot_down_payment_data']['balance_80_amortizations'] = balance_80_amortizations
            if data.get('payment_20_80_data'):
                data['payment_20_80_data']['balance_80_amortizations'] = balance_80_amortizations
        
        # Calculate base registration and move-in fees
        tlp = tcp / 1.12
        data['registration_fee'] = tlp * (registration_fee_percent / 100)
        data['move_in_fee'] = tlp * (move_in_fee_percent / 100)
        
        # Generate PDF
        pdf_service = PDFService(current_app.config['UPLOAD_FOLDER'])
        pdf_path = pdf_service.generate_proposal(data)
        
        # Return success response
        filename = os.path.basename(pdf_path)
        return jsonify({
            'success': True,
            'message': 'Proposal generated successfully!',
            'download_url': f'/download/{filename}'
        })
    
    except Exception as e:
        current_app.logger.error(f"Error generating proposal: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Error generating proposal: {str(e)}'
        }), 500


@main_bp.route('/download/<filename>')
def download_file(filename: str):
    """
    Download generated PDF file.
    
    Args:
        filename: Name of the file to download
        
    Returns:
        File download response
    """
    try:
        # Secure the filename
        safe_filename = secure_filename(filename)
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], safe_filename)
        
        # Log for debugging
        current_app.logger.info(f"Attempting to download file: {file_path}")
        current_app.logger.info(f"File exists: {os.path.exists(file_path)}")
        
        if os.path.exists(file_path):
            return send_file(
                file_path, 
                as_attachment=True, 
                download_name=safe_filename,
                mimetype='application/pdf'
            )
        else:
            current_app.logger.error(f"File not found: {file_path}")
            return jsonify({'error': 'File not found', 'path': file_path}), 404
    except Exception as e:
        current_app.logger.error(f"Error downloading file: {str(e)}", exc_info=True)
        return jsonify({'error': f'Error downloading file: {str(e)}'}), 500


@main_bp.route('/api/compute', methods=['POST'])
def compute():
    """
    API endpoint for real-time computations.
    
    Returns:
        JSON with computed values
    """
    try:
        data = request.get_json()
        comp_service = ComputationService()
        
        computation_type = data.get('type')
        tcp = float(data.get('tcp', 0))
        reservation_fee = float(data.get('reservation_fee', 0))
        registration_fee_percent = float(data.get('registration_fee_percent', 0))
        move_in_fee_percent = float(data.get('move_in_fee_percent', 0))
        
        result = {}
        
        if computation_type == 'spot_cash':
            discount = float(data.get('discount', 0))
            result = comp_service.compute_spot_cash(
                tcp, discount, reservation_fee,
                registration_fee_percent, move_in_fee_percent
            )
        elif computation_type == 'spot_down_payment':
            discount = float(data.get('discount', 0))
            result = comp_service.compute_spot_down_payment(
                tcp, discount, reservation_fee,
                registration_fee_percent, move_in_fee_percent
            )
        elif computation_type == 'deferred_payment':
            terms = data.get('terms', [])
            result = comp_service.compute_deferred_payment(
                tcp, reservation_fee,
                registration_fee_percent, move_in_fee_percent,
                terms
            )
        elif computation_type == '20_80_payment':
            terms = data.get('terms', [])
            result = comp_service.compute_20_80_payment(
                tcp, reservation_fee,
                registration_fee_percent, move_in_fee_percent,
                terms
            )
        elif computation_type == '80_balance':
            years = float(data.get('years', 0))
            rate = float(data.get('rate', 0))
            result = comp_service.compute_80_balance_amortization(tcp, years, rate)
        
        return jsonify({
            'success': True,
            'data': result
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400

