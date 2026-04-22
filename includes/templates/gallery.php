<?php if (!empty($content['heading'])): ?>
    <div class="text-center mb-5">
        <h2 class="fw-bold"><?php echo e($content['heading']); ?></h2>
    </div>
<?php endif; ?>

<div class="row g-3">
    <?php
    $items = $content['items'] ?? [];
    $cols = $content['columns'] ?? '3';
    $col_class = 'col-md-' . (12 / $cols);
    foreach ($items as $item):
    ?>
    <div class="<?php echo $col_class; ?>">
        <a href="<?php echo e($item['image'] ?? '#'); ?>" class="gallery-item" data-lightbox="site-gallery">
            <img src="<?php echo e($item['image'] ?? ''); ?>" class="img-fluid rounded shadow-sm" alt="Gallery Image" loading="lazy">
        </a>
    </div>
    <?php endforeach; ?>
</div>
