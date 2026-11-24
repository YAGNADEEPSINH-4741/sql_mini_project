<?php
/**
 * AUDIT TRAIL & DATABASE TRIGGERS INSPECTOR
 * Reads Oracle Table: AUDIT_LOGS
 * Demonstrates automated real-time capturing by:
 * - TRG_ACCOUNTS_AUDIT
 * - TRG_TRANSACTIONS_AUDIT
 * - TRG_AUDIT_DELETE
 */
require_once __DIR__ . '/layout_header.php';
?>

<div class="fintech-card">
    <div class="card-header">
        <h4><i class="bi bi-shield-lock-fill text-danger"></i> Automated Database Audit Logs (AUDIT_LOGS Table)</h4>
        <div style="display: flex; gap: 10px; align-items: center;">
            <span class="badge badge-success"><i class="bi bi-cpu-fill"></i> Trigger Automation Active</span>
            <button onclick="loadAuditLogs()" class="btn btn-outline btn-sm">
                <i class="bi bi-arrow-clockwise"></i> Refresh
            </button>
        </div>
    </div>
    <div class="card-body">
        <p style="color: #64748b; font-size: 0.85rem; margin-bottom: 20px;">
            This audit ledger is maintained entirely at the database engine level through <strong>Oracle Row-Level & Statement-Level Triggers</strong>.
            Any balance update, new financial transaction, or record deletion writes an immutable log row with pre/post-change states and client network identity.
        </p>

        <div class="table-responsive">
            <table class="fintech-table" id="auditTable">
                <thead>
                    <tr>
                        <th>Log ID</th>
                        <th>Target Table</th>
                        <th>Operation</th>
                        <th>Record ID</th>
                        <th>Old State / Value</th>
                        <th>New State / Value</th>
                        <th>Triggered By</th>
                        <th>Timestamp</th>
                    </tr>
                </thead>
                <tbody id="auditBody">
                    <tr><td colspan="8" style="text-align: center; padding: 20px;">Loading trigger audit trail...</td></tr>
                </tbody>
            </table>
        </div>
    </div>
</div>

<script>
async function loadAuditLogs() {
    const tbody = document.getElementById('auditBody');
    try {
        const logs = await fetchAPI('list_audit_logs');
        tbody.innerHTML = '';
        if (!logs.length) {
            tbody.innerHTML = '<tr><td colspan="8" style="text-align: center; padding: 20px;">No audit events recorded yet.</td></tr>';
            return;
        }

        logs.forEach(log => {
            let opBadge = 'badge-info';
            if (log.OPERATION_TYPE === 'INSERT') opBadge = 'badge-success';
            if (log.OPERATION_TYPE === 'UPDATE') opBadge = 'badge-warning';
            if (log.OPERATION_TYPE === 'DELETE') opBadge = 'badge-danger';

            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td><strong>#${log.LOG_ID}</strong></td>
                <td><code>${log.TABLE_NAME}</code></td>
                <td><span class="badge ${opBadge}">${log.OPERATION_TYPE}</span></td>
                <td><code>${log.RECORD_ID}</code></td>
                <td style="max-width: 200px; word-break: break-all; color: #ef4444; font-size: 0.8rem;">${log.OLD_VALUE || '-'}</td>
                <td style="max-width: 250px; word-break: break-all; color: #059669; font-size: 0.8rem;">${log.NEW_VALUE || '-'}</td>
                <td><span class="badge badge-neutral">${log.CHANGED_BY}</span></td>
                <td style="color: #64748b; font-size: 0.8rem;">${log.CHANGED_AT}</td>
            `;
            tbody.appendChild(tr);
        });
    } catch (err) {
        tbody.innerHTML = '<tr><td colspan="8" style="text-align: center; color: red;">Failed to load audit logs.</td></tr>';
    }
}

document.addEventListener('DOMContentLoaded', loadAuditLogs);
</script>

<?php require_once __DIR__ . '/layout_footer.php'; ?>
