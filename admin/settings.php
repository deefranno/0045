<?php
require_once '../includes/config.php';
require_once '../includes/auth.php';
require_once '../includes/functions.php';

require_login();

$message = '';

if ($_SERVER['REQUEST_METHOD'] === 'POST' && verify_csrf_token($_POST['csrf_token'] ?? '')) {
    foreach ($_POST['settings'] as $key => $value) {
        $stmt = $pdo->prepare("UPDATE settings SET value = ? WHERE `key` = ?");
        $stmt->execute([$value, $key]);
    }

    // Handle Logo Upload separately if provided
    if (isset($_FILES['logo_file']) && $_FILES['logo_file']['error'] === UPLOAD_ERR_OK) {
        $logo_path = upload_image($_FILES['logo_file']);
        if ($logo_path) {
            $stmt = $pdo->prepare("UPDATE settings SET value = ? WHERE `key` = 'logo_url'");
            $stmt->execute([$logo_path]);
        }
    }

    $message = "Settings updated successfully.";

    // Reload settings
    $stmt = $pdo->query("SELECT `key`, `value` FROM `settings`");
    $site_settings = [];
    while ($row = $stmt->fetch()) {
        $site_settings[$row['key']] = $row['value'];
    }
}

$csrf_token = generate_csrf_token();
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Global Settings - Website Builder</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css">
    <style>
        .sidebar { min-height: 100vh; background: #212529; color: white; }
        .sidebar a { color: rgba(255,255,255,0.8); text-decoration: none; padding: 10px 20px; display: block; }
        .sidebar a:hover, .sidebar a.active { background: rgba(255,255,255,0.1); color: white; }
        .main-content { padding: 20px; background: #f8f9fa; min-height: 100vh; }
    </style>
</head>
<body>
    <div class="container-fluid">
        <div class="row">
            <div class="col-md-3 col-lg-2 p-0 sidebar">
                <div class="p-3"><h5 class="mb-4">CMS Admin</h5><hr></div>
                <a href="index.php"><i class="bi bi-speedometer2 me-2"></i> Dashboard</a>
                <a href="sections.php"><i class="bi bi-layers me-2"></i> Sections</a>
                <a href="settings.php" class="active"><i class="bi bi-gear me-2"></i> Settings</a>
                <a href="media.php"><i class="bi bi-images me-2"></i> Media Manager</a>
                <a href="backup.php"><i class="bi bi-cloud-download me-2"></i> Backup/Restore</a>
                <div class="mt-auto p-3"><hr><a href="logout.php" class="text-danger"><i class="bi bi-box-arrow-right me-2"></i> Logout</a></div>
            </div>

            <div class="col-md-9 col-lg-10 main-content">
                <h3 class="mb-4">Global Settings</h3>

                <?php if ($message): ?>
                    <div class="alert alert-success alert-dismissible fade show"><?php echo e($message); ?><button type="button" class="btn-close" data-bs-dismiss="alert"></button></div>
                <?php endif; ?>

                <form method="POST" enctype="multipart/form-data">
                    <input type="hidden" name="csrf_token" value="<?php echo $csrf_token; ?>">

                    <div class="row">
                        <div class="col-lg-6">
                            <div class="card border-0 shadow-sm mb-4">
                                <div class="card-header bg-white"><strong>Site Information & Colors</strong></div>
                                <div class="card-body">
                                    <div class="mb-3">
                                        <label class="form-label">Site Title</label>
                                        <input type="text" name="settings[site_title]" class="form-control" value="<?php echo e(get_setting('site_title')); ?>">
                                    </div>
                                    <div class="mb-3">
                                        <label class="form-label">Primary Color</label>
                                        <input type="color" name="settings[primary_color]" class="form-control form-control-color w-100" value="<?php echo e(get_setting('primary_color', '#0d6efd')); ?>">
                                    </div>
                                    <div class="mb-3">
                                        <label class="form-label">Secondary Color</label>
                                        <input type="color" name="settings[secondary_color]" class="form-control form-control-color w-100" value="<?php echo e(get_setting('secondary_color', '#6c757d')); ?>">
                                    </div>
                                    <div class="mb-3">
                                        <label class="form-label">Background Color</label>
                                        <input type="color" name="settings[bg_color]" class="form-control form-control-color w-100" value="<?php echo e(get_setting('bg_color', '#ffffff')); ?>">
                                    </div>
                                    <div class="mb-3">
                                        <label class="form-label">Google Font Name</label>
                                        <input type="text" name="settings[font_family]" class="form-control" value="<?php echo e(get_setting('font_family', 'Inter')); ?>" placeholder="e.g. Inter, Roboto, Playfair Display">
                                    </div>
                                </div>
                            </div>

                            <div class="card border-0 shadow-sm mb-4">
                                <div class="card-header bg-white"><strong>Header & Logo</strong></div>
                                <div class="card-body">
                                    <div class="mb-3">
                                        <label class="form-label">Logo Image</label>
                                        <?php if (get_setting('logo_url')): ?>
                                            <div class="mb-2"><img src="../<?php echo e(get_setting('logo_url')); ?>" style="max-height: 50px;"></div>
                                        <?php endif; ?>
                                        <input type="file" name="logo_file" class="form-control">
                                    </div>
                                    <div class="row">
                                        <div class="col-md-6 mb-3">
                                            <label class="form-label">Logo Width (px)</label>
                                            <input type="number" name="settings[logo_width]" class="form-control" value="<?php echo e(get_setting('logo_width', '150')); ?>">
                                        </div>
                                        <div class="col-md-6 mb-3">
                                            <label class="form-label">Header Height (px)</label>
                                            <input type="number" name="settings[header_height]" class="form-control" value="<?php echo e(get_setting('header_height', '80')); ?>">
                                        </div>
                                    </div>
                                    <div class="form-check form-switch">
                                        <input class="form-check-input" type="checkbox" name="settings[sticky_header]" value="1" <?php echo get_setting('sticky_header') ? 'checked' : ''; ?>>
                                        <label class="form-check-label">Sticky Header</label>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div class="col-lg-6">
                            <div class="card border-0 shadow-sm mb-4">
                                <div class="card-header bg-white"><strong>Integrations & Extras</strong></div>
                                <div class="card-body">
                                    <div class="mb-3">
                                        <label class="form-label">Formspree Endpoint URL</label>
                                        <input type="text" name="settings[formspree_url]" class="form-control" value="<?php echo e(get_setting('formspree_url')); ?>" placeholder="https://formspree.io/f/xxxxx">
                                    </div>
                                    <div class="mb-3">
                                        <label class="form-label">WhatsApp Number (e.g. 1234567890)</label>
                                        <input type="text" name="settings[whatsapp_number]" class="form-control" value="<?php echo e(get_setting('whatsapp_number')); ?>">
                                    </div>
                                    <div class="mb-3">
                                        <label class="form-label">Analytics Script / Google Tag</label>
                                        <textarea name="settings[analytics_code]" class="form-control font-monospace" rows="4"><?php echo e(get_setting('analytics_code')); ?></textarea>
                                    </div>
                                    <div class="mb-3">
                                        <label class="form-label">Custom Site CSS</label>
                                        <textarea name="settings[custom_css]" class="form-control font-monospace" rows="4"><?php echo e(get_setting('custom_css')); ?></textarea>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <button type="submit" class="btn btn-primary btn-lg"><i class="bi bi-save me-2"></i> Save All Settings</button>
                </form>
            </div>
        </div>
    </div>
</body>
</html>
