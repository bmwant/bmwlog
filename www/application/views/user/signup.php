<div id="content">
    <div class="row">
        <div class="column_6">
            <?php echo form_open('user/signup') ?>
            <label for="email">E-mail</label> 
            <input type="text" name="email" /><br />

            <label for="password">Password</label> 
            <input type="password" name="password" /><br />

            <label for="fname">First name</label> 
            <input type="text" name="fname" /><br />

            <label for="lname">Last name</label> 
            <input type="text" name="lname" /><br />

            <label for="nickname">Nickname</label> 
            <input type="text" name="nickname" /><br />
            
            <div class="margin-bottom margin-top">
                <a class="button success small icon ok" onclick="$(this).closest('form').submit();">Register me</a>
            </div>
        </div>
        </form>

        <div class="column_6 margin-bottom padding">
            <h1 class="text book center color theme">Register account</h1>
            <div class="error text color dark">
                <?php echo validation_errors(); ?>
            </div>
        </div>
        
    </div>
</div>