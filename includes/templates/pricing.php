<?php if (!empty($content['heading'])): ?>
    <div class="text-center mb-5">
        <h2 class="fw-bold"><?php echo e($content['heading']); ?></h2>
        <?php if (!empty($content['subheading'])): ?>
            <p class="text-muted"><?php echo e($content['subheading']); ?></p>
        <?php endif; ?>
    </div>
<?php endif; ?>

<div class="row g-4 justify-content-center">
    <?php
    $items = $content['items'] ?? [];
    foreach ($items as $item):
    ?>
    <div class="col-md-4">
        <div class="card h-100 border-0 shadow-sm text-center overflow-hidden">
            <?php if (!empty($item['image'])): ?>
                <img src="<?php echo e($item['image']); ?>" class="card-img-top" alt="Gallery Image" loading="lazy">
            <?php endif; ?>
            <div class="card-body">
                <h5 class="card-title fw-bold"><?php echo e($item['title'] ?? ''); ?></h5>
                <p class="card-text text-muted"><?php echo e($item['text'] ?? ''); ?></p>
                <?php if (!empty($item['price'])): ?>
                    <h3 class="text-primary fw-bold"><?php echo e($item['price']); ?></h3>
                <?php endif; ?>
                <?php if (!empty($item['button_text'])): ?>
                    <a href="<?php echo e($item['button_link'] ?? '#'); ?>" class="btn btn-outline-primary mt-3"><?php echo e($item['button_text']); ?></a>
                <?php endif; ?>
            </div>
        </div>
    </div>
    <?php endforeach; ?>
</div>
