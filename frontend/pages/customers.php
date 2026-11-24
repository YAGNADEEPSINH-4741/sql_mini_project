<?php
/**
 * CUSTOMER MANAGEMENT MODULE
 * Project: Smart Banking Management System
 */
require_once __DIR__ . '/layout_header.php';
?>

<div class="fintech-card">
    <div class="card-header">
        <h4><i class="bi bi-people-fill text-primary"></i> Customer Directory (CUSTOMERS Table)</h4>
        <div style="display: flex; gap: 12px;">
            <input type="text" id="custSearch" class="form-control" placeholder="Search customer by name, email, city..." style="width: 260px;">
            <button onclick="Modal.open('newCustomerModal')" class="btn btn-primary">
                <i class="bi bi-person-plus-fill"></i> Register New Customer
            </button>
        </div>
    </div>
    <div class="card-body" style="padding: 0;">
        <div class="table-responsive">
            <table class="fintech-table" id="customersTable">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Full Name</th>
                        <th>Contact Email</th>
                        <th>Phone Number</th>
                        <th>City / State</th>
                        <th>KYC Status</th>
                        <th>Date of Birth</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody id="customersBody">
                    <tr><td colspan="8" style="text-align: center; padding: 20px;">Loading customer records...</td></tr>
                </tbody>
            </table>
        </div>
    </div>
</div>

<!-- Register Customer Modal -->
<div class="modal-overlay" id="newCustomerModal">
    <div class="modal-container">
        <div class="modal-header">
            <h5><i class="bi bi-person-plus-fill text-primary"></i> Register New Customer</h5>
            <button class="modal-close" onclick="Modal.close('newCustomerModal')">&times;</button>
        </div>
        <form id="createCustomerForm">
            <div class="modal-body">
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 14px;">
                    <div class="form-group">
                        <label class="form-label">First Name *</label>
                        <input type="text" name="first_name" class="form-control" required placeholder="e.g. Rahul">
                    </div>
                    <div class="form-group">
                        <label class="form-label">Last Name *</label>
                        <input type="text" name="last_name" class="form-control" required placeholder="e.g. Verma">
                    </div>
                </div>

                <div class="form-group">
                    <label class="form-label">Email Address *</label>
                    <input type="email" name="email" class="form-control" required placeholder="e.g. rahul.v@example.com">
                </div>

                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 14px;">
                    <div class="form-group">
                        <label class="form-label">Phone Number *</label>
                        <input type="text" name="phone" class="form-control" required placeholder="+91-9876543210">
                    </div>
                    <div class="form-group">
                        <label class="form-label">Date of Birth *</label>
                        <input type="date" name="dob" class="form-control" required value="1996-05-15">
                    </div>
                </div>

                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 14px;">
                    <div class="form-group">
                        <label class="form-label">Gender</label>
                        <select name="gender" class="form-select">
                            <option value="Male">Male</option>
                            <option value="Female">Female</option>
                            <option value="Other">Other</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label class="form-label">City *</label>
                        <input type="text" name="city" class="form-control" required placeholder="e.g. Mumbai">
                    </div>
                </div>

                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 14px;">
                    <div class="form-group">
                        <label class="form-label">State</label>
                        <input type="text" name="state" class="form-control" value="Maharashtra">
                    </div>
                    <div class="form-group">
                        <label class="form-label">PIN Code</label>
                        <input type="text" name="pincode" class="form-control" value="400001">
                    </div>
                </div>

                <div class="form-group">
                    <label class="form-label">Residential Address</label>
                    <textarea name="address" class="form-control" rows="2" placeholder="Street, building, area..."></textarea>
                </div>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" onclick="Modal.close('newCustomerModal')">Cancel</button>
                <button type="submit" class="btn btn-primary"><i class="bi bi-check-lg"></i> Register Customer</button>
            </div>
        </form>
    </div>
</div>

<script>
async function loadCustomers() {
    const tbody = document.getElementById('customersBody');
    try {
        const customers = await fetchAPI('list_customers');
        tbody.innerHTML = '';
        customers.forEach(c => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td><strong>#${c.CUSTOMER_ID}</strong></td>
                <td><strong>${c.FIRST_NAME} ${c.LAST_NAME}</strong></td>
                <td>${c.EMAIL}</td>
                <td><code>${c.PHONE}</code></td>
                <td>${c.CITY}, ${c.STATE}</td>
                <td><span class="badge badge-success">${c.KYC_STATUS}</span></td>
                <td>${c.DATE_OF_BIRTH}</td>
                <td>
                    <a href="accounts.php?customer_id=${c.CUSTOMER_ID}" class="btn btn-outline btn-sm" title="View Accounts">
                        <i class="bi bi-wallet2"></i> Accounts
                    </a>
                </td>
            `;
            tbody.appendChild(tr);
        });
        setupTableSearch('custSearch', 'customersTable');
    } catch (err) {
        tbody.innerHTML = '<tr><td colspan="8" style="text-align: center; color: red;">Failed to load customers.</td></tr>';
    }
}

document.getElementById('createCustomerForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    const formData = new FormData(this);
    const payload = Object.fromEntries(formData.entries());

    try {
        await fetchAPI('create_customer', payload, 'POST');
        Toast.success('Customer registered successfully!');
        Modal.close('newCustomerModal');
        this.reset();
        loadCustomers();
    } catch (err) {}
});

document.addEventListener('DOMContentLoaded', loadCustomers);
</script>

<?php require_once __DIR__ . '/layout_footer.php'; ?>
