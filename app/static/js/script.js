// DOM Elements
const proposalForm = document.getElementById('proposalForm');
const productType = document.getElementById('product_type');
const verticalFields = document.getElementById('vertical_fields');
const horizontalFields = document.getElementById('horizontal_fields');
const projectTypeVertical = document.getElementById('project_type_vertical');
const projectTypeHorizontal = document.getElementById('project_type_horizontal');
const brandVertical = document.getElementById('brand_vertical');
const brandHorizontal = document.getElementById('brand_horizontal');
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
projectTypeVertical.addEventListener('change', handleProjectTypeVerticalChange);
projectTypeHorizontal.addEventListener('change', handleProjectTypeHorizontalChange);

// Auto-calculation event listeners
tcpField.addEventListener('input', function() {
    calculateReservationFee();
    calculateAll();
});
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
        handleProjectTypeVerticalChange();
    } else {
        verticalFields.style.display = 'none';
        horizontalFields.style.display = 'block';
        clearFieldGroup(verticalFields);
        handleProjectTypeHorizontalChange();
    }
    
    // Calculate reservation fee for horizontal projects
    calculateReservationFee();
}

/**
 * Handle vertical project type change (Mid Rise/High Rise)
 * Mid Rise Building -> Moldex Residence (read only)
 * High Rise Building -> The Grand Series (read only)
 */
function handleProjectTypeVerticalChange() {
    const selectedType = projectTypeVertical.value;
    
    if (selectedType === 'Mid Rise Building') {
        brandVertical.value = 'Moldex Residence';
        brandVertical.disabled = true;
        // Show only relevant options
        Array.from(brandVertical.options).forEach(option => {
            option.style.display = (option.value === 'Moldex Residence') ? 'block' : 'none';
        });
    } else if (selectedType === 'High Rise Building') {
        brandVertical.value = 'The Grand Series';
        brandVertical.disabled = true;
        // Show only relevant options
        Array.from(brandVertical.options).forEach(option => {
            option.style.display = (option.value === 'The Grand Series') ? 'block' : 'none';
        });
    }
}

/**
 * Handle horizontal project type change (House and Lot/Lot Only)
 * House and Lot or Lot Only -> Show only Metro Gate (default) and Heritage Homes/ Villas
 */
function handleProjectTypeHorizontalChange() {
    const selectedType = projectTypeHorizontal.value;
    
    // Show/hide fields based on project type
    if (selectedType === 'House and Lot') {
        houseAndLotFields.style.display = 'block';
        lotOnlyFields.style.display = 'none';
        clearFieldGroup(lotOnlyFields);
    } else {
        houseAndLotFields.style.display = 'none';
        lotOnlyFields.style.display = 'block';
        clearFieldGroup(houseAndLotFields);
    }
    
    // For both House and Lot and Lot Only, show only Metro Gate and Heritage Homes/ Villas
    brandHorizontal.disabled = false;
    brandHorizontal.value = 'Metro Gate'; // Set default to Metro Gate
    
    // Show only Metro Gate and Heritage options
    Array.from(brandHorizontal.options).forEach(option => {
        if (option.value === 'Metro Gate' || option.value === 'Heritage') {
            option.style.display = 'block';
        } else {
            option.style.display = 'none';
        }
    });
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
 * Calculate reservation fee for Horizontal projects based on TCP
 */
function calculateReservationFee() {
    const selectedProductType = productType.value;
    
    // Only auto-calculate for Horizontal projects
    if (selectedProductType === 'Horizontal') {
        const tcp = parseFloat(tcpField.value) || 0;
        
        if (tcp > 0) {
            let reservationFee = 0;
            
            if (tcp < 1500000) {
                reservationFee = 10000;
            } else if (tcp >= 1500000 && tcp <= 2999999) {
                reservationFee = 20000;
            } else if (tcp >= 3000000 && tcp <= 4999999) {
                reservationFee = 30000;
            } else if (tcp >= 5000000 && tcp <= 9999999) {
                reservationFee = 40000;
            } else if (tcp >= 10000000 && tcp <= 14999999) {
                reservationFee = 60000;
            } else if (tcp >= 15000000 && tcp <= 19999999) {
                reservationFee = 80000;
            } else if (tcp >= 20000000) {
                reservationFee = 100000;
            }
            
            reservationFeeField.value = reservationFee;
        }
    }
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
            // When enabled: TLP * Reg Fee %
            regFee = tlp * (regFeePercent / 100);
        } else {
            // When disabled: DTCP * Reg Fee %
            regFee = dtcp * (regFeePercent / 100);
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
        
        // Add display options checkboxes
        formData.set('show_spot_cash', document.getElementById('show_spot_cash').checked);
        formData.set('show_deferred_payment', document.getElementById('show_deferred_payment').checked);
        formData.set('show_spot_down_payment', document.getElementById('show_spot_down_payment').checked);
        formData.set('show_20_80_payment', document.getElementById('show_20_80_payment').checked);
        formData.set('show_balance_5yr', document.getElementById('show_balance_5yr').checked);
        formData.set('show_balance_7yr', document.getElementById('show_balance_7yr').checked);
        formData.set('show_balance_10yr', document.getElementById('show_balance_10yr').checked);
        
        // Handle conditional fields based on product type
        const productTypeValue = formData.get('product_type');
        
        if (productTypeValue === 'Vertical') {
            formData.set('project_type', formData.get('project_type') || '');
            formData.set('brand', formData.get('brand') || formData.get('brand_vertical') || '');
            formData.set('address', formData.get('address') || formData.get('address_vertical') || '');
            formData.set('property_details_vertical', formData.get('property_details_vertical') || '');
            formData.set('floor_area', formData.get('floor_area') || formData.get('floor_area_vertical') || '');
            
            const pictureFiles = document.getElementById('picture_vertical').files;
            if (pictureFiles.length > 0) {
                for (let i = 0; i < Math.min(pictureFiles.length, 4); i++) {
                    formData.append('pictures', pictureFiles[i]);
                }
            }
        } else {
            formData.set('project_type', formData.get('project_type_horiz') || '');
            formData.set('brand', formData.get('brand_horiz') || '');
            formData.set('address', formData.get('address_horiz') || '');
            
            if (formData.get('project_type_horiz') === 'House and Lot') {
                formData.set('lot_area', formData.get('lot_area_hl') || '');
                formData.set('floor_area', formData.get('floor_area_hl') || '');
                
                const pictureFiles = document.getElementById('picture_hl').files;
                if (pictureFiles.length > 0) {
                    for (let i = 0; i < Math.min(pictureFiles.length, 4); i++) {
                        formData.append('pictures', pictureFiles[i]);
                    }
                }
            } else {
                formData.set('lot_area', formData.get('lot_area_lot') || '');
                
                const pictureFiles = document.getElementById('picture_lot').files;
                if (pictureFiles.length > 0) {
                    for (let i = 0; i < Math.min(pictureFiles.length, 4); i++) {
                        formData.append('pictures', pictureFiles[i]);
                    }
                }
            }
        }
        
        // Send request
        const response = await fetch('/generate-proposal', {
            method: 'POST',
            body: formData
        });
        
        if (response.ok) {
            // Check if response is a PDF file
            const contentType = response.headers.get('content-type');
            if (contentType && contentType.includes('application/pdf')) {
                // Get the blob and trigger download
                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.style.display = 'none';
                a.href = url;
                
                // Get filename from Content-Disposition header or use default
                const contentDisposition = response.headers.get('content-disposition');
                let filename = 'proposal.pdf';
                if (contentDisposition) {
                    const filenameMatch = contentDisposition.match(/filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/);
                    if (filenameMatch && filenameMatch[1]) {
                        filename = filenameMatch[1].replace(/['"]/g, '');
                    }
                }
                a.download = filename;
                
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
                document.body.removeChild(a);
                
                showMessage('success', 'Proposal generated and downloaded successfully!');
            } else {
                // Try to parse as JSON for error messages
                const result = await response.json();
                showMessage('error', result.message || 'Failed to generate proposal');
            }
        } else {
            // Handle error response
            try {
                const result = await response.json();
                showMessage('error', result.message || 'Failed to generate proposal');
            } catch {
                showMessage('error', 'Failed to generate proposal. Please try again.');
            }
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
