<?php
echo '<h2>'.$item['title'].'</h2>';
echo $item['text'];
echo '<br>';
foreach($tags as $tag)
    echo $tag.' ';