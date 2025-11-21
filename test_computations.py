"""Test script for computation service."""
import sys
import io
from app.services.computation_service import ComputationService

# Set stdout to UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def format_currency(amount):
    """Format amount as currency."""
    return f"PHP {amount:,.2f}"


def test_spot_cash():
    """Test Spot Cash computation."""
    print("\n" + "="*60)
    print("SPOT CASH COMPUTATION TEST")
    print("="*60)
    
    service = ComputationService()
    result = service.compute_spot_cash(
        tcp=8000000,
        discount_percent=5,
        reservation_fee=50000,
        registration_fee_percent=6,
        move_in_fee_percent=1.5
    )
    
    print(f"Total Contract Price: {format_currency(result['tcp'])}")
    print(f"Discount ({result['discount_percent']}%): {format_currency(result['term_discount'])}")
    print(f"Discounted TCP: {format_currency(result['dtcp'])}")
    print(f"Reservation Fee: {format_currency(result['reservation_fee'])}")
    print(f"Net TCP: {format_currency(result['ntcp'])}")
    print(f"Total List Price: {format_currency(result['tlp'])}")
    print(f"Registration Fee: {format_currency(result['registration_fee'])}")
    print(f"Move-in Fee: {format_currency(result['move_in_fee'])}")


def test_spot_down_payment():
    """Test Spot Down Payment computation."""
    print("\n" + "="*60)
    print("SPOT DOWN PAYMENT COMPUTATION TEST")
    print("="*60)
    
    service = ComputationService()
    result = service.compute_spot_down_payment(
        tcp=8000000,
        discount_percent=5,
        reservation_fee=50000,
        registration_fee_percent=6,
        move_in_fee_percent=1.5
    )
    
    print(f"Total Contract Price: {format_currency(result['tcp'])}")
    print(f"20% Down Payment: {format_currency(result['down_payment'])}")
    print(f"Discount ({result['discount_percent']}%): {format_currency(result['term_discount'])}")
    print(f"Reservation Fee: {format_currency(result['reservation_fee'])}")
    print(f"Net Down Payment: {format_currency(result['ndp'])}")
    print(f"80% Balance: {format_currency(result['balance_80'])}")
    print(f"Registration Fee: {format_currency(result['registration_fee'])}")
    print(f"Move-in Fee: {format_currency(result['move_in_fee'])}")


def test_deferred_payment():
    """Test Deferred Payment computation."""
    print("\n" + "="*60)
    print("DEFERRED PAYMENT COMPUTATION TEST")
    print("="*60)
    
    service = ComputationService()
    result = service.compute_deferred_payment(
        tcp=8000000,
        reservation_fee=50000,
        registration_fee_percent=6,
        move_in_fee_percent=1.5,
        terms=[12, 18, 24]
    )
    
    print(f"Total Contract Price: {format_currency(result['tcp'])}")
    print(f"Reservation Fee: {format_currency(result['reservation_fee'])}")
    print(f"Net TCP: {format_currency(result['ntcp'])}")
    print("\nMonthly Amortizations:")
    for term, amount in sorted(result['monthly_amortizations'].items()):
        print(f"  {term} months: {format_currency(amount)}")
    print(f"Registration Fee: {format_currency(result['registration_fee'])}")
    print(f"Move-in Fee: {format_currency(result['move_in_fee'])}")


def test_20_80_payment():
    """Test 20/80 Payment computation."""
    print("\n" + "="*60)
    print("20/80 PAYMENT COMPUTATION TEST")
    print("="*60)
    
    service = ComputationService()
    result = service.compute_20_80_payment(
        tcp=8000000,
        reservation_fee=50000,
        registration_fee_percent=6,
        move_in_fee_percent=1.5,
        terms_20=[12, 18, 24]
    )
    
    print(f"Total Contract Price: {format_currency(result['tcp'])}")
    print(f"20% Down Payment: {format_currency(result['down_payment'])}")
    print(f"Net Down Payment: {format_currency(result['ndp'])}")
    print("\n20% Monthly Amortizations:")
    for term, amount in sorted(result['monthly_amortizations_20'].items()):
        print(f"  {term} months: {format_currency(amount)}")
    print("\nStaggered RGF Monthly:")
    for term, amount in sorted(result['staggered_rgf_monthly'].items()):
        print(f"  {term} months: {format_currency(amount)}")
    print("\nTotal Monthly (DP + RGF):")
    for term, amount in sorted(result['total_monthly_with_rgf'].items()):
        print(f"  {term} months: {format_currency(amount)}")
    print(f"\n80% Balance: {format_currency(result['balance_80'])}")
    print(f"Registration Fee: {format_currency(result['registration_fee'])}")
    print(f"Move-in Fee: {format_currency(result['move_in_fee'])}")
    print(f"\n20% Net Down Payment: {format_currency(result['net_down_payment_20'])}")
    print(f"20% with Move-in Fee: {format_currency(result['with_move_in'])}")
    print(f"20% with Reg Fee: {format_currency(result['with_reg_fee'])}")
    print(f"20% with Both: {format_currency(result['with_reg_and_move_in'])}")


def test_80_balance_amortization():
    """Test 80% Balance Amortization computation."""
    print("\n" + "="*60)
    print("80% BALANCE AMORTIZATION TEST")
    print("="*60)
    
    service = ComputationService()
    result = service.compute_80_balance_amortization(
        tcp=8000000,
        years=10,
        interest_rate=10
    )
    
    print(f"Total Contract Price: {format_currency(8000000)}")
    print(f"80% Balance: {format_currency(result['balance_80'])}")
    print(f"Years: {result['years']}")
    print(f"Interest Rate: {result['interest_rate']}%")
    print(f"Monthly Amortization: {format_currency(result['monthly_amortization'])}")
    print(f"Total Amount: {format_currency(result['total_amount'])}")


if __name__ == '__main__':
    print("\n" + "="*60)
    print("MOLDEX REALTY COMPUTATION SERVICE TESTS")
    print("="*60)
    
    test_spot_cash()
    test_spot_down_payment()
    test_deferred_payment()
    test_20_80_payment()
    test_80_balance_amortization()
    
    print("\n" + "="*60)
    print("ALL TESTS COMPLETED")
    print("="*60 + "\n")

