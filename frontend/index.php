<?php
/**
 * APPLICATION ENTRY POINT / ROUTER
 */
require_once __DIR__ . '/../backend/includes/auth.php';

if (Auth::check()) {
    header("Location: pages/dashboard.php");
} else {
    header("Location: pages/login.php");
}
exit;
