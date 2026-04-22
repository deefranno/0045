<?php
require_once '../includes/config.php';
require_once '../includes/auth.php';
require_once '../includes/functions.php';

require_login();

// Simple stats for dashboard
$section_count = $pdo->query("SELECT COUNT(*) FROM sections")->fetchColumn();
$last_update = $pdo->query("SELECT MAX(created_at) FROM sections")->fetchColumn();
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard - Website Builder</title>
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
            <!-- Sidebar -->
            <div class="col-md-3 col-lg-2 p-0 sidebar">
                <div class="p-3">
                    <h5 class="mb-4">CMS Admin</h5>
                    <hr>
                </div>
                <a href="index.php" class="active"><i class="bi bi-speedometer2 me-2"></i> Dashboard</a>
                <a href="sections.php"><i class="bi bi-layers me-2"></i> Sections</a>
                <a href="settings.php"><i class="bi bi-gear me-2"></i> Settings</a>
                <a href="media.php"><i class="bi bi-images me-2"></i> Media Manager</a>
                <a href="profile.php"><i class="bi bi-person-circle me-2"></i> Profile</a>
                <a href="backup.php"><i class="bi bi-cloud-download me-2"></i> Backup/Restore</a>
                <div class="mt-auto p-3">
                    <hr>
                    <a href="logout.php" class="text-danger"><i class="bi bi-box-arrow-right me-2"></i> Logout</a>
                </div>
            </div>

            <!-- Main Content -->
            <div class="col-md-9 col-lg-10 main-content">
                <nav class="navbar navbar-expand-lg navbar-light bg-white mb-4 rounded shadow-sm">
                    <div class="container-fluid">
                        <span class="navbar-brand">Welcome, <?php echo e($_SESSION['username']); ?>!</span>
                        <a href="../index.php" target="_blank" class="btn btn-outline-primary btn-sm">View Site <i class="bi bi-box-arrow-up-right"></i></a>
                    </div>
                </nav>

                <div class="row g-4">
                    <div class="col-md-4">
                        <div class="card border-0 shadow-sm">
                            <div class="card-body">
                                <h6 class="text-muted mb-2">Total Sections</h6>
                                <h3 class="mb-0"><?php echo $section_count; ?></h3>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="card border-0 shadow-sm">
                            <div class="card-body">
                                <h6 class="text-muted mb-2">Last Update</h6>
                                <h3 class="mb-0 h5"><?php echo $last_update ?: 'Never'; ?></h3>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="card border-0 shadow-sm">
                            <div class="card-body">
                                <h6 class="text-muted mb-2">PHP Version</h6>
                                <h3 class="mb-0 h5"><?php echo PHP_VERSION; ?></h3>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="mt-5">
                    <h4>Quick Actions</h4>
                    <div class="row g-3">
                        <div class="col-auto">
                            <a href="edit-section.php" class="btn btn-success"><i class="bi bi-plus-lg"></i> Add New Section</a>
                        </div>
                        <div class="col-auto">
                            <a href="settings.php" class="btn btn-primary"><i class="bi bi-palette"></i> Customize Design</a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
