<?php if (!empty($content['heading'])): ?>
    <div class="text-center mb-5">
        <h2 class="fw-bold"><?php echo e($content['heading']); ?></h2>
    </div>
<?php endif; ?>

<div class="row g-4">
    <?php
    $items = $content['items'] ?? [];
    foreach ($items as $item):
    ?>
    <div class="col-md-6 col-lg-4">
        <div class="card h-100 border-0 shadow-sm p-4">
            <div class="card-body">
                <p class="card-text fs-5 italic">"<?php echo e($item['text'] ?? ''); ?>"</p>
                <div class="d-flex align-items-center mt-3">
                    <?php if (!empty($item['image'])): ?>
                        <img src="<?php echo e($item['image']); ?>" class="rounded-circle me-3" style="width: 50px; height: 50px; object-fit: cover;">
                    <?php endif; ?>
                    <div>
                        <h6 class="mb-0 fw-bold"><?php echo e($item['title'] ?? ''); ?></h6>
                        <small class="text-muted"><?php echo e($item['price'] ?? ''); // Using price field for role/company ?></small>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <?php endforeach; ?>
</div>
