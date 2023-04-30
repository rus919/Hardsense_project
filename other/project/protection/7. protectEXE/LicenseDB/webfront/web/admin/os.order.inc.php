<?php

// prevent user directly accessing this page.
if( !defined('VALID_ENTRY_POINT') ){
    exit;
}

include('../include/adodb5/adodb.inc.php');

$conn = newConn('default');

$table_name = 'orders';

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
$total = $conn->GetOne('select count(*) from orders as a left join products as b on a.pid=b.pid'. (empty($cond)?'':' where '.$cond) );
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
$rs = &$conn->PageExecute('select a.OID,a.PID,b.Name,a.Number,a.Time,a.IP,a.PaidTime,c.Username,c.UID,a.Type from Orders as a left join Products as b on a.PID=b.PID, Users as c where a.UID=c.UID'.( empty($cond) ? '': ' and ' .$cond ), $size, $page );
if (!$rs){ 
    $selected_content = $conn->ErrorMsg();
    goto end_of_page;
}

// output table.
$selected_content = '<table cellspacing="1" cellpadding="5" width="600" class="dg"><caption>'.t(array( 'zh-cn'=>'用户订单',     'zh-tw'=>'用戶訂單',    'en-us'=>'Orders' )).'</caption>';
$selected_content .= '<tr><td class="dg-h" width="20" valign="top">ID</td><td class="dg-h" width="70"  valign="top" title="Username">'.t( array('zh-cn'=>'用户名','zh-tw'=>'用戶名', 'en-us'=>'Username') ).'</td><td class="dg-h" width="150"  valign="top" title="Product">'.t( array('zh-cn'=>'产品名称','zh-tw'=>'產品名稱', 'en-us'=>'Product Name') ).'</td><td class="dg-h" width="30" valign="top" title="Number">'.t( array('zh-cn'=>'数量','zh-tw'=>'數量', 'en-us'=>'Number') ).'</td><td class="dg-h" width="100" valign="top" title="Time">'.t( array('zh-cn'=>'下单时间','zh-tw'=>'下單時間', 'en-us'=>'Order Time') ).'</td><td class="dg-h" width="30" valign="top" title="Paid">'.t( array('zh-cn'=>'付款','zh-tw'=>'付款', 'en-us'=>'Paid') ).'</td><td class="dg-h" width="22"></td></tr>';
while( !$rs->EOF ){
    $selected_content .= '<tr>';
    $selected_content .= '<td class="dg-cell"'.($rs->fields[9]==1?' style="background-color:#eeeecc;"':'').'>'.$rs->fields[0].'</td>';
    $selected_content .= '<td class="dg-cell"><a href="'.url('/order-system/customers/edit/'.$rs->fields[8]).'">'.$rs->fields[7].'</a></td>';
    $selected_content .= '<td class="dg-cell"><a href="'.url('/order-system/products/edit/'.$rs->fields[1]).'">'.htmlspecialchars($rs->fields[2]).'</a></td>';
    $selected_content .= '<td class="dg-cell">'.$rs->fields[3].'</td>';
    $selected_content .= '<td class="dg-cell">'.date('Y-n-j G:i:s',$rs->fields[4]).'</td>';
    $selected_content .= '<td class="dg-cell">'.($rs->fields[6]==0?'':'Yes').'</td>';

    $selected_content .= '<td class="dg-cell"><a class="edit" href="'.url( implode( '/', get_path_array() ). '/edit/'. strtolower( $rs->fields[0] ) .'/'. implode('/', $param) ).'">'.t(array('zh-cn'=>'编辑','zh-tw'=>'編輯','en-us'=>'Edit')).'</a></td>';
    $selected_content .= '</tr>';
    $rs->MoveNext();
}
$selected_content .= '</table>';

$rs->Close();

$num = $conn->GetOne('select sum(b.Price*a.Number) from orders as a left join products as b on a.pid=b.pid'.( empty($cond) ? '': ' where ' .$cond ));
$selected_content .= '<div id="total">'.t(array('zh-cn'=>'总金额','zh-tw'=>'總金額','en-us'=>'Total amount')).': '.(is_null($num)?'0':$num).'</div>';

$conn->Close();



// output page toolbar.
$selected_content .= gen_page_toolbar( $cond, $total, $size, $page );

$selected_content .= '<div id="display_opt">'.t(array('zh-cn'=>'显示选项','zh-tw'=>'顯示選項','en-us'=>'Display options')).': ';

$selected_content .= '<a href="'.gen_search_url('',$page,$size).'">'. t(array('zh-cn'=>'全部','zh-tw'=>'全部','en-us'=>'All')).'</a> - ';

$selected_content .= '<a href="'.gen_search_url('a.PaidTime=0',$page,$size).'">'. t(array('zh-cn'=>'未付费','zh-tw'=>'未付費','en-us'=>'Unpaid')).'</a> - ';
$selected_content .= '<a href="'.gen_search_url('a.PaidTime>0',$page,$size).'">'. t(array('zh-cn'=>'已付费','zh-tw'=>'已付費','en-us'=>'Paid')).'</a> - ';

$selected_content .= '<a href="'.gen_search_url('a.RenewID=0',$page,$size).'">'. t(array('zh-cn'=>'首付记录','zh-tw'=>'首付記錄','en-us'=>'First Order')).'</a> - ';
$selected_content .= '<a href="'.gen_search_url('a.RenewID>0',$page,$size).'">'. t(array('zh-cn'=>'续费记录','zh-tw'=>'續費記錄','en-us'=>'Renew Orders')).'</a> ';

$selected_content .= '</div>';

$selected_content .= gen_search_form( $cond ,array('zh-cn'=>'*例如: a.CID=123','zh-tw'=>'*例如: a.CID=123','en-us'=>'*For example: a.CID=123'));
// exit point.
end_of_page:
?>