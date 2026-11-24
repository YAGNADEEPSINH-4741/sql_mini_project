<?php
/**
 * AUTHENTICATION LOGIN PAGE
 * Project: Smart Banking Management System
 */
require_once __DIR__ . '/../../backend/includes/auth.php';

if (Auth::check()) {
    header("Location: dashboard.php");
    exit;
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Smart Banking Management System - Admin Login</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">
    <link rel="stylesheet" href="../assets/css/style.css">
    <style>
        .login-wrapper {
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            background: radial-gradient(circle at 10% 20%, rgb(15, 23, 42) 0%, rgb(11, 19, 41) 90%);
            padding: 20px;
        }
        .login-box {
            width: 100%;
            max-width: 440px;
            background: #ffffff;
            border-radius: var(--radius-lg);
            padding: 40px;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.45);
        }
        .login-brand {
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 24px;
        }
        .login-brand h2 {
            font-size: 1.35rem;
            font-weight: 800;
            color: var(--secondary);
            margin: 0;
        }
        .badge-academic {
            background: #eff6ff;
            color: #2563eb;
            font-size: 0.72rem;
            font-weight: 700;
            padding: 4px 10px;
            border-radius: 20px;
            border: 1px solid #bfdbfe;
            margin-bottom: 20px;
            display: inline-block;
        }
        .demo-credentials-box {
            background-color: #f8fafc;
            border: 1px dashed #cbd5e1;
            border-radius: var(--radius-sm);
            padding: 14px;
            margin-top: 24px;
            font-size: 0.8rem;
            color: #475569;
        }
    </style>
</head>
<body>

<div class="login-wrapper">
    <div class="login-box">
        <div class="login-brand">
            <div class="brand-icon">
                <i class="bi bi-bank2"></i>
            </div>
            <div>
                <h2>SMART BANK</h2>
                <small style="color: #64748b; font-size: 0.75rem;">Oracle SQL & PL/SQL Management</small>
            </div>
        </div>

        <span class="badge-academic">
            <i class="bi bi-mortarboard-fill"></i> College RDBMS Mini Project
        </span>

        <form id="loginForm">
            <div class="form-group">
                <label class="form-label"><i class="bi bi-person-fill"></i> Username</label>
                <input type="text" id="username" class="form-control" placeholder="Enter username (e.g. admin)" required value="admin">
            </div>

            <div class="form-group">
                <label class="form-label"><i class="bi bi-lock-fill"></i> Password</label>
                <input type="password" id="password" class="form-control" placeholder="Enter password (e.g. admin123)" required value="admin123">
            </div>

            <button type="submit" id="loginBtn" class="btn btn-primary" style="width: 100%; padding: 12px; margin-top: 8px;">
                <i class="bi bi-box-arrow-in-right"></i> Sign In to Dashboard
            </button>
        </form>

        <div class="demo-credentials-box">
            <div style="font-weight: 600; margin-bottom: 6px; color: #0f172a;">
                <i class="bi bi-key-fill text-warning"></i> Demo Administrator Credentials:
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 3px;">
                <span>Username: <strong>admin</strong></span>
                <span>Password: <strong>admin123</strong></span>
            </div>
            <div style="font-size: 0.72rem; color: #64748b; margin-top: 6px;">
                Backed by Oracle Database tables <code>ADMIN_USERS</code> with BCrypt hash security.
            </div>
        </div>
    </div>
</div>

<script src="../assets/js/app.js"></script>
<script>
document.getElementById('loginForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    const btn = document.getElementById('loginBtn');
    btn.disabled = true;
    btn.innerHTML = '<span class="spinner-border spinner-border-sm"></span> Signing in...';

    const user = document.getElementById('username').value;
    const pass = document.getElementById('password').value;

    try {
        await fetchAPI('login', { username: user, password: pass }, 'POST');
        Toast.success('Authentication verified! Loading dashboard...');
        setTimeout(() => {
            window.location.href = 'dashboard.php';
        }, 600);
    } catch (err) {
        btn.disabled = false;
        btn.innerHTML = '<i class="bi bi-box-arrow-in-right"></i> Sign In to Dashboard';
    }
});
</script>

</body>
</html>
