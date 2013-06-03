<div id="content">
    <div class="row">
        <div class="column_8">
            <?php foreach ($post as $item): ?>
                <h2><a href=<?php echo '/post/'.$item['id'] ?> class="text bold color theme"><?php echo $item['title'] ?></a></h2>
                <small class="bck light">August 12, 2013</small>
                <div id="main" class="text justify">
                    <?php echo $item['text'] ?>
                </div>
                <div id="delim">
                    <br /></div>
            <?php endforeach ?>
        </div>
        <div class="column_4">
        </div>
    </div>
</div>
