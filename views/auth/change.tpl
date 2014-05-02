<form class="form-horizontal" action="/auth/update" method="post">
  <div class="control-group">
    <label class="control-label" for="inputPassword">New Password</label>
    <div class="controls">
      <input type="password" name="password" id="inputPassword" placeholder="Password">
      <input type="hidden" name="reset_code" value="{{reset_code}}" />
    </div>
  </div>
  <div class="control-group">
    <div class="controls">
      <button type="submit" class="btn">Update</button>
    </div>
  </div>
</form>
%rebase layout title="Change password"
