# Moldex Realty Computation Formulas Reference

This document provides a comprehensive reference for all computation formulas used in the Sample Computation Generator.

## Table of Contents
1. [Common Variables](#common-variables)
2. [Spot Cash](#spot-cash)
3. [Deferred Payment](#deferred-payment)
4. [Spot Down Payment](#spot-down-payment)
5. [20/80 Payment Terms](#2080-payment-terms)
6. [80% Balance Amortization](#80-balance-amortization)

---

## Common Variables

| Variable | Description | Example |
|----------|-------------|---------|
| TCP | Total Contract Price | ₱8,000,000 |
| RF | Reservation Fee | ₱50,000 |
| RGF | Registration Fee | Calculated |
| MIF | Move-in Fee | Calculated |
| TLP | Total List Price (VAT removed) | TCP ÷ 1.12 |
| VAT | Value Added Tax | 12% (included in TCP) |

---

## Spot Cash

**Use Case:** Payment in full within 7 days with discount

### Formulas

1. **Term Discount (TD)**
   ```
   TD = TCP × (Discount % ÷ 100)
   ```

2. **Discounted Total Contract Price (DTCP)**
   ```
   DTCP = TCP - TD
   ```

3. **Net Total Contract Price (NTCP)**
   ```
   NTCP = DTCP - RF
   ```

4. **Total List Price (TLP)**
   ```
   TLP = DTCP ÷ 1.12
   ```

5. **Registration Fee (RGF)**
   ```
   RGF = TLP × (Registration Fee % ÷ 100)
   ```

6. **Move-in Fee (MIF)**
   ```
   MIF = TLP × (Move-in Fee % ÷ 100)
   ```

### Example Calculation

**Given:**
- TCP = ₱8,000,000
- Discount = 5%
- RF = ₱50,000
- Registration Fee % = 6%
- Move-in Fee % = 1.5%

**Results:**
- TD = ₱8,000,000 × 5% = ₱400,000
- DTCP = ₱8,000,000 - ₱400,000 = ₱7,600,000
- NTCP = ₱7,600,000 - ₱50,000 = ₱7,550,000
- TLP = ₱7,600,000 ÷ 1.12 = ₱6,785,714.29
- RGF = ₱6,785,714.29 × 6% = ₱407,142.86
- MIF = ₱6,785,714.29 × 1.5% = ₱101,785.71

---

## Deferred Payment

**Use Case:** Pay over time without interest (installment payment)

### Formulas

1. **Net Total Contract Price (NTCP)**
   ```
   NTCP = TCP - RF
   ```

2. **Monthly Amortization**
   ```
   Monthly Amortization = NTCP ÷ Number of Months
   ```

3. **Total List Price (TLP)**
   ```
   TLP = TCP ÷ 1.12
   ```

4. **Registration Fee (RGF)**
   ```
   RGF = TLP × (Registration Fee % ÷ 100)
   ```

5. **Move-in Fee (MIF)**
   ```
   MIF = TLP × (Move-in Fee % ÷ 100)
   ```

### Example Calculation

**Given:**
- TCP = ₱8,000,000
- RF = ₱50,000
- Terms = 12, 18, 24 months

**Results:**
- NTCP = ₱8,000,000 - ₱50,000 = ₱7,950,000
- 12 months = ₱7,950,000 ÷ 12 = ₱662,500.00
- 18 months = ₱7,950,000 ÷ 18 = ₱441,666.67
- 24 months = ₱7,950,000 ÷ 24 = ₱331,250.00

---

## Spot Down Payment

**Use Case:** Pay 20% down with discount, finance 80% balance

### Formulas

1. **20% Down Payment (DP)**
   ```
   DP = TCP × 20%
   ```

2. **Term Discount (TD)**
   ```
   TD = DP × (Discount % ÷ 100)
   ```

3. **Net Down Payment (NDP)**
   ```
   NDP = DP - TD - RF
   ```

4. **80% Balance**
   ```
   80% Balance = TCP × 80%
   ```

5. **Total List Price (TLP)**
   ```
   TLP = TCP ÷ 1.12
   ```

6. **Registration Fee (RGF)**
   ```
   RGF = TLP × (Registration Fee % ÷ 100)
   ```

7. **Move-in Fee (MIF)**
   ```
   MIF = TLP × (Move-in Fee % ÷ 100)
   ```

### Example Calculation

**Given:**
- TCP = ₱8,000,000
- Discount = 5%
- RF = ₱50,000

**Results:**
- DP = ₱8,000,000 × 20% = ₱1,600,000
- TD = ₱1,600,000 × 5% = ₱80,000
- NDP = ₱1,600,000 - ₱80,000 - ₱50,000 = ₱1,470,000
- 80% Balance = ₱8,000,000 × 80% = ₱6,400,000

---

## 20/80 Payment Terms

**Use Case:** Pay 20% down over months, finance 80% balance

### Formulas

#### 20% Down Payment Calculations

1. **20% Down Payment (DP)**
   ```
   DP = TCP × 20%
   ```

2. **Net Down Payment (NDP)**
   ```
   NDP = DP - RF
   ```

3. **Monthly Amortization (20%)**
   ```
   Monthly Amortization = NDP ÷ Number of Months
   ```

4. **Staggered RGF Monthly**
   ```
   Staggered RGF Monthly = RGF ÷ Number of Months
   ```

5. **Total Monthly (DP + RGF)**
   ```
   Total Monthly = Monthly Amortization + Staggered RGF Monthly
   ```

#### Payment Options

1. **20% Net Down Payment**
   ```
   = NDP
   ```

2. **20% with Move-in Fee**
   ```
   = NDP + MIF
   ```

3. **20% with Registration Fee**
   ```
   = NDP + RGF
   ```

4. **20% with Both Fees**
   ```
   = NDP + RGF + MIF
   ```

#### 80% Balance Calculations

1. **80% Balance**
   ```
   80% Balance = TCP × 80%
   ```

2. **80% with Registration Fee**
   ```
   80% with RGF = 80% Balance + RGF
   ```

### Example Calculation

**Given:**
- TCP = ₱8,000,000
- RF = ₱50,000
- Terms = 12, 18, 24 months
- RGF = ₱428,571.43

**Results:**
- DP = ₱1,600,000
- NDP = ₱1,550,000

**Monthly Amortizations (20%):**
- 12 months: ₱1,550,000 ÷ 12 = ₱129,166.67
- 18 months: ₱1,550,000 ÷ 18 = ₱86,111.11
- 24 months: ₱1,550,000 ÷ 24 = ₱64,583.33

**Staggered RGF:**
- 12 months: ₱428,571.43 ÷ 12 = ₱35,714.29
- 18 months: ₱428,571.43 ÷ 18 = ₱23,809.52
- 24 months: ₱428,571.43 ÷ 24 = ₱17,857.14

**Total Monthly (DP + RGF):**
- 12 months: ₱129,166.67 + ₱35,714.29 = ₱164,880.95
- 18 months: ₱86,111.11 + ₱23,809.52 = ₱109,920.63
- 24 months: ₱64,583.33 + ₱17,857.14 = ₱82,440.48

---

## 80% Balance Amortization

**Use Case:** Calculate monthly payments for 80% balance with interest

### Formula

```
Monthly Amortization = (Balance × (1 + (Years × Interest Rate))) ÷ Years ÷ 12
```

Where:
- Balance = TCP × 80%
- Years = Number of years to pay
- Interest Rate = Annual interest rate (as decimal, e.g., 0.10 for 10%)

### Example Calculation

**Given:**
- TCP = ₱8,000,000
- Years = 10
- Interest Rate = 10% per annum

**Calculation:**
```
Balance = ₱8,000,000 × 80% = ₱6,400,000
Monthly Amortization = ₱6,400,000 × (1 + (10 × 0.10)) ÷ 10 ÷ 12
                     = ₱6,400,000 × 2 ÷ 10 ÷ 12
                     = ₱12,800,000 ÷ 10 ÷ 12
                     = ₱106,666.67 per month
```

**Total Amount:**
```
Total Amount = Monthly Amortization × Years × 12
             = ₱106,666.67 × 10 × 12
             = ₱12,800,000
```

---

## VAT Calculation

All prices are VAT-inclusive. To get the base price (Total List Price):

```
TLP = Price with VAT ÷ 1.12
```

To calculate VAT amount:

```
VAT Amount = Price with VAT - (Price with VAT ÷ 1.12)
```

Or:

```
VAT Amount = TLP × 0.12
```

---

## Notes

1. **Rounding:** All currency values are rounded to 2 decimal places (centavos).

2. **Payment Timing:** 
   - Spot Cash discounts are valid for 7 calendar days from reservation
   - Monthly payments typically start 30 days after down payment

3. **Fees:**
   - Registration fees cover transfer of title and documentation
   - Move-in fees cover initial occupancy charges
   - All fees are based on Total List Price (VAT-exclusive amount)

4. **Interest Calculation:**
   - The 80% balance formula uses simple interest calculation
   - For compound interest, banks may use different formulas
   - Actual bank rates may vary from in-house financing

5. **Disclaimer:**
   - All computations are subject to management approval
   - Prices and terms may change without prior notice
   - Final amounts may vary due to additional charges or adjustments

---

**Last Updated:** November 11, 2024  
**Version:** 1.0.0

