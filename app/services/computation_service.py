"""Service for handling real estate computation calculations."""
from typing import Dict, Any, List, Optional


class ComputationService:
    """Service class for real estate payment computations."""
    
    @staticmethod
    def compute_spot_cash(
        tcp: float,
        discount_percent: float,
        reservation_fee: float,
        registration_fee_percent: float,
        move_in_fee_percent: float,
        use_tlp_for_reg_fee: bool = True
    ) -> Dict[str, float]:
        """
        Calculate Spot Cash payment terms.
        
        Args:
            tcp: Total Contract Price
            discount_percent: Term discount percentage
            reservation_fee: Reservation fee amount
            registration_fee_percent: Registration fee percentage
            move_in_fee_percent: Move-in fee percentage
            use_tlp_for_reg_fee: If True, use Net TCP / 1.12 for reg fee calculation
            
        Returns:
            Dictionary containing computed values
        """
        term_discount = tcp * (discount_percent / 100)
        dtcp = tcp - term_discount  # Discounted Total Contract Price
        ntcp = dtcp  # Net Total Contract Price = DTCP
        dtcp_less_rf = dtcp - reservation_fee  # DTCP - RF (for PDF only)
        
        # Handle special case: TCP <= 3,600,000
        if tcp <= 3600000:
            tlp = dtcp  # TLP = DTCP when TCP <= 3,600,000
        else:
            tlp = dtcp / 1.12  # Total List Price (removing 12% VAT)
        
        # Calculate Registration Fee based on toggle
        if use_tlp_for_reg_fee:
            # When enabled: Net TCP / 1.12 * Reg Fee %
            registration_fee = (ntcp / 1.12) * (registration_fee_percent / 100)
        else:
            # When disabled: Net TCP * Reg Fee %
            registration_fee = ntcp * (registration_fee_percent / 100)
        
        move_in_fee = tlp * (move_in_fee_percent / 100)
        
        # Calculate Total Payment
        total_payment = ntcp + registration_fee + move_in_fee
        
        return {
            'tcp': tcp,
            'term_discount': term_discount,
            'discount_percent': discount_percent,
            'dtcp': dtcp,
            'reservation_fee': reservation_fee,
            'ntcp': ntcp,
            'dtcp_less_rf': dtcp_less_rf,  # For PDF only
            'tlp': tlp,
            'registration_fee': registration_fee,
            'move_in_fee': move_in_fee,
            'net_tcp': ntcp,
            'total_payment': total_payment
        }
    
    @staticmethod
    def compute_spot_down_payment(
        tcp: float,
        discount_percent: float,
        reservation_fee: float,
        registration_fee_percent: float,
        move_in_fee_percent: float,
        use_tlp_for_reg_fee: bool = True
    ) -> Dict[str, float]:
        """
        Calculate Spot Down Payment terms.
        
        Args:
            tcp: Total Contract Price
            discount_percent: Term discount percentage
            reservation_fee: Reservation fee amount
            registration_fee_percent: Registration fee percentage
            move_in_fee_percent: Move-in fee percentage
            use_tlp_for_reg_fee: If True, use TLP for reg fee calculation
            
        Returns:
            Dictionary containing computed values
        """
        down_payment = tcp * 0.20  # 20% Down Payment
        term_discount = down_payment * (discount_percent / 100)
        ndp = down_payment - term_discount - reservation_fee  # Net Down Payment
        balance_80 = tcp * 0.80  # 80% Balance
        
        # Handle special case: TCP <= 3,600,000
        if tcp <= 3600000:
            tlp = tcp  # TLP = TCP when TCP <= 3,600,000
        else:
            tlp = tcp / 1.12  # Total List Price
        
        # Calculate Registration Fee based on toggle
        if use_tlp_for_reg_fee:
            # When enabled: TLP * Reg Fee %
            registration_fee = tlp * (registration_fee_percent / 100)
        else:
            # When disabled: TCP * Reg Fee %
            registration_fee = tcp * (registration_fee_percent / 100)
        
        move_in_fee = tlp * (move_in_fee_percent / 100)
        
        return {
            'tcp': tcp,
            'down_payment': down_payment,
            'discount_percent': discount_percent,
            'term_discount': term_discount,
            'reservation_fee': reservation_fee,
            'ndp': ndp,
            'balance_80': balance_80,
            'tlp': tlp,
            'registration_fee': registration_fee,
            'move_in_fee': move_in_fee,
            'net_down_payment': ndp
        }
    
    @staticmethod
    def compute_deferred_payment(
        tcp: float,
        reservation_fee: float,
        registration_fee_percent: float,
        move_in_fee_percent: float,
        terms: List[int],
        use_tlp_for_reg_fee: bool = True
    ) -> Dict[str, Any]:
        """
        Calculate Deferred Payment terms.
        
        Args:
            tcp: Total Contract Price
            reservation_fee: Reservation fee amount
            registration_fee_percent: Registration fee percentage
            move_in_fee_percent: Move-in fee percentage
            terms: List of term lengths in months
            use_tlp_for_reg_fee: If True, use TLP for reg fee calculation
            
        Returns:
            Dictionary containing computed values
        """
        ntcp = tcp  # Net Total Contract Price = TCP (no discount in deferred)
        tcp_less_rf = tcp - reservation_fee  # TCP - RF (for PDF and monthly amortization calculation)
        
        # Handle special case: TCP <= 3,600,000
        if tcp <= 3600000:
            tlp = tcp  # TLP = TCP when TCP <= 3,600,000
        else:
            tlp = tcp / 1.12  # Total List Price
        
        # Calculate Registration Fee based on toggle
        if use_tlp_for_reg_fee:
            # When enabled: TLP * Reg Fee %
            registration_fee = tlp * (registration_fee_percent / 100)
        else:
            # When disabled: TCP * Reg Fee %
            registration_fee = tcp * (registration_fee_percent / 100)
        
        move_in_fee = tlp * (move_in_fee_percent / 100)
        
        # Calculate monthly amortizations for each term (based on TCP - RF)
        monthly_amortizations = {}
        for term in terms:
            if term > 0:
                monthly_amortizations[term] = tcp_less_rf / term
        
        return {
            'tcp': tcp,
            'reservation_fee': reservation_fee,
            'ntcp': ntcp,
            'tcp_less_rf': tcp_less_rf,  # For PDF only
            'tlp': tlp,
            'registration_fee': registration_fee,
            'move_in_fee': move_in_fee,
            'monthly_amortizations': monthly_amortizations
        }
    
    @staticmethod
    def compute_20_80_payment(
        tcp: float,
        reservation_fee: float,
        registration_fee_percent: float,
        move_in_fee_percent: float,
        terms_20: List[int],
        use_tlp_for_reg_fee: bool = True
    ) -> Dict[str, Any]:
        """
        Calculate 20/80 Payment terms.
        
        Args:
            tcp: Total Contract Price
            reservation_fee: Reservation fee amount
            registration_fee_percent: Registration fee percentage
            move_in_fee_percent: Move-in fee percentage
            terms_20: List of term lengths for 20% in months
            use_tlp_for_reg_fee: If True, use TLP for reg fee calculation
            
        Returns:
            Dictionary containing computed values
        """
        down_payment = tcp * 0.20  # 20% Down Payment
        ndp = down_payment - reservation_fee  # Net Down Payment
        balance_80 = tcp * 0.80  # 80% Balance
        
        # Handle special case: TCP <= 3,600,000
        if tcp <= 3600000:
            tlp = tcp  # TLP = TCP when TCP <= 3,600,000
        else:
            tlp = tcp / 1.12  # Total List Price
        
        # Calculate Registration Fee based on toggle
        if use_tlp_for_reg_fee:
            # When enabled: TLP * Reg Fee %
            registration_fee = tlp * (registration_fee_percent / 100)
        else:
            # When disabled: TCP * Reg Fee %
            registration_fee = tcp * (registration_fee_percent / 100)
        
        move_in_fee = tlp * (move_in_fee_percent / 100)
        
        # Calculate monthly amortizations for 20% down payment
        monthly_amortizations_20 = {}
        staggered_rgf_monthly = {}
        total_monthly_with_rgf = {}
        
        for term in terms_20:
            if term > 0:
                monthly_amortizations_20[term] = ndp / term
                staggered_rgf_monthly[term] = registration_fee / term
                total_monthly_with_rgf[term] = monthly_amortizations_20[term] + staggered_rgf_monthly[term]
        
        # Calculate payment options
        net_down_payment_20 = ndp
        with_move_in = ndp + move_in_fee
        with_reg_fee = ndp + registration_fee
        with_reg_and_move_in = ndp + registration_fee + move_in_fee
        
        return {
            'tcp': tcp,
            'down_payment': down_payment,
            'reservation_fee': reservation_fee,
            'ndp': ndp,
            'balance_80': balance_80,
            'tlp': tlp,
            'registration_fee': registration_fee,
            'move_in_fee': move_in_fee,
            'monthly_amortizations_20': monthly_amortizations_20,
            'staggered_rgf_monthly': staggered_rgf_monthly,
            'total_monthly_with_rgf': total_monthly_with_rgf,
            'net_down_payment_20': net_down_payment_20,
            'with_move_in': with_move_in,
            'with_reg_fee': with_reg_fee,
            'with_reg_and_move_in': with_reg_and_move_in
        }
    
    @staticmethod
    def compute_80_balance_amortization(
        tcp: float,
        years: float,
        interest_rate: float,
        registration_fee: float = 0
    ) -> Dict[str, float]:
        """
        Calculate 80% Balance Amortization using Factor Rates.
        
        Factor Rates:
        - 1-5 years: 0.0212470447
        - 6-7 years: 0.0181919633
        - 8-10 years: 0.0161334957
        
        Formula:
        - MA = 80% Balance * Factor Rate
        - MA with Reg Fee = (80% Balance + Reg Fee) * Factor Rate
        
        Args:
            tcp: Total Contract Price
            years: Number of years to pay
            interest_rate: Annual interest rate as percentage (for display)
            registration_fee: Registration fee amount
            
        Returns:
            Dictionary containing computed values
        """
        balance_80 = tcp * 0.80
        
        # Determine factor rate based on years
        if 1 <= years <= 5:
            factor_rate = 0.0212470447
        elif 6 <= years <= 7:
            factor_rate = 0.0181919633
        elif 8 <= years <= 10:
            factor_rate = 0.0161334957
        else:
            factor_rate = 0  # Invalid term
        
        # Calculate MA using factor rate
        monthly_amortization = balance_80 * factor_rate
        
        # Calculate MA with Registration Fee
        balance_80_with_reg = balance_80 + registration_fee
        ma_with_reg = balance_80_with_reg * factor_rate
        
        total_amount = monthly_amortization * years * 12
        
        return {
            'balance_80': balance_80,
            'monthly_amortization': monthly_amortization,
            'ma': monthly_amortization,  # PDF expects 'ma'
            'ma_with_reg': ma_with_reg,  # PDF expects 'ma_with_reg'
            'years': years,
            'interest_rate': interest_rate,
            'rate': interest_rate,  # PDF expects 'rate'
            'total_amount': total_amount,
            'factor_rate': factor_rate
        }
    
    @staticmethod
    def compute_80_with_reg_fee(
        balance_80: float,
        registration_fee: float,
        years: float,
        interest_rate: float
    ) -> Dict[str, float]:
        """
        Calculate 80% Balance with Registration Fee.
        
        Args:
            balance_80: 80% balance amount
            registration_fee: Registration fee amount
            years: Number of years to pay
            interest_rate: Annual interest rate as percentage
            
        Returns:
            Dictionary containing computed values
        """
        total_80_with_reg = balance_80 + registration_fee
        interest_decimal = interest_rate / 100
        
        if years > 0:
            monthly_amortization = (balance_80 * (1 + (years * interest_decimal))) / years / 12
        else:
            monthly_amortization = 0
        
        return {
            'balance_80_with_reg': total_80_with_reg,
            'monthly_amortization': monthly_amortization
        }

