# Computation Formula Updates - Implementation Summary

**Date**: November 21, 2024  
**Version**: 2.0.0

## Overview

This document summarizes all the computation formula updates implemented in the Moldex Realty Proposal Generator application.

---

## 1. 80% Balance Terms - Factor Rate Implementation

### Changes Made

**Old Formula:**
```
MA = Balance × (1 + (Years × Interest Rate)) ÷ Years ÷ 12
```

**New Formula:**
```
MA = 80% Balance × Factor Rate
MA with Reg Fee = (80% Balance + Reg Fee) × Factor Rate
```

### Factor Rates Applied

| Term Range | Factor Rate | Interest Rate (Display) |
|------------|-------------|------------------------|
| 1-5 years  | 0.0212470447 | 10% |
| 6-7 years  | 0.0181919633 | 13% |
| 8-10 years | 0.0161334957 | 15% |

### UI Changes

- **Removed**: Term 1, Rate 1, Term 2, Rate 2, Term 3, Rate 3 input fields
- **Added**: Static table with pre-defined terms:
  - 5 years (10%)
  - 7 years (13%)
  - 10 years (15%)

### Files Modified

- `app/services/computation_service.py` - Updated `compute_80_balance_amortization()` method
- `app/templates/index.html` - Removed input fields, added static table
- `app/static/js/script.js` - Updated `calculate80Balance()` and `update80BalanceTable()` functions
- `app/routes/main.py` - Updated to use static terms

---

## 2. TLP Toggle for Registration Fee Calculation

### Feature Description

Added a toggle checkbox in the Contract Details section to control how Registration Fee is calculated.

### Calculation Logic

#### When TLP Toggle is ENABLED (Default):

**Spot Cash:**
```
Registration Fee = (Net TCP / 1.12) × Reg Fee %
```

**Deferred Payment, Spot Down Payment, 20/80 Payment Terms:**
```
Registration Fee = TLP × Reg Fee %
```

#### When TLP Toggle is DISABLED:

**Spot Cash:**
```
Registration Fee = Net TCP × Reg Fee %
```

**Deferred Payment, Spot Down Payment, 20/80 Payment Terms:**
```
Registration Fee = TCP × Reg Fee %
```

### Example Calculation

**Given:**
- TCP = ₱5,000,000
- TLP = ₱4,464,285.71
- Reg Fee % = 6%
- Move-in Fee = 1.5%

**When Enabled:**
```
Reg Fee = 5,000,000 / 1.12 × 6% = ₱267,857.14
```

**When Disabled:**
```
Reg Fee = 5,000,000 × 6% = ₱300,000
```

### Files Modified

- `app/templates/index.html` - Added TLP toggle checkbox
- `app/services/computation_service.py` - Updated all computation methods to accept `use_tlp_for_reg_fee` parameter
- `app/static/js/script.js` - Updated all calculation functions to use toggle value
- `app/routes/main.py` - Pass toggle value to computation service

---

## 3. Spot Cash - Total Payment Field

### Changes Made

Added a new "Total Payment" field to the Spot Cash section.

### Formula

```
Total Payment = Net TCP + Registration Fee + Move-in Fee
```

### Display Location

- **UI**: Added below Move-in Fee in Spot Cash section
- **PDF**: Added below Move-in Fee in Spot Cash table

### Files Modified

- `app/templates/index.html` - Added Total Payment input field
- `app/services/computation_service.py` - Added `total_payment` to return dictionary
- `app/static/js/script.js` - Calculate and display Total Payment
- `app/services/pdf_service.py` - Added Total Payment row to PDF table

---

## 4. TCP ≤ 3,600,000 Special Case

### Rule Implementation

When TCP is equal to or less than ₱3,600,000:

**Spot Cash:**
```
NET TCP = DTCP
TLP = DTCP
```

**Deferred Payment:**
```
NET TCP = DTCP
TLP = TCP
```

**All Other Payment Terms:**
```
TLP = TCP
```

### Logic

```python
if tcp <= 3600000:
    tlp = dtcp  # For Spot Cash
    tlp = tcp   # For other payment terms
else:
    tlp = tcp / 1.12  # Standard calculation
```

### Files Modified

- `app/services/computation_service.py` - Added conditional logic in all computation methods
- `app/static/js/script.js` - Added conditional logic in all JavaScript functions

---

## 5. Summary of All Formula Changes

### Spot Cash

| Field | Old Formula | New Formula |
|-------|-------------|-------------|
| TLP | DTCP ÷ 1.12 | DTCP ÷ 1.12 (or DTCP if TCP ≤ 3.6M) |
| Reg Fee | TLP × % | (Net TCP / 1.12) × % (if toggle enabled) |
| Total Payment | N/A | **NEW**: NTCP + RGF + MIF |

### Deferred Payment

| Field | Old Formula | New Formula |
|-------|-------------|-------------|
| TLP | TCP ÷ 1.12 | TCP ÷ 1.12 (or TCP if TCP ≤ 3.6M) |
| Reg Fee | TLP × % | TLP × % (or TCP × % if toggle disabled) |

### Spot Down Payment & 20/80 Payment Terms

| Field | Old Formula | New Formula |
|-------|-------------|-------------|
| TLP | TCP ÷ 1.12 | TCP ÷ 1.12 (or TCP if TCP ≤ 3.6M) |
| Reg Fee | TLP × % | TLP × % (or TCP × % if toggle disabled) |

### 80% Balance Terms

| Field | Old Formula | New Formula |
|-------|-------------|-------------|
| MA | Balance × (1 + (Years × Rate)) ÷ Years ÷ 12 | **Balance × Factor Rate** |
| MA with Reg Fee | (Balance + RGF) × (1 + (Years × Rate)) ÷ Years ÷ 12 | **(Balance + RGF) × Factor Rate** |

---

## 6. Testing Checklist

### Manual Testing Required

- [ ] Test Spot Cash with TLP toggle enabled
- [ ] Test Spot Cash with TLP toggle disabled
- [ ] Test Spot Cash with TCP ≤ 3,600,000
- [ ] Test Spot Cash with TCP > 3,600,000
- [ ] Verify Total Payment calculation
- [ ] Test Deferred Payment with both toggle states
- [ ] Test Spot Down Payment with both toggle states
- [ ] Test 20/80 Payment Terms with both toggle states
- [ ] Verify 80% Balance calculations for all three terms (5yr, 7yr, 10yr)
- [ ] Generate PDF and verify all values are correct
- [ ] Verify Total Payment appears in PDF

### Test Cases

#### Test Case 1: Standard Calculation
- TCP: ₱5,000,000
- Reg Fee %: 6%
- Move-in Fee %: 1.5%
- TLP Toggle: Enabled

**Expected Results:**
- TLP: ₱4,464,285.71
- Reg Fee (Spot Cash): ₱267,857.14
- Reg Fee (Others): ₱267,857.14

#### Test Case 2: Toggle Disabled
- TCP: ₱5,000,000
- Reg Fee %: 6%
- TLP Toggle: Disabled

**Expected Results:**
- Reg Fee (Spot Cash): ₱300,000
- Reg Fee (Others): ₱300,000

#### Test Case 3: Low TCP
- TCP: ₱3,000,000
- Discount: 5%
- Reg Fee %: 6%

**Expected Results:**
- DTCP: ₱2,850,000
- TLP: ₱2,850,000 (same as DTCP)

#### Test Case 4: 80% Balance
- TCP: ₱5,000,000
- 80% Balance: ₱4,000,000
- Reg Fee: ₱267,857.14

**Expected Results:**
- 5 years MA: ₱4,000,000 × 0.0212470447 = ₱84,988.18
- 5 years MA with Reg: ₱4,267,857.14 × 0.0212470447 = ₱90,677.01
- 7 years MA: ₱4,000,000 × 0.0181919633 = ₱72,767.85
- 10 years MA: ₱4,000,000 × 0.0161334957 = ₱64,533.98

---

## 7. Deployment Instructions

### For Local Development

1. Pull latest changes from GitHub:
   ```bash
   git pull origin main
   ```

2. No new dependencies required

3. Test the application:
   ```bash
   python app.py
   ```

### For PythonAnywhere

1. SSH into PythonAnywhere or use bash console

2. Navigate to project directory:
   ```bash
   cd ~/realty-proposal-generator
   ```

3. Pull latest changes:
   ```bash
   git pull origin main
   ```

4. Reload the web app:
   - Go to Web tab
   - Click "Reload" button

---

## 8. Files Modified Summary

| File | Changes |
|------|---------|
| `app/services/computation_service.py` | Updated all computation methods with new formulas |
| `app/templates/index.html` | Added TLP toggle, removed 80% input fields, added Total Payment |
| `app/static/js/script.js` | Updated all calculation functions |
| `app/routes/main.py` | Updated to pass TLP toggle and use static 80% terms |
| `app/services/pdf_service.py` | Added Total Payment to Spot Cash PDF section |

---

## 9. Version History

### Version 2.0.0 (November 21, 2024)
- Implemented factor rates for 80% Balance Terms
- Added TLP toggle for Registration Fee calculation
- Added Total Payment to Spot Cash
- Implemented TCP ≤ 3,600,000 special case
- Made 80% Balance table static

### Version 1.0.0 (November 11, 2024)
- Initial release with basic computations

---

## 10. Support & Contact

For questions or issues regarding these updates:
- GitHub Repository: https://github.com/edson0312/realty-proposal-generator
- Deployment URL: https://edson001.pythonanywhere.com

---

**Document Version**: 1.0  
**Last Updated**: November 21, 2024  
**Author**: Development Team

