<?php if (!empty($content['heading'])): ?>
    <div class="text-center mb-5">
        <h2 class="fw-bold"><?php echo e($content['heading']); ?></h2>
    </div>
<?php endif; ?>

<div class="accordion" id="accordion-<?php echo $section['id']; ?>">
    <?php
    $items = $content['items'] ?? [];
    foreach ($items as $index => $item):
    ?>
    <div class="accordion-item">
        <h2 class="accordion-header">
            <button class="accordion-button <?php echo $index === 0 ? '' : 'collapsed'; ?>" type="button" data-bs-toggle="collapse" data-bs-target="#collapse-<?php echo $section['id'] . '-' . $index; ?>">
                <?php echo e($item['title'] ?? ''); ?>
            </button>
        </h2>
        <div id="collapse-<?php echo $section['id'] . '-' . $index; ?>" class="accordion-collapse collapse <?php echo $index === 0 ? 'show' : ''; ?>" data-bs-parent="#accordion-<?php echo $section['id']; ?>">
            <div class="accordion-body">
                <?php echo nl2br(e($item['text'] ?? '')); ?>
            </div>
        </div>
    </div>
    <?php endforeach; ?>
</div>
