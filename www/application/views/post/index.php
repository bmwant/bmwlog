<?php foreach ($post as $item): ?>

    <h2><?php echo $item['title'] ?></h2>
    <div id="main">
        <?php echo $item['text'] ?>
    </div>

<?php endforeach ?>
