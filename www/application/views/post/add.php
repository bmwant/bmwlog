<div class="content">
<h2>Add new post</h2>
<div class="column_4 center">
<?php echo validation_errors(); ?>

<?php echo form_open('post/add') ?>

	<label for="title">Title</label> 
	<input type="text" name="title" /><br />

	<label for="text">Text</label>
	<textarea name="text"></textarea><br />
        <div class="margin-top">
            <a href="#" class="button success small icon ok" onclick="$(this).closest('form').submit()">Add</a>
        </div>
</div>
</form>
</div>
