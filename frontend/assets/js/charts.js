/**
 * DASHBOARD CHARTS (Chart.js 4.x)
 * Project: Smart Banking Management System
 */

function initDashboardCharts(chartData) {
    if (!chartData) return;

    // 1. Monthly Deposits vs Withdrawals (Area / Line Chart)
    const ctxMonthly = document.getElementById('monthlyTxnChart');
    if (ctxMonthly && chartData.monthly_stats) {
        new Chart(ctxMonthly, {
            type: 'line',
            data: {
                labels: chartData.monthly_stats.labels,
                datasets: [
                    {
                        label: 'Deposits (INR)',
                        data: chartData.monthly_stats.deposits,
                        borderColor: '#2563eb',
                        backgroundColor: 'rgba(37, 99, 235, 0.08)',
                        fill: true,
                        tension: 0.35,
                        borderWidth: 2.5,
                        pointRadius: 4,
                        pointBackgroundColor: '#2563eb'
                    },
                    {
                        label: 'Withdrawals (INR)',
                        data: chartData.monthly_stats.withdrawals,
                        borderColor: '#ef4444',
                        backgroundColor: 'rgba(239, 68, 68, 0.05)',
                        fill: true,
                        tension: 0.35,
                        borderWidth: 2.5,
                        pointRadius: 4,
                        pointBackgroundColor: '#ef4444'
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'top',
                        labels: { boxWidth: 12, font: { family: 'Inter', size: 12, weight: 500 } }
                    },
                    tooltip: {
                        callbacks: {
                            label: function(c) {
                                return ` ${c.dataset.label}: ₹ ${c.parsed.y.toLocaleString('en-IN')}`;
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: { color: '#f1f5f9' },
                        ticks: {
                            callback: function(v) { return '₹ ' + (v / 1000) + 'k'; }
                        }
                    },
                    x: {
                        grid: { display: false }
                    }
                }
            }
        });
    }

    // 2. Account Types Distribution (Doughnut Chart)
    const ctxAccounts = document.getElementById('accountTypesChart');
    if (ctxAccounts && chartData.account_types) {
        const types = chartData.account_types;
        new Chart(ctxAccounts, {
            type: 'doughnut',
            data: {
                labels: Object.keys(types),
                datasets: [{
                    data: Object.values(types),
                    backgroundColor: ['#2563eb', '#10b981', '#f59e0b', '#8b5cf6'],
                    borderWidth: 2,
                    borderColor: '#ffffff'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                cutout: '70%',
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: { boxWidth: 10, font: { family: 'Inter', size: 11 } }
                    }
                }
            }
        });
    }
}
