<?php
/**
 * BANK ACCOUNT MANAGEMENT MODULE
 * Invokes Oracle Stored Procedure: CREATE_BANK_ACCOUNT
 * Reads Relational View: CUSTOMER_ACCOUNT_VIEW
 */
require_once __DIR__ . '/layout_header.php';
?>

<div class="fintech-card">
    <div class="card-header">
        <h4><i class="bi bi-wallet2 text-indigo"></i> Bank Accounts Management (CUSTOMER_ACCOUNT_VIEW)</h4>
        <div style="display: flex; gap: 12px;">
            <input type="text" id="accSearch" class="form-control" placeholder="Search by account #, customer, branch..." style="width: 280px;">
            <button onclick="openCreateAccountModal()" class="btn btn-primary">
                <i class="bi bi-plus-circle-fill"></i> Open Bank Account (PL/SQL)
            </button>
        </div>
    </div>
    <div class="card-body" style="padding: 0;">
        <div class="table-responsive">
            <table class="fintech-table" id="accountsTable">
                <thead>
                    <tr>
                        <th>Account Number</th>
                        <th>Account Holder</th>
                        <th>Type</th>
                        <th>Current Balance</th>
                        <th>Branch</th>
                        <th>IFSC Code</th>
                        <th>Status</th>
                        <th>Opened Date</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody id="accountsBody">
                    <tr><td colspan="9" style="text-align: center; padding: 20px;">Loading bank accounts...</td></tr>
                </tbody>
            </table>
        </div>
    </div>
</div>

<!-- Create Account Modal -->
<div class="modal-overlay" id="newAccountModal">
    <div class="modal-container">
        <div class="modal-header">
            <h5><i class="bi bi-wallet2 text-primary"></i> Open Account via PL/SQL Procedure</h5>
            <button class="modal-close" onclick="Modal.close('newAccountModal')">&times;</button>
        </div>
        <form id="createAccountForm">
            <div class="modal-body">
                <div class="form-group">
                    <label class="form-label">Select Customer *</label>
                    <select id="custSelect" name="customer_id" class="form-select" required>
                        <option value="">-- Choose Customer --</option>
                    </select>
                </div>

                <div class="form-group">
                    <label class="form-label">Home Branch *</label>
                    <select id="branchSelect" name="branch_id" class="form-select" required>
                        <option value="101">Nariman Point Corporate Branch (Mumbai)</option>
                        <option value="102">Connaught Place Premier Branch (New Delhi)</option>
                        <option value="103">Koramangala Tech Hub Branch (Bengaluru)</option>
                        <option value="104">Ashram Road Financial Branch (Ahmedabad)</option>
                        <option value="105">Banjara Hills Elite Branch (Hyderabad)</option>
                    </select>
                </div>

                <div class="form-group">
                    <label class="form-label">Account Type *</label>
                    <select id="typeSelect" name="type_id" class="form-select" required>
                        <option value="1">Standard Savings Account (Min Bal: ₹ 1,000)</option>
                        <option value="2">Premium Privilege Savings (Min Bal: ₹ 10,000)</option>
                        <option value="3">Current Business Account (Min Bal: ₹ 5,000, Overdraft: Y)</option>
                        <option value="4">Fixed Deposit Account (Min Bal: ₹ 5,000, 7.10% APR)</option>
                        <option value="5">Corporate Salary Account (Zero Balance)</option>
                    </select>
                </div>

                <div class="form-group">
                    <label class="form-label">Initial Deposit Amount (INR) *</label>
                    <input type="number" name="initial_deposit" class="form-control" min="0" step="100" value="5000" required>
                    <small style="color: #64748b; font-size: 0.75rem;">
                        <i class="bi bi-shield-check"></i> Enforced by Trigger <code>TRG_VALIDATE_ACCOUNT_MIN_BAL</code>
                    </small>
                </div>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" onclick="Modal.close('newAccountModal')">Cancel</button>
                <button type="submit" class="btn btn-primary"><i class="bi bi-check-circle-fill"></i> Execute CREATE_BANK_ACCOUNT</button>
            </div>
        </form>
    </div>
</div>

<script>
async function loadAccounts() {
    const tbody = document.getElementById('accountsBody');
    try {
        const accounts = await fetchAPI('list_accounts');
        tbody.innerHTML = '';
        accounts.forEach(a => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td><code><strong>${a.ACCOUNT_NUMBER}</strong></code></td>
                <td><strong>${a.CUSTOMER_NAME}</strong></td>
                <td><span class="badge badge-info">${a.ACCOUNT_TYPE}</span></td>
                <td><strong style="color: #059669; font-size: 0.95rem;">${formatINR(a.BALANCE)}</strong></td>
                <td>${a.BRANCH_NAME}</td>
                <td><code>${a.IFSC_CODE}</code></td>
                <td><span class="badge badge-success">${a.ACCOUNT_STATUS}</span></td>
                <td>${a.OPENED_DATE}</td>
                <td>
                    <a href="transactions.php?account_id=${a.ACCOUNT_ID}" class="btn btn-outline btn-sm" title="View Statement">
                        <i class="bi bi-receipt"></i> Statement
                    </a>
                </td>
            `;
            tbody.appendChild(tr);
        });
        setupTableSearch('accSearch', 'accountsTable');
    } catch (err) {
        tbody.innerHTML = '<tr><td colspan="9" style="text-align: center; color: red;">Failed to load accounts.</td></tr>';
    }
}

async function openCreateAccountModal() {
    try {
        const custs = await fetchAPI('list_customers');
        const sel = document.getElementById('custSelect');
        sel.innerHTML = '<option value="">-- Choose Customer --</option>';
        custs.forEach(c => {
            sel.innerHTML += `<option value="${c.CUSTOMER_ID}">${c.FIRST_NAME} ${c.LAST_NAME} (#${c.CUSTOMER_ID} - ${c.CITY})</option>`;
        });
        Modal.open('newAccountModal');
    } catch (err) {}
}

document.getElementById('createAccountForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    const formData = new FormData(this);
    const payload = Object.fromEntries(formData.entries());

    try {
        const res = await fetchAPI('create_account', payload, 'POST');
        Toast.success('Account created successfully: ' + (res.account_number || ''));
        Modal.close('newAccountModal');
        this.reset();
        loadAccounts();
    } catch (err) {}
});

document.addEventListener('DOMContentLoaded', loadAccounts);
</script>

<?php require_once __DIR__ . '/layout_footer.php'; ?>
