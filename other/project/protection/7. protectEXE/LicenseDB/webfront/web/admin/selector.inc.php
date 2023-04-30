<?php

// prevent user directly accessing this page.
if( !defined('VALID_ENTRY_POINT') ){
    exit;
}

include('../include/sqlfilter.inc.php');
//
// $selector         indicates the path selector.
// $selector_array   indicates the path selector array.
// $breadcrumb       indicates the current location.
// $param            the parameter array for internal specific program.
// $selected_content the application result.
//

ensure_admin_login();

define('PATH_NAME','p');

$selector = isset( $_GET[ PATH_NAME ] ) ? $_GET[ PATH_NAME ] : '';

// get path selector
$selector = trim_path( trim( $selector ) );

// get path selector array
$selector_array = explode( '/', $selector );

// intro picture
$intro_pic = '';

// set page language.
$set_lang = false;
if( count( $selector_array ) > 0 ){
    switch( $selector_array[0] ){
        case 'en-us':
        case 'zh-cn':
        case 'zh-tw':
            $lang = array_shift( $selector_array );
            $set_lang = true;
            break;
    }
}

$selected_content = t( array( 'zh-cn'=>'您所查找的页面不存在!', 'zh-tw'=>'您所查找的檔案不存在！', 'en-us'=>'Page not found!' ) );
$breadcrumb = t( array( 'zh-cn'=>'页面未找到', 'zh-tw'=>'檔案未找到', 'en-us'=>'Page not found' ) ); //t( array( 'zh-cn'=>'首页', 'zh-tw'=>'首頁', 'en-us'=>'Home' ) )
$param = array();

// select page and application.
if( count( $selector_array ) == 0 || empty($selector_array[0]) ){
    $selector_array = array('order-system','orders');
}

switch( $selector_array[0] ){
    case 'logout':
        session_unset();
        header('Location: '.url('/'));exit;
        break;
    case 'licensing-records':
        $s = t( array( 'zh-cn'=>'授权记录', 'zh-tw'=>'授權記錄', 'en-us'=>'License Records' ) );
        if( count( $selector_array ) > 2 && (int)$selector_array[1] > 0 ){
			$pid = (int)$selector_array[1];
            switch( $selector_array[2] ){
                case 'licenses':
                    if( count( $selector_array ) > 3 && ( $selector_array[3]=='add' || $selector_array[3]=='edit' || $selector_array[3]=='delete') ){
                        switch( $selector_array[3]){
                            case 'add':
                                $breadcrumb = $s. ' / '. t( array( 'zh-cn'=>'授权凭证 / 添加', 'zh-tw'=>'授權憑證 / 添加', 'en-us'=>'Licenses / Add' ) );
                                break;
                            case 'edit':
                                $breadcrumb = $s. ' / '. t( array( 'zh-cn'=>'授权凭证 / 编辑', 'zh-tw'=>'授權憑證 / 編輯', 'en-us'=>'Licenses / Edit' ) );
                                break;
                            case 'delete':
                                $breadcrumb = $s. ' / '. t( array( 'zh-cn'=>'授权凭证 / 删除', 'zh-tw'=>'授權憑證 / 刪除', 'en-us'=>'Licenses / Delete' ) );
                                break;
                        }
                        $param = array_slice( $selector_array, 3 );
                        include( 'rl.licenses.edit.inc.php' );
                    }
                    else{
                        $breadcrumb = $s. ' / '. t( array( 'zh-cn'=>'授权凭证', 'zh-tw'=>'授權憑證', 'en-us'=>'Licenses' ) );
                        $param = array_slice( $selector_array, 3 );
                        include('rl.licenses.inc.php');
                    }
                    break;
                case 'logs':
                    $breadcrumb = $s. ' / '. t( array( 'zh-cn'=>'授权日志', 'zh-tw'=>'授權日誌', 'en-us'=>'Logs' ) );
                    $param = array_slice( $selector_array, 3 );
                    include('rl.logs.inc.php');
                    break;
                case 'failures':
                    $breadcrumb = $s. ' / '. t( array( 'zh-cn'=>'失败日志', 'zh-tw'=>'失敗日誌', 'en-us'=>'Failures' ) );
                    $param = array_slice( $selector_array, 3 );
                    include('rl.failures.inc.php');
                    break;
            }
        }
		else{
			$breadcrumb = $s;
			$param = array_slice( $selector_array, 1 );
            include('rl.products.inc.php');
		}
        break;
    case 'order-system':
        if( count( $selector_array ) > 1 ){
            $s = t(array( 'zh-cn'=>'订单系统', 'zh-tw'=>'訂單系統', 'en-us'=>'Order System' ));
            switch( $selector_array[1] ){
                case 'customers':
                    if( count( $selector_array ) > 2 && ( $selector_array[2]=='add' || $selector_array[2]=='edit' || $selector_array[2]=='delete') ){
                        switch( $selector_array[2]){
                            case 'add':
                                $breadcrumb = $s. ' / '. t( array( 'zh-cn'=>'客户管理 / 添加', 'zh-tw'=>'客戶管理 / 添加', 'en-us'=>'Customers / Add' ) );
                                break;
                            case 'edit':
                                $breadcrumb = $s. ' / '. t( array( 'zh-cn'=>'客户管理 / 编辑', 'zh-tw'=>'客戶管理 / 編輯', 'en-us'=>'Customers / Edit' ) );
                                break;
                            case 'delete':
                                $breadcrumb = $s. ' / '. t( array( 'zh-cn'=>'客户管理 / 删除', 'zh-tw'=>'客戶管理 / 刪除', 'en-us'=>'Customers / Delete' ) );
                                break;
                        }
                        $param = array_slice( $selector_array, 2 );
                        include( 'os.users.edit.inc.php' );
                    }
                    else{
                        $breadcrumb = $s. ' / '. t( array( 'zh-cn'=>'用户管理', 'zh-tw'=>'用戶管理', 'en-us'=>'User management' ) );
                        $param = array_slice( $selector_array, 2 );
                        include('os.users.inc.php');
                    }
                    break;
                case 'products':
                    if( count( $selector_array ) > 2 && ( $selector_array[2]=='add' || $selector_array[2]=='edit' || $selector_array[2]=='delete') ){
                        switch( $selector_array[2]){
                            case 'add':
                                $breadcrumb = $s. ' / '. t( array( 'zh-cn'=>'产品设置 / 添加', 'zh-tw'=>'產品設置 / 添加', 'en-us'=>'Products / Add' ) );
                                break;
                            case 'edit':
                                $breadcrumb = $s. ' / '. t( array( 'zh-cn'=>'产品设置 / 编辑', 'zh-tw'=>'產品設置 / 編輯', 'en-us'=>'Products / Edit' ) );
                                break;
                            case 'delete':
                                $breadcrumb = $s. ' / '. t( array( 'zh-cn'=>'产品设置 / 删除', 'zh-tw'=>'產品設置 / 刪除', 'en-us'=>'Products / Delete' ) );
                                break;
                        }
                        $param = array_slice( $selector_array, 2 );
                        include( 'os.products.edit.inc.php' );
                    }
                    else{
                        $breadcrumb = $s. ' / '. t( array( 'zh-cn'=>'产品设置', 'zh-tw'=>'產品設置', 'en-us'=>'Products' ) );
                        $param = array_slice( $selector_array, 2 );
                        include('os.products.inc.php');
                    }
                    break;
                case 'cards':
                    if( count( $selector_array ) > 2 && ( $selector_array[2]=='auto-add' || $selector_array[2]=='add' || $selector_array[2]=='edit' || $selector_array[2]=='delete') ){
                        switch( $selector_array[2]){
                            case 'auto-add':
                                $breadcrumb = $s. ' / '. t( array( 'zh-cn'=>'充值卡管理 / 自动添加', 'zh-tw'=>'充值卡管理 / 自動添加', 'en-us'=>'Card management / Add automatically' ) );
                                break;
                            case 'add':
                                $breadcrumb = $s. ' / '. t( array( 'zh-cn'=>'充值卡管理 / 手动添加', 'zh-tw'=>'充值卡管理 / 手動添加', 'en-us'=>'Card management / Add manually' ) );
                                break;
                            case 'edit':
                                $breadcrumb = $s. ' / '. t( array( 'zh-cn'=>'充值卡管理 / 编辑', 'zh-tw'=>'充值卡管理 / 編輯', 'en-us'=>'Card management / Edit' ) );
                                break;
                            case 'delete':
                                $breadcrumb = $s. ' / '. t( array( 'zh-cn'=>'充值卡管理 / 删除', 'zh-tw'=>'充值卡管理 / 刪除', 'en-us'=>'Card management / Delete' ) );
                                break;
                        }
                        $param = array_slice( $selector_array, 2 );
                        if( strcasecmp( $selector_array[2], 'auto-add' ) === 0 ){
                            include( 'os.cards.auto.inc.php' );
                        }
                        else{
                            include( 'os.cards.edit.inc.php' );
                        }
                    }
                    else{
                        $breadcrumb = $s .' / '. t( array( 'zh-cn'=>'充值卡管理', 'zh-tw'=>'充值卡管理', 'en-us'=>'Card management' ) );
                        $param = array_slice( $selector_array, 2 );
                        include('os.cards.inc.php');
                    }
                    break;
                case 'charges':
                    if( count( $selector_array ) > 2 && ( $selector_array[2]=='add' || $selector_array[2]=='edit' || $selector_array[2]=='delete') ){
                        switch( $selector_array[2]){
                            case 'add':
                                $breadcrumb = $s. ' / '. t( array( 'zh-cn'=>'充值记录 / 添加', 'zh-tw'=>'充值記錄 / 添加', 'en-us'=>'Charges / Add' ) );
                                break;
                            case 'edit':
                                $breadcrumb = $s. ' / '. t( array( 'zh-cn'=>'充值记录 / 编辑', 'zh-tw'=>'充值記錄 / 編輯', 'en-us'=>'Charges / Edit' ) );
                                break;
                            case 'delete':
                                $breadcrumb = $s. ' / '. t( array( 'zh-cn'=>'充值记录 / 删除', 'zh-tw'=>'充值記錄 / 刪除', 'en-us'=>'Charges / Delete' ) );
                                break;
                        }
                        $param = array_slice( $selector_array, 2 );
                        include( 'os.charge.edit.inc.php' );
                    }
                    else{
                        $breadcrumb = $s. ' / '. t( array( 'zh-cn'=>'充值记录', 'zh-tw'=>'充值記錄', 'en-us'=>'Charges' ) );
                        $param = array_slice( $selector_array, 2 );
                        include('os.charge.inc.php');
                    }
                    break;
                case 'orders':
                    if( count( $selector_array ) > 2 && ( $selector_array[2]=='add' || $selector_array[2]=='edit' || $selector_array[2]=='delete') ){
                        switch( $selector_array[2]){
                            case 'add':
                                $breadcrumb = $s. ' / '. t( array( 'zh-cn'=>'用户订单 / 添加', 'zh-tw'=>'用戶訂單 / 添加', 'en-us'=>'Orders / Add' ) );
                                break;
                            case 'edit':
                                $breadcrumb = $s. ' / '. t( array( 'zh-cn'=>'用户订单 / 编辑', 'zh-tw'=>'用戶訂單 / 編輯', 'en-us'=>'Orders / Edit' ) );
                                break;
                            case 'delete':
                                $breadcrumb = $s. ' / '. t( array( 'zh-cn'=>'用户订单 / 删除', 'zh-tw'=>'用戶訂單 / 刪除', 'en-us'=>'Orders / Delete' ) );
                                break;
                        }
                        $param = array_slice( $selector_array, 2 );
                        include( 'os.order.edit.inc.php' );
                    }
                    else{
                        $breadcrumb = $s. ' / '. t( array( 'zh-cn'=>'充值记录', 'zh-tw'=>'充值記錄', 'en-us'=>'Orders' ) );
                        $param = array_slice( $selector_array, 2 );
                        include('os.order.inc.php');
                    }
                    break;
            }
        }
        break;
}


function t( $array ){
    global $lang;
    return $array[ $lang ];
}

function url( $url, $ilang = null ){
    global $lang, $set_lang, $urlrewrite, $path_root;
    if( !is_null( $ilang ) ){
        $url = '/'.$ilang.'/'.trim_path( $url );
    }
    elseif( $set_lang ){
        $url = '/'.$lang.'/'.trim_path( $url );
    }
    else{
        $url = '/'.trim_path( $url );
    }
    if( $urlrewrite ){
        return $path_root.'/admin'.$url;
    }
    else{
        return $path_root.'/admin/index.php?'.PATH_NAME.'='.$url;
    }
}
function user_url( $url, $ilang = null ){
    global $lang, $set_lang, $urlrewrite, $path_root;
    if( !is_null( $ilang ) ){
        $url = '/'.$ilang.'/'.trim_path( $url );
    }
    elseif( $set_lang ){
        $url = '/'.$lang.'/'.trim_path( $url );
    }
    else{
        $url = '/'.trim_path( $url );
    }
    if( $urlrewrite ){
        return $path_root.$url;
    }
    else{
        return $path_root.'/index.php?'.PATH_NAME.'='.$url;
    }
}

function trim_path( $selector ){
    // remove leading slashes.
    while( strlen( $selector ) > 0 && $selector[0] == '/' ){
        $selector = substr( $selector, 1 );
    }

    // remove tailing slashes.
    while( strlen( $selector ) > 0 && $selector[ strlen( $selector ) - 1 ] == '/'){
        $selector = substr( $selector, 0, strlen( $selector ) - 1 );
    }

    return $selector;
}

function get_page_input_param( &$cond, &$page, &$num, $allowId=array() ){
    global $param;
    if( count( $param ) >= 2 ){
        $i = 0;
        $cnt = count( $param );
        while( $i < $cnt ){
            switch( $param[$i] ){
                case 'search':
                    $cond = $param[$i + 1];
                    if( !SqlFilter::is_allow( $cond, $allowId ) ){
                        $cond = '';
                    }
                    $i ++;
                    break;
                case 'page':
                    $page = (int) $param[ $i + 1 ];
                    $i ++;
                    break;
                case 'of-page-size':
                    $num = (int) $param[ $i + 1 ];
                    $i ++;
                    break;
            }
            $i ++;
        }
    }
}

function get_path_array(){
    global $selector_array, $param;
    return array_slice( $selector_array, 0, count( $selector_array ) - count( $param ) );
}

function gen_page_toolbar( $cond, $total, $size, $page ){
    $path  = get_path_array();
    $search = empty( $cond ) ? '': '/search/'. urlencode($cond);
    $pages = ceil( $total / $size );

    $record_start = ( $page - 1 ) * $size + 1 ;
    $record_start = $pages > 0 ? $record_start : 0;
    $record_end   = $page * $size <= $total ? $page * $size : $total;

    $page_start =  ($page % 10) == 0 ? $page : ( $page <= 10 ? 1 : $page - ( $page % 10 ) );
    $page_end   =  ( $page_start + 9 ) <= $pages ? ( $page_start + 9 ) : $pages;
    $page_end   =  $page_end == 10 ? 9 : $page_end;

    if( $page > 1 ){
        $ps = '<a href="'. url( implode( '/', $path ) . $search. '/page/'. ( $page - 1 ) . '/of-page-size/'. $size ) .'">'. t( array( 'zh-cn'=>'前一页', 'zh-tw'=>'前一頁', 'en-us'=>'Prev' ) ) .'</a> ';
    }
    else{
        $ps = '';
    }
    for( $i = $page_start ; $i <= $page_end ; $i ++ ){
        if( $i != $page ){
            $ps .= '<a href="'. url( implode( '/', $path ) . $search. '/page/'. $i . '/of-page-size/'. $size ) .'">'. $i .'</a> ';
        }
        else{
            $ps .= '<span class="current">'. $i .'</span> ';
        }
    }
    if( $page < $pages ){
        $ps .= '<a href="'. url( implode( '/', $path ) . $search. '/page/'. ( $page + 1 ) . '/of-page-size/'. $size ) .'">'. t( array( 'zh-cn'=>'后一页', 'zh-tw'=>'後一頁', 'en-us'=>'Next' ) ) .'</a>';
    }
    $p = str_replace('%',$pages,t(array('zh-cn'=>'共%页','zh-tw'=>'共%頁','en-us'=>'Total % pages'))).' ';
    $p .= t(array('zh-cn'=>'当前页码','zh-tw'=>'当前頁碼','en-us'=>'Page')) .': <input id="pagetool_page" type="text" value="'. $page .'" maxlength="10" size="3"/> ';
    $p .= t(array('zh-cn'=>'每页数量','zh-tw'=>'每頁數量','en-us'=>'Page size')) .': <input id="pagetool_size" type="text" value="'. $size .'" maxlength="10" size="3"/> ';
    $p .='<input type="button" value="Go" onclick="document.location=\'';
    $p .= url( implode( '/', $path ) );
    $p .= $search. '/page/\'+document.getElementById(\'pagetool_page\').value+\'/of-page-size/\'+document.getElementById(\'pagetool_size\').value;"/>';

    $zh_cn = '<div id="pagetool_left">显示共'. $total .'条记录中的'. $record_start .' - '. $record_end .'</div><div id="pagetool_right">'. $p .'</div>';
    $zh_tw = '<div id="pagetool_left">顯示共'. $total .'條記錄中的'. $record_start .' - '. $record_end .'</div><div id="pagetool_right">'. $p .'</div>';
    $en_us = '<div id="pagetool_left">'. $record_start .' - '. $record_end .' of '. $total .' records</div><div id="pagetool_right">'. $p .'</div>';

    $p = t( array( 'zh-cn'=>$zh_cn, 'zh-tw'=>$zh_tw, 'en-us'=>$en_us ) );
    $p = '<div id="pagetool">'. $p .'<div id="pagetool_num">'.$ps.'</div></div>';
    return $p;
}

function is_post(){
    return $_SERVER['REQUEST_METHOD']=='POST';
}

function gen_search_form( $cond, $exp ){
    $path  = get_path_array();
    $search = empty( $cond ) ? '': '/search/'. urlencode($cond);

    $form = '<div id="search_form">'.t( array('zh-cn'=>'搜索','zh-tw'=>'搜索','en-us'=>'Search') ).' <input id="search_content" class="box" type="text" value="'.htmlspecialchars($cond).'"/> <input type="button" value="Go" class="go" onclick="if(document.getElementById(\'search_content\').value!=\'\'){document.location=\'';
    $form .= url( implode( '/', $path ) );
    $form .= '/search/\'+document.getElementById(\'search_content\').value+\'/page/1/of-page-size/\'+document.getElementById(\'pagetool_size\').value;}';
    $form .= 'else{document.location=\'';
    $form .= url( implode( '/', $path ) );
    $form .= '/page/1/of-page-size/\'+document.getElementById(\'pagetool_size\').value;}"/><br/>';
    $form .= t($exp);
    $form .= '</div>';
    return $form;
}

function gen_search_url($cond, $page, $size){
    $path  = get_path_array();
    $search = empty( $cond ) ? '': '/search/'. urlencode($cond);
    return url( implode( '/', $path ) . $search. '/page/'.$page.'/of-page-size/'.$size );
}

function newConn($conf){
    global $sqlConf;
    $conn = &ADONewConnection($sqlConf[$conf]['type']); 
    if($sqlConf[$conf]['persist']){
        $conn->PConnect($sqlConf[$conf]['host'],$sqlConf[$conf]['username'],$sqlConf[$conf]['password'],$sqlConf[$conf]['database']);
    }
    else{
        $conn->Connect($sqlConf[$conf]['host'],$sqlConf[$conf]['username'],$sqlConf[$conf]['password'],$sqlConf[$conf]['database']);
    }
	$conn->Execute('set names utf8');
    return $conn;
}

function newLicConn( $pid ){
	$conn = newConn('default');
	$rs = $conn->Execute('select d_host, d_database, d_username, d_password from products where pid='.$pid);
	if( $rs && $rs->RecordCount() > 0 ){
		$host = $rs->fields[0];
		$db   = $rs->fields[1];
		$user = $rs->fields[2];
		$pass = $rs->fields[3];

		$cc = &ADONewConnection('mysql'); 
		$cc->Connect( $host, $user, $pass, $db );
		$conn->Execute('set names utf8');
		return $cc;
	}
	return null;
}

function get_uid($conf='default'){
    if( !isset( $_SESSION['UID'] ) ){
        $conn = newConn($conf);
        $sql = 'select UID from Users where Username='.$conn->qstr($_SESSION['Username']);
        $uid = $conn->GetOne($sql);
        $_SESSION['UID']=(int)$uid;
    }
    return (int)$_SESSION['UID'];
}

function ensure_admin_login(){
    if( !isset( $_SESSION['Username'] ) || !isset($_SESSION['IsAdmin']) || !$_SESSION['IsAdmin'] ){
        header('Location: /');
        exit;
    }
}

function update_license_key( $conf, $oid ){
	// to update license keys, simply remove the generated keys.

	$conn = newConn( $conf );

	$rs = &$conn->Execute('select a.OID,a.UID,a.PID,a.Number,c.Username,b.OutPath,b.Keyname from Orders as a left join Products as b on a.PID=b.PID, Users as c where a.oid=' .$oid .' and a.UID=c.UID');
	if (!$rs){ 
		return false;
	}
	$uid = $rs->fields[1];
	$pid = $rs->fields[2];
	$num = $rs->fields[3];
	$username = $rs->fields[4];
	$outPath  = $rs->fields[5];
	$keyname  = $rs->fields[6];

    $c = $outPath[ strlen($outPath) - 1 ];
    $outPath .= $c == "\\" ? '': "\\";
    $outPath .= $username."\\";
	$fn;

	for( $i = 1; $i <= $num ; $i ++ ){
        $name = $uid .'-'.$oid.'-'.$i;
        $fn = $outPath.$name.'-'.$keyname;
		if( file_exists( $fn ) ){
			unlink( $fn );
		}
		$fn = $outPath.$name.'.conf';
		if( file_exists( $fn ) ){
			unlink( $fn );
		}

	}
	return !file_exists( $fn );
}

?>
