<?php


// prevent user directly accessing this page.
if( !defined('VALID_ENTRY_POINT') ){
    exit;
}

$key = trim( $_SESSION['Username'] );

include('./include/adodb5/adodb.inc.php');

$conn = newConn('default');
$table_name = 'Users';

// check connection.
if (!$conn){
    $selected_content = t( array( 'zh-cn'=>'连接数据库失败。', 'zh-tw'=>'連接數據庫失敗。', 'en-us'=>'Unable to connect database.' ) ); 
    goto end_of_page;
}

if( is_post() ){
    $password = $_POST['Password'];
    $confirmPassword = $_POST['ConfirmPassword'];

    if( empty($password) || empty($confirmPassword) ){
        $selected_content = t(array( 'zh-cn'=>'密码和确认密码不能为空', 'zh-tw'=>'密碼和確定密碼不能為空。', 'en-us'=>'Password and confirm passowrd cannot be empty.' ));
        goto end_of_page;
    }

    if( strcasecmp( $password, $confirmPassword ) !== 0 ){
        $selected_content = t( array( 'zh-cn'=>'您输入的密码不一致，请重新输入。',     'zh-tw'=>'您輸入的密碼不一致，請重新輸入。',    'en-us'=>'Confirm password mismatch, pelease re-enter password.' ));
        goto end_of_page;
    }

    if( strlen( $password ) < 6 ){
        $selected_content = t( array( 'zh-cn'=>'密码至少含6个字母或数字。',     'zh-tw'=>'密碼至少含6個字母或數字。',    'en-us'=>'Password contains at least 6 digits or numbers.' ));
        goto end_of_page;
    }

    if( strlen( $password ) > 32 ){
        $selected_content = t( array( 'zh-cn'=>'密码太长。',     'zh-tw'=>'密碼太長。',    'en-us'=>'Password too long.' ));
        goto end_of_page;
    }

    $sql = 'update '.$table_name.' set '.
        'Password='.$conn->qstr(md5(trim($password))).
        ' where Username='.$conn->qstr( $key );
    $conn->Execute($sql);
    if ($conn->ErrorNo() != 0){ 
        $selected_content = $conn->ErrorMsg();
    }
    else{
        $selected_content = completed( array( 'zh-cn'=>'更新成功。', 'zh-tw'=>'更新成功。', 'en-us'=>'Updating Success.' ) );
    }
    goto end_of_page;
}
else{
    $rs = &$conn->Execute('select UID,Username,Password,RegTime,RegIP,LastTime,LastIP,LoginCount,IsAdmin,Amount from '. $table_name . ' where Username=' .$conn->qstr( $key ) );
    if (!$rs){ 
        $selected_content = $conn->ErrorMsg();
        goto end_of_page;
    }
}


new_begin:

$selected_content  = '<form method="post" action="'.url( implode( '/', $selector_array ) ).'">';
$selected_content .= '<table cellspacing="1" cellpadding="5" width="600" class="dg"><caption>'.t(array( 'zh-cn'=>'我的帐号',     'zh-tw'=>'我的帳號',    'en-us'=>'My Account' )).'</caption>';

/*
$selected_content .= '<tr><td width="100" class="dg-cell">UID</td><td class="dg-cell">';
$selected_content .= htmlspecialchars( $rs->fields[0] ) .'</td></tr>';
*/

$selected_content .= '<tr><td class="dg-cell">'.t( array( 'zh-cn'=>'用户名', 'zh-tw'=>'用戶名', 'en-us'=>'Username' ) ).'</td><td class="dg-cell">';
$selected_content .= htmlspecialchars( $rs->fields[1] ) .'</td></tr>';

$selected_content .= '<tr><td class="dg-cell" valign="top">'.t( array( 'zh-cn'=>'密码', 'zh-tw'=>'密碼', 'en-us'=>'Password' ) ).'</td><td class="dg-cell">';
$selected_content .= '<input name="Password" class="ledit" type="password" value="" maxlength="32"/></td></tr>';

$selected_content .= '<tr><td class="dg-cell" valign="top">'.t( array( 'zh-cn'=>'确认密码', 'zh-tw'=>'確認密碼', 'en-us'=>'Confirm Password' ) ).'</td><td class="dg-cell">';
$selected_content .= '<input name="ConfirmPassword" class="ledit" type="password" value="" maxlength="32"/></td></tr>';

$selected_content .= '<tr><td class="dg-cell">'.t( array( 'zh-cn'=>'注册时间', 'zh-tw'=>'註冊時間', 'en-us'=>'Register Time' ) ).'</td><td class="dg-cell">';
$selected_content .= htmlspecialchars( $rs->fields[3] ) .'</td></tr>';

/*
$selected_content .= '<tr><td class="dg-cell">'.t( array( 'zh-cn'=>'注册IP', 'zh-tw'=>'註冊IP', 'en-us'=>'Register IP' ) ).'</td><td class="dg-cell">';
$selected_content .= htmlspecialchars( $rs->fields[4] ).'</td></tr>';

$selected_content .= '<tr><td class="dg-cell">'.t( array( 'zh-cn'=>'最后登陆时间', 'zh-tw'=>'最後登陸時間', 'en-us'=>'Last Logon Time' ) ).'</td><td class="dg-cell">';
$selected_content .= htmlspecialchars( $rs->fields[5] ).'</td></tr>';

$selected_content .= '<tr><td class="dg-cell">'.t( array( 'zh-cn'=>'最后登陆IP', 'zh-tw'=>'最後登陸IP', 'en-us'=>'Last Logon IP' ) ).'</td><td class="dg-cell">';
$selected_content .= htmlspecialchars( $rs->fields[6] ).'</td></tr>';
*/

$selected_content .= '<tr><td class="dg-cell">'.t( array( 'zh-cn'=>'登录次数', 'zh-tw'=>'登入次數', 'en-us'=>'Logon Count' ) ).'</td><td class="dg-cell">';
$selected_content .= htmlspecialchars( $rs->fields[7] ).'</td></tr>';

$selected_content .= '<tr><td class="dg-cell">'.t( array( 'zh-cn'=>'账户余额', 'zh-tw'=>'賬戶餘額', 'en-us'=>'Amount' ) ).'</td><td class="dg-cell">';
$selected_content .= htmlspecialchars( $rs->fields[9] ) .'</td></tr>';

$selected_content .= '</table>';
$selected_content .= '<br/><div id="form_toolbar">';
$selected_content .= '<div id="form_toolbar_left"><input class="lbtn" type="submit" value="'.t( array('zh-cn'=>'更新','zh-tw'=>'更新', 'en-us'=>'Update') ) .'"/></div>';
$selected_content .= '<div id="form_toolbar_right"></div>';
$selected_content .= '</form>';

function completed( $t ){
    global $is_new, $param;
    $text  = t( $t ); 
    $text .= '<br/><br/><input type="button" value="'.t( array( 'zh-cn'=>'返回', 'zh-tw'=>'返回', 'en-us'=>'Return' ) ).'" ';
    $text .= 'onclick="document.location=\''.str_replace("'","\'",url( implode( '/', get_path_array() ). '/'. implode( '/', array_slice( $param, $is_new? 1:2 ) ) )).'\';"/>';
    return $text;
}

end_of_page:
?>