<?php

// prevent user directly accessing this page.
if( !defined('VALID_ENTRY_POINT') ){
    exit;
}

include('../include/adodb5/adodb.inc.php');

$conn = newConn('default');

$table_name = 'products';

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
$rs = &$conn->PageExecute('select Pid,Name,Price,PriceVersion,Time,Published from '. $table_name. ( empty($cond) ? '': ' where ' .$cond ), $size, $page );
if (!$rs){ 
    $selected_content = $conn->ErrorMsg();
    goto end_of_page;
}

// output table.
$selected_content = '<div id="licenses-add"><input class="lbtn" type="button" value="'.t( array('zh-cn'=>'新建','zh-tw'=>'新建', 'en-us'=>'New') ) .'" ';
$selected_content .= 'onclick="document.location=\''.str_replace("'","\'",url( implode( '/', get_path_array() ). '/add/'. implode( '/', $param ) )).'\';"/></div>';
$selected_content .= '<table cellspacing="1" cellpadding="5" width="600" class="dg"><caption>'.t(array( 'zh-cn'=>'产品设置',     'zh-tw'=>'產品設置',    'en-us'=>'Products' )).'</caption>';
$selected_content .= '<tr><td class="dg-h" width="30" valign="top">ID</td><td class="dg-h" width="110"  valign="top">'. t(array('zh-cn'=>'产品名称','zh-tw'=>'產品名稱','en-us'=>'Product Name')).'</td><td class="dg-h" width="40" valign="top">'. t(array('zh-cn'=>'价格','zh-tw'=>'價格','en-us'=>'Price')).'</td><td class="dg-h" width="60" valign="top">'. t(array('zh-cn'=>'价格版本','zh-tw'=>'價格版本','en-us'=>'Price Version')).'</td><td class="dg-h" width="110" valign="top">'. t(array('zh-cn'=>'添加时间','zh-tw'=>'添加時間','en-us'=>'Time')).'</td><td class="dg-h" width="50" valign="top">'. t(array('zh-cn'=>'已发布','zh-tw'=>'已發布','en-us'=>'Published')).'</td><td class="dg-h" width="22"></td></tr>';
while( !$rs->EOF ){
    $selected_content .= '<tr>';
    $selected_content .= '<td class="dg-cell">'.$rs->fields[0].'</td>';
    $selected_content .= '<td class="dg-cell">'.$rs->fields[1].'</td>';
    $selected_content .= '<td class="dg-cell">'.$rs->fields[2].'</td>';
    $selected_content .= '<td class="dg-cell">'.$rs->fields[3].'</td>';
    $selected_content .= '<td class="dg-cell">'.$rs->fields[4].'</td>';
    $selected_content .= '<td class="dg-cell">'.($rs->fields[5]>0?'Yes':'').'</td>';
    $selected_content .= '<td class="dg-cell"><a class="edit" href="'.url( implode( '/', get_path_array() ). '/edit/'. strtolower( $rs->fields[0] ) .'/'. implode('/', $param) ).'">'.t(array('zh-cn'=>'编辑','zh-tw'=>'編輯','en-us'=>'Edit')).'</a></td>';
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

$selected_content .= '<a href="'.gen_search_url('published=0',$page,$size).'">'. t(array('zh-cn'=>'未发布','zh-tw'=>'未發布','en-us'=>'Unpublished')).'</a> - ';
$selected_content .= '<a href="'.gen_search_url('published=1',$page,$size).'">'. t(array('zh-cn'=>'已发布','zh-tw'=>'已發布','en-us'=>'Published')).'</a>  ';
$selected_content .= '</div>';

$selected_content .= gen_search_form( $cond ,array('zh-cn'=>'*例如: Name=\'Safengine\'','zh-tw'=>'*例如: Name=\'safengine\'','en-us'=>'*For example: Name=\'safengine\''));
// exit point.
end_of_page:
?>