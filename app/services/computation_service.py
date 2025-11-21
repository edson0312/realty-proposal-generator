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
        move_in_fee_percent: float
    ) -> Dict[str, float]:
        """
        Calculate Spot Cash payment terms.
        
        Args:
            tcp: Total Contract Price
            discount_percent: Term discount percentage
            reservation_fee: Reservation fee amount
            registration_fee_percent: Registration fee percentage
            move_in_fee_percent: Move-in fee percentage
            
        Returns:
            Dictionary containing computed values
        """
        term_discount = tcp * (discount_percent / 100)
        dtcp = tcp - term_discount  # Discounted Total Contract Price
        ntcp = dtcp - reservation_fee  # Net Total Contract Price
        tlp = dtcp / 1.12  # Total List Price (removing 12% VAT)
        registration_fee = tlp * (registration_fee_percent / 100)
        move_in_fee = tlp * (move_in_fee_percent / 100)
        
        return {
            'tcp': tcp,
            'term_discount': term_discount,
            'discount_percent': discount_percent,
            'dtcp': dtcp,
            'reservation_fee': reservation_fee,
            'ntcp': ntcp,
            'tlp': tlp,
            'registration_fee': registration_fee,
            'move_in_fee': move_in_fee,
            'net_tcp': ntcp
        }
    
    @staticmethod
    def compute_spot_down_payment(
        tcp: float,
        discount_percent: float,
        reservation_fee: float,
        registration_fee_percent: float,
        move_in_fee_percent: float
    ) -> Dict[str, float]:
        """
        Calculate Spot Down Payment terms.
        
        Args:
            tcp: Total Contract Price
            discount_percent: Term discount percentage
            reservation_fee: Reservation fee amount
            registration_fee_percent: Registration fee percentage
            move_in_fee_percent: Move-in fee percentage
            
        Returns:
            Dictionary containing computed values
        """
        down_payment = tcp * 0.20  # 20% Down Payment
        term_discount = down_payment * (discount_percent / 100)
        ndp = down_payment - term_discount - reservation_fee  # Net Down Payment
        balance_80 = tcp * 0.80  # 80% Balance
        tlp = tcp / 1.12  # Total List Price
        registration_fee = tlp * (registration_fee_percent / 100)
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
        terms: List[int]
    ) -> Dict[str, Any]:
        """
        Calculate Deferred Payment terms.
        
        Args:
            tcp: Total Contract Price
            reservation_fee: Reservation fee amount
            registration_fee_percent: Registration fee percentage
            move_in_fee_percent: Move-in fee percentage
            terms: List of term lengths in months
            
        Returns:
            Dictionary containing computed values
        """
        ntcp = tcp - reservation_fee  # Net Total Contract Price
        tlp = tcp / 1.12  # Total List Price
        registration_fee = tlp * (registration_fee_percent / 100)
        move_in_fee = tlp * (move_in_fee_percent / 100)
        
        # Calculate monthly amortizations for each term
        monthly_amortizations = {}
        for term in terms:
            if term > 0:
                monthly_amortizations[term] = ntcp / term
        
        return {
            'tcp': tcp,
            'reservation_fee': reservation_fee,
            'ntcp': ntcp,
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
        terms_20: List[int]
    ) -> Dict[str, Any]:
        """
        Calculate 20/80 Payment terms.
        
        Args:
            tcp: Total Contract Price
            reservation_fee: Reservation fee amount
            registration_fee_percent: Registration fee percentage
            move_in_fee_percent: Move-in fee percentage
            terms_20: List of term lengths for 20% in months
            
        Returns:
            Dictionary containing computed values
        """
        down_payment = tcp * 0.20  # 20% Down Payment
        ndp = down_payment - reservation_fee  # Net Down Payment
        balance_80 = tcp * 0.80  # 80% Balance
        tlp = tcp / 1.12  # Total List Price
        registration_fee = tlp * (registration_fee_percent / 100)
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
        interest_rate: float
    ) -> Dict[str, float]:
        """
        Calculate 80% Balance Amortization.
        
        Formula: TCP × 80% × (1 + (Years × Interest)) ÷ Years ÷ 12
        
        Args:
            tcp: Total Contract Price
            years: Number of years to pay
            interest_rate: Annual interest rate as percentage
            
        Returns:
            Dictionary containing computed values
        """
        balance_80 = tcp * 0.80
        interest_decimal = interest_rate / 100
        
        if years > 0:
            monthly_amortization = (balance_80 * (1 + (years * interest_decimal))) / years / 12
        else:
            monthly_amortization = 0
        
        total_amount = monthly_amortization * years * 12
        
        # Calculate MA with Registration Fee
        tlp = tcp / 1.12
        # Assuming 6% registration fee as default if not provided
        reg_fee_amount = tlp * 0.06
        balance_80_with_reg = balance_80 + reg_fee_amount
        
        if years > 0:
            ma_with_reg = (balance_80_with_reg * (1 + (years * interest_decimal))) / years / 12
        else:
            ma_with_reg = 0
        
        return {
            'balance_80': balance_80,
            'monthly_amortization': monthly_amortization,
            'ma': monthly_amortization,  # PDF expects 'ma'
            'ma_with_reg': ma_with_reg,  # PDF expects 'ma_with_reg'
            'years': years,
            'interest_rate': interest_rate,
            'rate': interest_rate,  # PDF expects 'rate'
            'total_amount': total_amount
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

