<?php

// prevent user directly accessing this page.
if( !defined('VALID_ENTRY_POINT') ){
    exit;
}

include('./include/adodb5/adodb.inc.php');

$conf = 'default';
$conn = newConn($conf);

$table_name = 'Charge';

// check connection.
if (!$conn){
    $selected_content = t( array( 'zh-cn'=>'连接数据库失败。', 'zh-tw'=>'連接數據庫失敗。', 'en-us'=>'Unable to connect database.' ) ); 
    goto end_of_page;
}

// page setting.
$cond = '';
$size = $shopping_cart_page_size;
$page = 1;

get_page_input_param( $cond, $page, $size, array('a.cardid') );
sql_strong_filter( $cond, array('a.cardid!=0','a.cardid=0') );

// get total records.
$total = $conn->GetOne('select count(*) from '. $table_name. ' as a where UID='.get_uid($conf). (empty($cond)?'':' and '.$cond) );
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
$rs = &$conn->PageExecute('select a.CID,a.UID,a.CardID,b.CardNumber,a.Credential,a.Amount,a.Remarks,a.Time from '. $table_name .' as a left join Cards as b on a.CardID=b.CardID where a.UID='.get_uid($conf) . ( empty($cond) ? '': ' and ' .$cond ) .' order by a.Time desc', $size, $page );
if (!$rs){ 
    $selected_content = $conn->ErrorMsg();
    goto end_of_page;
}

// output table.
$selected_content = '<div id="licenses-add"><input class="lbtn" type="button" value="'.t( array('zh-cn'=>'充值','zh-tw'=>'充值', 'en-us'=>'Charging') ) .'" ';
$selected_content .= 'onclick="document.location=\''.str_replace("'","\'",url( implode( '/', get_path_array() ). '/add/'. implode( '/', $param ) )).'\';"/></div>';
$selected_content .= '<table cellspacing="1" cellpadding="5" width="600" class="dg"><caption>'.t(array( 'zh-cn'=>'充值中心',     'zh-tw'=>'充值中心',    'en-us'=>'Charging Center' )).'</caption>';
$selected_content .= '<tr>';
$selected_content .= '<td class="dg-h" width="30" valign="top">ID</td>';
$selected_content .= '<td class="dg-h" width="60" valign="top">'            .t(array('zh-cn'=>'充值方式','zh-tw'=>'充值方式','en-us'=>'Payment<br/>Method')).'</td>';
$selected_content .= '<td class="dg-h" width="150" valign="top">' .t(array('zh-cn'=>'充值卡号/网银订单号','zh-tw'=>'充值卡號/網銀訂單號','en-us'=>'Card No. / Order No.')).              '</td>';
$selected_content .= '<td class="dg-h" width="30" valign="top">' .t(array('zh-cn'=>'金额','zh-tw'=>'金額','en-us'=>'Amount')).             '</td>';
$selected_content .= '<td class="dg-h" width="110" valign="top">'.t(array('zh-cn'=>'充值时间','zh-tw'=>'充值時間','en-us'=>'Charging Time')). '</td>';
$selected_content .= '<td class="dg-h" width="30" valign="top"></td></tr>';

while( !$rs->EOF ){
    $selected_content .= '<tr>';
    $selected_content .= '<td class="dg-cell">'.$rs->fields[0].'</td>';
    $selected_content .= '<td class="dg-cell">'.( !empty($rs->fields[2]) ?
        t(array('zh-cn'=>'充值卡','zh-tw'=>'充值卡','en-us'=>'Prepaid Card'))
       :t(array('zh-cn'=>'网银充值','zh-tw'=>'網銀充值','en-us'=>'Online Bank'))
                                                ).'</td>';
    $selected_content .= '<td class="dg-cell">'.( !empty($rs->fields[2]) ? $rs->fields[3] : $rs->fields[4] ).'</td>';
    $selected_content .= '<td class="dg-cell">'.$rs->fields[5].'</td>';
    $selected_content .= '<td class="dg-cell">'.$rs->fields[7].'</td>';
    $selected_content .= '<td class="dg-cell"><a class="edit" href="'.url( implode( '/', get_path_array() ). '/edit/'. strtolower( $rs->fields[0] ) .'/'. implode('/', $param) ).'">'.t(array('zh-cn'=>'详情','zh-tw'=>'詳情','en-us'=>'Detail')).'</a></td>';
    $selected_content .= '</tr>';
    $rs->MoveNext();
}
$selected_content .= '</table>';

$rs->Close();

$num = $conn->GetOne('select sum(Amount) from '.$table_name.' as a where UID='.get_uid($conf).( empty($cond) ? '': ' and ' .$cond ));
$account_amount = $conn->GetOne('select amount from users where uid='.get_uid($conf));
$selected_content .= '<div id="total">'.t(array('zh-cn'=>'总金额','zh-tw'=>'總金額','en-us'=>'Total amount')).': '.(is_null( $num ) ? '0': $num) ;
$selected_content .= ' '. t(array('zh-cn'=>'帐户余额','zh-tw'=>'帳戶餘額','en-us'=>'Account amount')) . ': '. (is_null( $account_amount ) ? '0': $account_amount);
$selected_content .= '</div>';

$conn->Close();

// output page toolbar.
$selected_content .= gen_page_toolbar( $cond, $total, $size, $page );
$selected_content .= '<div id="display_opt">'.t(array('zh-cn'=>'显示选项','zh-tw'=>'顯示選項','en-us'=>'Display options')).': ';

$selected_content .= '<a href="'.gen_search_url('',$page,$size).'">'. t(array('zh-cn'=>'全部','zh-tw'=>'全部','en-us'=>'All')).'</a> - ';

$selected_content .= '<a href="'.gen_search_url('a.CardID!=0',$page,$size).'">'.t(array('zh-cn'=>'充值卡','zh-tw'=>'充值卡','en-us'=>'Prepaid Card')).'</a> - ';
$selected_content .= '<a href="'.gen_search_url('a.CardID=0',$page,$size).'">'. t(array('zh-cn'=>'网银充值','zh-tw'=>'網銀充值','en-us'=>'Online Bank')).'</a>  ';
$selected_content .= '</div>';

//$selected_content .= gen_search_form( $cond ,array('zh-cn'=>'*例如: Used=1','zh-tw'=>'*例如: Used=1','en-us'=>'*For example: Used=1'));

// exit point.
end_of_page:
?>