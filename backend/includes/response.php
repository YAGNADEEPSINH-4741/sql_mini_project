<?php
/**
 * JSON RESPONSE & SANITIZATION HELPERS
 */

function jsonSuccess($data = [], $message = 'Operation completed successfully.') {
    header('Content-Type: application/json');
    echo json_encode([
        'success' => true,
        'message' => $message,
        'data' => $data
    ]);
    exit;
}

function jsonError($message = 'An unexpected error occurred.', $code = 400, $data = []) {
    header('Content-Type: application/json');
    http_response_code($code);
    echo json_encode([
        'success' => false,
        'error' => $message,
        'data' => $data
    ]);
    exit;
}

function getJsonInput() {
    $raw = file_get_contents('php://input');
    $decoded = json_decode($raw, true);
    return is_array($decoded) ? $decoded : $_POST;
}

function sanitize($input) {
    if (is_array($input)) {
        return array_map('sanitize', $input);
    }
    return htmlspecialchars(trim((string)$input), ENT_QUOTES, 'UTF-8');
}
