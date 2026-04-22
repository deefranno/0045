<?php
/**
 * Database Configuration
 */

// Database credentials - For cPanel, users will update these
define('DB_HOST', 'localhost');
define('DB_NAME', 'website_builder');
define('DB_USER', 'root');
define('DB_PASS', '');

try {
    $pdo = new PDO("mysql:host=" . DB_HOST . ";dbname=" . DB_NAME . ";charset=utf8mb4", DB_USER, DB_PASS);
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    $pdo->setAttribute(PDO::ATTR_DEFAULT_FETCH_MODE, PDO::FETCH_ASSOC);
} catch (PDOException $e) {
    // In production, you might want to log this instead of displaying it
    // die("Connection failed: " . $e->getMessage());
    $pdo = null; // Ensure $pdo is at least defined
}

// Global settings cache
$site_settings = [];
if ($pdo) {
    try {
        $stmt = $pdo->query("SELECT `key`, `value` FROM `settings`");
        while ($row = $stmt->fetch()) {
            $site_settings[$row['key']] = $row['value'];
        }
    } catch (Exception $e) {
        // Table might not exist yet
    }
}

function get_setting($key, $default = '') {
    global $site_settings;
    return $site_settings[$key] ?? $default;
}
?>
