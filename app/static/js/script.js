// DOM Elements
const proposalForm = document.getElementById('proposalForm');
const productType = document.getElementById('product_type');
const verticalFields = document.getElementById('vertical_fields');
const horizontalFields = document.getElementById('horizontal_fields');
const projectTypeHorizontal = document.getElementById('project_type_horizontal');
const houseAndLotFields = document.getElementById('house_and_lot_fields');
const lotOnlyFields = document.getElementById('lot_only_fields');
const generateBtn = document.getElementById('generateBtn');
const loadingSpinner = document.getElementById('loadingSpinner');
const messageDisplay = document.getElementById('messageDisplay');

// Contract detail fields
const tcpField = document.getElementById('tcp');
const reservationFeeField = document.getElementById('reservation_fee');
const registrationFeePercentField = document.getElementById('registration_fee_percent');
const moveInFeePercentField = document.getElementById('move_in_fee_percent');
const useTLPToggleField = document.getElementById('use_tlp_toggle');

// Spot Cash fields
const spotCashDiscountField = document.getElementById('spot_cash_discount');
const spotCashDiscountAmountField = document.getElementById('spot_cash_discount_amount');
const spotCashNetTCPField = document.getElementById('spot_cash_net_tcp');
const spotCashTLPField = document.getElementById('spot_cash_tlp');
const spotCashRegFeeField = document.getElementById('spot_cash_registration_fee');
const spotCashMoveInFeeField = document.getElementById('spot_cash_move_in_fee');
const spotCashTotalPaymentField = document.getElementById('spot_cash_total_payment');

// Deferred Payment fields
const deferredDiscountField = document.getElementById('deferred_discount');
const deferredDiscountAmountField = document.getElementById('deferred_discount_amount');
const deferredTLPField = document.getElementById('deferred_tlp');
const deferredRegFeeField = document.getElementById('deferred_registration_fee');
const deferredMoveInFeeField = document.getElementById('deferred_move_in_fee');
const deferredTerm1Field = document.getElementById('deferred_term1');
const deferredTerm2Field = document.getElementById('deferred_term2');
const deferredTerm3Field = document.getElementById('deferred_term3');

// Spot Down Payment fields
const spotDownDiscountField = document.getElementById('spot_down_discount');
const spotDownDiscountAmountField = document.getElementById('spot_down_discount_amount');
const spotDown80BalanceField = document.getElementById('spot_down_80_balance');
const spotDownTLPField = document.getElementById('spot_down_tlp');
const spotDownRegFeeField = document.getElementById('spot_down_registration_fee');
const spotDownMoveInFeeField = document.getElementById('spot_down_move_in_fee');

// 20/80 Payment fields
const payment2080NetDPField = document.getElementById('payment_20_80_net_dp');
const payment2080WithMoveInField = document.getElementById('payment_20_80_with_move_in');
const payment2080WithRegField = document.getElementById('payment_20_80_with_reg');
const payment2080WithBothField = document.getElementById('payment_20_80_with_both');
const payment2080TLPField = document.getElementById('payment_20_80_tlp');
const payment2080RegFeeField = document.getElementById('payment_20_80_registration_fee');
const payment2080MoveInFeeField = document.getElementById('payment_20_80_move_in_fee');
const payment2080Term1Field = document.getElementById('payment_20_80_term1');
const payment2080Term2Field = document.getElementById('payment_20_80_term2');
const payment2080Term3Field = document.getElementById('payment_20_80_term3');

// 80% Balance fields
const balance80Field = document.getElementById('balance_80');
const balance80WithRegField = document.getElementById('balance_80_with_reg');
const balance80MA5Field = document.getElementById('balance_80_ma_5');
const balance80MAReg5Field = document.getElementById('balance_80_ma_reg_5');
const balance80MA7Field = document.getElementById('balance_80_ma_7');
const balance80MAReg7Field = document.getElementById('balance_80_ma_reg_7');
const balance80MA10Field = document.getElementById('balance_80_ma_10');
const balance80MAReg10Field = document.getElementById('balance_80_ma_reg_10');

// Event Listeners
productType.addEventListener('change', handleProductTypeChange);
projectTypeHorizontal.addEventListener('change', handleProjectTypeHorizontalChange);

// Auto-calculation event listeners
tcpField.addEventListener('input', calculateAll);
reservationFeeField.addEventListener('input', calculateAll);
registrationFeePercentField.addEventListener('input', calculateAll);
moveInFeePercentField.addEventListener('input', calculateAll);
useTLPToggleField.addEventListener('change', calculateAll);

spotCashDiscountField.addEventListener('input', calculateAll);
deferredDiscountField.addEventListener('input', calculateAll);
spotDownDiscountField.addEventListener('input', calculateAll);

// Term change listeners
deferredTerm1Field.addEventListener('input', calculateAll);
deferredTerm2Field.addEventListener('input', calculateAll);
deferredTerm3Field.addEventListener('input', calculateAll);
payment2080Term1Field.addEventListener('input', calculateAll);
payment2080Term2Field.addEventListener('input', calculateAll);
payment2080Term3Field.addEventListener('input', calculateAll);

// Form submission
proposalForm.addEventListener('submit', handleFormSubmit);

// Initialize form state
handleProductTypeChange();
calculateAll();

/**
 * Handle product type change (Vertical/Horizontal)
 */
function handleProductTypeChange() {
    const selectedType = productType.value;
    
    if (selectedType === 'Vertical') {
        verticalFields.style.display = 'block';
        horizontalFields.style.display = 'none';
        clearFieldGroup(horizontalFields);
    } else {
        verticalFields.style.display = 'none';
        horizontalFields.style.display = 'block';
        clearFieldGroup(verticalFields);
        handleProjectTypeHorizontalChange();
    }
}

/**
 * Handle horizontal project type change (House and Lot/Lot)
 */
function handleProjectTypeHorizontalChange() {
    const selectedType = projectTypeHorizontal.value;
    
    if (selectedType === 'House and Lot') {
        houseAndLotFields.style.display = 'block';
        lotOnlyFields.style.display = 'none';
        clearFieldGroup(lotOnlyFields);
    } else {
        houseAndLotFields.style.display = 'none';
        lotOnlyFields.style.display = 'block';
        clearFieldGroup(houseAndLotFields);
    }
}

/**
 * Clear all input fields in a group
 */
function clearFieldGroup(fieldGroup) {
    const inputs = fieldGroup.querySelectorAll('input, select, textarea');
    inputs.forEach(input => {
        if (input.type === 'file') {
            input.value = '';
        } else if (input.tagName === 'SELECT') {
            input.selectedIndex = 0;
        } else if (!input.readOnly && !input.disabled && !input.hasAttribute('value')) {
            input.value = '';
        }
    });
}

/**
 * Calculate all payment terms
 */
function calculateAll() {
    calculateSpotCash();
    calculateDeferredPayment();
    calculateSpotDownPayment();
    calculate2080Payment();
    calculate80Balance();
}

/**
 * Calculate Spot Cash values
 * TLP, Reg Fee, and Move In Fee are based on Net TCP (after discount)
 */
function calculateSpotCash() {
    const tcp = parseFloat(tcpField.value) || 0;
    const discount = parseFloat(spotCashDiscountField.value) || 0;
    const reservationFee = parseFloat(reservationFeeField.value) || 0;
    const regFeePercent = parseFloat(registrationFeePercentField.value) || 0;
    const moveInFeePercent = parseFloat(moveInFeePercentField.value) || 0;
    const useTLP = useTLPToggleField.checked;
    
    if (tcp > 0) {
        const termDiscount = tcp * (discount / 100);
        const dtcp = tcp - termDiscount; // Discounted TCP
        const ntcp = dtcp; // Net TCP = DTCP
        
        // Handle special case: TCP <= 3,600,000
        const tlp = (tcp <= 3600000) ? dtcp : (dtcp / 1.12);
        
        // Calculate Registration Fee based on toggle
        let regFee;
        if (useTLP) {
            // When enabled: Net TCP / 1.12 * Reg Fee %
            regFee = (ntcp / 1.12) * (regFeePercent / 100);
        } else {
            // When disabled: Net TCP * Reg Fee %
            regFee = ntcp * (regFeePercent / 100);
        }
        
        const moveInFee = tlp * (moveInFeePercent / 100);
        const totalPayment = ntcp + regFee + moveInFee;
        
        spotCashDiscountAmountField.value = termDiscount.toFixed(2);
        spotCashNetTCPField.value = ntcp.toFixed(2);
        spotCashTLPField.value = tlp.toFixed(2);
        spotCashRegFeeField.value = regFee.toFixed(2);
        spotCashMoveInFeeField.value = moveInFee.toFixed(2);
        spotCashTotalPaymentField.value = totalPayment.toFixed(2);
    }
}

/**
 * Calculate Deferred Payment values
 * TLP, Reg Fee, and Move In Fee are based on TCP (not discounted)
 */
function calculateDeferredPayment() {
    const tcp = parseFloat(tcpField.value) || 0;
    const discount = parseFloat(deferredDiscountField.value) || 0;
    const reservationFee = parseFloat(reservationFeeField.value) || 0;
    const regFeePercent = parseFloat(registrationFeePercentField.value) || 0;
    const moveInFeePercent = parseFloat(moveInFeePercentField.value) || 0;
    const useTLP = useTLPToggleField.checked;
    
    if (tcp > 0) {
        const discountAmount = tcp * (discount / 100);
        
        // Handle special case: TCP <= 3,600,000
        const tlp = (tcp <= 3600000) ? tcp : (tcp / 1.12);
        
        // Calculate Registration Fee based on toggle
        let regFee;
        if (useTLP) {
            // When enabled: TLP * Reg Fee %
            regFee = tlp * (regFeePercent / 100);
        } else {
            // When disabled: TCP * Reg Fee %
            regFee = tcp * (regFeePercent / 100);
        }
        
        const moveInFee = tlp * (moveInFeePercent / 100);
        
        deferredDiscountAmountField.value = discountAmount.toFixed(2);
        deferredTLPField.value = tlp.toFixed(2);
        deferredRegFeeField.value = regFee.toFixed(2);
        deferredMoveInFeeField.value = moveInFee.toFixed(2);
        
        // Calculate monthly amortizations
        const netAmount = tcp - discountAmount - reservationFee;
        const terms = [
            parseInt(deferredTerm1Field.value) || 0,
            parseInt(deferredTerm2Field.value) || 0,
            parseInt(deferredTerm3Field.value) || 0
        ].filter(t => t > 0);
        
        updateDeferredTable(terms, netAmount, regFee, moveInFee);
    }
}

/**
 * Update Deferred Payment computation table
 */
function updateDeferredTable(terms, netAmount, regFee, moveInFee) {
    const tbody = document.getElementById('deferred_computation_body');
    
    if (terms.length === 0 || netAmount <= 0) {
        tbody.innerHTML = '<tr><td colspan="5" style="text-align: center; color: #6b7280;">Enter contract details and terms to see computations</td></tr>';
        return;
    }
    
    let html = '';
    terms.forEach(term => {
        const ma = netAmount / term;
        const maWithReg = (netAmount + regFee) / term;
        const maWithMove = (netAmount + moveInFee) / term;
        const maWithBoth = (netAmount + regFee + moveInFee) / term;
        
        html += `
            <tr>
                <td>${term}</td>
                <td>${formatCurrency(ma)}</td>
                <td>${formatCurrency(maWithReg)}</td>
                <td>${formatCurrency(maWithMove)}</td>
                <td>${formatCurrency(maWithBoth)}</td>
            </tr>
        `;
    });
    
    tbody.innerHTML = html;
}

/**
 * Calculate Spot Down Payment values
 * TLP, Reg Fee, and Move In Fee are based on TCP (not discounted)
 */
function calculateSpotDownPayment() {
    const tcp = parseFloat(tcpField.value) || 0;
    const discount = parseFloat(spotDownDiscountField.value) || 0;
    const reservationFee = parseFloat(reservationFeeField.value) || 0;
    const regFeePercent = parseFloat(registrationFeePercentField.value) || 0;
    const moveInFeePercent = parseFloat(moveInFeePercentField.value) || 0;
    const useTLP = useTLPToggleField.checked;
    
    if (tcp > 0) {
        const downPayment = tcp * 0.20;
        const termDiscount = downPayment * (discount / 100);
        const balance80 = tcp * 0.80;
        
        // Handle special case: TCP <= 3,600,000
        const tlp = (tcp <= 3600000) ? tcp : (tcp / 1.12);
        
        // Calculate Registration Fee based on toggle
        let regFee;
        if (useTLP) {
            // When enabled: TLP * Reg Fee %
            regFee = tlp * (regFeePercent / 100);
        } else {
            // When disabled: TCP * Reg Fee %
            regFee = tcp * (regFeePercent / 100);
        }
        
        const moveInFee = tlp * (moveInFeePercent / 100);
        
        spotDownDiscountAmountField.value = termDiscount.toFixed(2);
        spotDown80BalanceField.value = balance80.toFixed(2);
        spotDownTLPField.value = tlp.toFixed(2);
        spotDownRegFeeField.value = regFee.toFixed(2);
        spotDownMoveInFeeField.value = moveInFee.toFixed(2);
    }
}

/**
 * Calculate 20/80 Payment values
 * TLP, Reg Fee, and Move In Fee are based on TCP (not discounted)
 */
function calculate2080Payment() {
    const tcp = parseFloat(tcpField.value) || 0;
    const reservationFee = parseFloat(reservationFeeField.value) || 0;
    const regFeePercent = parseFloat(registrationFeePercentField.value) || 0;
    const moveInFeePercent = parseFloat(moveInFeePercentField.value) || 0;
    const useTLP = useTLPToggleField.checked;
    
    if (tcp > 0) {
        const downPayment = tcp * 0.20;
        const ndp = downPayment - reservationFee;
        const balance80 = tcp * 0.80;
        
        // Handle special case: TCP <= 3,600,000
        const tlp = (tcp <= 3600000) ? tcp : (tcp / 1.12);
        
        // Calculate Registration Fee based on toggle
        let regFee;
        if (useTLP) {
            // When enabled: TLP * Reg Fee %
            regFee = tlp * (regFeePercent / 100);
        } else {
            // When disabled: TCP * Reg Fee %
            regFee = tcp * (regFeePercent / 100);
        }
        
        const moveInFee = tlp * (moveInFeePercent / 100);
        
        payment2080NetDPField.value = ndp.toFixed(2);
        payment2080WithMoveInField.value = (ndp + moveInFee).toFixed(2);
        payment2080WithRegField.value = (ndp + regFee).toFixed(2);
        payment2080WithBothField.value = (ndp + regFee + moveInFee).toFixed(2);
        payment2080TLPField.value = tlp.toFixed(2);
        payment2080RegFeeField.value = regFee.toFixed(2);
        payment2080MoveInFeeField.value = moveInFee.toFixed(2);
        
        // Calculate monthly amortizations
        const terms = [
            parseInt(payment2080Term1Field.value) || 0,
            parseInt(payment2080Term2Field.value) || 0,
            parseInt(payment2080Term3Field.value) || 0
        ].filter(t => t > 0);
        
        update2080Table(terms, ndp, regFee, moveInFee);
    }
}

/**
 * Update 20/80 Payment computation table
 */
function update2080Table(terms, ndp, regFee, moveInFee) {
    const tbody = document.getElementById('payment_20_80_computation_body');
    
    if (terms.length === 0 || ndp <= 0) {
        tbody.innerHTML = '<tr><td colspan="5" style="text-align: center; color: #6b7280;">Enter contract details and terms to see computations</td></tr>';
        return;
    }
    
    let html = '';
    terms.forEach(term => {
        const ma = ndp / term;
        const maWithReg = (ndp + regFee) / term;
        const maWithMove = (ndp + moveInFee) / term;
        const maWithBoth = (ndp + regFee + moveInFee) / term;
        
        html += `
            <tr>
                <td>${term}</td>
                <td>${formatCurrency(ma)}</td>
                <td>${formatCurrency(maWithReg)}</td>
                <td>${formatCurrency(maWithMove)}</td>
                <td>${formatCurrency(maWithBoth)}</td>
            </tr>
        `;
    });
    
    tbody.innerHTML = html;
}

/**
 * Calculate 80% Balance values with Factor Rates
 */
function calculate80Balance() {
    const tcp = parseFloat(tcpField.value) || 0;
    const regFeePercent = parseFloat(registrationFeePercentField.value) || 0;
    const useTLP = useTLPToggleField.checked;
    
    if (tcp > 0) {
        const balance80 = tcp * 0.80;
        
        // Handle special case: TCP <= 3,600,000
        const tlp = (tcp <= 3600000) ? tcp : (tcp / 1.12);
        
        // Calculate Registration Fee based on toggle
        let regFee;
        if (useTLP) {
            regFee = tlp * (regFeePercent / 100);
        } else {
            regFee = tcp * (regFeePercent / 100);
        }
        
        const balance80WithReg = balance80 + regFee;
        
        balance80Field.value = balance80.toFixed(2);
        balance80WithRegField.value = balance80WithReg.toFixed(2);
        
        // Calculate with static terms and factor rates
        // Factor Rates: 1-5 years: 0.0212470447, 6-7 years: 0.0181919633, 8-10 years: 0.0161334957
        const terms = [
            { years: 5, rate: 10, factorRate: 0.0212470447 },
            { years: 7, rate: 13, factorRate: 0.0181919633 },
            { years: 10, rate: 15, factorRate: 0.0161334957 }
        ];
        
        update80BalanceTable(terms, balance80, balance80WithReg);
    }
}

/**
 * Update 80% Balance computation table with Factor Rates
 */
function update80BalanceTable(terms, balance80, balance80WithReg) {
    if (balance80 <= 0) {
        balance80MA5Field.textContent = '-';
        balance80MAReg5Field.textContent = '-';
        balance80MA7Field.textContent = '-';
        balance80MAReg7Field.textContent = '-';
        balance80MA10Field.textContent = '-';
        balance80MAReg10Field.textContent = '-';
        return;
    }
    
    // Calculate MA using factor rates
    // Formula: MA = 80% Balance * Factor Rate
    // Formula: MA with Reg Fee = (80% Balance + Reg Fee) * Factor Rate
    terms.forEach(term => {
        const ma = balance80 * term.factorRate;
        const maWithReg = balance80WithReg * term.factorRate;
        
        if (term.years === 5) {
            balance80MA5Field.textContent = formatCurrency(ma);
            balance80MAReg5Field.textContent = formatCurrency(maWithReg);
        } else if (term.years === 7) {
            balance80MA7Field.textContent = formatCurrency(ma);
            balance80MAReg7Field.textContent = formatCurrency(maWithReg);
        } else if (term.years === 10) {
            balance80MA10Field.textContent = formatCurrency(ma);
            balance80MAReg10Field.textContent = formatCurrency(maWithReg);
        }
    });
}

/**
 * Handle form submission
 */
async function handleFormSubmit(e) {
    e.preventDefault();
    
    // Validate required fields
    if (!validateForm()) {
        return;
    }
    
    // Show loading state
    generateBtn.disabled = true;
    loadingSpinner.style.display = 'block';
    messageDisplay.style.display = 'none';
    
    try {
        const formData = new FormData(proposalForm);
        
        // Handle conditional fields based on product type
        const productTypeValue = formData.get('product_type');
        
        if (productTypeValue === 'Vertical') {
            formData.set('project_type', formData.get('project_type') || '');
            formData.set('brand', formData.get('brand') || formData.get('brand_vertical') || '');
            formData.set('address', formData.get('address') || formData.get('address_vertical') || '');
            formData.set('property_details_vertical', formData.get('property_details_vertical') || '');
            formData.set('floor_area', formData.get('floor_area') || formData.get('floor_area_vertical') || '');
            
            const pictureFile = document.getElementById('picture_vertical').files[0];
            if (pictureFile) {
                formData.set('picture', pictureFile);
            }
        } else {
            formData.set('project_type', formData.get('project_type_horiz') || '');
            formData.set('brand', formData.get('brand_horiz') || '');
            formData.set('address', formData.get('address_horiz') || '');
            
            if (formData.get('project_type_horiz') === 'House and Lot') {
                formData.set('lot_area', formData.get('lot_area_hl') || '');
                formData.set('floor_area', formData.get('floor_area_hl') || '');
                
                const pictureFile = document.getElementById('picture_hl').files[0];
                if (pictureFile) {
                    formData.set('picture', pictureFile);
                }
            } else {
                formData.set('lot_area', formData.get('lot_area_lot') || '');
                
                const pictureFile = document.getElementById('picture_lot').files[0];
                if (pictureFile) {
                    formData.set('picture', pictureFile);
                }
            }
        }
        
        // Send request
        const response = await fetch('/generate-proposal', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        if (result.success) {
            showMessage('success', `
                Proposal generated successfully! 
                <a href="${result.download_url}" target="_blank">Click here to download</a>
            `);
        } else {
            showMessage('error', result.message || 'Failed to generate proposal');
        }
    } catch (error) {
        console.error('Error:', error);
        showMessage('error', 'An error occurred while generating the proposal. Please try again.');
    } finally {
        generateBtn.disabled = false;
        loadingSpinner.style.display = 'none';
    }
}

/**
 * Validate form fields
 */
function validateForm() {
    const requiredFields = proposalForm.querySelectorAll('[required]');
    let isValid = true;
    
    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            field.style.borderColor = '#ef4444';
            isValid = false;
        } else {
            field.style.borderColor = '#e5e7eb';
        }
    });
    
    if (!isValid) {
        showMessage('error', 'Please fill in all required fields marked with *');
        return false;
    }
    
    const tcp = parseFloat(tcpField.value);
    if (tcp <= 0 || isNaN(tcp)) {
        showMessage('error', 'Total Contract Price must be greater than 0');
        return false;
    }
    
    return true;
}

/**
 * Show message to user
 */
function showMessage(type, message) {
    messageDisplay.className = `message-display ${type}`;
    messageDisplay.innerHTML = message;
    messageDisplay.style.display = 'block';
    messageDisplay.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

/**
 * Format number as currency with Peso sign
 */
function formatCurrency(amount) {
    return '₱' + new Intl.NumberFormat('en-PH', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
    }).format(amount);
}

/**
 * Format number as percentage
 */
function formatPercent(value) {
    return parseFloat(value).toFixed(2) + '%';
}

// Initialize calculations on page load
window.addEventListener('load', () => {
    calculateAll();
});
