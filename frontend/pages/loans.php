<?php
/**
 * LOAN MANAGEMENT MODULE
 * Invokes Oracle PL/SQL Package: LOAN_PACKAGE
 * Features: Apply for Loan, Approve / Reject, Record EMI Payment, and Interactive EMI Calculator
 */
require_once __DIR__ . '/layout_header.php';
?>

<!-- EMI Calculator Widget -->
<div class="fintech-card" style="background: linear-gradient(135deg, #f8fafc, #edf2f7);">
    <div class="card-header">
        <h4><i class="bi bi-calculator text-primary"></i> Interactive EMI Calculator (CALCULATE_MONTHLY_EMI Function)</h4>
        <span class="badge badge-info">PL/SQL Formula Engine</span>
    </div>
    <div class="card-body">
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)) 2fr; gap: 20px; align-items: center;">
            <div class="form-group" style="margin: 0;">
                <label class="form-label">Principal Amount (₹)</label>
                <input type="number" id="calcP" class="form-control" value="1000000" step="50000">
            </div>
            <div class="form-group" style="margin: 0;">
                <label class="form-label">Interest Rate (% APR)</label>
                <input type="number" id="calcR" class="form-control" value="9.5" step="0.25">
            </div>
            <div class="form-group" style="margin: 0;">
                <label class="form-label">Term (Months)</label>
                <input type="number" id="calcN" class="form-control" value="60" step="12">
            </div>
            <div style="background: white; border-radius: var(--radius-sm); padding: 14px 20px; border: 1px solid var(--border-color); display: flex; justify-content: space-around;">
                <div>
                    <div style="font-size: 0.72rem; color: #64748b; text-transform: uppercase; font-weight: 700;">Monthly EMI</div>
                    <div id="resEMI" style="font-size: 1.3rem; font-weight: 800; color: #2563eb;">₹ 21,001.90</div>
                </div>
                <div>
                    <div style="font-size: 0.72rem; color: #64748b; text-transform: uppercase; font-weight: 700;">Total Interest</div>
                    <div id="resInt" style="font-size: 1.3rem; font-weight: 800; color: #f59e0b;">₹ 2,60,114.00</div>
                </div>
                <div>
                    <div style="font-size: 0.72rem; color: #64748b; text-transform: uppercase; font-weight: 700;">Total Payable</div>
                    <div id="resTot" style="font-size: 1.3rem; font-weight: 800; color: #10b981;">₹ 12,60,114.00</div>
                </div>
            </div>
        </div>
    </div>
</div>

<!-- Loans Directory -->
<div class="fintech-card">
    <div class="card-header">
        <h4><i class="bi bi-cash-stack text-warning"></i> Loan Portfolio & Applications (LOAN_DETAILS_VIEW)</h4>
        <div style="display: flex; gap: 12px;">
            <input type="text" id="loanSearch" class="form-control" placeholder="Search loan #, borrower, type..." style="width: 260px;">
            <button onclick="openApplyLoanModal()" class="btn btn-primary">
                <i class="bi bi-file-earmark-plus-fill"></i> Apply For Loan
            </button>
        </div>
    </div>
    <div class="card-body" style="padding: 0;">
        <div class="table-responsive">
            <table class="fintech-table" id="loansTable">
                <thead>
                    <tr>
                        <th>Loan #</th>
                        <th>Borrower</th>
                        <th>Type</th>
                        <th>Sanctioned Amount</th>
                        <th>Rate / Term</th>
                        <th>Monthly EMI</th>
                        <th>Outstanding Balance</th>
                        <th>Status</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody id="loansBody">
                    <tr><td colspan="9" style="text-align: center; padding: 20px;">Loading loan portfolio...</td></tr>
                </tbody>
            </table>
        </div>
    </div>
</div>

<!-- Apply Loan Modal -->
<div class="modal-overlay" id="applyLoanModal">
    <div class="modal-container">
        <div class="modal-header">
            <h5><i class="bi bi-file-earmark-plus-fill text-primary"></i> New Loan Application (APPLY_FOR_LOAN)</h5>
            <button class="modal-close" onclick="Modal.close('applyLoanModal')">&times;</button>
        </div>
        <form id="applyLoanForm">
            <div class="modal-body">
                <div class="form-group">
                    <label class="form-label">Select Borrower Customer *</label>
                    <select id="loanCustSelect" name="customer_id" class="form-select" required></select>
                </div>
                <div class="form-group">
                    <label class="form-label">Branch *</label>
                    <select name="branch_id" class="form-select" required>
                        <option value="101">Nariman Point Corporate Branch (Mumbai)</option>
                        <option value="102">Connaught Place Premier Branch (New Delhi)</option>
                        <option value="103">Koramangala Tech Hub Branch (Bengaluru)</option>
                        <option value="104">Ashram Road Financial Branch (Ahmedabad)</option>
                    </select>
                </div>
                <div class="form-group">
                    <label class="form-label">Loan Type *</label>
                    <select name="loan_type" class="form-select" required>
                        <option value="Home Loan">Home Loan (8.50% APR)</option>
                        <option value="Auto Loan">Auto Loan (9.25% APR)</option>
                        <option value="Business Loan">Business Loan (11.50% APR)</option>
                        <option value="Personal Loan">Personal Loan (12.00% APR)</option>
                        <option value="Education Loan">Education Loan (9.00% APR)</option>
                    </select>
                </div>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 14px;">
                    <div class="form-group">
                        <label class="form-label">Loan Amount (INR) *</label>
                        <input type="number" name="loan_amount" class="form-control" required min="10000" step="5000" value="500000">
                    </div>
                    <div class="form-group">
                        <label class="form-label">Term (Months) *</label>
                        <input type="number" name="term_months" class="form-control" required min="6" max="360" value="36">
                    </div>
                </div>
                <div class="form-group">
                    <label class="form-label">Interest Rate (% APR)</label>
                    <input type="number" name="interest_rate" class="form-control" required min="1" max="25" step="0.25" value="10.5">
                </div>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" onclick="Modal.close('applyLoanModal')">Cancel</button>
                <button type="submit" class="btn btn-primary"><i class="bi bi-send-fill"></i> Submit Application</button>
            </div>
        </form>
    </div>
</div>

<!-- Pay EMI Modal -->
<div class="modal-overlay" id="payEmiModal">
    <div class="modal-container">
        <div class="modal-header">
            <h5><i class="bi bi-cash text-success"></i> Record Loan EMI Payment (PROCESS_LOAN_PAYMENT)</h5>
            <button class="modal-close" onclick="Modal.close('payEmiModal')">&times;</button>
        </div>
        <form id="payEmiForm">
            <div class="modal-body">
                <input type="hidden" id="payLoanNumber" name="loan_number">
                <div class="form-group">
                    <label class="form-label">Loan Reference</label>
                    <input type="text" id="payLoanDisplay" class="form-control" readonly>
                </div>
                <div class="form-group">
                    <label class="form-label">EMI Repayment Amount (INR) *</label>
                    <input type="number" id="payAmount" name="amount" class="form-control" required min="100" step="1">
                </div>
                <div class="form-group">
                    <label class="form-label">Payment Method</label>
                    <select name="method" class="form-select">
                        <option value="Online Transfer">Online Net Banking</option>
                        <option value="Auto Debit">Auto Debit (ECS / NACH)</option>
                        <option value="Cheque">Cheque Deposit</option>
                        <option value="Cash">Cash at Counter</option>
                    </select>
                </div>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" onclick="Modal.close('payEmiModal')">Cancel</button>
                <button type="submit" class="btn btn-success"><i class="bi bi-check-lg"></i> Post EMI Payment</button>
            </div>
        </form>
    </div>
</div>

<script>
// Live Calculator
async function updateCalculator() {
    const p = parseFloat(document.getElementById('calcP').value) || 0;
    const r = parseFloat(document.getElementById('calcR').value) || 0;
    const n = parseInt(document.getElementById('calcN').value) || 0;

    try {
        const res = await fetchAPI('calculate_emi', { principal: p, rate: r, months: n }, 'POST');
        document.getElementById('resEMI').innerText = formatINR(res.monthly_emi);
        document.getElementById('resInt').innerText = formatINR(res.total_interest);
        document.getElementById('resTot').innerText = formatINR(res.total_payable);
    } catch (err) {}
}

document.getElementById('calcP').addEventListener('input', updateCalculator);
document.getElementById('calcR').addEventListener('input', updateCalculator);
document.getElementById('calcN').addEventListener('input', updateCalculator);

async function loadLoans() {
    const tbody = document.getElementById('loansBody');
    try {
        const loans = await fetchAPI('list_loans');
        tbody.innerHTML = '';
        loans.forEach(l => {
            let badgeClass = 'badge-warning';
            if (l.LOAN_STATUS === 'Approved' || l.LOAN_STATUS === 'Disbursed') badgeClass = 'badge-success';
            if (l.LOAN_STATUS === 'Rejected') badgeClass = 'badge-danger';
            if (l.LOAN_STATUS === 'Closed') badgeClass = 'badge-neutral';

            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td><code><strong>${l.LOAN_NUMBER}</strong></code></td>
                <td><strong>${l.BORROWER_NAME}</strong></td>
                <td><span class="badge badge-info">${l.LOAN_TYPE}</span></td>
                <td>${formatINR(l.LOAN_AMOUNT)}</td>
                <td>${l.INTEREST_RATE}% / ${l.TERM_MONTHS} mos</td>
                <td><strong>${formatINR(l.MONTHLY_EMI)}</strong></td>
                <td><strong style="color: #b45309;">${formatINR(l.OUTSTANDING_BALANCE)}</strong></td>
                <td><span class="badge ${badgeClass}">${l.LOAN_STATUS}</span></td>
                <td>
                    ${l.LOAN_STATUS === 'Pending' ? `
                        <button onclick="decideLoan('${l.LOAN_NUMBER}', 'Approved')" class="btn btn-success btn-sm"><i class="bi bi-check"></i></button>
                        <button onclick="decideLoan('${l.LOAN_NUMBER}', 'Rejected')" class="btn btn-secondary btn-sm"><i class="bi bi-x"></i></button>
                    ` : ''}
                    ${l.LOAN_STATUS === 'Approved' || l.LOAN_STATUS === 'Disbursed' ? `
                        <button onclick="openPayEmiModal('${l.LOAN_NUMBER}', ${l.MONTHLY_EMI})" class="btn btn-primary btn-sm"><i class="bi bi-cash"></i> Pay EMI</button>
                    ` : ''}
                </td>
            `;
            tbody.appendChild(tr);
        });
        setupTableSearch('loanSearch', 'loansTable');
    } catch (err) {
        tbody.innerHTML = '<tr><td colspan="9" style="text-align: center; color: red;">Failed to load loans.</td></tr>';
    }
}

async function decideLoan(loanNo, decision) {
    if (!confirm(`Confirm loan decision: ${decision} for ${loanNo}?`)) return;
    try {
        await fetchAPI('decide_loan', { loan_number: loanNo, decision: decision }, 'POST');
        Toast.success(`Loan ${loanNo} marked as ${decision}.`);
        loadLoans();
    } catch (err) {}
}

function openPayEmiModal(loanNo, emi) {
    document.getElementById('payLoanNumber').value = loanNo;
    document.getElementById('payLoanDisplay').value = loanNo;
    document.getElementById('payAmount').value = emi;
    Modal.open('payEmiModal');
}

document.getElementById('payEmiForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    const payload = Object.fromEntries(new FormData(this).entries());
    try {
        const res = await fetchAPI('loan_payment', payload, 'POST');
        Toast.success('EMI payment recorded! Ref: ' + res.payment_ref);
        Modal.close('payEmiModal');
        loadLoans();
    } catch (err) {}
});

async function openApplyLoanModal() {
    try {
        const custs = await fetchAPI('list_customers');
        const sel = document.getElementById('loanCustSelect');
        sel.innerHTML = '<option value="">-- Choose Borrower --</option>';
        custs.forEach(c => {
            sel.innerHTML += `<option value="${c.CUSTOMER_ID}">${c.FIRST_NAME} ${c.LAST_NAME} (#${c.CUSTOMER_ID})</option>`;
        });
        Modal.open('applyLoanModal');
    } catch (err) {}
}

document.getElementById('applyLoanForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    const payload = Object.fromEntries(new FormData(this).entries());
    try {
        const res = await fetchAPI('apply_loan', payload, 'POST');
        Toast.success('Loan application submitted! Loan #: ' + res.loan_number);
        Modal.close('applyLoanModal');
        this.reset();
        loadLoans();
    } catch (err) {}
});

document.addEventListener('DOMContentLoaded', function() {
    loadLoans();
    updateCalculator();
});
</script>

<?php require_once __DIR__ . '/layout_footer.php'; ?>
