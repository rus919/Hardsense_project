<?php


// prevent user directly accessing this page.
if( !defined('VALID_ENTRY_POINT') ){
    exit;
}

$is_new = false;
$is_del = false;
$key = '';

if( count( $param ) == 0 ){
missing:
    $selected_content = t( array( 'zh-cn'=>'缺失参数。', 'zh-tw'=>'缺失參數。', 'en-us'=>'Missing parameters.' ) ); 
    goto end_of_page;
}
else{
    switch( strtolower( $param[0] ) ){
        case 'add':
            $is_new = true;
            if( !is_post() ){
                goto new_begin;
            }
            break;
        case 'delete':
            if( count( $param ) == 1 ){
                goto missing;
            }
            $is_del = true;
            $key = (int)$param[1];
            break;
        case 'edit':
            if( count( $param ) == 1 ){
                goto missing;
            }
            $key = (int)$param[1];
            break;
    }
}

include('../include/adodb5/adodb.inc.php');

$conn = newConn('default');

$table_name = 'Users';

// check connection.
if (!$conn){
    $selected_content = t( array( 'zh-cn'=>'连接数据库失败。', 'zh-tw'=>'連接數據庫失敗。', 'en-us'=>'Unable to connect database.' ) ); 
    goto end_of_page;
}

if( $is_new ){
    if( empty($_POST['Username']) || empty($_POST['Password']) ){
        $selected_content = t(array( 'zh-cn'=>'Username, Password 不能为空', 'zh-tw'=>'Username, Password 不能為空。', 'en-us'=>'Username, Password cannot be empty.' ));
        goto end_of_page;
    }
    $sql='insert into '.$table_name.' (Username,Password,RegTime,RegIP,LastTime,LastIP,LoginCount,IsAdmin,Amount) values ('.
        $conn->qstr(trim($_POST['Username'])).",".
        $conn->qstr(md5(trim($_POST['Password']))).",".
        $conn->sysTimeStamp.",".
        $conn->qstr($_SERVER['REMOTE_ADDR']).",".
        $conn->sysTimeStamp.",".
        $conn->qstr($_SERVER['REMOTE_ADDR']).",".
        '0,'.
        (isset($_POST['IsAdmin'])?'1':'0').','.
        (int)($_POST['Amount']).
        ')';

    $conn->Execute($sql);
    if ($conn->ErrorNo() != 0){ 
        $selected_content = $conn->ErrorMsg();
    }
    else{
        $selected_content = completed( array( 'zh-cn'=>'添加成功。', 'zh-tw'=>'添加成功。', 'en-us'=>'Adding Success.' ) );
    }
    goto end_of_page;
}

if( $is_del ){
    $conn->Execute('delete from '.$table_name.' where UID='. $key );
    if ($conn->ErrorNo() != 0){ 
        $selected_content = $conn->ErrorMsg();
    }
    else{
        $selected_content = completed( array( 'zh-cn'=>'删除成功。', 'zh-tw'=>'刪除成功。', 'en-us'=>'Deleting Success.' ) );
    }
    goto end_of_page;
}
else{
    if( is_post() ){
        $sql = 'update '.$table_name.' set '.
            (empty($_POST['Password'])?'':'Password='.$conn->qstr(md5(trim($_POST['Password']))).',').
            'IsAdmin='. (isset($_POST['IsAdmin'])?'1':'0').','.
            'Amount='.(int)($_POST['Amount']).
            ' where UID='.$key;
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
        $rs = &$conn->Execute('select UID,Username,Password,RegTime,RegIP,LastTime,LastIP,LoginCount,IsAdmin,Amount from '. $table_name . ' where UId=' .$key);
        if (!$rs){ 
            $selected_content = $conn->ErrorMsg();
            goto end_of_page;
        }
    }
}


new_begin:

$selected_content  = '<form method="post" action="'.url( implode( '/', $selector_array ) ).'">';
$selected_content .= '<table cellspacing="1" cellpadding="5" width="600" class="dg">';

$selected_content .= '<tr><td width="100" class="dg-cell">ID</td><td class="dg-cell">';
$selected_content .= ($is_new? '' : htmlspecialchars( $rs->fields[0] ) ).'</td></tr>';

$selected_content .= '<tr><td class="dg-cell">'.t( array( 'zh-cn'=>'用户名', 'zh-tw'=>'用戶名', 'en-us'=>'Username' ) ).'</td><td class="dg-cell">';
$selected_content .= ($is_new? '<input name="Username" class="ledit" type="text" value="" maxlength="64"/>':htmlspecialchars( $rs->fields[1] ) ).'</td></tr>';

$selected_content .= '<tr><td class="dg-cell" valign="top">'.t( array( 'zh-cn'=>'用户密码', 'zh-tw'=>'用戶密碼', 'en-us'=>'Password' ) ).'</td><td class="dg-cell">';
$selected_content .= '<input name="Password" class="ledit" type="text" value="" maxlength="32"/>'.($is_new?'':'<br/>'.t( array( 'zh-cn'=>'留空则原密码不变，否则修改密码。', 'zh-tw'=>'留空則原密碼不變，否則修改密碼。', 'en-us'=>'Leave blank to keep old password, otherwise change to new password.' ) )).'</td></tr>';

$selected_content .= '<tr><td class="dg-cell">'.t( array( 'zh-cn'=>'注册时间', 'zh-tw'=>'註冊時間', 'en-us'=>'Register Time' ) ).'</td><td class="dg-cell">';
$selected_content .= ($is_new? '' : htmlspecialchars( $rs->fields[3] ) ).'</td></tr>';

$selected_content .= '<tr><td class="dg-cell">'.t( array( 'zh-cn'=>'注册IP', 'zh-tw'=>'註冊IP', 'en-us'=>'Register IP' ) ).'</td><td class="dg-cell">';
$selected_content .= ($is_new? '' : htmlspecialchars( $rs->fields[4] ) ).'</td></tr>';

$selected_content .= '<tr><td class="dg-cell">'.t( array( 'zh-cn'=>'最后登陆时间', 'zh-tw'=>'最後登陸時間', 'en-us'=>'Last Logon Time' ) ).'</td><td class="dg-cell">';
$selected_content .= ($is_new? '' : htmlspecialchars( $rs->fields[5] ) ).'</td></tr>';

$selected_content .= '<tr><td class="dg-cell">'.t( array( 'zh-cn'=>'最后登陆IP', 'zh-tw'=>'最後登陸IP', 'en-us'=>'Last Logon IP' ) ).'</td><td class="dg-cell">';
$selected_content .= ($is_new? '' : htmlspecialchars( $rs->fields[6] ) ).'</td></tr>';

$selected_content .= '<tr><td class="dg-cell">'.t( array( 'zh-cn'=>'登陆次数', 'zh-tw'=>'登入次數', 'en-us'=>'Logon Count' ) ).'</td><td class="dg-cell">';
$selected_content .= ($is_new? '' : htmlspecialchars( $rs->fields[7] ) ).'</td></tr>';

$selected_content .= '<tr><td class="dg-cell">'.t( array( 'zh-cn'=>'管理员', 'zh-tw'=>'管理員', 'en-us'=>'Is Admin' ) ).'</td><td class="dg-cell">';
$selected_content .= '<input name="IsAdmin" type="checkbox" '.     ($is_new?'':( ((int)$rs->fields[8])>0? 'checked="checked"':'') ).'/></td></tr>';

$selected_content .= '<tr><td class="dg-cell">'.t( array( 'zh-cn'=>'账户余额', 'zh-tw'=>'賬戶餘額', 'en-us'=>'Amount' ) ).'</td><td class="dg-cell">';
$selected_content .= '<input name="Amount" class="ledit" type="text" value="'.  ($is_new?'0': htmlspecialchars( $rs->fields[9] ) ).'" maxlength="10"/></td></tr>';

$selected_content .= '</table>';
$selected_content .= '<br/><div id="form_toolbar">';
$selected_content .= '<div id="form_toolbar_left"><input class="lbtn" type="submit" value="'.t( $is_new? array('zh-cn'=>'添加','zh-tw'=>'添加', 'en-us'=>'Add') : array('zh-cn'=>'更新','zh-tw'=>'更新', 'en-us'=>'Update') ) .'"/></div>';
$selected_content .= '<div id="form_toolbar_right"><input class="lbtn" type="button" '.($is_new?'disabled="disabled"':'').' value="'.t( array('zh-cn'=>'新建','zh-tw'=>'新建', 'en-us'=>'New') ) .'" ';
$selected_content .= 'onclick="document.location=\''.str_replace("'","\'",url( implode( '/', get_path_array() ). '/add/'. implode( '/', array_slice( $param, 2 ) ) )).'\';"/>';
$selected_content .= '<input class="lbtn" type="button" '.($is_new?'disabled="disabled"':'').' value="'.t( array('zh-cn'=>'删除','zh-tw'=>'刪除', 'en-us'=>'Delete') ) .'" ';
$selected_content .= 'onclick="document.location=\''.str_replace("'","\'",url( implode( '/', get_path_array() ). '/delete/'. implode( '/', array_slice( $param, 1) ) )).'\';"/></div><div id="edit-return"><a href="'.url( implode( '/', get_path_array() ). '/'. implode( '/', array_slice( $param, $is_new? 1:2 ) ) ).'">'.t( array( 'zh-cn'=>'返回', 'zh-tw'=>'返回', 'en-us'=>'Return' ) ).'</a></div>';
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