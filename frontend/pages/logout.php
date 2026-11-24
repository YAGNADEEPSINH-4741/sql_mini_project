<?php
/**
 * LOGOUT SCRIPT
 */
require_once __DIR__ . '/../../backend/includes/auth.php';
Auth::logout();
header("Location: login.php");
exit;
