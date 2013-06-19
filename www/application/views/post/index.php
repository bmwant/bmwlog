<div id="content">
    <div class="row">
        <div class="column_8">
            <?php foreach ($post as $item): ?>
            <div class="post-header">
                <a href=<?php echo '/post/'.$item['id'] ?> class="text bold color theme"><?php echo $item['title'] ?></a>
            </div>
            <small class="post-date bck light">
                    <?php echo $item['date_posted'] ?>
                </small>
                <div id="main" class="post-small-text text justify">
                    <?php echo $item['text'] ?>
                </div>
                <div id="post-delim"><br /></div>
            <?php endforeach ?>
        </div>
        <div class="column_4">
        </div>
    </div>
</div>
