<?php
/**
 * SHARED LAYOUT HEADER & SIDEBAR NAVIGATION
 * Project: Smart Banking Management System
 */
require_once __DIR__ . '/../../backend/includes/auth.php';
Auth::requireAuth();
$currentUser = Auth::user();
$activePage = basename($_SERVER['PHP_SELF'], '.php');
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title><?= ucfirst($activePage) ?> - Smart Banking Management System</title>
    <!-- Fonts & Icons -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">
    <link rel="stylesheet" href="../assets/css/style.css">
    <!-- Chart.js -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body>

<div class="app-wrapper">
    <!-- Sidebar -->
    <aside class="sidebar">
        <div class="sidebar-brand">
            <div class="brand-icon">
                <i class="bi bi-bank2"></i>
            </div>
            <span>SmartBank</span>
        </div>

        <ul class="sidebar-menu">
            <li class="menu-category">Overview</li>
            <li>
                <a href="dashboard.php" class="nav-link <?= $activePage === 'dashboard' ? 'active' : '' ?>">
                    <i class="bi bi-grid-1x2-fill"></i>
                    <span>Dashboard</span>
                </a>
            </li>

            <li class="menu-category">Banking Core</li>
            <li>
                <a href="customers.php" class="nav-link <?= $activePage === 'customers' ? 'active' : '' ?>">
                    <i class="bi bi-people-fill"></i>
                    <span>Customers</span>
                </a>
            </li>
            <li>
                <a href="accounts.php" class="nav-link <?= $activePage === 'accounts' ? 'active' : '' ?>">
                    <i class="bi bi-wallet2"></i>
                    <span>Bank Accounts</span>
                </a>
            </li>
            <li>
                <a href="transactions.php" class="nav-link <?= $activePage === 'transactions' ? 'active' : '' ?>">
                    <i class="bi bi-arrow-left-right"></i>
                    <span>Transactions</span>
                </a>
            </li>
            <li>
                <a href="beneficiaries.php" class="nav-link <?= $activePage === 'beneficiaries' ? 'active' : '' ?>">
                    <i class="bi bi-person-check-fill"></i>
                    <span>Beneficiaries</span>
                </a>
            </li>

            <li class="menu-category">Credit & Loans</li>
            <li>
                <a href="loans.php" class="nav-link <?= $activePage === 'loans' ? 'active' : '' ?>">
                    <i class="bi bi-cash-coin"></i>
                    <span>Loan Management</span>
                </a>
            </li>

            <li class="menu-category">Analytics & Security</li>
            <li>
                <a href="reports.php" class="nav-link <?= $activePage === 'reports' ? 'active' : '' ?>">
                    <i class="bi bi-file-earmark-bar-graph-fill"></i>
                    <span>Reports & Export</span>
                </a>
            </li>
            <li>
                <a href="audit_logs.php" class="nav-link <?= $activePage === 'audit_logs' ? 'active' : '' ?>">
                    <i class="bi bi-shield-check"></i>
                    <span>Audit Trail (Triggers)</span>
                </a>
            </li>
        </ul>

        <div class="sidebar-footer">
            <div class="user-snippet">
                <div class="avatar">
                    <?= strtoupper(substr($currentUser['name'] ?? 'A', 0, 1)) ?>
                </div>
                <div class="user-info">
                    <span class="user-name"><?= htmlspecialchars($currentUser['name'] ?? 'Admin') ?></span>
                    <span class="user-role"><?= htmlspecialchars($currentUser['role'] ?? 'Manager') ?></span>
                </div>
            </div>
            <a href="logout.php" title="Sign Out" style="color: #ef4444; font-size: 1.15rem;">
                <i class="bi bi-box-arrow-right"></i>
            </a>
        </div>
    </aside>

    <!-- Main Content Container -->
    <div class="main-wrapper">
        <!-- Topbar -->
        <header class="topbar">
            <h1 class="page-title"><?= ucfirst(str_replace('_', ' ', $activePage)) ?></h1>
            <div class="topbar-actions">
                <button type="button" class="btn btn-sm btn-outline-primary rounded-pill px-3 py-1" data-bs-toggle="modal" data-bs-target="#projectTeamModal" style="font-size: 0.82rem; font-weight: 500;">
                    <i class="bi bi-people-fill me-1"></i> Project Team
                </button>
                <div class="db-pill">
                    <span class="db-indicator"></span>
                    <span>Oracle 10g / PL/SQL Active</span>
                </div>
                <div style="font-size: 0.85rem; color: #64748b;">
                    <i class="bi bi-calendar3"></i> <?= date('d M Y') ?>
                </div>
            </div>
        </header>

        <!-- Dynamic Content Body -->
        <main class="content-area">
