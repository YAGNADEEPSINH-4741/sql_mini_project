<?php
/**
 * TRANSACTION MANAGEMENT MODULE
 * Invokes Oracle PL/SQL Stored Procedures:
 * - DEPOSIT_MONEY
 * - WITHDRAW_MONEY
 * - TRANSFER_MONEY (Atomic Two-Phase Transfer)
 */
require_once __DIR__ . '/layout_header.php';
?>

<div class="fintech-card">
    <div class="card-header">
        <h4><i class="bi bi-arrow-left-right text-accent"></i> Transaction Ledger & Operations</h4>
        <div style="display: flex; gap: 10px;">
            <button onclick="Modal.open('depositModal')" class="btn btn-primary btn-sm">
                <i class="bi bi-plus-circle"></i> Deposit
            </button>
            <button onclick="Modal.open('withdrawModal')" class="btn btn-secondary btn-sm">
                <i class="bi bi-dash-circle"></i> Withdraw
            </button>
            <button onclick="Modal.open('transferModal')" class="btn btn-success btn-sm">
                <i class="bi bi-arrow-left-right"></i> Atomic Fund Transfer
            </button>
        </div>
    </div>
    <div class="card-body">
        <div style="display: flex; gap: 14px; margin-bottom: 20px; align-items: center;">
            <input type="text" id="txnSearch" class="form-control" placeholder="Search reference, account, holder, description..." style="max-width: 380px;">
            <div style="font-size: 0.82rem; color: #64748b;">
                <i class="bi bi-info-circle-fill"></i> Real-time automated auditing via <code>TRG_TRANSACTIONS_AUDIT</code>
            </div>
        </div>

        <div class="table-responsive">
            <table class="fintech-table" id="transactionsTable">
                <thead>
                    <tr>
                        <th>Reference #</th>
                        <th>Account Number</th>
                        <th>Account Holder</th>
                        <th>Type</th>
                        <th>Amount (INR)</th>
                        <th>Balance After</th>
                        <th>Counterparty Account</th>
                        <th>Date & Time</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody id="transactionsBody">
                    <tr><td colspan="9" style="text-align: center; padding: 20px;">Loading transactions...</td></tr>
                </tbody>
            </table>
        </div>
    </div>
</div>

<!-- Modal: Deposit -->
<div class="modal-overlay" id="depositModal">
    <div class="modal-container">
        <div class="modal-header">
            <h5><i class="bi bi-plus-circle-fill text-primary"></i> Process Deposit (DEPOSIT_MONEY)</h5>
            <button class="modal-close" onclick="Modal.close('depositModal')">&times;</button>
        </div>
        <form id="depositForm">
            <div class="modal-body">
                <div class="form-group">
                    <label class="form-label">Target Account Number *</label>
                    <input type="text" name="account_number" class="form-control" required placeholder="e.g. SB1001002001">
                </div>
                <div class="form-group">
                    <label class="form-label">Deposit Amount (INR) *</label>
                    <input type="number" name="amount" class="form-control" required min="1" step="0.01" placeholder="e.g. 10000">
                </div>
                <div class="form-group">
                    <label class="form-label">Description / Remarks</label>
                    <input type="text" name="description" class="form-control" placeholder="Branch Cash Deposit / Online Remittance">
                </div>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" onclick="Modal.close('depositModal')">Cancel</button>
                <button type="submit" class="btn btn-primary"><i class="bi bi-check-lg"></i> Execute Deposit</button>
            </div>
        </form>
    </div>
</div>

<!-- Modal: Withdraw -->
<div class="modal-overlay" id="withdrawModal">
    <div class="modal-container">
        <div class="modal-header">
            <h5><i class="bi bi-dash-circle-fill text-danger"></i> Process Withdrawal (WITHDRAW_MONEY)</h5>
            <button class="modal-close" onclick="Modal.close('withdrawModal')">&times;</button>
        </div>
        <form id="withdrawForm">
            <div class="modal-body">
                <div class="form-group">
                    <label class="form-label">Source Account Number *</label>
                    <input type="text" name="account_number" class="form-control" required placeholder="e.g. SB1001002001">
                </div>
                <div class="form-group">
                    <label class="form-label">Withdrawal Amount (INR) *</label>
                    <input type="number" name="amount" class="form-control" required min="1" step="0.01" placeholder="e.g. 2500">
                </div>
                <div class="form-group">
                    <label class="form-label">Description / Remarks</label>
                    <input type="text" name="description" class="form-control" placeholder="ATM / Counter Cash Withdrawal">
                </div>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" onclick="Modal.close('withdrawModal')">Cancel</button>
                <button type="submit" class="btn btn-primary" style="background-color: var(--danger);"><i class="bi bi-check-lg"></i> Execute Withdrawal</button>
            </div>
        </form>
    </div>
</div>

<!-- Modal: Atomic Fund Transfer -->
<div class="modal-overlay" id="transferModal">
    <div class="modal-container">
        <div class="modal-header">
            <h5><i class="bi bi-arrow-left-right text-success"></i> Atomic Fund Transfer (TRANSFER_MONEY)</h5>
            <button class="modal-close" onclick="Modal.close('transferModal')">&times;</button>
        </div>
        <form id="transferForm">
            <div class="modal-body">
                <div class="form-group">
                    <label class="form-label">Sender Account Number *</label>
                    <input type="text" name="sender_account" class="form-control" required placeholder="e.g. SB1001002001">
                </div>
                <div class="form-group">
                    <label class="form-label">Beneficiary Account Number *</label>
                    <input type="text" name="receiver_account" class="form-control" required placeholder="e.g. SB1002002003">
                </div>
                <div class="form-group">
                    <label class="form-label">Transfer Amount (INR) *</label>
                    <input type="number" name="amount" class="form-control" required min="1" step="0.01" placeholder="e.g. 5000">
                </div>
                <div class="form-group">
                    <label class="form-label">Transfer Purpose / Remarks</label>
                    <input type="text" name="description" class="form-control" placeholder="Vendor Settlement / Personal Remittance">
                </div>
                <div style="background-color: #f0fdf4; border: 1px solid #bbf7d0; border-radius: var(--radius-sm); padding: 10px; font-size: 0.75rem; color: #166534;">
                    <i class="bi bi-lock-fill"></i> <strong>ACID Guarantee:</strong> Executes in an isolated Oracle transaction with row-level locks, dual-ledger entries, and full automatic ROLLBACK if either account fails.
                </div>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" onclick="Modal.close('transferModal')">Cancel</button>
                <button type="submit" class="btn btn-success"><i class="bi bi-send-fill"></i> Execute Transfer</button>
            </div>
        </form>
    </div>
</div>

<script>
async function loadTransactions() {
    const tbody = document.getElementById('transactionsBody');
    try {
        const txns = await fetchAPI('list_transactions');
        tbody.innerHTML = '';
        txns.forEach(t => {
            let badgeClass = 'badge-success';
            if (t.TRANSACTION_TYPE === 'Withdrawal' || t.TRANSACTION_TYPE === 'Transfer_Debit') {
                badgeClass = 'badge-danger';
            }
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td><strong>${t.TRANSACTION_REF}</strong></td>
                <td><code>${t.ACCOUNT_NUMBER}</code></td>
                <td>${t.ACCOUNT_HOLDER}</td>
                <td><span class="badge ${badgeClass}">${t.TRANSACTION_TYPE}</span></td>
                <td><strong style="font-size: 0.95rem;">${formatINR(t.AMOUNT)}</strong></td>
                <td>${formatINR(t.BALANCE_AFTER)}</td>
                <td>${t.RELATED_ACCOUNT_NUMBER ? `<code>${t.RELATED_ACCOUNT_NUMBER}</code> (${t.RELATED_ACCOUNT_HOLDER})` : '-'}</td>
                <td style="color: #64748b; font-size: 0.8rem;">${t.TRANSACTION_DATE}</td>
                <td><span class="badge badge-success">${t.TRANSACTION_STATUS}</span></td>
            `;
            tbody.appendChild(tr);
        });
        setupTableSearch('txnSearch', 'transactionsTable');
    } catch (err) {
        tbody.innerHTML = '<tr><td colspan="9" style="text-align: center; color: red;">Failed to load transactions.</td></tr>';
    }
}

// Deposit Submit
document.getElementById('depositForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    const payload = Object.fromEntries(new FormData(this).entries());
    try {
        await fetchAPI('deposit', payload, 'POST');
        Toast.success('Deposit completed successfully!');
        Modal.close('depositModal');
        this.reset();
        loadTransactions();
    } catch (err) {}
});

// Withdraw Submit
document.getElementById('withdrawForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    const payload = Object.fromEntries(new FormData(this).entries());
    try {
        await fetchAPI('withdraw', payload, 'POST');
        Toast.success('Withdrawal processed successfully!');
        Modal.close('withdrawModal');
        this.reset();
        loadTransactions();
    } catch (err) {}
});

// Transfer Submit
document.getElementById('transferForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    const payload = Object.fromEntries(new FormData(this).entries());
    try {
        await fetchAPI('transfer', payload, 'POST');
        Toast.success('Atomic Fund Transfer completed successfully!');
        Modal.close('transferModal');
        this.reset();
        loadTransactions();
    } catch (err) {}
});

document.addEventListener('DOMContentLoaded', function() {
    loadTransactions();
    // Auto open modal if URL action set
    const urlParams = new URLSearchParams(window.location.search);
    const act = urlParams.get('action');
    if (act === 'deposit') Modal.open('depositModal');
    if (act === 'withdraw') Modal.open('withdrawModal');
    if (act === 'transfer') Modal.open('transferModal');
});
</script>

<?php require_once __DIR__ . '/layout_footer.php'; ?>
