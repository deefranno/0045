<?php
require_once '../includes/config.php';
require_once '../includes/auth.php';
require_once '../includes/functions.php';

require_login();

$message = '';
$error = '';

// Handle Actions
if ($_SERVER['REQUEST_METHOD'] === 'POST' && verify_csrf_token($_POST['csrf_token'] ?? '')) {
    $action = $_POST['action'] ?? '';
    $id = intval($_POST['id'] ?? 0);

    if ($action === 'delete' && $id > 0) {
        $stmt = $pdo->prepare("DELETE FROM sections WHERE id = ?");
        $stmt->execute([$id]);
        $message = "Section deleted successfully.";
    } elseif ($action === 'toggle' && $id > 0) {
        $stmt = $pdo->prepare("UPDATE sections SET is_visible = 1 - is_visible WHERE id = ?");
        $stmt->execute([$id]);
        $message = "Visibility toggled.";
    } elseif ($action === 'duplicate' && $id > 0) {
        $stmt = $pdo->prepare("SELECT * FROM sections WHERE id = ?");
        $stmt->execute([$id]);
        $section = $stmt->fetch();
        if ($section) {
            $stmt = $pdo->prepare("INSERT INTO sections (title, slug, type, content, settings, sort_order) VALUES (?, ?, ?, ?, ?, ?)");
            $stmt->execute([
                $section['title'] . ' (Copy)',
                $section['slug'] . '-copy',
                $section['type'],
                $section['content'],
                $section['settings'],
                $section['sort_order'] + 1
            ]);
            $message = "Section duplicated.";
        }
    } elseif ($action === 'reorder') {
        $orders = $_POST['order'] ?? [];
        foreach ($orders as $id => $order) {
            $stmt = $pdo->prepare("UPDATE sections SET sort_order = ? WHERE id = ?");
            $stmt->execute([intval($order), intval($id)]);
        }
        $message = "Order updated.";
    }
}

$sections = get_sections($pdo, false);
$csrf_token = generate_csrf_token();
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Manage Sections - Website Builder</title>
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
                <a href="sections.php" class="active"><i class="bi bi-layers me-2"></i> Sections</a>
                <a href="settings.php"><i class="bi bi-gear me-2"></i> Settings</a>
                <a href="media.php"><i class="bi bi-images me-2"></i> Media Manager</a>
                <a href="profile.php"><i class="bi bi-person-circle me-2"></i> Profile</a>
                <a href="backup.php"><i class="bi bi-cloud-download me-2"></i> Backup/Restore</a>
                <div class="mt-auto p-3"><hr><a href="logout.php" class="text-danger"><i class="bi bi-box-arrow-right me-2"></i> Logout</a></div>
            </div>

            <div class="col-md-9 col-lg-10 main-content">
                <div class="d-flex justify-content-between align-items-center mb-4">
                    <h3>Manage Sections</h3>
                    <a href="edit-section.php" class="btn btn-primary"><i class="bi bi-plus-lg"></i> Add New Section</a>
                </div>

                <?php if ($message): ?>
                    <div class="alert alert-success alert-dismissible fade show"><?php echo e($message); ?><button type="button" class="btn-close" data-bs-dismiss="alert"></button></div>
                <?php endif; ?>

                <div class="card border-0 shadow-sm">
                    <div class="card-body">
                        <form method="POST">
                            <input type="hidden" name="csrf_token" value="<?php echo $csrf_token; ?>">
                            <input type="hidden" name="action" value="reorder">
                            <div class="table-responsive">
                                <table class="table table-hover align-middle">
                                    <thead class="table-light">
                                        <tr>
                                            <th width="50">Order</th>
                                            <th>Title</th>
                                            <th>Slug</th>
                                            <th>Type</th>
                                            <th>Status</th>
                                            <th class="text-end">Actions</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <?php foreach ($sections as $s): ?>
                                        <tr>
                                            <td>
                                                <input type="number" name="order[<?php echo $s['id']; ?>]" value="<?php echo $s['sort_order']; ?>" class="form-control form-control-sm" style="width: 60px;">
                                            </td>
                                            <td><strong><?php echo e($s['title']); ?></strong></td>
                                            <td><code>#<?php echo e($s['slug']); ?></code></td>
                                            <td><span class="badge bg-secondary"><?php echo e($s['type']); ?></span></td>
                                            <td>
                                                <?php if ($s['is_visible']): ?>
                                                    <span class="badge bg-success">Visible</span>
                                                <?php else: ?>
                                                    <span class="badge bg-warning">Hidden</span>
                                                <?php endif; ?>
                                            </td>
                                            <td class="text-end">
                                                <div class="btn-group">
                                                    <a href="edit-section.php?id=<?php echo $s['id']; ?>" class="btn btn-sm btn-outline-primary" title="Edit"><i class="bi bi-pencil"></i></a>
                                                    <form method="POST" class="d-inline">
                                                        <input type="hidden" name="csrf_token" value="<?php echo $csrf_token; ?>">
                                                        <input type="hidden" name="id" value="<?php echo $s['id']; ?>">
                                                        <button type="submit" name="action" value="toggle" class="btn btn-sm btn-outline-secondary" title="Show/Hide"><i class="bi <?php echo $s['is_visible'] ? 'bi-eye-slash' : 'bi-eye'; ?>"></i></button>
                                                        <button type="submit" name="action" value="duplicate" class="btn btn-sm btn-outline-info" title="Duplicate"><i class="bi bi-files"></i></button>
                                                        <button type="submit" name="action" value="delete" class="btn btn-sm btn-outline-danger" onclick="return confirm('Are you sure?')" title="Delete"><i class="bi bi-trash"></i></button>
                                                    </form>
                                                </div>
                                            </td>
                                        </tr>
                                        <?php endforeach; ?>
                                    </tbody>
                                </table>
                            </div>
                            <button type="submit" class="btn btn-sm btn-secondary mt-3">Update Sorting Order</button>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
