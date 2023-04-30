<?php

// prevent user directly accessing this page.
if( !defined('VALID_ENTRY_POINT') ){
    exit;
}

include('../include/adodb5/adodb.inc.php');

$conn = newConn('default');

$table_name = 'charge';

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
$total = $conn->GetOne('select count(*) from charge as a left join users as b on a.uID=b.uId'. (empty($cond)?'':' where '.$cond) );
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
$rs = &$conn->PageExecute('select a.CID,a.UID,b.Username,a.CardId,a.Credential,a.Amount,a.Time,a.Type from charge as a left join users as b on a.uID=b.uId'.( empty($cond) ? '': ' where ' .$cond ).' order by a.Time desc', $size, $page );
if (!$rs){ 
    $selected_content = $conn->ErrorMsg();
    goto end_of_page;
}

// output table.
$selected_content = '<table cellspacing="1" cellpadding="5" width="600" class="dg"><caption>'.t(array( 'zh-cn'=>'充值记录',     'zh-tw'=>'充值記錄',    'en-us'=>'Charges' )).'</caption>';
$selected_content .= '<tr><td class="dg-h" width="20" valign="top">ID</td><td class="dg-h" width="50"  valign="top">'.t( array('zh-cn'=>'用户名','zh-tw'=>'用戶名', 'en-us'=>'Username') ) .'</td><td class="dg-h" width="20" valign="top">'.t( array('zh-cn'=>'卡ID','zh-tw'=>'卡ID', 'en-us'=>'CardID') ) .'</td><td class="dg-h" width="100" valign="top">'.t( array('zh-cn'=>'充值凭据','zh-tw'=>'充值憑據', 'en-us'=>'Credential') ) .'</td><td class="dg-h" width="20" valign="top">'.t( array('zh-cn'=>'金额','zh-tw'=>'金額', 'en-us'=>'Amount') ) .'</td><td class="dg-h" width="50" valign="top">'.t( array('zh-cn'=>'充值时间','zh-tw'=>'充值時間', 'en-us'=>'Time') ) .'</td><td class="dg-h" width="22"></td></tr>';
while( !$rs->EOF ){
    $selected_content .= '<tr>';
    $selected_content .= '<td class="dg-cell"'.($rs->fields[7]==1?' style="background-color:#eeeecc"':'').'>'.$rs->fields[0].'</td>';
    $selected_content .= '<td class="dg-cell"><a href="'.url('/system-settings/user-management/edit/'.$rs->fields[1]).'">'.htmlspecialchars($rs->fields[2]).'</a></td>';
    $selected_content .= '<td class="dg-cell">';

    $selected_content .= $rs->fields[3];

    $selected_content .= '</td>';
    $selected_content .= '<td class="dg-cell">'.htmlspecialchars($rs->fields[4]).'</td>';
    $selected_content .= '<td class="dg-cell">'.$rs->fields[5].'</td>';
    $selected_content .= '<td class="dg-cell">'.$rs->fields[6].'</td>';

    $selected_content .= '<td class="dg-cell"><a class="edit" href="'.url( implode( '/', get_path_array() ). '/edit/'. strtolower( $rs->fields[0] ) .'/'. implode('/', $param) ).'">'.t(array('zh-cn'=>'编辑','zh-tw'=>'編輯','en-us'=>'Edit')).'</a></td>';
    $selected_content .= '</tr>';
    $rs->MoveNext();
}
$selected_content .= '</table>';

$rs->Close();

$num = $conn->GetOne('select sum(a.Amount) from charge as a left join users as b on a.uID=b.uId'.( empty($cond) ? '': ' where ' .$cond ));
$selected_content .= '<div id="total">'.t(array('zh-cn'=>'总金额','zh-tw'=>'總金額','en-us'=>'Total amount')).': '.$num.'</div>';

$conn->Close();



// output page toolbar.
$selected_content .= gen_page_toolbar( $cond, $total, $size, $page );

$selected_content .= '<div id="display_opt">'.t(array('zh-cn'=>'显示选项','zh-tw'=>'顯示選項','en-us'=>'Display options')).': ';

$selected_content .= '<a href="'.gen_search_url('',$page,$size).'">'. t(array('zh-cn'=>'全部','zh-tw'=>'全部','en-us'=>'All')).'</a> - ';

$selected_content .= '<a href="'.gen_search_url('a.CardId>0',$page,$size).'">'. t(array('zh-cn'=>'充值卡充值','zh-tw'=>'充值卡充值','en-us'=>'Paid by cards')).'</a> - ';
$selected_content .= '<a href="'.gen_search_url('a.CardId=0',$page,$size).'">'. t(array('zh-cn'=>'网银充值','zh-tw'=>'網銀充值','en-us'=>'Paid by online bank')).'</a> ';
$selected_content .= '</div>';

$selected_content .= gen_search_form( $cond ,array('zh-cn'=>'*例如: a.CID=123','zh-tw'=>'*例如: a.CID=123','en-us'=>'*For example: a.CID=123'));
// exit point.
end_of_page:
?>