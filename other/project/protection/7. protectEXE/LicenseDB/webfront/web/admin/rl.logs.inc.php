<?php

// prevent user directly accessing this page.
if( !defined('VALID_ENTRY_POINT') ){
    exit;
}

include('../include/adodb5/adodb.inc.php');

$conn = newLicConn($pid);

$table_name = 'log';

// check connection.
if (!$conn){
    $selected_content = t( array( 'zh-cn'=>'连接数据库失败。', 'zh-tw'=>'連接數據庫失敗。', 'en-us'=>'Unable to connect database.' ) ); 
    goto end_of_page;
}

// page setting.
$cond = '';
$size = 50;
$page = 1;

get_page_input_param( $cond, $page, $size );

// get total records.
$total = $conn->GetOne('select count(*) from '. $table_name. (empty($cond)?'':' where '.$cond) );
if( is_null( $total ) ){
    $selected_content = t( array( 'zh-cn'=>'没有记录', 'zh-tw'=>'沒有記錄', 'en-us'=>'Not record(s) found.' ) ); 
    goto end_of_page;
}

// check page size.
if( $size < 1 ){
    $selected_content = t( array( 'zh-cn'=>'无效页大小', 'zh-tw'=>'無效頁大小', 'en-us'=>'Invalid Page Size' ) ). ': '. $size;
    goto end_of_page;
}

$total_pages = ceil( $total / $size );

// check page index.
if( $page < 1 || ( $page > $total_pages && $total_pages > 0 )){
    $selected_content = t( array( 'zh-cn'=>'无效页码', 'zh-tw'=>'無效頁碼', 'en-us'=>'Invalid Page Index' ) ). ': '. $page;
    goto end_of_page;
}

// display page contents.
$rs = &$conn->PageExecute('select Time,UserID,HardwareHash,IP from '. $table_name . ( empty($cond) ? '': ' where ' .$cond ) .' order by Time desc', $size, $page );
if (!$rs){ 
    $selected_content = $conn->ErrorMsg();
    goto end_of_page;
}

// output table.

$selected_content = '<div class="ntab" style="background-image:url(\''.($urlrewrite?'':'..').'/images/tbg.png\')">';
$selected_content .= '<span class="itab">';
$selected_content .= '<a href="'.url('/licensing-records/'.$pid.'/licenses').'">'.t(array( 'zh-cn'=>'授权凭证',     'zh-tw'=>'授權憑證',    'en-us'=>'Licenses' )).'</a> ';
$selected_content .= '</span>';
$selected_content .= '<span class="atab" style="background-image:url(\''.($urlrewrite?'':'..').'/images/tf.png\')">';
$selected_content .= t(array( 'zh-cn'=>'授权日志',     'zh-tw'=>'授權日誌',    'en-us'=>'Logs' )).' ';
//$selected_content .= '<a href="'.url('/licensing-records/'.$pid.'/logs').'">'.t(array( 'zh-cn'=>'授权日志',     'zh-tw'=>'授權日誌',    'en-us'=>'Logs' )).'</a> ';
$selected_content .= '</span>';
$selected_content .= '<span class="itab">';
$selected_content .= '<a href="'.url('/licensing-records/'.$pid.'/failures').'">'.t(array( 'zh-cn'=>'失败日志',     'zh-tw'=>'失敗日誌',    'en-us'=>'Failures' )).'</a>';
$selected_content .= '</span>';
$selected_content .= '</div>';

$selected_content .= '<table cellspacing="1" cellpadding="5" width="600" class="dg">';
$selected_content .= '<tr><td class="dg-h" width="110">Time</td><td class="dg-h">UserID</td><td class="dg-h" width="200">HardwareHash</td><td class="dg-h" width="80">IP</td></tr>';
while( !$rs->EOF ){
    $selected_content .= '<tr>';
    $selected_content .= '<td class="dg-cell">'.$rs->fields[0].'</td>';
    $selected_content .= '<td class="dg-cell">'.$rs->fields[1].'</td>';
    $selected_content .= '<td class="dg-cell">'.$rs->fields[2].'</td>';
    $selected_content .= '<td class="dg-cell">'.$rs->fields[3].'</td>';
    $selected_content .= '</tr>';
    $rs->MoveNext();
}
$selected_content .= '</table>';

$rs->Close();
$conn->Close();

// output page toolbar.
$selected_content .= gen_page_toolbar( $cond, $total, $size, $page );
$selected_content .= gen_search_form( $cond ,array('zh-cn'=>'*例如: IP=\'127.0.0.1\' and UserID=\'test\'','zh-tw'=>'*例如: IP=\'127.0.0.1\' and UserID=\'test\'','en-us'=>'*For example: IP=\'127.0.0.1\' and UserID=\'test\''));

// exit point.
end_of_page:
?>