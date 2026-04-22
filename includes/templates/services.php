<?php if (!empty($content['heading'])): ?>
    <div class="text-center mb-5">
        <h2 class="fw-bold"><?php echo e($content['heading']); ?></h2>
        <?php if (!empty($content['subheading'])): ?>
            <p class="text-muted"><?php echo e($content['subheading']); ?></p>
        <?php endif; ?>
    </div>
<?php endif; ?>

<div class="row g-4">
    <?php
    $items = $content['items'] ?? [];
    foreach ($items as $item):
    ?>
    <div class="col-md-4">
        <div class="card h-100 border-0 shadow-sm text-center p-4">
            <div class="card-body">
                <?php if (!empty($item['icon'])): ?>
                    <div class="mb-3 text-primary" style="font-size: 2rem;"><i class="bi <?php echo e($item['icon']); ?>"></i></div>
                <?php endif; ?>
                <h5 class="card-title fw-bold"><?php echo e($item['title'] ?? ''); ?></h5>
                <p class="card-text text-muted"><?php echo e($item['text'] ?? ''); ?></p>
            </div>
        </div>
    </div>
    <?php endforeach; ?>
</div>
