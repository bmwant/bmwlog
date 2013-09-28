<div id="content">
    <div class="row">
        <div class="column_6">

            <?php echo validation_errors(); ?>

            <?php echo form_open('post/add') ?>
            <script type="text/javascript" src="http://js.nicedit.com/nicEdit-latest.js"></script> <script type="text/javascript">
                //<![CDATA[
                bkLib.onDomLoaded(function() {
                    new nicEditor().panelInstance('text1');
                });
                //]]>
            </script>
            <script>
	$(function() {
		
		$( "#datepicker" ).datepicker();
	});
	</script>
            <label for="title">Title</label> 
            <input type="text" name="title" /><br />

            <label for="datepick">Date posted</label> 
            
            <input type="text" id="datepicker" class="hastDatapicker" /><br />
            
            <label for="text">Text</label>
            <textarea id="text1" name="text"></textarea><br />

            <div class="margin-bottom">
                <a href="#" class="button success small icon ok" onclick="if(nicEditors.findEditor('text1').getContent()!='<br>'){nicEditors.findEditor('text1').saveContent();}$(this).closest('form').submit();">Add</a>
            </div>
        </div>
        </form>

        <div class="column_6 text center thin italic color theme">
            <h1>Add new post</h1>
        </div>

    </div>
</div>