<div class="row align-items-center">
    <div class="col-lg-8 mx-auto text-center">
        <?php if (!empty($content['heading'])): ?>
            <h2 class="fw-bold mb-4"><?php echo e($content['heading']); ?></h2>
        <?php endif; ?>
        <?php if (!empty($content['text'])): ?>
            <p class="lead mb-4"><?php echo e($content['text']); ?></p>
        <?php endif; ?>

        <?php if (!empty($content['button_link'])): ?>
            <div class="position-relative d-inline-block">
                <img src="<?php echo e($content['image'] ?: 'https://via.placeholder.com/800x450'); ?>" class="img-fluid rounded shadow" alt="Video Thumbnail">
                <a href="<?php echo e($content['button_link']); ?>" class="btn btn-primary rounded-circle position-absolute top-50 start-50 translate-middle" style="width: 80px; height: 80px; display: flex; align-items: center; justify-content: center;" data-bs-toggle="modal" data-bs-target="#videoModal-<?php echo $section['id']; ?>">
                    <i class="bi bi-play-fill fs-1"></i>
                </a>
            </div>

            <!-- Modal -->
            <div class="modal fade" id="videoModal-<?php echo $section['id']; ?>" tabindex="-1" aria-hidden="true">
                <div class="modal-dialog modal-lg modal-dialog-centered">
                    <div class="modal-content bg-black border-0">
                        <div class="modal-body p-0">
                            <div class="ratio ratio-16x9">
                                <?php
                                $video_url = $content['button_link'];
                                if (strpos($video_url, 'youtube.com') !== false || strpos($video_url, 'youtu.be') !== false) {
                                    $id = '';
                                    if (preg_match('%(?:youtube(?:-nocookie)?\.com/(?:[^/]+/.+/|(?:v|e(?:mbed)?)/|.*[?&]v=)|youtu\.be/)([^"&?/ ]{11})%i', $video_url, $match)) {
                                        $id = $match[1];
                                    }
                                    echo '<iframe src="https://www.youtube.com/embed/' . $id . '" allowfullscreen></iframe>';
                                } elseif (strpos($video_url, 'vimeo.com') !== false) {
                                    $id = (int) substr(parse_url($video_url, PHP_URL_PATH), 1);
                                    echo '<iframe src="https://player.vimeo.com/video/' . $id . '" allowfullscreen></iframe>';
                                }
                                ?>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        <?php endif; ?>
    </div>
</div>
