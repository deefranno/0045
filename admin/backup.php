<?php
require_once '../includes/config.php';
require_once '../includes/auth.php';
require_once '../includes/functions.php';

require_login();

$message = '';
$error = '';

if ($_SERVER['REQUEST_METHOD'] === 'POST' && verify_csrf_token($_POST['csrf_token'] ?? '')) {
    if (isset($_POST['action']) && $_POST['action'] === 'export') {
        $data = [
            'settings' => $pdo->query("SELECT * FROM settings")->fetchAll(),
            'sections' => $pdo->query("SELECT * FROM sections")->fetchAll()
        ];

        header('Content-Type: application/json');
        header('Content-Disposition: attachment; filename="website_backup_' . date('Y-m-d') . '.json"');
        echo json_encode($data, JSON_PRETTY_PRINT);
        exit;
    }

    if (isset($_POST['action']) && $_POST['action'] === 'import' && isset($_FILES['backup_file'])) {
        $json = file_get_contents($_FILES['backup_file']['tmp_name']);
        $data = json_decode($json, true);

        if ($data) {
            try {
                $pdo->beginTransaction();

                if (isset($data['settings'])) {
                    foreach ($data['settings'] as $s) {
                        $stmt = $pdo->prepare("INSERT INTO settings (`key`, value) VALUES (?, ?) ON DUPLICATE KEY UPDATE value = ?");
                        $stmt->execute([$s['key'], $s['value'], $s['value']]);
                    }
                }

                if (isset($data['sections'])) {
                    $pdo->exec("TRUNCATE TABLE sections");
                    foreach ($data['sections'] as $sec) {
                        $stmt = $pdo->prepare("INSERT INTO sections (title, slug, type, content, settings, sort_order, is_visible) VALUES (?, ?, ?, ?, ?, ?, ?)");
                        $stmt->execute([$sec['title'], $sec['slug'], $sec['type'], $sec['content'], $sec['settings'], $sec['sort_order'], $sec['is_visible']]);
                    }
                }

                $pdo->commit();
                $message = "Backup restored successfully!";
            } catch (Exception $e) {
                $pdo->rollBack();
                $error = "Error restoring backup: " . $e->getMessage();
            }
        } else {
            $error = "Invalid backup file.";
        }
    }
}

$csrf_token = generate_csrf_token();
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Backup/Restore - Website Builder</title>
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
                <a href="settings.php"><i class="bi bi-gear me-2"></i> Settings</a>
                <a href="media.php"><i class="bi bi-images me-2"></i> Media Manager</a>
                <a href="backup.php" class="active"><i class="bi bi-cloud-download me-2"></i> Backup/Restore</a>
                <div class="mt-auto p-3"><hr><a href="logout.php" class="text-danger"><i class="bi bi-box-arrow-right me-2"></i> Logout</a></div>
            </div>

            <div class="col-md-9 col-lg-10 main-content">
                <h3 class="mb-4">Backup & Restore</h3>

                <?php if ($message): ?>
                    <div class="alert alert-success"><?php echo e($message); ?></div>
                <?php endif; ?>
                <?php if ($error): ?>
                    <div class="alert alert-danger"><?php echo e($error); ?></div>
                <?php endif; ?>

                <div class="row">
                    <div class="col-md-6">
                        <div class="card border-0 shadow-sm mb-4">
                            <div class="card-header bg-white"><strong>Export Content</strong></div>
                            <div class="card-body">
                                <p class="text-muted">Download all settings and sections as a JSON file.</p>
                                <form method="POST">
                                    <input type="hidden" name="csrf_token" value="<?php echo $csrf_token; ?>">
                                    <input type="hidden" name="action" value="export">
                                    <button type="submit" class="btn btn-primary"><i class="bi bi-download me-2"></i> Download Backup</button>
                                </form>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="card border-0 shadow-sm mb-4">
                            <div class="card-header bg-white"><strong>Import Content</strong></div>
                            <div class="card-body">
                                <p class="text-muted">Restore your website from a previously exported JSON file. <span class="text-danger">Warning: This will overwrite current content.</span></p>
                                <form method="POST" enctype="multipart/form-data">
                                    <input type="hidden" name="csrf_token" value="<?php echo $csrf_token; ?>">
                                    <input type="hidden" name="action" value="import">
                                    <div class="mb-3">
                                        <input type="file" name="backup_file" class="form-control" required>
                                    </div>
                                    <button type="submit" class="btn btn-warning" onclick="return confirm('This will replace all sections and settings. Proceed?')"><i class="bi bi-cloud-upload me-2"></i> Restore Backup</button>
                                </form>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
