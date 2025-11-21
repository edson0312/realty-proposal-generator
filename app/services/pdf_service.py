"""Service for generating PDF proposals."""
import os
from datetime import datetime
from typing import Dict, Any, Optional
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfgen import canvas


class PDFService:
    """Service class for generating PDF proposals."""
    
    def __init__(self, output_folder: str = "uploads"):
        """
        Initialize PDF service.
        
        Args:
            output_folder: Directory to save generated PDFs
        """
        self.output_folder = output_folder
        os.makedirs(output_folder, exist_ok=True)
    
    def generate_proposal(self, data: Dict[str, Any]) -> str:
        """
        Generate a complete proposal PDF.
        
        Args:
            data: Dictionary containing all form data and computations
            
        Returns:
            Path to generated PDF file
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"proposal_{data['client_name'].replace(' ', '_')}_{timestamp}.pdf"
        filepath = os.path.join(self.output_folder, filename)
        
        doc = SimpleDocTemplate(
            filepath,
            pagesize=letter,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=1*inch,
            bottomMargin=0.75*inch
        )
        
        # Build PDF content
        story = []
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1e3a8a'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#1e3a8a'),
            spaceAfter=12,
            spaceBefore=20,
            fontName='Helvetica-Bold'
        )
        
        subheading_style = ParagraphStyle(
            'CustomSubHeading',
            parent=styles['Heading3'],
            fontSize=12,
            textColor=colors.HexColor('#2563eb'),
            spaceAfter=10,
            fontName='Helvetica-Bold'
        )
        
        # Add header image if exists
        header_img_path = os.path.join('img', 'Moldex_Page_Header.jpg')
        if os.path.exists(header_img_path):
            try:
                img = Image(header_img_path, width=6.5*inch, height=1.2*inch)
                story.append(img)
                story.append(Spacer(1, 0.3*inch))
            except:
                pass
        
        # Title
        story.append(Paragraph("Proposal", title_style))
        story.append(Paragraph(
            f"Date: {datetime.now().strftime('%B %d, %Y')}", 
            ParagraphStyle('Date', parent=styles['Normal'], alignment=TA_RIGHT)
        ))
        story.append(Spacer(1, 0.3*inch))
        
        # Greeting
        greeting_text = f"Good day! Thank you for considering Moldex Realty as your next investment. Here's a detailed sample computation to help you explore your dream home."
        story.append(Paragraph(greeting_text, styles['Normal']))
        story.append(Spacer(1, 0.2*inch))
        
        # Client Details
        story.append(Paragraph("CLIENT'S DETAILS", heading_style))
        client_data = [
            ['Client\'s Name:', data['client_name']],
            ['Email Address:', data['email']],
            ['Contact No.:', data.get('contact_no', 'N/A')]
        ]
        client_table = Table(client_data, colWidths=[2*inch, 4*inch])
        client_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#374151')),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        story.append(client_table)
        story.append(Spacer(1, 0.2*inch))
        
        # Project Details
        story.append(Paragraph("PROJECT DETAILS", heading_style))
        story.append(self._create_project_details_section(data))
        story.append(Spacer(1, 0.2*inch))
        
        # Add property picture if available
        if data.get('picture_path') and os.path.exists(data['picture_path']):
            try:
                prop_img = Image(data['picture_path'], width=4*inch, height=3*inch)
                story.append(prop_img)
                story.append(Spacer(1, 0.2*inch))
            except:
                pass
        
        # Project Advantages (if provided)
        if data.get('project_advantages'):
            story.append(Paragraph("PROJECT ADVANTAGES", heading_style))
            advantages_text = data['project_advantages'].replace('\n', '<br/>')
            advantages_para = Paragraph(advantages_text, styles['Normal'])
            story.append(advantages_para)
            story.append(Spacer(1, 0.3*inch))
        
        # Contract Details
        story.append(Paragraph("CONTRACT DETAILS", heading_style))
        story.append(self._create_contract_details_section(data))
        story.append(Spacer(1, 0.3*inch))
        
        # Payment Terms Computations
        story.append(PageBreak())
        story.append(Paragraph("PAYMENT TERMS", heading_style))
        
        # Add computation tables based on available data
        if data.get('spot_cash_data'):
            story.append(self._create_spot_cash_section(data['spot_cash_data']))
            story.append(Spacer(1, 0.3*inch))
        
        if data.get('deferred_payment_data'):
            deferred_elements = self._create_deferred_payment_section(data['deferred_payment_data'])
            if isinstance(deferred_elements, list):
                story.extend(deferred_elements)
            else:
                story.append(deferred_elements)
            story.append(Spacer(1, 0.3*inch))
        
        if data.get('spot_down_payment_data'):
            story.append(self._create_spot_down_payment_section(data['spot_down_payment_data']))
            story.append(Spacer(1, 0.3*inch))
        
        if data.get('payment_20_80_data'):
            payment_elements = self._create_20_80_payment_section(data['payment_20_80_data'])
            if isinstance(payment_elements, list):
                story.extend(payment_elements)
            else:
                story.append(payment_elements)
            story.append(Spacer(1, 0.3*inch))
            
            # Add 80% Balance section if available
            if data['payment_20_80_data'].get('balance_80_amortizations'):
                balance_elements = self._create_80_balance_section(
                    data['payment_20_80_data']['balance_80_amortizations'],
                    data['payment_20_80_data']['balance_80'],
                    data.get('registration_fee', 0)
                )
                if isinstance(balance_elements, list):
                    story.extend(balance_elements)
                else:
                    story.append(balance_elements)
                story.append(Spacer(1, 0.3*inch))
        
        # Disclaimer
        story.append(PageBreak())
        story.append(Paragraph("DISCLAIMER / ACKNOWLEDGEMENT", heading_style))
        story.append(self._create_disclaimer_section())
        story.append(Spacer(1, 0.5*inch))
        
        # Signatures
        story.append(self._create_signature_section())
        story.append(Spacer(1, 0.15*inch))
        
        # Note section with Move-In and Registration Fee details
        story.append(self._create_note_section())
        
        # Build PDF
        doc.build(story)
        
        return filepath
    
    def _create_project_details_section(self, data: Dict[str, Any]) -> Table:
        """Create project details table."""
        project_data = []
        project_data.append(['Product Type:', data.get('product_type', 'N/A')])
        
        if data.get('product_type') == 'Vertical':
            project_data.append(['Project Type:', data.get('project_type', 'N/A')])
            project_data.append(['Brand:', data.get('brand', 'N/A')])
            project_data.append(['Address:', data.get('address', 'N/A')])
            if data.get('property_details'):
                project_data.append(['Property Details:', data.get('property_details', 'N/A')])
            project_data.append(['Tower/Building:', data.get('tower_building', 'N/A')])
            project_data.append(['Floor/Unit:', data.get('floor_unit', 'N/A')])
            project_data.append(['Floor Area:', data.get('floor_area', 'N/A')])
        else:  # Horizontal
            project_data.append(['Project Type:', data.get('project_type', 'N/A')])
            project_data.append(['Brand:', data.get('brand', 'N/A')])
            project_data.append(['Address:', data.get('address', 'N/A')])
            project_data.append(['Phase:', data.get('phase', 'N/A')])
            project_data.append(['Block/Lot:', data.get('block_lot', 'N/A')])
            
            if data.get('project_type') == 'House and Lot':
                project_data.append(['House Model:', data.get('house_model', 'N/A')])
                project_data.append(['Property Details:', data.get('property_details', 'N/A')])
                project_data.append(['Lot Area:', data.get('lot_area', 'N/A')])
                project_data.append(['Floor Area:', data.get('floor_area', 'N/A')])
            else:  # Lot
                project_data.append(['Lot Area:', data.get('lot_area', 'N/A')])
        
        table = Table(project_data, colWidths=[2*inch, 4*inch])
        table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#374151')),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        return table
    
    def _create_contract_details_section(self, data: Dict[str, Any]) -> Table:
        """Create contract details table - UPDATED to remove Registration and Move-in Fee."""
        contract_data = [
            ['Total Contract Price (TCP):', self._format_currency(data.get('tcp', 0))],
            ['Reservation Fee:', self._format_currency(data.get('reservation_fee', 0))],
            ['Registration Fee %:', f"{data.get('registration_fee_percent', 0):.2f}%"],
            ['Move-in Fee %:', f"{data.get('move_in_fee_percent', 0):.2f}%"],
        ]
        
        table = Table(contract_data, colWidths=[2.5*inch, 3.5*inch])
        table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#374151')),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f3f4f6')),
        ]))
        return table
    
    def _create_spot_cash_section(self, data: Dict[str, float]) -> Table:
        """Create Spot Cash computation table."""
        styles = getSampleStyleSheet()
        subheading = ParagraphStyle(
            'TableSubheading',
            parent=styles['Heading3'],
            fontSize=12,
            textColor=colors.white,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        table_data = [
            [Paragraph("SPOT CASH", subheading)],
            [''],
            ['Description', 'Formula', 'Amount'],
            ['Total Contract Price (TCP)', '—', self._format_currency(data['tcp'])],
            ['Less the Term Discount (TD)', f"TCP × {data['discount_percent']}%", self._format_currency(data['term_discount'])],
            ['Discounted TCP (DTCP)/Net TCP (NTCP)', 'TCP - TD', self._format_currency(data['dtcp'])],
            ['Less Reservation Fee (RF)', 'Input', self._format_currency(data['reservation_fee'])],
            ['DTCP - RF', 'DTCP - RF', self._format_currency(data.get('dtcp_less_rf', 0))],
            ['Total List Price (TLP)', 'DTCP ÷ 1.12', self._format_currency(data['tlp'])],
            ['Registration Fee (RGF)', 'TLP × %', self._format_currency(data['registration_fee'])],
            ['Move-in Fee (MIF)', 'TLP × %', self._format_currency(data['move_in_fee'])],
            ['Total Payment', 'NTCP + RGF + MIF', self._format_currency(data.get('total_payment', 0))],
        ]
        
        table = Table(table_data, colWidths=[2.5*inch, 1.8*inch, 1.8*inch], hAlign='CENTER')
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e3a8a')),
            ('SPAN', (0, 0), (-1, 0)),
            ('FONTNAME', (0, 2), (-1, 2), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 2), (-1, -1), 9),
            ('BACKGROUND', (0, 2), (-1, 2), colors.HexColor('#e5e7eb')),
            ('TEXTCOLOR', (0, 2), (-1, -1), colors.HexColor('#1f2937')),
            ('ALIGN', (2, 2), (2, -1), 'RIGHT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 2), (-1, -1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 3), (-1, -1), [colors.white, colors.HexColor('#f9fafb')]),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
        ]))
        return table
    
    def _create_deferred_payment_section(self, data: Dict[str, Any]) -> list:
        """Create Deferred Payment computation section with new table format."""
        styles = getSampleStyleSheet()
        elements = []
        
        subheading = ParagraphStyle(
            'TableSubheading',
            parent=styles['Heading3'],
            fontSize=12,
            textColor=colors.white,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        # Main computation table
        table_data = [
            [Paragraph("DEFERRED PAYMENT", subheading)],
            [''],
            ['Description', 'Formula', 'Amount'],
            ['Total Contract Price (TCP)/Net TCP (NTCP)', '—', self._format_currency(data['tcp'])],
            ['Less Reservation Fee (RF)', 'Input', self._format_currency(data['reservation_fee'])],
            ['TCP - RF', 'TCP - RF', self._format_currency(data.get('tcp_less_rf', 0))],
            ['Total List Price (TLP)', 'TCP ÷ 1.12', self._format_currency(data['tlp'])],
            ['Registration Fee (RGF)', 'TLP × %', self._format_currency(data['registration_fee'])],
            ['Move-in Fee (MIF)', 'TLP × %', self._format_currency(data['move_in_fee'])],
        ]
        
        table = Table(table_data, colWidths=[2.5*inch, 1.8*inch, 1.8*inch], hAlign='CENTER')
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e3a8a')),
            ('SPAN', (0, 0), (-1, 0)),
            ('FONTNAME', (0, 2), (-1, 2), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 2), (-1, -1), 9),
            ('BACKGROUND', (0, 2), (-1, 2), colors.HexColor('#e5e7eb')),
            ('TEXTCOLOR', (0, 2), (-1, -1), colors.HexColor('#1f2937')),
            ('ALIGN', (2, 2), (2, -1), 'RIGHT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 2), (-1, -1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 3), (-1, -1), [colors.white, colors.HexColor('#f9fafb')]),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
        ]))
        elements.append(table)
        
        # Add MA table if monthly amortizations exist
        if data.get('monthly_amortizations'):
            elements.append(Spacer(1, 0.2*inch))
            ma_table = self._create_ma_table(data, 'DEFERRED')
            elements.append(ma_table)
        
        return elements
    
    def _create_ma_table(self, data: Dict[str, Any], payment_type: str) -> Table:
        """Create Monthly Amortization breakdown table."""
        ma_data = [['Months', 'MA', 'MA with Reg Fee', 'MA with Move In Fee', 'MA with Reg Fee & Move In Fee']]
        
        if payment_type == 'DEFERRED':
            net_amount = data['ntcp']
            reg_fee = data['registration_fee']
            move_fee = data['move_in_fee']
            
            for term in sorted(data.get('monthly_amortizations', {}).keys()):
                ma = net_amount / term
                ma_reg = (net_amount + reg_fee) / term
                ma_move = (net_amount + move_fee) / term
                ma_both = (net_amount + reg_fee + move_fee) / term
                
                ma_data.append([
                    str(term),
                    self._format_currency(ma),
                    self._format_currency(ma_reg),
                    self._format_currency(ma_move),
                    self._format_currency(ma_both)
                ])
        
        elif payment_type == '20/80':
            ndp = data['ndp']
            reg_fee = data['registration_fee']
            move_fee = data['move_in_fee']
            
            for term in sorted(data.get('monthly_amortizations_20', {}).keys()):
                ma = ndp / term
                ma_reg = (ndp + reg_fee) / term
                ma_move = (ndp + move_fee) / term
                ma_both = (ndp + reg_fee + move_fee) / term
                
                ma_data.append([
                    str(term),
                    self._format_currency(ma),
                    self._format_currency(ma_reg),
                    self._format_currency(ma_move),
                    self._format_currency(ma_both)
                ])
        
        col_widths = [0.85*inch, 1.3*inch, 1.3*inch, 1.3*inch, 1.35*inch]
        table = Table(ma_data, colWidths=col_widths, hAlign='CENTER')
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2563eb')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('ALIGN', (1, 1), (-1, -1), 'RIGHT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9fafb')]),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
        ]))
        return table
    
    def _create_spot_down_payment_section(self, data: Dict[str, float]) -> Table:
        """Create Spot Down Payment computation table."""
        styles = getSampleStyleSheet()
        subheading = ParagraphStyle(
            'TableSubheading',
            parent=styles['Heading3'],
            fontSize=12,
            textColor=colors.white,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        table_data = [
            [Paragraph("SPOT DOWN PAYMENT", subheading)],
            [''],
            ['Description', 'Formula', 'Amount'],
            ['Total Contract Price (TCP)', '—', self._format_currency(data['tcp'])],
            ['Get the 20% Down Payment (DP)', 'TCP × 20%', self._format_currency(data['down_payment'])],
            ['Less the Term Discount (TD)', f"DP × {data['discount_percent']}%", self._format_currency(data['term_discount'])],
            ['Less Reservation Fee (RF)', 'Input', self._format_currency(data['reservation_fee'])],
            ['Net Down Payment (NDP)', 'DP - (TD + RF)', self._format_currency(data['ndp'])],
            ['80% Balance', 'TCP × 80%', self._format_currency(data['balance_80'])],
            ['Total List Price (TLP)', 'TCP ÷ 1.12', self._format_currency(data['tlp'])],
            ['Registration Fee (RGF)', 'TLP × %', self._format_currency(data['registration_fee'])],
            ['Move-in Fee (MIF)', 'TLP × %', self._format_currency(data['move_in_fee'])],
        ]
        
        table = Table(table_data, colWidths=[2.5*inch, 1.8*inch, 1.8*inch], hAlign='CENTER')
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e3a8a')),
            ('SPAN', (0, 0), (-1, 0)),
            ('FONTNAME', (0, 2), (-1, 2), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 2), (-1, -1), 9),
            ('BACKGROUND', (0, 2), (-1, 2), colors.HexColor('#e5e7eb')),
            ('TEXTCOLOR', (0, 2), (-1, -1), colors.HexColor('#1f2937')),
            ('ALIGN', (2, 2), (2, -1), 'RIGHT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 2), (-1, -1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 3), (-1, -1), [colors.white, colors.HexColor('#f9fafb')]),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
        ]))
        return table
    
    def _create_20_80_payment_section(self, data: Dict[str, Any]) -> list:
        """Create 20/80 Payment computation section with new table format."""
        styles = getSampleStyleSheet()
        elements = []
        
        subheading = ParagraphStyle(
            'TableSubheading',
            parent=styles['Heading3'],
            fontSize=12,
            textColor=colors.white,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        # Main computation table
        table_data = [
            [Paragraph("20/80 PAYMENT TERM", subheading)],
            [''],
            ['Description', 'Formula', 'Amount'],
            ['Total Contract Price (TCP)', '—', self._format_currency(data['tcp'])],
            ['Get the 20% Down Payment (DP)', 'TCP × 20%', self._format_currency(data['down_payment'])],
            ['Less Reservation Fee (RF)', 'Input', self._format_currency(data['reservation_fee'])],
            ['Net Down Payment (NDP)', 'DP - RF', self._format_currency(data['ndp'])],
            ['80% Balance', 'TCP × 80%', self._format_currency(data['balance_80'])],
            ['Total List Price (TLP)', 'TCP ÷ 1.12', self._format_currency(data['tlp'])],
            ['Registration Fee (RGF)', 'TLP × %', self._format_currency(data['registration_fee'])],
            ['Move-in Fee (MIF)', 'TLP × %', self._format_currency(data['move_in_fee'])],
            [''],
            ['Payment Options:', '', ''],
            ['20% Net Down Payment', '', self._format_currency(data['net_down_payment_20'])],
            ['20% with Move-in Fee', '', self._format_currency(data['with_move_in'])],
            ['20% with Reg Fee', '', self._format_currency(data['with_reg_fee'])],
            ['20% with Reg Fee & Move-in Fee', '', self._format_currency(data['with_reg_and_move_in'])],
        ]
        
        table = Table(table_data, colWidths=[2.5*inch, 1.8*inch, 1.8*inch], hAlign='CENTER')
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e3a8a')),
            ('SPAN', (0, 0), (-1, 0)),
            ('FONTNAME', (0, 2), (-1, 2), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 2), (-1, -1), 9),
            ('BACKGROUND', (0, 2), (-1, 2), colors.HexColor('#e5e7eb')),
            ('TEXTCOLOR', (0, 2), (-1, -1), colors.HexColor('#1f2937')),
            ('ALIGN', (2, 2), (2, -1), 'RIGHT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 2), (-1, -1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 3), (-1, -1), [colors.white, colors.HexColor('#f9fafb')]),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
        ]))
        elements.append(table)
        
        # Add MA table if monthly amortizations exist
        if data.get('monthly_amortizations_20'):
            elements.append(Spacer(1, 0.2*inch))
            ma_table = self._create_ma_table(data, '20/80')
            elements.append(ma_table)
        
        return elements
    
    def _create_80_balance_section(self, amortizations: list, balance_80: float, registration_fee: float) -> list:
        """Create 80% Balance Terms computation section."""
        styles = getSampleStyleSheet()
        elements = []
        
        subheading = ParagraphStyle(
            'TableSubheading',
            parent=styles['Heading3'],
            fontSize=12,
            textColor=colors.white,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        # Main section - 80% Balance details
        table_data = [
            [Paragraph("80% BALANCE TERMS", subheading)],
            [''],
            ['Description', 'Formula', 'Amount'],
            ['80% Balance', 'TCP × 80%', self._format_currency(balance_80)],
            ['80% with Reg Fee', '80% Balance + Reg Fee', self._format_currency(balance_80 + registration_fee)],
        ]
        
        table = Table(table_data, colWidths=[2.5*inch, 1.8*inch, 1.8*inch], hAlign='CENTER')
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e3a8a')),
            ('SPAN', (0, 0), (-1, 0)),
            ('FONTNAME', (0, 2), (-1, 2), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 2), (-1, -1), 9),
            ('BACKGROUND', (0, 2), (-1, 2), colors.HexColor('#e5e7eb')),
            ('TEXTCOLOR', (0, 2), (-1, -1), colors.HexColor('#1f2937')),
            ('ALIGN', (2, 2), (2, -1), 'RIGHT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 2), (-1, -1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 3), (-1, -1), [colors.white, colors.HexColor('#f9fafb')]),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
        ]))
        elements.append(table)
        elements.append(Spacer(1, 0.2*inch))
        
        # Create the MA table with dynamic columns
        if amortizations:
            ma_table = self._create_80_balance_ma_table(amortizations)
            elements.append(ma_table)
        
        return elements
    
    def _create_80_balance_ma_table(self, amortizations: list) -> Table:
        """Create the monthly amortization table for 80% Balance."""
        # Build header row
        header_row = ['Years (Interest %)']
        ma_row = ['MA']
        ma_with_reg_row = ['MA with Reg Fee']
        
        for amort in amortizations:
            years = int(amort['years'])
            rate = amort['rate']
            header_row.append(f"{years} years ({rate:.0f}%)")
            ma_row.append(self._format_currency(amort['ma']))
            ma_with_reg_row.append(self._format_currency(amort['ma_with_reg']))
        
        table_data = [
            header_row,
            ma_row,
            ma_with_reg_row
        ]
        
        # Calculate column widths dynamically - match main payment table width (6.1 inches)
        num_columns = len(header_row)
        label_width = 1.8 * inch
        data_width = (6.1*inch - label_width) / (num_columns - 1)
        col_widths = [label_width] + [data_width] * (num_columns - 1)
        
        table = Table(table_data, colWidths=col_widths, hAlign='CENTER')
        table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2563eb')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#1f2937')),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('ALIGN', (1, 1), (-1, -1), 'RIGHT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9fafb')]),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
        ]))
        
        return table
    
    def _create_disclaimer_section(self) -> Table:
        """Create disclaimer section."""
        disclaimer_items = [
            "1. This sample computation is valid for one whole calendar week (7 calendar days) from the date of signing.",
            "2. The bank-accredited appraiser will be for cash and check deposit is exclusive for application fees only.",
            "3. All check payments must be payable to Moldex Realty Inc. / Moldex Land Inc.",
            "4. Inclusive terms, terms, and discounts are for cash basis only and must be settled within 7 days from reservation or notice.",
            "5. Prices are VAT inclusive whenever applicable.",
            "6. The developer reserves the right to correct any figure in this sample computation in case of typographical error.",
            "7. Sellers and organic employees on-site are not allowed to issue official receipts, provisional receipts, or acknowledgment receipts.",
            "8. The depositor's copy and photocopy of the check must be attached to the sales documents.",
            "9. The buyer understands (and evidences by their signature in the form) that the sample computation may only be considered final if approved by management."
        ]
        
        # Join with HTML line breaks for proper rendering in PDF
        disclaimer_text = "<br/><br/>".join(disclaimer_items)
        
        styles = getSampleStyleSheet()
        normal_style = ParagraphStyle(
            'DisclaimerStyle',
            parent=styles['Normal'],
            fontSize=8,
            leading=12,
            textColor=colors.HexColor('#374151')
        )
        
        table_data = [
            [Paragraph(disclaimer_text, normal_style)]
        ]
        
        table = Table(table_data, colWidths=[6.5*inch])
        table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('BOX', (0, 0), (-1, -1), 1, colors.grey),
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f9fafb')),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('RIGHTPADDING', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ]))
        return table
    
    def _create_signature_section(self) -> Table:
        """Create signature section."""
        styles = getSampleStyleSheet()
        label_style = ParagraphStyle(
            'SignatureLabel',
            parent=styles['Normal'],
            fontSize=10,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#6b7280')
        )
        
        table_data = [
            ['Acknowledged by:', ''],
            ['', ''],
            ['', ''],
            ['_________________________________', '_________________________________'],
            [Paragraph("Buyer's Signature Over Printed Name", label_style), 
             Paragraph("Seller's Signature Over Printed Name", label_style)],
        ]
        
        table = Table(table_data, colWidths=[3.25*inch, 3.25*inch])
        table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('SPAN', (0, 0), (-1, 0)),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'BOTTOM'),
            ('BOTTOMPADDING', (0, 3), (-1, 3), 0),
            ('TOPPADDING', (0, 4), (-1, 4), 2),
        ]))
        return table
    
    def _create_note_section(self) -> Table:
        """Create note section with Move-In and Registration fees details."""
        styles = getSampleStyleSheet()
        
        note_style = ParagraphStyle(
            'NoteStyle',
            parent=styles['Normal'],
            fontSize=9,
            leading=11,
            textColor=colors.HexColor('#1f2937')
        )
        
        bold_style = ParagraphStyle(
            'BoldStyle',
            parent=note_style,
            fontName='Helvetica-Bold',
            fontSize=9
        )
        
        # Create the note content - more compact
        note_content = """<b>Note:</b><br/>
Registration and Move-In Fees are required under <b>PD 957</b> and <b>DHSUD regulations</b> 
as part of the legal process for property registration and turnover."""
        
        # Create two-column layout for Move In Fee and Registration Fee
        move_in_items = [
            "☑ Occupancy Permit",
            "☑ Fire Safety Compliance",
            "☑ Fire Insurance (para sa In-House Fin)",
            "☑ Electric Guarantee Consumption/Service",
            "☑ Water Guarantee Deposit/Connection Charges",
            "☑ Processing Fee/Service Fee"
        ]
        
        registration_items = [
            "☑ Documentary Stamp",
            "☑ Transfer Fee",
            "☑ Registration and IT Fee",
            "☑ Annotation/Legal/Notarization Fees",
            "☑ Processing Fee",
            "☑ Service Fee"
        ]
        
        move_in_text = "<br/>".join(move_in_items)
        registration_text = "<br/>".join(registration_items)
        
        # Main table with note and two columns - removed empty row
        main_data = [
            [Paragraph(note_content, note_style)],
            [Table([
                [Paragraph("<b>Move In Fee</b>", bold_style), Paragraph("<b>Registration Fee</b>", bold_style)],
                [Paragraph(move_in_text, note_style), Paragraph(registration_text, note_style)]
            ], colWidths=[3.25*inch, 3.25*inch])]
        ]
        
        table = Table(main_data, colWidths=[6.5*inch])
        table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('BOX', (0, 0), (-1, -1), 1, colors.grey),
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f9fafb')),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('RIGHTPADDING', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        
        # Style the inner table
        inner_table = main_data[1][0]
        inner_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('ALIGN', (0, 0), (-1, 0), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
            ('TOPPADDING', (0, 0), (-1, 0), 6),
            ('TOPPADDING', (0, 1), (-1, 1), 4),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ]))
        
        return table
    
    @staticmethod
    def _format_currency(amount: float) -> str:
        """Format amount as Philippine Peso currency."""
        return f"P{amount:,.2f}"

