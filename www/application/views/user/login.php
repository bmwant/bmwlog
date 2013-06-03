<div id="content">
    <div class="row">
        <div class="column_6">
            
            <?php echo form_open('user/login') ?>

            <label for="email">E-mail</label> 
            <input type="text" name="email" /><br />
            
            <label for="password">Password</label> 
            <input type="password" name="password" /><br />
                <!--
                <fieldset>
                    <label>Remember me</label>
                    <div data-control="checkbox">
                        <input type="checkbox" value="None" id="prueba" />
                        <label for="prueba"></label>
                    </div>
                </fieldset>
                -->
            <div class="margin-bottom margin-top">
                <a class="center button large icon ok" onclick="$(this).closest('form').submit();"></a>
            </div>
            </form>
        </div>
        <div class="column_6 margin-bottom padding">
            <h1 class="text book center color theme">Login</h1>
            <div class="error text color dark">
                <?php echo validation_errors(); ?>
            </div>
        </div>
    </div>
</div>