<?php

// prevent user directly accessing this page.
if( !defined('VALID_ENTRY_POINT') ){
    exit;
}

include('./include/adodb5/adodb.inc.php');

$conf = 'default';
$conn = newConn($conf);

$table_name = 'Orders';

// check connection.
if (!$conn){
    $selected_content = t( array( 'zh-cn'=>'连接数据库失败。', 'zh-tw'=>'連接數據庫失敗。', 'en-us'=>'Unable to connect database.' ) ); 
    goto end_of_page;
}

// page setting.
$cond = '';
$size = $shopping_cart_page_size;
$page = 1;

get_page_input_param( $cond, $page, $size, array('paidtime') );
sql_strong_filter( $cond, array('paidtime=0','paidtime>0') );

// get total records.
$total = $conn->GetOne('select count(*) from '. $table_name. ' as a left join Products as b on a.PID=b.PID, Users as c where a.RenewID=0 and a.UID=c.UID and a.UID='.get_uid($conf). (empty($cond)?'':' and '.$cond) );
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
$rs = &$conn->PageExecute('select a.OID,a.UID,c.Username,a.PID,b.Name,b.Price,a.Number,a.Time,a.IP,a.PaidTime from '. $table_name .' as a left join Products as b on a.PID=b.PID, Users as c where a.RenewID=0 and a.UID=c.UID and a.UID='.get_uid($conf) . ( empty($cond) ? '': ' and ' .$cond ) .' order by a.Time desc', $size, $page );
if (!$rs){ 
    $selected_content = $conn->ErrorMsg();
    goto end_of_page;
}

// output table.
$selected_content = '<table cellspacing="1" cellpadding="5" width="600" class="dg"><caption>'.t(array( 'zh-cn'=>'我的购物车',     'zh-tw'=>'我的購物車',    'en-us'=>'Shopping Cart' )).'</caption>';
$selected_content .= '<tr><td class="dg-h" width="30">ID</td><td class="dg-h">'.t(array('zh-cn'=>'产品名称','zh-tw'=>'產品名稱','en-us'=>'Product Name')).'</td><td class="dg-h" width="40">'.t(array('zh-cn'=>'单价','zh-tw'=>'單價','en-us'=>'Price')).'</td><!--<td class="dg-h" width="40">'.t(array('zh-cn'=>'数量','zh-tw'=>'數量','en-us'=>'Number')).'</td>--><td class="dg-h" width="110">'.t(array('zh-cn'=>'下单时间','zh-tw'=>'下单時間','en-us'=>'Adding Time')).'</td><td class="dg-h" width="110">'.t(array('zh-cn'=>'付款时间','zh-tw'=>'付款時間','en-us'=>'Paying Time')).'</td><td class="dg-h" width="50"></td></tr>';
while( !$rs->EOF ){
    $selected_content .= '<tr>';
    $selected_content .= '<td class="dg-cell">'.$rs->fields[0].'</td>';
    $selected_content .= '<td class="dg-cell">'.htmlspecialchars($rs->fields[4]).'</td>';
    $selected_content .= '<td class="dg-cell">'.$rs->fields[5].'</td>';
   // $selected_content .= '<td class="dg-cell">'.$rs->fields[6].'</td>';
    $selected_content .= '<td class="dg-cell">'.date('Y-n-j G:i:s',$rs->fields[7]).'</td>';
    $selected_content .= '<td class="dg-cell">'.( ( $rs->fields[9] > 0 ) ? date('Y-n-j G:i:s',$rs->fields[9]): t(array('zh-cn'=>'未付款','zh-tw'=>'未付款','en-us'=>'Unpaid')) ).'</td>';
    $selected_content .= '<td class="dg-cell"><a class="edit" href="'.url( implode( '/', get_path_array() ). '/edit/'. strtolower( $rs->fields[0] ) .'/'. implode('/', $param) ).'">'.t(array('zh-cn'=>'详情','zh-tw'=>'詳情','en-us'=>'Detail')).'</a></td>';
    $selected_content .= '</tr>';
    $rs->MoveNext();
}
$selected_content .= '</table>';

$rs->Close();

$num = $conn->GetOne('select sum(a.Number*b.Price) from '.$table_name.' as a left join Products as b on a.PID=b.PID, Users as c where a.UID=c.UID and a.UID='.get_uid($conf).( empty($cond) ? '': ' and ' .$cond ));
$selected_content .= '<div id="total">'.t(array('zh-cn'=>'总金额','zh-tw'=>'總金額','en-us'=>'Total amount')).': '.(is_null( $num ) ? '0': $num) .'</div>';

$conn->Close();

// output page toolbar.
$selected_content .= gen_page_toolbar( $cond, $total, $size, $page );
$selected_content .= '<div id="display_opt">'.t(array('zh-cn'=>'显示选项','zh-tw'=>'顯示選項','en-us'=>'Display options')).': ';

$selected_content .= '<a href="'.gen_search_url('',$page,$size).'">'. t(array('zh-cn'=>'全部','zh-tw'=>'全部','en-us'=>'All')).'</a> - ';

$selected_content .= '<a href="'.gen_search_url('paidtime=0',$page,$size).'">'. t(array('zh-cn'=>'未付款','zh-tw'=>'未付款','en-us'=>'Unpaid')).'</a> - ';
$selected_content .= '<a href="'.gen_search_url('paidtime>0',$page,$size).'">'. t(array('zh-cn'=>'已付款','zh-tw'=>'已付款','en-us'=>'Paid')).'</a>  ';
$selected_content .= '</div>';

//$selected_content .= gen_search_form( $cond ,array('zh-cn'=>'*例如: Used=1','zh-tw'=>'*例如: Used=1','en-us'=>'*For example: Used=1'));

// exit point.
end_of_page:
?>