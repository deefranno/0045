<div class="row align-items-center">
    <?php if (!empty($content['image'])): ?>
    <div class="col-lg-6 mb-4 mb-lg-0">
        <img src="<?php echo e($content['image']); ?>" class="img-fluid rounded shadow" alt="About Image" loading="lazy">
    </div>
    <?php endif; ?>
    <div class="<?php echo !empty($content['image']) ? 'col-lg-6' : 'col-12'; ?>">
        <h2 class="fw-bold mb-3"><?php echo e($content['heading'] ?? ''); ?></h2>
        <div class="content-text"><?php echo nl2br(e($content['text'] ?? '')); ?></div>
    </div>
</div>
