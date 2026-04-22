<div class="row">
    <div class="col-lg-6 mx-auto">
        <?php if (!empty($content['heading'])): ?>
            <h2 class="fw-bold mb-4"><?php echo e($content['heading']); ?></h2>
        <?php endif; ?>
        <?php if (!empty($content['text'])): ?>
            <p class="mb-4"><?php echo e($content['text']); ?></p>
        <?php endif; ?>

        <?php
        $form_url = get_setting('formspree_url');
        if ($form_url):
        ?>
        <form action="<?php echo e($form_url); ?>" method="POST">
            <div class="mb-3">
                <label class="form-label">Full Name</label>
                <input type="text" name="name" class="form-control" required>
            </div>
            <div class="mb-3">
                <label class="form-label">Email Address</label>
                <input type="email" name="_replyto" class="form-control" required>
            </div>
            <div class="mb-3">
                <label class="form-label">Message</label>
                <textarea name="message" class="form-control" rows="5" required></textarea>
            </div>
            <!-- Honeypot -->
            <input type="text" name="_gotcha" style="display:none">
            <button type="submit" class="btn btn-primary px-5 py-2 w-100">Send Message</button>
        </form>
        <?php else: ?>
            <div class="alert alert-info">Please set a Formspree Endpoint URL in the admin settings to enable this form.</div>
        <?php endif; ?>
    </div>
</div>
