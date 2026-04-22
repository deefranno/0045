<?php
require_once '../includes/config.php';
require_once '../includes/auth.php';
require_once '../includes/functions.php';

require_login();

$message = '';
$error = '';

if ($_SERVER['REQUEST_METHOD'] === 'POST' && verify_csrf_token($_POST['csrf_token'] ?? '')) {
    if (isset($_FILES['image'])) {
        $path = upload_image($_FILES['image']);
        if ($path) {
            $message = "Image uploaded successfully.";
        } else {
            $error = "Failed to upload image. Check format and size.";
        }
    }

    if (isset($_POST['delete_file'])) {
        $file = $_POST['delete_file'];
        if (strpos($file, 'uploads/') === 0 && file_exists('../' . $file)) {
            unlink('../' . $file);
            $message = "File deleted.";
        }
    }
}

$files = glob('../uploads/*');
$csrf_token = generate_csrf_token();
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Media Manager - Website Builder</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css">
    <style>
        .sidebar { min-height: 100vh; background: #212529; color: white; }
        .sidebar a { color: rgba(255,255,255,0.8); text-decoration: none; padding: 10px 20px; display: block; }
        .sidebar a:hover, .sidebar a.active { background: rgba(255,255,255,0.1); color: white; }
        .main-content { padding: 20px; background: #f8f9fa; min-height: 100vh; }
        .media-card { position: relative; overflow: hidden; }
        .media-card .btn-delete { position: absolute; top: 5px; right: 5px; display: none; }
        .media-card:hover .btn-delete { display: block; }
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
                <a href="media.php" class="active"><i class="bi bi-images me-2"></i> Media Manager</a>
                <a href="backup.php"><i class="bi bi-cloud-download me-2"></i> Backup/Restore</a>
                <div class="mt-auto p-3"><hr><a href="logout.php" class="text-danger"><i class="bi bi-box-arrow-right me-2"></i> Logout</a></div>
            </div>

            <div class="col-md-9 col-lg-10 main-content">
                <div class="d-flex justify-content-between align-items-center mb-4">
                    <h3>Media Manager</h3>
                    <form method="POST" enctype="multipart/form-data" class="d-flex gap-2">
                        <input type="hidden" name="csrf_token" value="<?php echo $csrf_token; ?>">
                        <input type="file" name="image" class="form-control form-control-sm" required>
                        <button type="submit" class="btn btn-primary btn-sm">Upload</button>
                    </form>
                </div>

                <?php if ($message): ?>
                    <div class="alert alert-success"><?php echo e($message); ?></div>
                <?php endif; ?>
                <?php if ($error): ?>
                    <div class="alert alert-danger"><?php echo e($error); ?></div>
                <?php endif; ?>

                <div class="row g-3">
                    <?php foreach ($files as $file):
                        $rel_path = 'uploads/' . basename($file);
                    ?>
                        <div class="col-6 col-md-4 col-lg-3">
                            <div class="card media-card h-100 shadow-sm">
                                <img src="../<?php echo $rel_path; ?>" class="card-img-top" style="height: 150px; object-fit: cover;">
                                <div class="card-body p-2">
                                    <small class="text-truncate d-block" title="<?php echo $rel_path; ?>"><?php echo basename($file); ?></small>
                                    <div class="input-group input-group-sm mt-2">
                                        <input type="text" class="form-control" value="<?php echo $rel_path; ?>" readonly id="path-<?php echo md5($file); ?>">
                                        <button class="btn btn-outline-secondary" onclick="navigator.clipboard.writeText('<?php echo $rel_path; ?>'); alert('Path copied!')"><i class="bi bi-copy"></i></button>
                                    </div>
                                </div>
                                <form method="POST" class="btn-delete">
                                    <input type="hidden" name="csrf_token" value="<?php echo $csrf_token; ?>">
                                    <input type="hidden" name="delete_file" value="<?php echo $rel_path; ?>">
                                    <button type="submit" class="btn btn-danger btn-sm rounded-circle" onclick="return confirm('Delete this file?')"><i class="bi bi-trash"></i></button>
                                </form>
                            </div>
                        </div>
                    <?php endforeach; ?>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
