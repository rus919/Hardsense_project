<?php

// prevent user directly accessing this page.
if( !defined('VALID_ENTRY_POINT') ){
    exit;
}

include('../include/adodb5/adodb.inc.php');

$conn = newConn('default');

$table_name = 'Cards';

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
$rs = &$conn->PageExecute('select CardId,CardNumber,Password,Amount,GeneratedTime,UsedTime,Discard from '. $table_name . ( empty($cond) ? '': ' where ' .$cond ) .' order by GeneratedTime desc', $size, $page );
if (!$rs){ 
    $selected_content = $conn->ErrorMsg();
    goto end_of_page;
}

// output table.
$selected_content = '<div id="licenses-add"><input class="lbtn" type="button" value="'.t( array('zh-cn'=>'自动添加','zh-tw'=>'自動添加', 'en-us'=>'Add automatically') ) .'" ';
$selected_content .= 'onclick="document.location=\''.str_replace("'","\'",url( implode( '/', get_path_array() ). '/auto-add/'. implode( '/', $param ) )).'\';"/> ';
$selected_content .= '<input class="lbtn" type="button" value="'.t( array('zh-cn'=>'手动添加','zh-tw'=>'手動添加', 'en-us'=>'Add manually') ) .'" ';
$selected_content .= 'onclick="document.location=\''.str_replace("'","\'",url( implode( '/', get_path_array() ). '/add/'. implode( '/', $param ) )).'\';"/></div>';
$selected_content .= '<table cellspacing="1" cellpadding="5" width="600" class="dg"><caption>'.t(array( 'zh-cn'=>'充值卡管理',     'zh-tw'=>'充值卡管理',    'en-us'=>'Card management' )).'</caption>';
$selected_content .= '<tr><td class="dg-h" width="50">ID</td><td class="dg-h" width="150">'.t( array('zh-cn'=>'卡号','zh-tw'=>'卡號', 'en-us'=>'Card Number') ) .'</td><td class="dg-h" width="150">'.t( array('zh-cn'=>'卡密码','zh-tw'=>'卡密碼', 'en-us'=>'Card Password') ) .'</td><td class="dg-h" width="80">'.t( array('zh-cn'=>'金额','zh-tw'=>'金額', 'en-us'=>'Amount') ) .'</td><td class="dg-h" width="100">'.t( array('zh-cn'=>'生成时间','zh-tw'=>'生成時間', 'en-us'=>'Generated') ) .'</td><td class="dg-h" width="100">'.t( array('zh-cn'=>'使用时间','zh-tw'=>'使用時間', 'en-us'=>'Used Time') ) .'</td><td class="dg-h" width="50">'.t( array('zh-cn'=>'作废','zh-tw'=>'作廢', 'en-us'=>'Discard') ) .'</td><td class="dg-h" width="50"></td></tr>';
while( !$rs->EOF ){
    $selected_content .= '<tr>';
    $selected_content .= '<td class="dg-cell">'.$rs->fields[0].'</td>';
    $selected_content .= '<td class="dg-cell">'.$rs->fields[1].'</td>';
    $selected_content .= '<td class="dg-cell">'.$rs->fields[2].'</td>';
    $selected_content .= '<td class="dg-cell">'.$rs->fields[3].'</td>';
    $selected_content .= '<td class="dg-cell">'.$rs->fields[4].'</td>';
    $selected_content .= '<td class="dg-cell">'.$rs->fields[5].'</td>';
    $selected_content .= '<td class="dg-cell">'.($rs->fields[6]>0?'Yes':'').'</td>';
    $selected_content .= '<td class="dg-cell"><a class="edit" href="'.url( implode( '/', get_path_array() ). '/edit/'. strtolower( $rs->fields[0] ) .'/'. implode('/', $param) ).'">'.t(array('zh-cn'=>'编辑','zh-tw'=>'編輯','en-us'=>'Edit')).'</a></td>';
    $selected_content .= '</tr>';
    $rs->MoveNext();
}
$selected_content .= '</table>';

$rs->Close();

$num = $conn->GetOne('select sum(Amount) from '.$table_name.( empty($cond) ? '': ' where ' .$cond ));
$selected_content .= '<div id="total">'.t(array('zh-cn'=>'总金额','zh-tw'=>'總金額','en-us'=>'Total amount')).': '.$num.'</div>';

$conn->Close();

// output page toolbar.
$selected_content .= gen_page_toolbar( $cond, $total, $size, $page );
$selected_content .= '<div id="display_opt">'.t(array('zh-cn'=>'显示选项','zh-tw'=>'顯示選項','en-us'=>'Display options')).': ';

$selected_content .= '<a href="'.gen_search_url('',$page,$size).'">'. t(array('zh-cn'=>'全部','zh-tw'=>'全部','en-us'=>'All')).'</a> - ';

$selected_content .= '<a href="'.gen_search_url('usedtime is null',$page,$size).'">'. t(array('zh-cn'=>'未使用','zh-tw'=>'未使用','en-us'=>'Unused')).'</a> - ';
$selected_content .= '<a href="'.gen_search_url('usedtime is not null',$page,$size).'">'. t(array('zh-cn'=>'已使用','zh-tw'=>'已使用','en-us'=>'Used')).'</a> - ';
$selected_content .= '<a href="'.gen_search_url('discard=0',$page,$size).'">'. t(array('zh-cn'=>'未作废','zh-tw'=>'未作廢','en-us'=>'Undiscard')).'</a> - ';
$selected_content .= '<a href="'.gen_search_url('discard=1',$page,$size).'">'. t(array('zh-cn'=>'已作废','zh-tw'=>'已作廢','en-us'=>'Discard')).'</a>  ';
$selected_content .= '</div>';
$selected_content .= gen_search_form( $cond ,array('zh-cn'=>'*例如: Used=1','zh-tw'=>'*例如: Used=1','en-us'=>'*For example: Used=1'));

// exit point.
end_of_page:
?>