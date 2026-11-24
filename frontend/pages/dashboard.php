<?php
/**
 * FINTECH DASHBOARD PAGE
 * Project: Smart Banking Management System
 */
require_once __DIR__ . '/layout_header.php';
?>

<!-- KPI Metric Cards Grid -->
<div class="metric-grid">
    <div class="metric-card">
        <div class="metric-details">
            <p>Total Customers</p>
            <h3 id="m-customers">--</h3>
        </div>
        <div class="metric-icon-box icon-blue">
            <i class="bi bi-people-fill"></i>
        </div>
    </div>

    <div class="metric-card">
        <div class="metric-details">
            <p>Active Accounts</p>
            <h3 id="m-accounts">--</h3>
        </div>
        <div class="metric-icon-box icon-indigo">
            <i class="bi bi-wallet2"></i>
        </div>
    </div>

    <div class="metric-card">
        <div class="metric-details">
            <p>Total Deposits</p>
            <h3 id="m-deposits">--</h3>
        </div>
        <div class="metric-icon-box icon-green">
            <i class="bi bi-arrow-down-left-circle-fill"></i>
        </div>
    </div>

    <div class="metric-card">
        <div class="metric-details">
            <p>Active Loan Volume</p>
            <h3 id="m-loans">--</h3>
        </div>
        <div class="metric-icon-box icon-amber">
            <i class="bi bi-cash-stack"></i>
        </div>
    </div>
</div>

<!-- Charts Section -->
<div style="display: grid; grid-template-columns: 2fr 1fr; gap: 24px; margin-bottom: 28px;">
    <!-- Monthly Transactions Line Chart -->
    <div class="fintech-card" style="margin-bottom: 0;">
        <div class="card-header">
            <h4><i class="bi bi-graph-up-arrow text-primary"></i> Monthly Cash Flow (Deposits vs Withdrawals)</h4>
            <span class="badge badge-info">Chart.js Visualizer</span>
        </div>
        <div class="card-body">
            <div style="height: 280px; position: relative;">
                <canvas id="monthlyTxnChart"></canvas>
            </div>
        </div>
    </div>

    <!-- Account Distribution Doughnut Chart -->
    <div class="fintech-card" style="margin-bottom: 0;">
        <div class="card-header">
            <h4><i class="bi bi-pie-chart-fill text-warning"></i> Account Portfolio</h4>
        </div>
        <div class="card-body">
            <div style="height: 280px; position: relative;">
                <canvas id="accountTypesChart"></canvas>
            </div>
        </div>
    </div>
</div>

<!-- Quick Action Shortcuts -->
<div class="fintech-card">
    <div class="card-header">
        <h4><i class="bi bi-lightning-charge-fill text-amber"></i> Quick PL/SQL Banking Procedures</h4>
    </div>
    <div class="card-body" style="display: flex; gap: 14px; flex-wrap: wrap;">
        <a href="transactions.php?action=deposit" class="btn btn-primary">
            <i class="bi bi-plus-circle-fill"></i> Quick Deposit
        </a>
        <a href="transactions.php?action=withdraw" class="btn btn-secondary">
            <i class="bi bi-dash-circle-fill"></i> Quick Withdrawal
        </a>
        <a href="transactions.php?action=transfer" class="btn btn-success">
            <i class="bi bi-arrow-left-right"></i> Atomic Transfer
        </a>
        <a href="loans.php?action=apply" class="btn btn-outline">
            <i class="bi bi-cash"></i> Apply Loan
        </a>
        <a href="accounts.php?action=new" class="btn btn-outline">
            <i class="bi bi-person-plus-fill"></i> Open Bank Account
        </a>
    </div>
</div>

<!-- Recent Transactions Table -->
<div class="fintech-card">
    <div class="card-header">
        <h4><i class="bi bi-clock-history text-info"></i> Real-time Transaction Ledger</h4>
        <a href="transactions.php" class="btn btn-outline btn-sm">View All Transactions</a>
    </div>
    <div class="card-body" style="padding: 0;">
        <div class="table-responsive">
            <table class="fintech-table" id="recentTxnsTable">
                <thead>
                    <tr>
                        <th>Reference #</th>
                        <th>Account</th>
                        <th>Holder</th>
                        <th>Type</th>
                        <th>Amount</th>
                        <th>Balance After</th>
                        <th>Timestamp</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody id="recentTxnsBody">
                    <tr><td colspan="8" style="text-align: center; padding: 20px;">Loading ledger records...</td></tr>
                </tbody>
            </table>
        </div>
    </div>
</div>

<script>
document.addEventListener('DOMContentLoaded', async function() {
    try {
        const data = await fetchAPI('dashboard_summary');
        
        // Populate KPIs
        document.getElementById('m-customers').innerText = data.metrics.total_customers;
        document.getElementById('m-accounts').innerText = data.metrics.total_accounts;
        document.getElementById('m-deposits').innerText = formatINR(data.metrics.total_deposits);
        document.getElementById('m-loans').innerText = formatINR(data.metrics.loan_amount);

        // Render Charts
        initDashboardCharts(data.charts);

        // Populate Recent Transactions Table
        const tbody = document.getElementById('recentTxnsBody');
        tbody.innerHTML = '';
        if (data.recent_transactions && data.recent_transactions.length > 0) {
            data.recent_transactions.forEach(t => {
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
                    <td><strong>${formatINR(t.AMOUNT)}</strong></td>
                    <td>${formatINR(t.BALANCE_AFTER)}</td>
                    <td style="color: #64748b; font-size: 0.8rem;">${t.TRANSACTION_DATE}</td>
                    <td><span class="badge badge-success">${t.TRANSACTION_STATUS}</span></td>
                `;
                tbody.appendChild(tr);
            });
        } else {
            tbody.innerHTML = '<tr><td colspan="8" style="text-align: center; padding: 20px;">No transactions recorded.</td></tr>';
        }
    } catch (err) {
        console.error(err);
    }
});
</script>

<?php require_once __DIR__ . '/layout_footer.php'; ?>
