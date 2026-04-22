<?php
require_once '../includes/config.php';
require_once '../includes/auth.php';
require_once '../includes/functions.php';

require_login();

$id = intval($_GET['id'] ?? 0);
$section = null;
if ($id > 0) {
    $stmt = $pdo->prepare("SELECT * FROM sections WHERE id = ?");
    $stmt->execute([$id]);
    $section = $stmt->fetch();
}

$message = '';
$error = '';

if ($_SERVER['REQUEST_METHOD'] === 'POST' && verify_csrf_token($_POST['csrf_token'] ?? '')) {
    $title = $_POST['title'] ?? '';
    $slug = $_POST['slug'] ?? '';
    $type = $_POST['type'] ?? 'hero';
    $is_visible = isset($_POST['is_visible']) ? 1 : 0;

    // Process items (for Services, Gallery, Pricing, FAQ, Testimonials)
    $items = [];
    if (isset($_POST['item_title'])) {
        foreach ($_POST['item_title'] as $index => $item_title) {
            $items[] = [
                'title' => $item_title,
                'text' => $_POST['item_text'][$index] ?? '',
                'image' => $_POST['item_image'][$index] ?? '',
                'icon' => $_POST['item_icon'][$index] ?? '',
                'price' => $_POST['item_price'][$index] ?? '',
                'button_text' => $_POST['item_btn_text'][$index] ?? '',
                'button_link' => $_POST['item_btn_link'][$index] ?? '',
                'video_url' => $_POST['item_video_url'][$index] ?? ''
            ];
        }
    }

    $content = [
        'heading' => $_POST['content_heading'] ?? '',
        'subheading' => $_POST['content_subheading'] ?? '',
        'text' => $_POST['content_text'] ?? '',
        'button_text' => $_POST['button_text'] ?? '',
        'button_link' => $_POST['button_link'] ?? '',
        'image' => $_POST['image'] ?? '',
        'columns' => $_POST['columns'] ?? '3',
        'items' => $items
    ];

    $settings = [
        'bg_type' => $_POST['bg_type'] ?? 'color',
        'bg_color' => $_POST['bg_color'] ?? '#ffffff',
        'bg_image' => $_POST['bg_image'] ?? '',
        'overlay_opacity' => $_POST['overlay_opacity'] ?? '0',
        'text_align' => $_POST['text_align'] ?? 'left',
        'padding_top' => $_POST['padding_top'] ?? '50',
        'padding_bottom' => $_POST['padding_bottom'] ?? '50',
        'heading_size' => $_POST['heading_size'] ?? '2.5rem',
        'heading_weight' => $_POST['heading_weight'] ?? '700',
        'custom_css' => $_POST['custom_css'] ?? ''
    ];

    $content_json = json_encode($content);
    $settings_json = json_encode($settings);

    if ($id > 0) {
        $stmt = $pdo->prepare("UPDATE sections SET title = ?, slug = ?, type = ?, content = ?, settings = ?, is_visible = ? WHERE id = ?");
        $stmt->execute([$title, $slug, $type, $content_json, $settings_json, $is_visible, $id]);
        $message = "Section updated successfully.";
    } else {
        $stmt = $pdo->prepare("INSERT INTO sections (title, slug, type, content, settings, is_visible) VALUES (?, ?, ?, ?, ?, ?)");
        $stmt->execute([$title, $slug, $type, $content_json, $settings_json, $is_visible]);
        $id = $pdo->lastInsertId();
        $message = "Section created successfully.";
    }

    // Refresh data
    $stmt = $pdo->prepare("SELECT * FROM sections WHERE id = ?");
    $stmt->execute([$id]);
    $section = $stmt->fetch();
}

$csrf_token = generate_csrf_token();
$c = $section ? json_decode($section['content'], true) : [];
$s = $section ? json_decode($section['settings'], true) : [];
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title><?php echo $id ? 'Edit' : 'Add'; ?> Section - Website Builder</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css">
    <style>
        .sidebar { min-height: 100vh; background: #212529; color: white; }
        .sidebar a { color: rgba(255,255,255,0.8); text-decoration: none; padding: 10px 20px; display: block; }
        .sidebar a:hover, .sidebar a.active { background: rgba(255,255,255,0.1); color: white; }
        .main-content { padding: 20px; background: #f8f9fa; min-height: 100vh; }
        .item-row { background: #fff; border: 1px solid #dee2e6; padding: 15px; margin-bottom: 10px; border-radius: 5px; position: relative; }
        .btn-remove-item { position: absolute; top: 10px; right: 10px; }
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
                <a href="backup.php"><i class="bi bi-cloud-download me-2"></i> Backup/Restore</a>
                <div class="mt-auto p-3"><hr><a href="logout.php" class="text-danger"><i class="bi bi-box-arrow-right me-2"></i> Logout</a></div>
            </div>

            <div class="col-md-9 col-lg-10 main-content">
                <nav aria-label="breadcrumb">
                  <ol class="breadcrumb"><li class="breadcrumb-item"><a href="sections.php">Sections</a></li><li class="breadcrumb-item active"><?php echo $id ? 'Edit' : 'Add New'; ?></li></ol>
                </nav>

                <?php if ($message): ?>
                    <div class="alert alert-success alert-dismissible fade show"><?php echo e($message); ?><button type="button" class="btn-close" data-bs-dismiss="alert"></button></div>
                <?php endif; ?>

                <form method="POST" id="sectionForm">
                    <input type="hidden" name="csrf_token" value="<?php echo $csrf_token; ?>">

                    <div class="row">
                        <div class="col-lg-8">
                            <div class="card border-0 shadow-sm mb-4">
                                <div class="card-header bg-white"><strong>Content Details</strong></div>
                                <div class="card-body">
                                    <div class="row mb-3">
                                        <div class="col-md-6">
                                            <label class="form-label">Internal Title</label>
                                            <input type="text" name="title" class="form-control" value="<?php echo e($section['title'] ?? ''); ?>" required>
                                        </div>
                                        <div class="col-md-6">
                                            <label class="form-label">Slug</label>
                                            <input type="text" name="slug" class="form-control" value="<?php echo e($section['slug'] ?? ''); ?>" required>
                                        </div>
                                    </div>
                                    <div class="mb-3">
                                        <label class="form-label">Section Type</label>
                                        <select name="type" class="form-select" id="typeSelect">
                                            <option value="hero" <?php echo ($section['type'] ?? '') === 'hero' ? 'selected' : ''; ?>>Hero</option>
                                            <option value="about" <?php echo ($section['type'] ?? '') === 'about' ? 'selected' : ''; ?>>About</option>
                                            <option value="services" <?php echo ($section['type'] ?? '') === 'services' ? 'selected' : ''; ?>>Services</option>
                                            <option value="gallery" <?php echo ($section['type'] ?? '') === 'gallery' ? 'selected' : ''; ?>>Gallery</option>
                                            <option value="pricing" <?php echo ($section['type'] ?? '') === 'pricing' ? 'selected' : ''; ?>>Pricing</option>
                                            <option value="testimonials" <?php echo ($section['type'] ?? '') === 'testimonials' ? 'selected' : ''; ?>>Testimonials</option>
                                            <option value="faq" <?php echo ($section['type'] ?? '') === 'faq' ? 'selected' : ''; ?>>FAQ</option>
                                            <option value="video" <?php echo ($section['type'] ?? '') === 'video' ? 'selected' : ''; ?>>Video Modal</option>
                                            <option value="contact" <?php echo ($section['type'] ?? '') === 'contact' ? 'selected' : ''; ?>>Contact Form</option>
                                            <option value="custom" <?php echo ($section['type'] ?? '') === 'custom' ? 'selected' : ''; ?>>Custom HTML</option>
                                        </select>
                                    </div>

                                    <div class="mb-3">
                                        <label class="form-label">Main Heading</label>
                                        <input type="text" name="content_heading" class="form-control" value="<?php echo e($c['heading'] ?? ''); ?>">
                                    </div>
                                    <div class="mb-3">
                                        <label class="form-label">Description / Text</label>
                                        <textarea name="content_text" class="form-control" rows="4"><?php echo e($c['text'] ?? ''); ?></textarea>
                                    </div>

                                    <div id="itemsContainer" class="mt-4">
                                        <h5>List Items</h5>
                                        <div id="itemsList">
                                            <?php
                                            $items = $c['items'] ?? [];
                                            foreach ($items as $item): ?>
                                                <div class="item-row">
                                                    <button type="button" class="btn btn-sm btn-danger btn-remove-item" onclick="this.parentElement.remove()">X</button>
                                                    <div class="row g-2">
                                                        <div class="col-md-6"><input type="text" name="item_title[]" class="form-control form-control-sm" placeholder="Item Title" value="<?php echo e($item['title'] ?? ''); ?>"></div>
                                                        <div class="col-md-6"><input type="text" name="item_icon[]" class="form-control form-control-sm" placeholder="Icon (bi-star)" value="<?php echo e($item['icon'] ?? ''); ?>"></div>
                                                        <div class="col-12"><textarea name="item_text[]" class="form-control form-control-sm mt-1" placeholder="Item Text"><?php echo e($item['text'] ?? ''); ?></textarea></div>
                                                        <div class="col-md-6"><input type="text" name="item_image[]" class="form-control form-control-sm mt-1" placeholder="Image URL" value="<?php echo e($item['image'] ?? ''); ?>"></div>
                                                        <div class="col-md-6"><input type="text" name="item_price[]" class="form-control form-control-sm mt-1" placeholder="Price" value="<?php echo e($item['price'] ?? ''); ?>"></div>
                                                        <div class="col-md-6"><input type="text" name="item_btn_text[]" class="form-control form-control-sm mt-1" placeholder="Button Text" value="<?php echo e($item['button_text'] ?? ''); ?>"></div>
                                                        <div class="col-md-6"><input type="text" name="item_btn_link[]" class="form-control form-control-sm mt-1" placeholder="Button Link" value="<?php echo e($item['button_link'] ?? ''); ?>"></div>
                                                    </div>
                                                </div>
                                            <?php endforeach; ?>
                                        </div>
                                        <button type="button" class="btn btn-outline-secondary btn-sm" id="addItemBtn">+ Add Item</button>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div class="col-lg-4">
                            <div class="card border-0 shadow-sm mb-4">
                                <div class="card-header bg-white"><strong>Section Settings</strong></div>
                                <div class="card-body">
                                    <div class="mb-3 form-check form-switch">
                                        <input class="form-check-input" type="checkbox" name="is_visible" <?php echo ($section['is_visible'] ?? 1) ? 'checked' : ''; ?>>
                                        <label class="form-check-label">Visible</label>
                                    </div>
                                    <div class="mb-3">
                                        <label class="form-label">Columns (1-4)</label>
                                        <select name="columns" class="form-select">
                                            <option value="1" <?php echo ($c['columns'] ?? '') === '1' ? 'selected' : ''; ?>>1 Column</option>
                                            <option value="2" <?php echo ($c['columns'] ?? '') === '2' ? 'selected' : ''; ?>>2 Columns</option>
                                            <option value="3" <?php echo ($c['columns'] ?? '3') === '3' ? 'selected' : ''; ?>>3 Columns</option>
                                            <option value="4" <?php echo ($c['columns'] ?? '') === '4' ? 'selected' : ''; ?>>4 Columns</option>
                                        </select>
                                    </div>
                                    <hr>
                                    <label class="form-label">Background</label>
                                    <select name="bg_type" class="form-select mb-2">
                                        <option value="color" <?php echo ($s['bg_type'] ?? '') === 'color' ? 'selected' : ''; ?>>Solid Color</option>
                                        <option value="image" <?php echo ($s['bg_type'] ?? '') === 'image' ? 'selected' : ''; ?>>Image</option>
                                    </select>
                                    <input type="color" name="bg_color" class="form-control form-control-color w-100 mb-2" value="<?php echo e($s['bg_color'] ?? '#ffffff'); ?>">
                                    <input type="text" name="bg_image" class="form-control mb-2" placeholder="BG Image URL" value="<?php echo e($s['bg_image'] ?? ''); ?>">
                                    <label class="form-label small">Overlay Opacity (0 to 1)</label>
                                    <input type="number" name="overlay_opacity" class="form-control mb-3" step="0.1" min="0" max="1" value="<?php echo e($s['overlay_opacity'] ?? '0'); ?>">
                                    <hr>
                                    <label class="form-label">Typography</label>
                                    <div class="row g-2 mb-3">
                                        <div class="col-6"><input type="text" name="heading_size" class="form-control form-control-sm" placeholder="Size (2.5rem)" value="<?php echo e($s['heading_size'] ?? ''); ?>"></div>
                                        <div class="col-6"><input type="text" name="heading_weight" class="form-control form-control-sm" placeholder="Weight (700)" value="<?php echo e($s['heading_weight'] ?? ''); ?>"></div>
                                    </div>
                                </div>
                            </div>
                            <button type="submit" class="btn btn-primary w-100 py-2"><i class="bi bi-save me-2"></i> Save Section</button>
                        </div>
                    </div>
                </form>
            </div>
        </div>
    </div>

    <script>
        document.getElementById('addItemBtn').addEventListener('click', function() {
            const container = document.getElementById('itemsList');
            const row = document.createElement('div');
            row.className = 'item-row';
            row.innerHTML = `
                <button type="button" class="btn btn-sm btn-danger btn-remove-item" onclick="this.parentElement.remove()">X</button>
                <div class="row g-2">
                    <div class="col-md-6"><input type="text" name="item_title[]" class="form-control form-control-sm" placeholder="Item Title"></div>
                    <div class="col-md-6"><input type="text" name="item_icon[]" class="form-control form-control-sm" placeholder="Icon (bi-star)"></div>
                    <div class="col-12"><textarea name="item_text[]" class="form-control form-control-sm mt-1" placeholder="Item Text"></textarea></div>
                    <div class="col-md-6"><input type="text" name="item_image[]" class="form-control form-control-sm mt-1" placeholder="Image URL"></div>
                    <div class="col-md-6"><input type="text" name="item_price[]" class="form-control form-control-sm mt-1" placeholder="Price"></div>
                    <div class="col-md-6"><input type="text" name="item_btn_text[]" class="form-control form-control-sm mt-1" placeholder="Button Text"></div>
                    <div class="col-md-6"><input type="text" name="item_btn_link[]" class="form-control form-control-sm mt-1" placeholder="Button Link"></div>
                </div>
            `;
            container.appendChild(row);
        });
    </script>
</body>
</html>
