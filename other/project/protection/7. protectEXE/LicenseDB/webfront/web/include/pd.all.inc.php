<?php

// prevent user directly accessing this page.
if( !defined('VALID_ENTRY_POINT') ){
    exit;
}

include('include/adodb5/adodb.inc.php');

$conn = newConn('default');

$table_name = 'products';

// check connection.
if (!$conn){
    $selected_content = t( array( 'zh-cn'=>'连接数据库失败。', 'zh-tw'=>'連接數據庫失敗。', 'en-us'=>'Unable to connect database.' ) ); 
    goto end_of_page;
}

// page setting.
$cond = '';
$size = $product_page_size;
$page = 1;

get_page_input_param( $cond, $page, $size );

//block search feature to prevent hacking.
$cond = '';

// get total records.
$total = $conn->GetOne('select count(*) from '. $table_name. ' where published=1');
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
$rs = &$conn->PageExecute('select Pid,Name,Pic,Description,Url,Price,PriceVersion,Time from '. $table_name. ' where published=1', $size, $page );
if (!$rs){ 
	//Table 'licensedb.products' doesn't exist
	if( $conn->ErrorNo() == 1146 ){
		header('Location: install.php');
		$prevent_output = true;
	}
	else{
	    $selected_content = $conn->ErrorMsg();
	}
    goto end_of_page;
}

// output table.

$selected_content = '';

while( !$rs->EOF ){
    $selected_content .= '<div class="pa"><table cellspacing="1" cellpadding="5" width="600">';
    $selected_content .= '<tr>';
    $selected_content .= '<td width="150"><img border="0" src="'.$rs->fields[2].'"/></td>';
    $selected_content .= '<td>';
    $selected_content .=    '<div class="ptitle">'.$rs->fields[1].'</div>';
    $selected_content .=    '<div class="pintro">'.$rs->fields[3].'</div>';
    $selected_content .=    '<div class="pbuy" onmouseover="this.className=\'pbuy2\'" onmouseout="this.className=\'pbuy\'"><a href="'.url('/members/cart/add/'.$rs->fields[0]).'">'.t(array('zh-cn'=>'加入购物车','zh-tw'=>'加入購物車','en-us'=>'Add to Cart')).'</a></div>';
	if( !empty( $rs->fields[4] ) ){
	    $selected_content .=    '<div class="pmore"><a href="'.$rs->fields[4].'" target="_blank">'.t(array('zh-cn'=>'了解更多','zh-tw'=>'了解更多','en-us'=>'More')).'</a></div>';
	}
    $selected_content .= '</td>';
    $selected_content .= '</tr>';
    $selected_content .= '</table></div>';
    $rs->MoveNext();
}


$rs->Close();
$conn->Close();

// output page toolbar.
$selected_content .= gen_page_index( $cond, $total, $size, $page );

// exit point.
end_of_page:
?>