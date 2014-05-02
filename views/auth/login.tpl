<div class="large-20 space push-center" style="min-width: 25em">
    <form class="ink-form " action="login" method="post">
        <fieldset>
            <div class="control-group column-group required validation gutters {{ 'error' if denied_msg else '' }}">
                <label class="large-40 content-left" for="username">Username:</label> 
                <div class="control large-60">
                    <input type="text" name="username">
                </div>
            </div>
            <div class="control-group column-group required validation gutters {{ 'error' if denied_msg else '' }}">
                <label class="large-40 content-left" for="password">Password:</label> 
                <div class="control large-60">
                    <input type="password" name="password">
                </div>
                <p class="tip large-100" style="text-align: center">{{ denied_msg }}</p>
            </div>
    
            <div class="column-group gutters" style="text-align: center">
                <button type="submit" class="ink-button green">Sign in</button>
            </div>
        </fieldset>
    </form>
</div>
%rebase layout title="Login"
