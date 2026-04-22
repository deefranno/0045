<?php
require_once '../includes/config.php';
require_once '../includes/auth.php';
require_once '../includes/functions.php';

require_login();

$message = '';
$error = '';

if ($_SERVER['REQUEST_METHOD'] === 'POST' && verify_csrf_token($_POST['csrf_token'] ?? '')) {
    $current_pass = $_POST['current_password'] ?? '';
    $new_pass = $_POST['new_password'] ?? '';
    $confirm_pass = $_POST['confirm_password'] ?? '';

    $stmt = $pdo->prepare("SELECT password FROM users WHERE id = ?");
    $stmt->execute([$_SESSION['user_id']]);
    $user = $stmt->fetch();

    if ($user && password_verify($current_pass, $user['password'])) {
        if ($new_pass === $confirm_pass) {
            $hashed = password_hash($new_pass, PASSWORD_DEFAULT);
            $stmt = $pdo->prepare("UPDATE users SET password = ? WHERE id = ?");
            $stmt->execute([$hashed, $_SESSION['user_id']]);
            $message = "Password updated successfully.";
        } else {
            $error = "New passwords do not match.";
        }
    } else {
        $error = "Current password incorrect.";
    }
}

$csrf_token = generate_csrf_token();
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Profile - Website Builder</title>
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
                <a href="backup.php"><i class="bi bi-cloud-download me-2"></i> Backup/Restore</a>
                <div class="mt-auto p-3"><hr><a href="logout.php" class="text-danger"><i class="bi bi-box-arrow-right me-2"></i> Logout</a></div>
            </div>

            <div class="col-md-9 col-lg-10 main-content">
                <h3 class="mb-4">Admin Profile</h3>
                <?php if ($message): ?> <div class="alert alert-success"><?php echo e($message); ?></div> <?php endif; ?>
                <?php if ($error): ?> <div class="alert alert-danger"><?php echo e($error); ?></div> <?php endif; ?>

                <div class="card border-0 shadow-sm" style="max-width: 500px;">
                    <div class="card-header bg-white"><strong>Change Password</strong></div>
                    <div class="card-body">
                        <form method="POST">
                            <input type="hidden" name="csrf_token" value="<?php echo $csrf_token; ?>">
                            <div class="mb-3">
                                <label class="form-label">Current Password</label>
                                <input type="password" name="current_password" class="form-control" required>
                            </div>
                            <div class="mb-3">
                                <label class="form-label">New Password</label>
                                <input type="password" name="new_password" class="form-control" required>
                            </div>
                            <div class="mb-3">
                                <label class="form-label">Confirm New Password</label>
                                <input type="password" name="confirm_password" class="form-control" required>
                            </div>
                            <button type="submit" class="btn btn-primary">Update Password</button>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
