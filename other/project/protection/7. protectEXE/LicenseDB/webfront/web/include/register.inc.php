<?php
// prevent user directly accessing this page.
if( !defined('VALID_ENTRY_POINT') ){
    exit;
}

session_unset();

if( is_post() ){

    include('include/adodb5/adodb.inc.php');

    $conf = 'default';
    $conn = newConn($conf);
    $lock_type = 1;

    $table_name = 'Users';

    // check connection.
    if (!$conn){
        $selected_content = t( array( 'zh-cn'=>'连接数据库失败。', 'zh-tw'=>'連接數據庫失敗。', 'en-us'=>'Unable to connect database.' ) ); 
        goto end_of_page;
    }

    if( !isset( $_POST['Username'] ) || !isset( $_POST['Password'] ) || !isset( $_POST['ConfirmPassword'] ) ){
        $selected_content = t( array( 'zh-cn'=>'用户名或密码不能为空。',     'zh-tw'=>'用戶名或密碼不能為空。',    'en-us'=>'Username or Password cannot be empty.' ));
        goto end_of_page;
    }

    $username = trim( $_POST['Username'] );
    $password = trim( $_POST['Password'] );
    $confirmPassword = trim ( $_POST['ConfirmPassword'] );

    if( empty( $username ) || empty( $password ) || empty( $confirmPassword ) ){
        $selected_content = t( array( 'zh-cn'=>'用户名或密码不能为空。',     'zh-tw'=>'用戶名或密碼不能為空。',    'en-us'=>'Username or Password cannot be empty.' ));
        goto end_of_page;
    }

    if( strcasecmp( $password, $confirmPassword ) !== 0 ){
        $selected_content = t( array( 'zh-cn'=>'您输入的密码不一致，请重新输入。',     'zh-tw'=>'您輸入的密碼不一致，請重新輸入。',    'en-us'=>'Confirm password mismatch, pelease re-enter password.' ));
        goto end_of_page;
    }

    if( strlen( $username ) < 6 || strlen( $password ) < 6 ){
        $selected_content = t( array( 'zh-cn'=>'用户名或密码至少含6个字母或数字。',     'zh-tw'=>'用戶名或密碼至少含6個字母或數字。',    'en-us'=>'Username or Password contains at least 6 digits or numbers.' ));
        goto end_of_page;
    }

    if( strlen( $username ) > 64 || strlen( $password ) > 32 ){
        $selected_content = t( array( 'zh-cn'=>'用户名或密码太长。',     'zh-tw'=>'用戶名或密碼太長。',    'en-us'=>'Username or Password too long.' ));
        goto end_of_page;
    }

    if( !validate_username( $username ) ){
        $selected_content = t( array( 'zh-cn'=>'用户名必须是字母，数字或电子邮件地址。',     'zh-tw'=>'用戶名必須是字母，數字或電子郵件地址。',    'en-us'=>'Username must be letters, digits or e-mail address.' ));
        goto end_of_page;
    }

    if( $register_interval > 0 && check_ip_lock( $conf, $lock_type, 1 ) ){
        $selected_content = t( array( 'zh-cn'=>'禁止短时间内多次申请账号。',     'zh-tw'=>'禁止短時間內多次申請帳號。',    'en-us'=>'Refuse to register new user in a short time.' ));
        goto end_of_page;
    }

    $sql = 'select count(*) from '.$table_name.' where Username='.$conn->qstr( $username ) ;

    $rs = $conn->GetOne( $sql );

    if( $rs > 0 ){
        $selected_content = t( array( 'zh-cn'=>'该用户名已经被使用。',     'zh-tw'=>'該用戶名已經被使用。',    'en-us'=>'Username is being used by other users.' ));
        goto end_of_page;
    }

    $sql = 'Insert into '.$table_name.' (Username,Password,RegTime,RegIP,LastTime,LastIP,LoginCount,IsAdmin,Amount) values ('.
           $conn->qstr( $username ) .','.
           $conn->qstr( md5( $password ) ) .','.
           $conn->sysTimeStamp.','.
           $conn->qstr( get_real_ip() ).','.
           $conn->sysTimeStamp.','.
           $conn->qstr( get_real_ip() ).','.
           '1,'.
           '0,'.
           '0'.
           ')';

    $rs = $conn->Execute($sql);
    if ($conn->ErrorNo() != 0){ 
        $selected_content = $conn->ErrorMsg();
    }
    else{
        $_SESSION['Username']   = $username;
        $_SESSION['IsAdmin']    = false;
        $_SESSION['LoginCount'] = 1;

        $selected_content = completed( array( 'zh-cn'=>'注册成功。', 'zh-tw'=>'註冊成功。', 'en-us'=>'Register Success.' ) );

        if( $register_interval > 0 ){
            lock_ip( $conf, $lock_type, $register_interval );
        }
    }
}
else{
    ob_start();
?>
<form method="post" action="<?php echo url('/register');?>">
<table cellspacing="0" cellpadding="5" border="0">
<tr><td colspan="2" align="center"><?php echo t(array('zh-cn'=>'创建新账号','zh-tw'=>'創建新帳號','en-us'=>'Create New Account'));?></td></tr>
<tr><td><?php echo t(array('zh-cn'=>'用户名','zh-tw'=>'用戶名','en-us'=>'Username'));?></td><td><input name="Username" type="text" value="" maxlength="64"/></td></tr>
<tr><td><?php echo t(array('zh-cn'=>'密码','zh-tw'=>'用戶名','en-us'=>'Password'));?></td><td><input name="Password" type="password" value="" maxlength="32"/></td></tr>
<tr><td><?php echo t(array('zh-cn'=>'确认密码','zh-tw'=>'確認密碼','en-us'=>'Confirm password'));?></td><td><input name="ConfirmPassword" type="password" value="" maxlength="32"/></td></tr>
<tr><td colspan="2"><input type="submit" value="<?php echo t(array('zh-cn'=>'立即注册','zh-tw'=>'立即註冊','en-us'=>'Register'));?>"/></td></tr>
</table>
</form>
<?php
    $selected_content = ob_get_contents();
    ob_clean();
}

function completed( $t ){
    global $is_new, $param;
    $text  = t( $t ); 
    $text .= '<br/><br/><input type="button" value="'.t( array( 'zh-cn'=>'进入主页', 'zh-tw'=>'進入主頁', 'en-us'=>'Goto homepage' ) ).'" ';
    $text .= 'onclick="document.location=\''.url('/').'\';"/>';
    return $text;
}

end_of_page:
?>