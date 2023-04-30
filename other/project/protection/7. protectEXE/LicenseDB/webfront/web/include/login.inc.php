<?php
// prevent user directly accessing this page.
if( !defined('VALID_ENTRY_POINT') ){
    exit;
}

include('include/adodb5/adodb.inc.php');

$conf = 'default';
$conn = newConn($conf);
$lock_type = 2;

$table_name = 'products';

// check connection.
if (!$conn){
    $selected_content = t( array( 'zh-cn'=>'连接数据库失败。', 'zh-tw'=>'連接數據庫失敗。', 'en-us'=>'Unable to connect database.' ) ); 
    goto end_of_page;
}

if( is_post() && !isset( $_SESSION['Username'] ) ){
    if( !isset( $_POST['Username'] ) || !isset( $_POST['Password'] ) ){
        $selected_content = t( array( 'zh-cn'=>'用户名或密码不能为空。',     'zh-tw'=>'用戶名或密碼不能為空。',    'en-us'=>'Username or Password cannot be empty.' ));
        goto end_of_page;
    }

    $username = trim( $_POST['Username'] );
    $password = trim( $_POST['Password'] );

    if( empty( $username ) || empty( $password ) ){
        $selected_content = t( array( 'zh-cn'=>'用户名或密码不能为空。',     'zh-tw'=>'用戶名或密碼不能為空。',    'en-us'=>'Username or Password cannot be empty.' ));
        goto end_of_page;
    }
    if( strlen( $username ) > 64 || strlen( $password ) >32 ){
        $selected_content = t( array( 'zh-cn'=>'用户名或密码无效。',     'zh-tw'=>'用戶名或密碼無效。',    'en-us'=>'Invalid Username or Password.' ));
        goto end_of_page;
    }

    if( !validate_username( $username ) ){
        $selected_content = t( array( 'zh-cn'=>'用户名必须是字母，数字或电子邮件地址。',     'zh-tw'=>'用戶名必須是字母，數字或電子郵件地址。',    'en-us'=>'Username must be letters, digits or e-mail address.' ));
        goto end_of_page;
    }

    if( $max_login_count > 0 && check_ip_lock( $conf, $lock_type, $max_login_count ) ){
        $selected_content = t( array( 'zh-cn'=>'多次登录错误，暂时禁止登录，请稍候再试。',     'zh-tw'=>'多次登錄錯誤，暫時禁止登錄，請稍候再試。',    'en-us'=>'Failed to login many times, refuse to login, please try later.' ));
        goto end_of_page;
    }

    $rs = $conn->Execute('select Username,LoginCount,IsAdmin from Users where Username='.$conn->qstr($username) .' and Password='.$conn->qstr(md5($password)) );
    if( !$rs || $rs->RecordCount() != 1 ){
        $selected_content = t( array( 'zh-cn'=>'登录错误！用户名或密码错误。',     'zh-tw'=>'登錄錯誤！用戶名或密碼錯誤。',    'en-us'=>'Login error! invalid username or password.' ));
        if( $max_login_count > 0 ){
            lock_ip( $conf, $lock_type, $login_interval );
        }
        goto end_of_page;
    }
    else{
        $_SESSION['Username']   = $rs->fields[0];
        $_SESSION['IsAdmin']    = (bool)$rs->fields[2];

        $cnt = (int)$rs->fields[1];
        $cnt ++ ;
        $rs->Close();

        $_SESSION['LoginCount'] = $cnt;

        $conn->Execute('UPDATE users SET LastIP='.$conn->qstr(get_real_ip()).', LoginCount='.$cnt. ' where Username='.$conn->qstr($username));
        $conn->Close();

    }
}
header('Location: '.url('/'));
exit;

end_of_page:
?>