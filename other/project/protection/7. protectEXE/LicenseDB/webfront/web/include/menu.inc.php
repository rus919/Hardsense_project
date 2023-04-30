<?php

// prevent user directly accessing this page.
if( !defined('VALID_ENTRY_POINT') ){
    exit;
}

?>
<dl class="menu">
<dt><?php echo t( array( 'zh-cn'=>'产品首页', 'zh-tw'=>'產品首頁', 'en-us'=>'Home' ) );?></dt>
<dd>
    <ul>
        <li><a href="<?php echo url('/');/* url('/browse-products'); */ ?>"><?php echo t( array( 'zh-cn'=>'浏览产品',     'zh-tw'=>'瀏覽產品',    'en-us'=>'Browse Products' ) );?></a></li>
    </ul>
</dd>
<?php
if( !( count( $selector_array ) > 0 && strcasecmp( $selector_array[0], 'register' ) === 0 ) ){
    if( !isset( $_SESSION['Username'] ) ){
?>
<dt><?php echo t( array( 'zh-cn'=>'请先登陆', 'zh-tw'=>'請先登陸', 'en-us'=>'Please Login' ));?></dt>
<dd>
<div id="login_box"><form method="post" action="<?php echo url('/login');?>">
<?php echo t( array( 'zh-cn'=>'用户名', 'zh-tw'=>'用戶名', 'en-us'=>'Username' ));?><br/>
    <input name="Username" type="text" value="" maxlength="64" class="loginipt"/><br/>
    <?php echo t( array( 'zh-cn'=>'密码', 'zh-tw'=>'密碼', 'en-us'=>'Password' ));?><br/>
    <input name="Password" type="password" value="" maxlength="32" class="loginipt"/><br/>
    <input name="Submit" type="submit" value="<?php echo t( array( 'zh-cn'=>'登陆', 'zh-tw'=>'登陸', 'en-us'=>'Login' ));?>" class="loginbtn"/><br/>
    <a href="<?php echo url('/register');?>"><?php echo t( array( 'zh-cn'=>'注册新用户', 'zh-tw'=>'註冊新用戶', 'en-us'=>'Create new account' ));?></a><br/>
</form></div>
</dd>
<?php
    }
    else{
?>
<dt><?php echo t( array( 'zh-cn'=>'会员中心', 'zh-tw'=>'會員中心', 'en-us'=>'Member Center' ) );?></dt>
<dd>
    <div id="login_box"><?php
    
echo htmlspecialchars( $_SESSION['Username'] );

?></div>
    <ul>
<?php 
    if( isset( $_SESSION['IsAdmin'] ) && $_SESSION['IsAdmin'] ){
?>        <li><a href="<?php echo admin_url('/'); ?>"><?php echo t( array( 'zh-cn'=>'切换后台',     'zh-tw'=>'切換後台',    'en-us'=>'Administration' ) );?></a></li>
<?php
    }
?>
        <li><a href="<?php echo url('members/my-account'); ?>"><?php echo t( array( 'zh-cn'=>'我的帐号',     'zh-tw'=>'我的帳號',    'en-us'=>'My Account' ) );?></a></li>
        <li><a href="<?php echo url('members/cart'); ?>"><?php echo t( array( 'zh-cn'=>'我的购物车', 'zh-tw'=>'我的購物車', 'en-us'=>'Shopping Cart' ) );?></a></li>
        <li><a href="<?php echo url('members/charge-now'); ?>"><?php echo t( array( 'zh-cn'=>'充值中心', 'zh-tw'=>'充值中心', 'en-us'=>'Charging Center' ) );?></a></li>
        <li><a href="<?php echo url('/logout');?>"><?php echo t( array( 'zh-cn'=>'退出登录',     'zh-tw'=>'退出登錄',    'en-us'=>'Logout' ) );?></a></li>
    </ul>
</dd>
<?php
    }
}
?>
</dl>
