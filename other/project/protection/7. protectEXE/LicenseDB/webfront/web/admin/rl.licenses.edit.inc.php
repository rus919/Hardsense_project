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
            $key = $param[1];
            break;
        case 'edit':
            if( count( $param ) == 1 ){
                goto missing;
            }
            $key = $param[1];
            break;
    }
}

include('../include/adodb5/adodb.inc.php');

$conn = newLicConn($pid);

$table_name = 'licenses';

// check connection.
if (!$conn){
    $selected_content = t( array( 'zh-cn'=>'连接数据库失败。', 'zh-tw'=>'連接數據庫失敗。', 'en-us'=>'Unable to connect database.' ) ); 
    goto end_of_page;
}

if( $is_new ){
    if( empty($_POST['LicenseHash']) ){
        $selected_content = t(array( 'zh-cn'=>'LicenseHash不能为空', 'zh-tw'=>'LicenseHash不能為空。', 'en-us'=>'LicenseHash cannot be empty.' ));
        goto end_of_page;
    }
    $sql='insert into '.$table_name.' (UserID,Remarks,LicenseHash,HardwareHash,'.(empty( $_POST['LicenseExpiration'] ) ?'':'LicenseExpiration,').'LicensedCount,TotalCount,Banned) values ('.
        $conn->qstr($_POST['UserID']).",".
        $conn->qstr($_POST['Remarks']).",".
        $conn->qstr($_POST['LicenseHash']).",".
        $conn->qstr($_POST['HardwareHash']).",".
        (empty( $_POST['LicenseExpiration'] ) ? '':$conn->qstr($_POST['LicenseExpiration']).',').
        (int)($_POST['LicensedCount']).",".
        (int)($_POST['TotalCount']).",".
        (isset($_POST['Banned'])?'1':'0').
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
    $conn->Execute('delete from '.$table_name.' where LicenseHash='. $conn->qstr($key) );
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
            'HardwareHash='.$conn->qstr($_POST['HardwareHash']).','.
            'UserID='.$conn->qstr($_POST['UserID']).','.
            'Remarks='.$conn->qstr($_POST['Remarks']).','.
            (empty( $_POST['LicenseExpiration'] ) ? '':'LicenseExpiration='.$conn->qstr($_POST['LicenseExpiration']).',').
            'LicensedCount='.(int)($_POST['LicensedCount']).','.
            'TotalCount='.(int)($_POST['TotalCount']).','.
            'Banned='. (isset($_POST['Banned'])?'1':'0').
            ' where LicenseHash=\''.$key.'\'';
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
        $rs = &$conn->Execute('select UserID,Remarks,LicenseHash,LicenseExpiration,LicensedCount,TotalCount,Banned,HardwareHash from '. $table_name . ' where licenseHash=' .$conn->qstr($key));
        if (!$rs){ 
            $selected_content = $conn->ErrorMsg();
            goto end_of_page;
        }
    }
}


new_begin:

$selected_content  = '<form method="post" action="'.url( implode( '/', $selector_array ) ).'">';
$selected_content .= '<table cellspacing="1" cellpadding="5" width="600" class="dg">';

$selected_content .= '<tr><td width="100" class="dg-cell">LicenseHash</td><td class="dg-cell">';
$selected_content .= ($is_new? '<input name="LicenseHash" class="ledit" type="text" value="" maxlength="32"/>' : htmlspecialchars( $rs->fields[2] ) ).'</td></tr>';

$selected_content .= '<tr><td width="100" class="dg-cell">HardwareHash</td><td class="dg-cell">';
$selected_content .= '<input name="HardwareHash" class="ledit" type="text" value="'.($is_new?'':htmlspecialchars( $rs->fields[7] )).'" maxlength="32"/></td></tr>';

$selected_content .= '<tr><td class="dg-cell">UserID</td><td class="dg-cell">';
$selected_content .= '<input name="UserID" class="ledit" type="text" value="'.  ($is_new?'': htmlspecialchars( $rs->fields[0] ) ).'"/></td></tr>';

$selected_content .= '<tr><td class="dg-cell">Remarks</td><td class="dg-cell">';
$selected_content .= '<textarea name="Remarks" class="lremark" rows="3" cols="80">'.($is_new?'': htmlspecialchars( $rs->fields[1] ) ).'</textarea></td></tr>';

$selected_content .= '<tr><td class="dg-cell">LicenseExpiration</td><td class="dg-cell">';
$selected_content .= '<input name="LicenseExpiration" class="ledit" type="text" value="'.  ($is_new?'': htmlspecialchars( $rs->fields[3] ) ).'" title="Example: 2010-7-3 or 2010-7-3 12:22:0"/></td></tr>';

$selected_content .= '<tr><td class="dg-cell">LicensedCount</td><td class="dg-cell">';
$selected_content .= '<input name="LicensedCount" class="ledit" type="text" value="'.  ($is_new?'': htmlspecialchars( $rs->fields[4] ) ).'" maxlength="11"/></td></tr>';

$selected_content .= '<tr><td class="dg-cell">TotalCount</td><td class="dg-cell">';
$selected_content .= '<input name="TotalCount" class="ledit" type="text" value="'.  ($is_new?'': htmlspecialchars( $rs->fields[5] ) ).'" maxlength="11"/></td></tr>';

$selected_content .= '<tr><td class="dg-cell">Banned</td><td class="dg-cell">';
$selected_content .= '<input name="Banned" type="checkbox" '.     ($is_new?'':( ((int)$rs->fields[6])>0? 'checked="checked"':'') ).'/></td></tr>';

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