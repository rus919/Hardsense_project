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

$table_name = 'Cards';

// check connection.
if (!$conn){
    $selected_content = t( array( 'zh-cn'=>'连接数据库失败。', 'zh-tw'=>'連接數據庫失敗。', 'en-us'=>'Unable to connect database.' ) ); 
    goto end_of_page;
}

if( $is_new ){
    if( empty($_POST['CardNumber']) || empty($_POST['Password']) || empty($_POST['Amount']) ){
        $selected_content = t(array( 'zh-cn'=>'CardNumber, Password, Amount 不能为空', 'zh-tw'=>'CardNumber, Password, Amount 不能為空。', 'en-us'=>'CardNumber, Password, Amount  cannot be empty.' ));
        goto end_of_page;
    }
    $sql='insert into '.$table_name.' (CardNumber,Password,Amount,GeneratedTime,UsedTime,Discard) values ('.
        $conn->qstr($_POST['CardNumber']).",".
        $conn->qstr($_POST['Password']).",".
        (int)$_POST['Amount'].",".
        $conn->sysTimeStamp.",".
        'null,'.
        (isset($_POST['Discard'])?'1':'0').
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
    $conn->Execute('delete from '.$table_name.' where CardId='. $key );
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
            'CardNumber='.$conn->qstr($_POST['CardNumber']).','.
            'Password='.$conn->qstr($_POST['Password']).','.
            'Amount='.(int)($_POST['Amount']).','.
            'Discard='. (isset($_POST['Discard'])?'1':'0').
            ' where CardId='.$key;
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
        $rs = &$conn->Execute('select CardId,CardNumber,Password,Amount,GeneratedTime,UsedTime,Discard from '. $table_name . ' where CardId=' .$key);
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

$selected_content .= '<tr><td class="dg-cell">'.t( array( 'zh-cn'=>'卡号', 'zh-tw'=>'卡號', 'en-us'=>'Card Number' ) ).'</td><td class="dg-cell">';
$selected_content .= '<input name="CardNumber" class="ledit" type="text" value="'.  ($is_new?'': htmlspecialchars( $rs->fields[1] ) ).'" maxlength="32"/></td></tr>';

$selected_content .= '<tr><td class="dg-cell">'.t( array( 'zh-cn'=>'卡密码', 'zh-tw'=>'卡密碼', 'en-us'=>'Card Password' ) ).'</td><td class="dg-cell">';
$selected_content .= '<input name="Password" class="ledit" type="text" value="'.  ($is_new?'': htmlspecialchars( $rs->fields[2] ) ).'" maxlength="32"/></td></tr>';

$selected_content .= '<tr><td class="dg-cell">'.t( array( 'zh-cn'=>'卡金额', 'zh-tw'=>'卡金額', 'en-us'=>'Card Amount' ) ).'</td><td class="dg-cell">';
$selected_content .= '<input name="Amount" class="ledit" type="text" value="'.  ($is_new?'': htmlspecialchars( $rs->fields[3] ) ).'" maxlength="10"/></td></tr>';

$selected_content .= '<tr><td class="dg-cell">'.t( array( 'zh-cn'=>'生成时间', 'zh-tw'=>'生成時間', 'en-us'=>'Generated Time' ) ).'</td><td class="dg-cell">';
$selected_content .= ($is_new?'': htmlspecialchars( $rs->fields[4] ) ) . '</td></tr>';


$selected_content .= '<tr><td class="dg-cell">'.t( array( 'zh-cn'=>'使用时间', 'zh-tw'=>'使用時間', 'en-us'=>'Used Time' ) ).'</td><td class="dg-cell">';
$selected_content .= ($is_new?'': htmlspecialchars( $rs->fields[5] ) ) . '</td></tr>';

$selected_content .= '<tr><td class="dg-cell">'.t( array( 'zh-cn'=>'作废', 'zh-tw'=>'作廢', 'en-us'=>'Discard' ) ).'</td><td class="dg-cell">';
$selected_content .= '<input name="Discard" type="checkbox" '.     ($is_new?'':( ((int)$rs->fields[6])>0? 'checked="checked"':'') ).'/></td></tr>';

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