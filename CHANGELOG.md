# Changelog - Moldex Realty Sample Computation Generator

## Version 1.1.0 (November 12, 2024)

### Major Updates

#### UI/UX Improvements
- ✅ **Updated Header Logo**: Changed to `Moldex_Page_Header.jpg`
- ✅ **Enhanced Read-only Fields**: Changed background color to `#e8eaf0` for better visual distinction from editable fields
- ✅ **Added Computation Tables**: Dynamic tables now show monthly amortization breakdowns

#### Contract Details Section
- ❌ **Removed**: Registration Fee and Move-in Fee fields (were redundant)
- ✨ **Simplified**: Now only shows TCP, Reservation Fee, and percentage fields

#### Spot Cash Section
- ✅ **Added TLP Field**: Total List Price (read-only, calculated)
- ✅ **Added Registration Fee Field**: Calculated based on Spot Cash TLP
- ✅ **Added Move-in Fee Field**: Calculated based on Spot Cash TLP
- 📝 **Note**: TLP, Reg Fee, and Move-in Fee are based on **Discounted TCP** (after discount)

#### Deferred Payment Section
- ✅ **Added TLP Field**: Total List Price (read-only, calculated)
- ✅ **Added Registration Fee Field**: Calculated based on TCP
- ✅ **Added Move-in Fee Field**: Calculated based on TCP
- ✅ **Default Terms**: Set to 12, 18, 24 months
- ✅ **Added Computation Table**: Shows monthly amortizations with 4 variations:
  - MA (Monthly Amortization)
  - MA with Reg Fee
  - MA with Move In Fee
  - MA with Reg Fee & Move In Fee
- 📝 **Note**: TLP, Reg Fee, and Move-in Fee are based on **TCP** (not discounted)

**Formulas:**
- MA = (TCP - Discount - Reservation Fee) / Term (months)
- MA with Reg Fee = (TCP - Discount - Reservation Fee + Reg Fee) / Term (months)
- MA with Move In Fee = (TCP - Discount - Reservation Fee + Move In Fee) / Term (months)
- MA with Reg Fee & Move In Fee = (TCP - Discount - Reservation Fee + Reg Fee + Move In Fee) / Term (months)

#### Spot Down Payment Section
- ✅ **Added TLP Field**: Total List Price (read-only, calculated)
- ✅ **Added Registration Fee Field**: Calculated based on TCP
- ✅ **Added Move-in Fee Field**: Calculated based on TCP
- ❌ **Removed**: 80% Balance Terms (moved to separate section)
- 📝 **Note**: TLP, Reg Fee, and Move-in Fee are based on **TCP** (not discounted)

#### 20/80 Payment Terms Section
- ✅ **Added TLP Field**: Total List Price (read-only, calculated)
- ✅ **Added Registration Fee Field**: Calculated based on TCP
- ✅ **Added Move-in Fee Field**: Calculated based on TCP
- ✅ **Default Terms**: Set to 12, 18, 24 months
- ✅ **Added Computation Table**: Shows monthly amortizations with 4 variations:
  - MA (Monthly Amortization)
  - MA with Reg Fee
  - MA with Move In Fee
  - MA with Reg Fee & Move In Fee
- 📝 **Note**: TLP, Reg Fee, and Move-in Fee are based on **TCP** (not discounted)

**Formulas:**
- MA = (20% Net Down Payment) / Term (months)
- MA with Reg Fee = (20% Net Down Payment + Reg Fee) / Term (months)
- MA with Move In Fee = (20% Net Down Payment + Move In Fee) / Term (months)
- MA with Reg Fee & Move In Fee = (20% Net Down Payment + Reg Fee + Move In Fee) / Term (months)

#### 80% Balance Terms Section (New Unified Section)
- ✅ **Consolidated**: Now shared between Spot Down Payment and 20/80 Payment Terms
- ✅ **Default Terms**: 
  - Term 1: 5 years at 10%
  - Term 2: 7 years at 13%
  - Term 3: 10 years at 15%
- ✅ **Added Computation Table**: Shows monthly amortizations with 2 variations:
  - MA (Monthly Amortization)
  - MA with Reg Fee
- ✅ **Dynamic Display**: Shows "Years (Interest %)" format
- ✅ **Flexible Terms**: Adapts to show only filled-in terms

**Formula:**
- MA = (80% Balance × (1 + (Years × Interest Rate))) ÷ Years ÷ 12
- MA with Reg Fee = ((80% Balance + Reg Fee) × (1 + (Years × Interest Rate))) ÷ Years ÷ 12

### Technical Changes

#### JavaScript Updates (`app/static/js/script.js`)
- ✅ **New Calculation Functions**:
  - `updateDeferredTable()`: Generates dynamic deferred payment table
  - `update2080Table()`: Generates dynamic 20/80 payment table
  - `update80BalanceTable()`: Generates dynamic 80% balance table
- ✅ **Enhanced `calculateAll()`**: Now triggers all table updates
- ✅ **Spot Cash Logic**: TLP based on Discounted TCP
- ✅ **Other Sections Logic**: TLP based on original TCP
- ✅ **Event Listeners**: Added for all term and rate fields

#### CSS Updates (`app/static/css/style.css`)
- ✅ **Read-only Field Styling**: New background color `#e8eaf0`
- ✅ **Computation Table Styles**: Professional table design with:
  - Blue header background
  - Alternating row colors
  - Right-aligned currency values
  - Responsive design

#### HTML Updates (`app/templates/index.html`)
- ✅ **Removed Fields**: Registration Fee and Move-in Fee from Contract Details
- ✅ **Added Fields**: TLP, Reg Fee, Move-in Fee to each payment section
- ✅ **Default Values**: Pre-filled term values for better UX
- ✅ **Computation Tables**: Three new dynamic tables
- ✅ **Updated Logo Path**: Changed to `Moldex_Page_Header.jpg`

### Formula Differences Summary

| Section | TLP Calculation | Reg Fee Calculation | Move-in Fee Calculation |
|---------|----------------|---------------------|------------------------|
| **Spot Cash** | Based on **Discounted TCP** | Based on Spot Cash TLP | Based on Spot Cash TLP |
| **Deferred Payment** | Based on **TCP** | Based on TCP TLP | Based on TCP TLP |
| **Spot Down Payment** | Based on **TCP** | Based on TCP TLP | Based on TCP TLP |
| **20/80 Payment** | Based on **TCP** | Based on TCP TLP | Based on TCP TLP |

### Validation & Testing

✅ **All formulas tested** with sample data (TCP = ₱5,000,000)
✅ **Results verified** against expected values
✅ **Dynamic tables** update correctly based on input
✅ **Read-only fields** properly styled and calculated
✅ **Default values** pre-filled for better user experience

### Example Test Results

**Test Data:**
- TCP: ₱5,000,000
- Reservation Fee: ₱30,000
- Registration Fee %: 6%
- Move-in Fee %: 1%

**Deferred Payment (12 months):**
- MA: ₱414,166.67 ✅
- MA with Reg Fee: ₱436,488.10 ✅
- MA with Move In Fee: ₱417,886.90 ✅
- MA with Reg Fee & Move In Fee: ₱440,208.33 ✅

**20/80 Payment (12 months):**
- MA: ₱80,833.33 ✅
- MA with Reg Fee: ₱103,154.76 ✅
- MA with Move In Fee: ₱84,553.57 ✅
- MA with Reg Fee & Move In Fee: ₱106,875.00 ✅

**80% Balance (5 years, 10%):**
- MA: ₱100,000.00 ✅
- MA with Reg Fee: ₱106,696.43 ✅

### User Experience Improvements

1. **Visual Clarity**: Read-only fields now have distinct gray background
2. **Auto-calculations**: All tables update in real-time as you type
3. **Default Values**: Common terms pre-filled (12, 18, 24 months; 5, 7, 10 years)
4. **Dynamic Tables**: Only shows columns for filled-in terms
5. **Professional Formatting**: Currency values properly formatted with commas

### Breaking Changes

⚠️ **None** - All changes are additive or cosmetic

### Migration Notes

- Old PDFs will still work
- New fields are automatically calculated
- No database migration needed (no database used)

---

## Version 1.0.0 (November 11, 2024)

### Initial Release
- Complete Flask web application
- PDF generation with ReportLab
- Multiple payment term support
- Responsive modern UI
- File upload functionality
- Auto-calculations

---

**Last Updated:** November 12, 2024  
**Current Version:** 1.1.0

