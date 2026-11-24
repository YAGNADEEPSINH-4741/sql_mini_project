<?php
/**
 * BENEFICIARY MANAGEMENT MODULE
 * Invokes Oracle Stored Procedure: CREATE_BENEFICIARY
 */
require_once __DIR__ . '/layout_header.php';
?>

<div class="fintech-card">
    <div class="card-header">
        <h4><i class="bi bi-person-check-fill text-primary"></i> Registered Beneficiaries (BENEFICIARIES Table)</h4>
        <button onclick="openAddBeneficiaryModal()" class="btn btn-primary">
            <i class="bi bi-person-plus-fill"></i> Add Beneficiary (CREATE_BENEFICIARY)
        </button>
    </div>
    <div class="card-body" style="padding: 0;">
        <div class="table-responsive">
            <table class="fintech-table" id="beneficiariesTable">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Owner Customer</th>
                        <th>Beneficiary Name</th>
                        <th>Beneficiary Account</th>
                        <th>Bank Name</th>
                        <th>IFSC Code</th>
                        <th>Per-Txn Limit</th>
                        <th>Status</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody id="beneficiariesBody">
                    <tr><td colspan="9" style="text-align: center; padding: 20px;">Loading beneficiaries...</td></tr>
                </tbody>
            </table>
        </div>
    </div>
</div>

<!-- Modal: Add Beneficiary -->
<div class="modal-overlay" id="addBenefModal">
    <div class="modal-container">
        <div class="modal-header">
            <h5><i class="bi bi-person-check-fill text-primary"></i> Add Beneficiary (PL/SQL Procedure)</h5>
            <button class="modal-close" onclick="Modal.close('addBenefModal')">&times;</button>
        </div>
        <form id="addBenefForm">
            <div class="modal-body">
                <div class="form-group">
                    <label class="form-label">Customer Owner *</label>
                    <select id="benefCustSelect" name="customer_id" class="form-select" required></select>
                </div>
                <div class="form-group">
                    <label class="form-label">Beneficiary Full Name *</label>
                    <input type="text" name="name" class="form-control" required placeholder="e.g. Priya Sharma">
                </div>
                <div class="form-group">
                    <label class="form-label">Beneficiary Account Number *</label>
                    <input type="text" name="account_number" class="form-control" required placeholder="e.g. SB1002002003">
                </div>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 14px;">
                    <div class="form-group">
                        <label class="form-label">Bank Name *</label>
                        <input type="text" name="bank_name" class="form-control" value="Smart Bank" required>
                    </div>
                    <div class="form-group">
                        <label class="form-label">IFSC Code *</label>
                        <input type="text" name="ifsc" class="form-control" value="SMBL0001001" required>
                    </div>
                </div>
                <div class="form-group">
                    <label class="form-label">Daily Transfer Limit (INR)</label>
                    <input type="number" name="limit" class="form-control" value="50000" min="1000" step="5000">
                </div>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" onclick="Modal.close('addBenefModal')">Cancel</button>
                <button type="submit" class="btn btn-primary"><i class="bi bi-check-lg"></i> Register Beneficiary</button>
            </div>
        </form>
    </div>
</div>

<script>
async function loadBeneficiaries() {
    const tbody = document.getElementById('beneficiariesBody');
    try {
        const bens = await fetchAPI('list_beneficiaries');
        tbody.innerHTML = '';
        bens.forEach(b => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td><strong>#${b.BENEFICIARY_ID}</strong></td>
                <td>Customer #${b.CUSTOMER_ID}</td>
                <td><strong>${b.BENEFICIARY_NAME}</strong></td>
                <td><code>${b.BENEFICIARY_ACCOUNT}</code></td>
                <td>${b.BANK_NAME}</td>
                <td><code>${b.IFSC_CODE}</code></td>
                <td>${formatINR(b.TRANSFER_LIMIT)}</td>
                <td><span class="badge badge-success">${b.STATUS}</span></td>
                <td>
                    <a href="transactions.php?action=transfer&target=${b.BENEFICIARY_ACCOUNT}" class="btn btn-success btn-sm">
                        <i class="bi bi-send-fill"></i> Pay
                    </a>
                </td>
            `;
            tbody.appendChild(tr);
        });
    } catch (err) {
        tbody.innerHTML = '<tr><td colspan="9" style="text-align: center; color: red;">Failed to load beneficiaries.</td></tr>';
    }
}

async function openAddBeneficiaryModal() {
    try {
        const custs = await fetchAPI('list_customers');
        const sel = document.getElementById('benefCustSelect');
        sel.innerHTML = '';
        custs.forEach(c => {
            sel.innerHTML += `<option value="${c.CUSTOMER_ID}">${c.FIRST_NAME} ${c.LAST_NAME} (#${c.CUSTOMER_ID})</option>`;
        });
        Modal.open('addBenefModal');
    } catch (err) {}
}

document.getElementById('addBenefForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    const payload = Object.fromEntries(new FormData(this).entries());
    try {
        await fetchAPI('create_beneficiary', payload, 'POST');
        Toast.success('Beneficiary registered successfully!');
        Modal.close('addBenefModal');
        this.reset();
        loadBeneficiaries();
    } catch (err) {}
});

document.addEventListener('DOMContentLoaded', loadBeneficiaries);
</script>

<?php require_once __DIR__ . '/layout_footer.php'; ?>
