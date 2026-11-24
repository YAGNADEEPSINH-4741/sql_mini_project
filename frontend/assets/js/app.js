/**
 * FRONTEND JAVASCRIPT APPLICATION ENGINE
 * Project: Smart Banking Management System
 */

const getApiUrl = () => {
    const loc = window.location.pathname;
    if (loc.includes('/frontend/pages/')) {
        return window.location.origin + loc.substring(0, loc.indexOf('/frontend/pages/')) + '/backend/api.php';
    } else if (loc.includes('/pages/')) {
        return window.location.origin + loc.substring(0, loc.indexOf('/pages/')) + '/backend/api.php';
    }
    return '../backend/api.php';
};
const API_URL = getApiUrl();

// Toast Notification Utility
const Toast = {
    show(message, type = 'success') {
        let container = document.getElementById('toast-container');
        if (!container) {
            container = document.createElement('div');
            container.id = 'toast-container';
            document.body.appendChild(container);
        }

        const toast = document.createElement('div');
        toast.className = `fintech-toast ${type}`;
        
        let icon = 'bi-check-circle-fill text-success';
        if (type === 'error') icon = 'bi-x-circle-fill text-danger';
        if (type === 'info') icon = 'bi-info-circle-fill text-info';

        toast.innerHTML = `<i class="bi ${icon}"></i> <span>${message}</span>`;
        container.appendChild(toast);

        setTimeout(() => {
            toast.style.opacity = '0';
            toast.style.transform = 'translateY(10px)';
            toast.style.transition = 'all 0.3s ease';
            setTimeout(() => toast.remove(), 300);
        }, 4000);
    },
    success(msg) { this.show(msg, 'success'); },
    error(msg) { this.show(msg, 'error'); },
    info(msg) { this.show(msg, 'info'); }
};

// Modal Utility
const Modal = {
    open(id) {
        const modal = document.getElementById(id);
        if (modal) {
            modal.classList.add('active');
            document.body.style.overflow = 'hidden';
        }
    },
    close(id) {
        const modal = document.getElementById(id);
        if (modal) {
            modal.classList.remove('active');
            document.body.style.overflow = '';
        }
    }
};

// API Client Wrapper
async function fetchAPI(action, data = null, method = 'GET') {
    let url = `${API_URL}?action=${action}`;
    const options = {
        method: method,
        headers: {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest'
        }
    };

    if (data && (method === 'POST' || method === 'PUT')) {
        options.body = JSON.stringify(data);
    }

    try {
        const res = await fetch(url, options);
        const result = await res.json();
        if (!result.success) {
            throw new Error(result.error || 'Server error occurred.');
        }
        return result.data;
    } catch (err) {
        Toast.error(err.message);
        throw err;
    }
}

// Global Search Filter on Data Tables
function setupTableSearch(inputId, tableId) {
    const input = document.getElementById(inputId);
    const table = document.getElementById(tableId);
    if (!input || !table) return;

    input.addEventListener('keyup', function() {
        const term = this.value.toLowerCase();
        const rows = table.querySelectorAll('tbody tr');
        rows.forEach(row => {
            const text = row.innerText.toLowerCase();
            row.style.display = text.includes(term) ? '' : 'none';
        });
    });
}

// Format Currency Utility
function formatINR(amount) {
    return '₹ ' + parseFloat(amount).toLocaleString('en-IN', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
    });
}
