<div id="content">
    <div class="row">
        <div class="column_8">
            
            <table class="margin-top">
                    <thead>
                        <tr>
                            <th>E-mail</th>
                            <th>First name</th>
                            <th>Last name</th>
                            <th>Nickname</th>
                        </tr>
                    </thead>
                    <tbody>
                        <?php foreach ($user as $item): ?>
                        <tr>
                            <td><?php echo $item['email'] ?></td>
                            <td><?php echo $item['first_name'] ?></td>
                            <td><?php echo $item['last_name'] ?></td>
                            <td><?php echo $item['nickname'] ?></td>
                        </tr>
                        <?php endforeach ?>
                    </tbody>
                </table>
            
        </div>
        <div class="column_4">
        </div>
    </div>
</div>
