<?php
/**
 * Core Functions
 */

/**
 * Sanitize output
 */
function e($text) {
    return htmlspecialchars($text ?? '', ENT_QUOTES, 'UTF-8');
}

/**
 * CSRF Protection
 */
function generate_csrf_token() {
    if (empty($_SESSION['csrf_token'])) {
        $_SESSION['csrf_token'] = bin2hex(random_bytes(32));
    }
    return $_SESSION['csrf_token'];
}

function verify_csrf_token($token) {
    return isset($_SESSION['csrf_token']) && hash_equals($_SESSION['csrf_token'], $token);
}

/**
 * File Upload Handler
 */
function upload_image($file, $target_dir = "../uploads/") {
    if (!isset($file) || $file['error'] !== UPLOAD_ERR_OK) {
        return false;
    }

    $allowed_types = ['image/jpeg', 'image/png', 'image/gif', 'image/webp'];
    if (!in_array($file['type'], $allowed_types)) {
        return false;
    }

    $ext = pathinfo($file['name'], PATHINFO_EXTENSION);
    $filename = uniqid() . '.' . $ext;
    $target_file = $target_dir . $filename;

    if (move_uploaded_file($file['tmp_name'], $target_file)) {
        return 'uploads/' . $filename;
    }

    return false;
}

/**
 * Get sections from database
 */
function get_sections($pdo, $visible_only = true) {
    $sql = "SELECT * FROM sections";
    if ($visible_only) {
        $sql .= " WHERE is_visible = 1";
    }
    $sql .= " ORDER BY sort_order ASC";

    $stmt = $pdo->query($sql);
    return $stmt->fetchAll();
}

/**
 * Render a section based on its type
 */
function render_section($section) {
    $content = json_decode($section['content'], true);
    $settings = json_decode($section['settings'], true);
    $type = $section['type'];
    $slug = $section['slug'];

    $bg_style = "";
    if (($settings['bg_type'] ?? '') === 'color') {
        $bg_style = "background-color: " . ($settings['bg_color'] ?? 'transparent') . ";";
    } elseif (($settings['bg_type'] ?? '') === 'image' && !empty($settings['bg_image'])) {
        $bg_style = "background-image: url('" . e($settings['bg_image']) . "'); background-size: cover; background-position: center;";
    }

    $padding = "padding-top: " . ($settings['padding_top'] ?? '50') . "px; padding-bottom: " . ($settings['padding_bottom'] ?? '50') . "px;";
    $text_align = "text-align: " . ($settings['text_align'] ?? 'left') . ";";
    $overlay_opacity = ($settings['overlay_opacity'] ?? '0');
    $position = (($settings['bg_type'] ?? '') === 'image') ? "position: relative;" : "";

    echo "<section id=\"" . e($slug) . "\" class=\"site-section section-" . e($type) . "\" style=\"$bg_style $padding $text_align $position\">";

    if ($overlay_opacity > 0 && ($settings['bg_type'] ?? '') === 'image') {
        echo "<div class=\"section-overlay\" style=\"position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,$overlay_opacity); z-index: 1;\"></div>";
    }

    echo "<div class=\"container\" style=\"position: relative; z-index: 2;\">";

    // Include template part based on type
    $template_file = __DIR__ . "/templates/" . $type . ".php";
    if (file_exists($template_file)) {
        include $template_file;
    } else {
        // Fallback for generic sections
        if (isset($content['heading'])) echo "<h2>" . e($content['heading']) . "</h2>";
        if (isset($content['text'])) echo "<div>" . $content['text'] . "</div>";
    }

    echo "</div>";
    echo "</section>";
}
?>
