<div id="content">
    <div class="row">
        <div class="column_8">
            <?php foreach ($post as $item): ?>

                <h2><?php echo $item['title'] ?></h2>
                <div id="main">
                    <?php echo $item['text'] ?>
                </div>

            <?php endforeach ?>
        </div>
        <div class="column_4">
        </div>
    </div>
</div>
