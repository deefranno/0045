<div class="row align-items-center py-5">
    <div class="col-lg-6">
        <h1 class="display-4 fw-bold mb-3"><?php echo e($content['heading'] ?? ''); ?></h1>
        <p class="lead mb-4"><?php echo e($content['subheading'] ?? ''); ?></p>
        <?php if (!empty($content['button_text'])): ?>
            <a href="<?php echo e($content['button_link'] ?? '#'); ?>" class="btn btn-primary btn-lg px-4 me-md-2"><?php echo e($content['button_text']); ?></a>
        <?php endif; ?>
    </div>
    <?php if (!empty($content['image'])): ?>
    <div class="col-lg-6">
        <img src="<?php echo e($content['image']); ?>" class="img-fluid rounded shadow-lg" alt="Hero Image" loading="lazy">
    </div>
    <?php endif; ?>
</div>
