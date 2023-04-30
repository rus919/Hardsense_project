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

$table_name = 'charge';

// check connection.
if (!$conn){
    $selected_content = t( array( 'zh-cn'=>'连接数据库失败。', 'zh-tw'=>'連接數據庫失敗。', 'en-us'=>'Unable to connect database.' ) ); 
    goto end_of_page;
}

if( $is_new ){
    if( empty($_POST['UID']) || empty($_POST['Amount']) ){
        $selected_content = t(array( 'zh-cn'=>'UID,Amount 不能为空。', 'zh-tw'=>'UID,Amount 不能為空。', 'en-us'=>'UID,Amount cannot be empty.' ));
        goto end_of_page;
    }
    $sql='insert into '.$table_name.' (UID,CardID,Credential,Amount,Remarks,Time) values ('.
        (int)($_POST['UID']).",".
        (int)($_POST['CardID']).",".
        $conn->qstr($_POST['Credential']).",".
        (int)($_POST['Amount']).",".
        $conn->qstr($_POST['Remarks']).",".
        $conn->sysTimeStamp.
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
    $conn->Execute('delete from '.$table_name.' where cid='. $key );
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
            'CardID='.(int)($_POST['CardID']).','.
            'Credential='.$conn->qstr($_POST['Credential']).','.
            'Amount='.(int)($_POST['Amount']).','.
            'Remarks='.$conn->qstr($_POST['Remarks']).','.
            'Time='. $conn->sysTimeStamp.
            ' where CID='.$key;
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
        $rs = &$conn->Execute('select a.CID,a.UID,b.Username,a.CardId,a.Credential,a.Amount,a.Remarks,a.Time,a.Type from charge as a , users as b where a.uID=b.uId and a.cid=' .$key);
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
$selected_content .= ($is_new?'': htmlspecialchars( $rs->fields[0] )).'</td></tr>';

$selected_content .= '<tr><td width="100" class="dg-cell">'.t( array('zh-cn'=>'用户名','zh-tw'=>'用戶名', 'en-us'=>'Username') ) .'</td><td class="dg-cell">';
$selected_content .= ($is_new?
                        '<input name="UID" class="ledit" type="text" value="1" maxlength="10"/>'
                       :'<a href="'.url('/system-settings/user-management/edit/'.$rs->fields[1]).'">'.htmlspecialchars($rs->fields[2]).'</a>').
                      '</td></tr>';

if( !$is_new ){
    $selected_content .= '<tr><td class="dg-cell">'.t( array('zh-cn'=>'充值方式','zh-tw'=>'充值方式', 'en-us'=>'Method') ) .'</td><td class="dg-cell">';
    switch( $rs->fields[8]==null ? 0 : $rs->fields[8] ){
        case 0:
            $selected_content .= t(array( 'zh-cn'=>'从网站充值', 'zh-tw'=>'從網站充值', 'en-us'=>'Charged from website' ));
            break;
        case 1:
            $selected_content .= t(array( 'zh-cn'=>'从客户端软件充值', 'zh-tw'=>'從客戶端軟件充值', 'en-us'=>'Charged from client side software' ));
            break;
    }
    $selected_content .= '</td></tr>';
}

$selected_content .= '<tr><td class="dg-cell">'.t( array('zh-cn'=>'卡ID','zh-tw'=>'卡ID', 'en-us'=>'CardID') ) .'</td><td class="dg-cell">';
$selected_content .= '<input name="CardID" class="ledit" type="text" value="'.  ($is_new?'': htmlspecialchars( $rs->fields[3] ) ).'" maxlength="10"/></td></tr>';

$selected_content .= '<tr><td class="dg-cell">'.t( array('zh-cn'=>'充值凭据','zh-tw'=>'充值憑據', 'en-us'=>'Credential') ) .'</td><td class="dg-cell">';
$selected_content .= '<input name="Credential" class="ledit" type="text" value="'.  ($is_new?'': htmlspecialchars( $rs->fields[4] ) ).'" maxlength="256"/></td></tr>';

$selected_content .= '<tr><td class="dg-cell">'.t( array('zh-cn'=>'金额','zh-tw'=>'金額', 'en-us'=>'Amount') ) .'</td><td class="dg-cell">';
$selected_content .= '<input name="Amount" class="ledit" type="text" value="'.  ($is_new?'': htmlspecialchars( $rs->fields[5] ) ).'" maxlength="10"/></td></tr>';

$selected_content .= '<tr><td class="dg-cell">'.t( array('zh-cn'=>'备注（用户可见）','zh-tw'=>'備註（用戶可見）', 'en-us'=>'Remarks(Visiable to user)') ) .'</td><td class="dg-cell">';
$selected_content .= '<textarea name="Remarks" class="lremark" rows="5" cols="80">'.($is_new?'': htmlspecialchars( $rs->fields[6] ) ).'</textarea></td></tr>';

$selected_content .= '<tr><td class="dg-cell">'.t( array('zh-cn'=>'充值时间','zh-tw'=>'充值時間', 'en-us'=>'Time') ) .'</td><td class="dg-cell">';
$selected_content .= ($is_new?'': htmlspecialchars( $rs->fields[7] ) ).'</td></tr>';

$selected_content .= '</table>';
$selected_content .= '<br/><div id="form_toolbar">';
$selected_content .= '<div id="form_toolbar_left"><input class="lbtn" type="submit" value="'.t( $is_new? array('zh-cn'=>'添加','zh-tw'=>'添加', 'en-us'=>'Add') : array('zh-cn'=>'更新','zh-tw'=>'更新', 'en-us'=>'Update') ) .'"/></div>';
$selected_content .= '<div id="form_toolbar_right"><input class="lbtn" type="button" disabled="disabled" value="'.t( array('zh-cn'=>'新建','zh-tw'=>'新建', 'en-us'=>'New') ) .'" ';
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