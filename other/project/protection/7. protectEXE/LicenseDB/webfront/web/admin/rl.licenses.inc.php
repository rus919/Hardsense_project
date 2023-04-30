<?php

// prevent user directly accessing this page.
if( !defined('VALID_ENTRY_POINT') ){
    exit;
}

include('../include/adodb5/adodb.inc.php');

$conn = newLicConn($pid);

$table_name = 'licenses';

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
$rs = &$conn->PageExecute('select UserID,Remarks,LicenseHash,LicenseExpiration,LicensedCount,TotalCount,Banned from '. $table_name. ( empty($cond) ? '': ' where ' .$cond ), $size, $page );
if (!$rs){ 
    $selected_content = $conn->ErrorMsg();
    goto end_of_page;
}

// output table.
$selected_content = '<div id="licenses-add"><input class="lbtn" type="button" value="'.t( array('zh-cn'=>'新建','zh-tw'=>'新建', 'en-us'=>'New') ) .'" ';
$selected_content .= 'onclick="document.location=\''.str_replace("'","\'",url( implode( '/', get_path_array() ). '/add/'. implode( '/', $param ) )).'\';"/></div>';

$selected_content .= '<div class="ntab" style="background-image:url(\''.($urlrewrite?'':'..').'/images/tbg.png\')">';
$selected_content .= '<span class="atab" style="background-image:url(\''.($urlrewrite?'':'..').'/images/tf.png\')">';
$selected_content .= t(array( 'zh-cn'=>'授权凭证',     'zh-tw'=>'授權憑證',    'en-us'=>'Licenses' )).' ';
$selected_content .= '</span>';
$selected_content .= '<span class="itab">';
$selected_content .= '<a href="'.url('/licensing-records/'.$pid.'/logs').'">'.t(array( 'zh-cn'=>'授权日志',     'zh-tw'=>'授權日誌',    'en-us'=>'Logs' )).'</a> ';
$selected_content .= '</span>';
$selected_content .= '<span class="itab">';
$selected_content .= '<a href="'.url('/licensing-records/'.$pid.'/failures').'">'.t(array( 'zh-cn'=>'失败日志',     'zh-tw'=>'失敗日誌',    'en-us'=>'Failures' )).'</a>';
$selected_content .= '</span>';
$selected_content .= '</div>';

$selected_content .= '<table cellspacing="1" cellpadding="5" width="600" class="dg">';
$selected_content .= '<tr><td class="dg-h" width="150" valign="top">UserID</td><td class="dg-h" width="110"  valign="top">LicenseExpiration</td><td class="dg-h" width="70" valign="top">LicensedCount</td><td class="dg-h" width="60" valign="top">TotalCount</td><td class="dg-h" width="50" valign="top">Banned</td><td class="dg-h" width="22"></td></tr>';
while( !$rs->EOF ){
    $selected_content .= '<tr>';
    $selected_content .= '<td class="dg-cell" title="'.$rs->fields[1].'">'.$rs->fields[0].'</td>';
    $selected_content .= '<td class="dg-cell">'.$rs->fields[3].'</td>';
    $selected_content .= '<td class="dg-cell">'.$rs->fields[4].'</td>';
    $selected_content .= '<td class="dg-cell">'.$rs->fields[5].'</td>';
    $selected_content .= '<td class="dg-cell">'.$rs->fields[6].'</td>';
    $selected_content .= '<td class="dg-cell"><a class="edit" href="'.url( implode( '/', get_path_array() ). '/edit/'. strtolower( $rs->fields[2] ) .'/'. implode('/', $param) ).'">'.t(array('zh-cn'=>'编辑','zh-tw'=>'編輯','en-us'=>'Edit')).'</a></td>';
    $selected_content .= '</tr>';
    $rs->MoveNext();
}
$selected_content .= '</table>';

$rs->Close();
$conn->Close();

// output page toolbar.
$selected_content .= gen_page_toolbar( $cond, $total, $size, $page );

$selected_content .= '<div id="display_opt">'.t(array('zh-cn'=>'显示选项','zh-tw'=>'顯示選項','en-us'=>'Display options')).': ';

$selected_content .= '<a href="'.gen_search_url('',$page,$size).'">'. t(array('zh-cn'=>'全部','zh-tw'=>'全部','en-us'=>'All')).'</a> - ';

$selected_content .= '<a href="'.gen_search_url('LicenseExpiration>now()',$page,$size).'">'. t(array('zh-cn'=>'未过期','zh-tw'=>'未過期','en-us'=>'Unexpired')).'</a> - ';
$selected_content .= '<a href="'.gen_search_url('LicenseExpiration<now()',$page,$size).'">'. t(array('zh-cn'=>'已过期','zh-tw'=>'已過期','en-us'=>'Expired')).'</a> - ';
$selected_content .= '<a href="'.gen_search_url('banned=0',$page,$size).'">'. t(array('zh-cn'=>'未封号','zh-tw'=>'未封號','en-us'=>'Unbanned')).'</a> - ';
$selected_content .= '<a href="'.gen_search_url('banned=1',$page,$size).'">'. t(array('zh-cn'=>'已封号','zh-tw'=>'已封號','en-us'=>'Banned')).'</a>  ';
$selected_content .= '</div>';

$selected_content .= gen_search_form( $cond ,array('zh-cn'=>'*例如: UserID=\'test\'','zh-tw'=>'*例如: UserID=\'test\'','en-us'=>'*For example: UserID=\'test\''));
// exit point.
end_of_page:
?>