<?php
require_once 'includes/config.php';
require_once 'includes/functions.php';

// If DB connection fails, show a simple error
if (!$pdo) {
    die("Database connection error. Please check includes/config.php and ensure database.sql is imported.");
}

$sections = get_sections($pdo);
$font_family = get_setting('font_family', 'Inter');
$primary_color = get_setting('primary_color', '#0d6efd');
$bg_color = get_setting('bg_color', '#ffffff');
$header_height = get_setting('header_height', '80');
$logo_url = get_setting('logo_url');
$logo_width = get_setting('logo_width', '150');
$sticky_header = get_setting('sticky_header');
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title><?php echo e(get_setting('site_title')); ?></title>

    <!-- Bootstrap 5 CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/lightbox2/2.11.4/css/lightbox.min.css">

    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=<?php echo str_replace(' ', '+', $font_family); ?>:wght@300;400;600;700&display=swap" rel="stylesheet">

    <style>
        :root {
            --primary-color: <?php echo $primary_color; ?>;
            --bg-color: <?php echo $bg_color; ?>;
            --header-height: <?php echo $header_height; ?>px;
            --font-family: '<?php echo $font_family; ?>', sans-serif;
        }

        body {
            font-family: var(--font-family);
            background-color: var(--bg-color);
            color: <?php echo get_setting('text_color', '#212529'); ?>;
        }

        .navbar {
            height: var(--header-height);
            background: white;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            transition: all 0.3s;
        }

        <?php if ($sticky_header): ?>
        .navbar.sticky-top {
            position: sticky;
            top: 0;
            z-index: 1020;
        }
        <?php endif; ?>

        .navbar-brand img {
            max-width: <?php echo $logo_width; ?>px;
            height: auto;
        }

        .btn-primary {
            background-color: var(--primary-color);
            border-color: var(--primary-color);
        }

        .section-padding {
            padding: 80px 0;
        }

        /* Floating WhatsApp */
        .whatsapp-float {
            position: fixed;
            bottom: 20px;
            right: 20px;
            background-color: #25d366;
            color: white;
            width: 60px;
            height: 60px;
            border-radius: 50px;
            text-align: center;
            font-size: 30px;
            box-shadow: 2px 2px 3px #999;
            z-index: 100;
            display: flex;
            align-items: center;
            justify-content: center;
            text-decoration: none;
        }

        /* Back to top */
        #back-to-top {
            position: fixed;
            bottom: 90px;
            right: 20px;
            display: none;
            z-index: 99;
        }

        <?php echo get_setting('custom_css'); ?>
    </style>
</head>
<body data-bs-spy="scroll" data-bs-target="#main-nav" data-bs-offset="100">

    <!-- Header / Navigation -->
    <nav id="main-nav" class="navbar navbar-expand-lg navbar-light <?php echo $sticky_header ? 'sticky-top' : ''; ?>">
        <div class="container">
            <a class="navbar-brand" href="#">
                <?php if ($logo_url): ?>
                    <img src="<?php echo e($logo_url); ?>" alt="Logo">
                <?php else: ?>
                    <span class="fw-bold"><?php echo e(get_setting('site_title')); ?></span>
                <?php endif; ?>
            </a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <?php foreach ($sections as $s): ?>
                        <li class="nav-item">
                            <a class="nav-link" href="#<?php echo e($s['slug']); ?>"><?php echo e($s['title']); ?></a>
                        </li>
                    <?php endforeach; ?>
                </ul>
            </div>
        </div>
    </nav>

    <!-- Content Sections -->
    <main>
        <?php
        if (empty($sections)) {
            echo '<div class="container py-5 text-center"><h3>No sections found. Please add sections in the admin panel.</h3></div>';
        } else {
            foreach ($sections as $section) {
                render_section($section);
            }
        }
        ?>
    </main>

    <!-- Footer -->
    <footer class="bg-dark text-white py-4 mt-5">
        <div class="container text-center">
            <p class="mb-0"><?php echo e(get_setting('footer_text')); ?></p>
        </div>
    </footer>

    <!-- Cookie Notice -->
    <?php if (get_setting('cookie_notice')): ?>
    <div id="cookie-notice" class="bg-dark text-white p-3 position-fixed bottom-0 start-0 w-100" style="z-index: 1050; display: none;">
        <div class="container d-flex justify-content-between align-items-center">
            <span>We use cookies to ensure you get the best experience on our website.</span>
            <button class="btn btn-sm btn-outline-light ms-3" onclick="acceptCookies()">Got it!</button>
        </div>
    </div>
    <script>
        function acceptCookies() {
            localStorage.setItem('cookiesAccepted', 'true');
            document.getElementById('cookie-notice').style.display = 'none';
        }
        if (!localStorage.getItem('cookiesAccepted')) {
            document.getElementById('cookie-notice').style.display = 'block';
        }
    </script>
    <?php endif; ?>

    <!-- Back to top -->
    <button type="button" class="btn btn-primary rounded-circle" id="back-to-top">
        <i class="bi bi-arrow-up"></i>
    </button>

    <!-- WhatsApp Button -->
    <?php if (get_setting('whatsapp_number')): ?>
    <a href="https://wa.me/<?php echo e(get_setting('whatsapp_number')); ?>?text=<?php echo urlencode(get_setting('whatsapp_message')); ?>" class="whatsapp-float" target="_blank">
        <i class="bi bi-whatsapp"></i>
    </a>
    <?php endif; ?>

    <!-- JS Scripts -->
    <script src="https://code.jquery.com/jquery-3.7.1.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/lightbox2/2.11.4/js/lightbox.min.js"></script>
    <script src="assets/js/scripts.js"></script>

    <?php echo get_setting('analytics_code'); ?>
</body>
</html>
