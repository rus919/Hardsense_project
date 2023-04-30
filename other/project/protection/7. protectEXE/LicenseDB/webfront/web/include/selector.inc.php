<?php

// prevent user directly accessing this page.
if( !defined('VALID_ENTRY_POINT') ){
    exit;
}

include('include/sqlfilter.inc.php');
//
// $selector         indicates the path selector.
// $selector_array   indicates the path selector array.
// $breadcrumb       indicates the current location.
// $param            the parameter array for internal specific program.
// $selected_content the application result.
//

define('PATH_NAME','p');

$prevent_output = false;

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
    $selector_array=array('browse-products');
}
switch( $selector_array[0] ){
    case 'browse-products':
        $s = t( array( 'zh-cn'=>'产品首页', 'zh-tw'=>'產品首頁', 'en-us'=>'Products' ) );
        $breadcrumb = $s. ' / '. t( array( 'zh-cn'=>'所有产品', 'zh-tw'=>'所有產品', 'en-us'=>'All Products' ) );
        $param = array_slice( $selector_array, 1 );
        include('include/pd.all.inc.php');
        break;
    case 'login':
        include('include/login.inc.php');
        break;
    case 'logout':
        session_unset();
        header('Location: '.url('/'));exit;
        break;
    case 'register':
        $breadcrumb = t( array( 'zh-cn'=>'注册新账号', 'zh-tw'=>'註冊新賬號', 'en-us'=>'Register new user' ) );
        include('include/register.inc.php');
        break;
    case 'check':
        $param = array_slice( $selector_array, 1 );
        include('include/check.inc.php');
        break;
    case 'members':
        ensure_user_login();
        if( count( $selector_array ) > 1 ){
            $s = t( array( 'zh-cn'=>'会员中心', 'zh-tw'=>'會員中心', 'en-us'=>'Member Center' ) );
            switch( $selector_array[1] ){
                case 'my-account':
					$intro_pic = 'account.png';
                    $breadcrumb = $s. ' / '. t( array( 'zh-cn'=>'我的账号', 'zh-tw'=>'我的帳號', 'en-us'=>'My Account' ) );
                    $param = array_slice( $selector_array, 2 );
                    include('include/members.account.inc.php');
                    break;
                case 'cart':
					$intro_pic = 'cart.png';
                    if( count( $selector_array ) > 2 && ( $selector_array[2]=='add' || $selector_array[2]=='edit' || $selector_array[2]=='delete' ) ){
                        switch( $selector_array[2]){
                            case 'add':
                                $breadcrumb = $s. ' / '. t( array( 'zh-cn'=>'我的购物车 / 添加', 'zh-tw'=>'我的購物車 / 添加', 'en-us'=>'Shopping Cart / Add' ) );
                                break;
                            case 'edit':
                                $breadcrumb = $s. ' / '. t( array( 'zh-cn'=>'我的购物车 / 详情', 'zh-tw'=>'我的購物車 / 詳情', 'en-us'=>'Shopping Cart / Detail' ) );
                                break;
                            case 'delete':
                                $breadcrumb = $s. ' / '. t( array( 'zh-cn'=>'我的购物车 / 删除', 'zh-tw'=>'我的購物車 / 刪除', 'en-us'=>'Shopping Cart / Delete' ) );
                                break;
                        }
                        $param = array_slice( $selector_array, 2 );
                        include( 'members.cart.edit.inc.php' );
                    }
                    else{
                        $breadcrumb = $s. ' / '. t( array( 'zh-cn'=>'我的购物车', 'zh-tw'=>'我的購物車', 'en-us'=>'Shopping Cart' ) );
                        $param = array_slice( $selector_array, 2 );
                        include('include/members.cart.inc.php');
                    }
                    break;
                case 'charge-now':
					$intro_pic = 'charging.png';
                    if( count( $selector_array ) > 2 && ( $selector_array[2]=='add' || $selector_array[2]=='edit' ) ){
                        switch( $selector_array[2]){
                            case 'add':
                                $breadcrumb = $s. ' / '. t( array( 'zh-cn'=>'充值中心 / 添加', 'zh-tw'=>'充值中心 / 添加', 'en-us'=>'Charging Center / Add' ) );
                                break;
                            case 'edit':
                                $breadcrumb = $s. ' / '. t( array( 'zh-cn'=>'充值中心 / 详情', 'zh-tw'=>'充值中心 / 詳情', 'en-us'=>'Charging Center / Detail' ) );
                                break;
                        }
                        $param = array_slice( $selector_array, 2 );
                        include( 'members.charge-now.edit.inc.php' );
                    }
                    else{
                        $breadcrumb = $s. ' / '. t( array( 'zh-cn'=>'充值中心', 'zh-tw'=>'充值中心', 'en-us'=>'Charging Center' ) );
                        $param = array_slice( $selector_array, 2 );
                        include('include/members.charge-now.inc.php');
                    }
                    break;
                case 'download-key':
                    $param = array_slice( $selector_array, 2 );
                    include('include/members.download-key.inc.php');
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
        return $path_root.$url;
    }
    else{
        return $path_root.'/index.php?'.PATH_NAME.'='.$url;
    }
}

function admin_url( $url, $ilang = null ){
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

function gen_page_index( $cond, $total, $size, $page ){
    $path  = get_path_array();
    $search = empty( $cond ) ? '': '/search/'. urlencode($cond);
    $pages = ceil( $total / $size );

    $record_start = ( $page - 1 ) * $size + 1 ;
    $record_start = $pages > 0 ? $record_start : 0;
    $record_end   = $page * $size <= $total ? $page * $size : $total;

    $page_start =  $page - ( $page % 10 ) + 1;
    $page_end   =  ( $page + 10 ) <= $pages ? ( $page + 10 ) : $pages;

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

    $p = '<div id="pagetool"><div id="pagetool_num">'.$ps.'</div></div>';
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
        @$conn->PConnect($sqlConf[$conf]['host'],$sqlConf[$conf]['username'],$sqlConf[$conf]['password'],$sqlConf[$conf]['database']);
    }
    else{
        @$conn->Connect($sqlConf[$conf]['host'],$sqlConf[$conf]['username'],$sqlConf[$conf]['password'],$sqlConf[$conf]['database']);
    }
	$conn->Execute('set names utf8');
    return $conn;
}

function get_real_ip(){
     $ip = false;

     if(!empty($_SERVER['HTTP_CLIENT_IP'])){
          $ip = $_SERVER['HTTP_CLIENT_IP'];
     }

     if(!empty($_SERVER['HTTP_X_FORWARDED_FOR'])){
          $ips = explode(", ", $_SERVER['HTTP_X_FORWARDED_FOR']);
          if($ip){
               array_unshift($ips, $ip);
               $ip = false;
          }
          for($i = 0; $i < count($ips); $i++){
               if(!preg_match("/^(10|172\.16|192\.168)\./i", $ips[$i])){
                    if(version_compare(phpversion(), "5.0.0", ">=")){
                         if(ip2long($ips[$i]) != false){
                              $ip = $ips[$i];
                              break;
                         }
                    }
                    else{
                         if(ip2long($ips[$i]) != - 1){
                              $ip = $ips[$i];
                              break;
                         }
                    }
               }
          }
     }
     return ($ip ? $ip : $_SERVER['REMOTE_ADDR']);
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

function ensure_user_login(){
    if( !isset( $_SESSION['Username'] ) ){
        header('Location: '.url('/') );
        exit;
    }
}

function sql_strong_filter( &$sql, $arr ){
    $sql = strtolower( $sql );
    if( !in_array( $sql, $arr ) ){
        $sql = '';
    }
}

function validate_username($username){
    for( $i=0, $cnt = strlen( $username ) ; $i < $cnt ; $i ++ ){
        $c = strtolower( $username[ $i ] );
        if( $c >= 'a' && $c <='z' ){
        }
        elseif( $c >='0' && $c <='9' ){
        }
        elseif( $c =='.' || $c == '@' || $c =='-' || $c == '_' ){
        }
        else{
            return false;
        }
    }
    return true;
}

function lock_ip( $conf, $type, $minutes ){

    $conn = newConn($conf);
    $conn->Execute('delete * from LockIP where Time<'.time() );

    $sql = 'select Count from LockIP where Type='.$type.' and IP='.$conn->qstr( get_real_ip() );
    $uid = $conn->GetOne($sql);

    if( !empty( $uid ) && $uid > 0 ){
        $sql = 'update LockIP set Count='.(++$uid).',Time='. (time() + 60*$minutes ) .' where Type='.$type.' and IP='.$conn->qstr( get_real_ip() );
    }
    else{
        $sql = 'insert into LockIP (Type,IP,Time,Count) value ('.$type.','.$conn->qstr(get_real_ip()).','.(time()+60*$minutes).',1)';
    }
    $conn->Execute($sql);
}

function check_ip_lock($conf, $type, $count){
    $conn = newConn($conf);
    $sql = 'select count(*) from LockIP where Type='.$type.' and Count>='.$count.' and Time>'.time().' and IP='.$conn->qstr( get_real_ip() );
    $uid = $conn->GetOne($sql);
    return $uid > 0;
}

function gen_license_key($conf,$username,$uid,$key,$force=false,$hardwareid=''){
    global $keygen_filename;
    $selected_content = '';
    $conn = newConn($conf);
    $rs = &$conn->Execute('select a.OID,a.UID,c.Username,a.PID,b.Name,b.Price,a.Number,a.Time,a.IP,a.PaidTime,a.PaidIP,b.Keyname,b.DataName,b.OutPath,'.
                'c_LockHardwareID,'.   //14
                'c_LockCPU,'.
                'c_LockMAC,'.
                'c_LockBIOS,'.
                'c_LockHDD,'.
                'c_NumDaysEn,'.
                'c_NumDays,'.
                'c_NumExecEn,'.
                'c_NumExec,'.
                'c_ExpDateEn,'.
                'c_ExpDate,'.
                'c_CountryIdEn,'.
                'c_CountryId,'.
                'c_ExecTimeEn,'.
                'c_ExecTime,'.
                'c_TotalExecTimeEn,'.
                'c_TotalExecTime,'.        //30

                'a.ExpDate as aExpDate,'.
				'a.HardwareID'.
        ' from orders as a left join Products as b on a.PID=b.PID, Users as c where a.UID=c.UID and a.UID='.$uid.' and a.OID=' .$key);
    if (!$rs){ 
        $selected_content = $conn->ErrorMsg();
        return $selected_content;
    }

	$hardwareid = strlen( $hardwareid ) == 0 ? $rs->fields[32] : $hardwareid;
	$mc = $rs->fields[14] > 0 && strlen( $hardwareid ) > 0;

    $oid = $rs->fields[0];
    $num = $rs->fields[6];
    $keyname = $rs->fields[11];
    $dataName = $rs->fields[12];
    $outPath = $rs->fields[13];

    /**
     * Generate keys.
     */

    /*
    string DataFile = "D:\\MyWebsite\\My Keygen\\SEKeygen.dat" ;
    string OutputPath = "D:\\MyWebsite\\My Keygen\\output\\" ;
    string FilenameFormat = "1-1-(%s)";
    */
    $c = $outPath[ strlen($outPath) - 1 ];
    $outPath .= $c == "\\" ? '': "\\";
    $outPath .= $username."\\";

    if( !file_exists( $outPath ) ){
        if( !mkdir( $outPath, 0, true) ){
             $selected_content .= t( array( 'zh-cn'=>'无法生成KEY文件或权限不足，请联系管理员。', 'zh-tw'=>'無法生成KEY文件或權限不足，請聯繫管理員。', 'en-us'=>'Unable to create key file or permission errors, please contact administrator.' ) );
            return $selected_content;
        }
    }

    // build config

    $config  = "bool     LockHardwareID  = ".($rs->fields[14]?'true':'false')." ;\r\n";
    $config .= "bool     LockCPU         = ".($rs->fields[15]?'true':'false')." ;\r\n";
    $config .= "bool     LockMAC         = ".($rs->fields[16]?'true':'false')." ;\r\n";
    $config .= "bool     LockBIOS        = ".($rs->fields[17]?'true':'false')." ;\r\n";
    $config .= "bool     LockHDD         = ".($rs->fields[18]?'true':'false')." ;\r\n";

    $config .= "bool     NumDaysEn       = ".($rs->fields[19]?'true':'false')." ;\r\n";
    $config .= "uint32   NumDays         = ".$rs->fields[20]." ;\r\n";

    $config .= "bool     NumExecEn       = ".($rs->fields[21]?'true':'false')." ;\r\n";
    $config .= "uint32   NumExec         = ".$rs->fields[22]." ;\r\n";

    $config .= "bool     ExpDateEn       = ".($rs->fields[23]?'true':'false')." ;\r\n";

    /*
    $newTime = time() + $rs->fields[24] * ( 60 * 60 * 24 ) ;
    $newTime = date('Y-n-j', $newTime);
    */
    if( $rs->fields[31] > 0 ){
        $newTime = date('Y-n-j', $rs->fields[31] );
        $config .= "datetime ExpDate         = \"".$newTime."\" ;\r\n";
    }
    else{
        $config .= "datetime ExpDate         = \"2000-1-1\" ;\r\n";
    }



    $config .= "bool     CountryIdEn     = ".($rs->fields[25]?'true':'false')." ;\r\n";
    $config .= "uint32   CountryId       = ".$rs->fields[26]." ;\r\n";

    $config .= "bool     ExecTimeEn      = ".($rs->fields[27]?'true':'false')." ;\r\n";
    $config .= "uint32   ExecTime        = ".$rs->fields[28]." ;\r\n";

    $config .= "bool     TotalExecTimeEn = ".($rs->fields[29]?'true':'false')." ;\r\n";
    $config .= "uint32   TotalExecTime   = ".$rs->fields[30]." ;\r\n";

    $config .= "string   DataFile        = \"". addslashes($dataName)."\" ; \r\n";
    $config .= "string   OutputPath      = \"". addslashes($outPath) ."\" ; \r\n";

    for( $i = 1 ; $i <= $num ; $i ++ ){
        $name = $uid .'-'.$oid.'-'.$i;
        $fn = $outPath.$name.'-'.$keyname;
        if( !file_exists( $fn ) || $force ){
            $text = $config;
            $userid = ($username.'-'.$oid.'-'.$i);
            $conf =  $outPath. $name .'.conf';
            $text .= "string   UserID          = \"".addslashes($userid)."\" ;\r\n";
            $text .= "string   Remarks         = \""."Network authorization: oid-".$oid."\" ;\r\n";
            $text .= "string   HardwareID      = \"".addslashes($hardwareid)."\" ;\r\n";
            $text .= "string   FilenameFormat  = \"".$name."-%s\" ; \r\n";

            file_put_contents( $conf, $text );
            $out = shell_exec( $keygen_filename .' '. $conf );
            if( strpos( $out, 'generated successfully.' ) === false ){
                $selected_content .= t( array( 'zh-cn'=>'无法生成KEY文件，请联系管理员。', 'zh-tw'=>'無法生成KEY文件，請聯繫管理員。', 'en-us'=>'Unable to create key file, please contact administrator.' ) );
                break;
            }
        }
    }

    return $selected_content;
}


function update_license_key( $conf, $oid ){
	// to update license keys, simply remove the generated keys.

	$conn = newConn( $conf );

	$oid = (int)$oid;

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

function gen_order($conf, $username, $uid, $key, $type){
    $selected_content = '';

    $conn = newConn( $conf );
    $table_name = 'orders';

	// filter input
	$uid = (int)$uid;
	$key = (int)$key;
	$type = (int)$type;

   // verify is user's order. prevent sql injection.
    $sql = 'select count(*) from Orders where UID='.$uid.' and OID='.$key;
    $paid = (int)$conn->GetOne( $sql );

    if( $paid == 0 ){
        return fmsg( t(array( 'zh-cn'=>'这不是你的订单。', 'zh-tw'=>'這不是你的訂單。', 'en-us'=> 'this is not your order.' )) );
    }

    $conn->BeginTrans();

    // get amount.
    $sql = 'select amount from Users where UID='.$uid;
    $amount = (int)$conn->GetOne( $sql );

    // get order amount
    $sql = 'select sum(a.Number*b.Price) from '.$table_name.' as a left join Products as b on a.PID=b.PID, Users as c where a.UID=c.UID and a.UID='.$uid.' and a.OID='.$key;
    $order_amount = (int)$conn->GetOne( $sql );

    if( $amount < $order_amount ){
        $selected_content = '('.($amount - $order_amount) . ') ';
        $selected_content .= t(array( 'zh-cn'=>'余额不足以支付订单。', 'zh-tw'=>'餘額不足以支付訂單。', 'en-us'=>'Your amount is not enough to pay for the order.' ));

        $selected_content = fmsg( $selected_content );

        $conn->FailTrans();
        goto tran_out;
    }else{
        $remain_amount = $amount - $order_amount;
        $sql = 'update Users set amount='.$remain_amount.' where UID='.$uid;
        $conn->Execute($sql);
        if ($conn->ErrorNo() != 0){ 
            $selected_content = fmsg( $conn->ErrorMsg() );

            $conn->FailTrans();
            goto tran_out;
        }
    }

    // get expiration date.
    $sql = 'select c_ExpDateEn,c_ExpDate,a.PID,b.ExpDate from Products as a left join orders as b on a.pid=b.pid where b.uid='.$uid.' and b.oid='.$key;
    $rs = $conn->Execute( $sql );
    if( !$rs || $rs->RecordCount() == 0 ){
        $selected_content = fmsg( $conn->ErrorMsg() );

        $conn->FailTrans();
        goto tran_out;
    }

    $expDateEn = $rs->fields[0];
    $expDate   = $rs->fields[1];
    $pid       = $rs->fields[2];
    $oDate     = $rs->fields[3];


    // check order is paid
    $sql = 'select count(*) from Orders where PaidTime!=0 and UID='.$uid.' and OID='.$key;
    $paid = (int)$conn->GetOne( $sql );
    if( $paid == 0 ){
        //
        if( $expDateEn ){
            $oDate = time() + 60*60*24*$expDate;
        }

        $sql = 'update '.$table_name.' set '.
            'Type='.$type.','.
            'PaidTime='.time().','.
            'PaidIP='.$conn->qstr(get_real_ip()).','.
            'ExpDate='.$oDate.
            ' where PaidTime=0 and UID='.$uid.' and OID='.$key;
        $conn->Execute($sql);
        if ($conn->ErrorNo() != 0){ 
            $selected_content = fmsg( $conn->ErrorMsg() );

            $conn->FailTrans();
        }
        else{
            if( $type == 0 ){
                $selected_content = completed( array( 'zh-cn'=>'支付成功。您的帐户余额为： '.$remain_amount, 'zh-tw'=>'支付成功。您的帳戶餘額為： '.$remain_amount, 'en-us'=>'Payment Success.Your account amount is: '.$remain_amount ));
            }
            else{
                $selected_content = smsg(t(array( 'zh-cn'=>'支付成功。您的帐户余额为： '.$remain_amount, 'zh-tw'=>'支付成功。您的帳戶餘額為： '.$remain_amount, 'en-us'=>'Payment Success.Your account amount is: '.$remain_amount )));
            }
        }
    }
    else{
        if( $expDateEn ){
            if( $oDate > time() ){
                $oDate += 60*60*24*$expDate;
            }
            else{
                $oDate = time() + 60*60*24*$expDate;
            }
        }

        //renew
        $sql = 'update orders set ExpDate='.$oDate.' where UID='.$uid.' and OID='.$key;
        $conn->Execute($sql);
        if ($conn->ErrorNo() != 0){ 
            $selected_content = fmsg( $conn->ErrorMsg() );

            $conn->FailTrans();
            goto tran_out;
        }

        $sql='insert into '.$table_name.' (UID,PID,Type,Number,Time,IP,PaidTime,PaidIP,RenewId) values ('.
            $uid.','.
            $pid.','.
            $type.','.
            '1,'.
            time().','.
            $conn->qstr(get_real_ip()).','.
            time().','.
            $conn->qstr(get_real_ip()).','.
            $key.
            ')';

        $conn->Execute($sql);
        if ($conn->ErrorNo() != 0){ 
            $selected_content = fmsg( $conn->ErrorMsg() );

            $conn->FailTrans();
            goto tran_out;
        }
        else{
            if( $type == 0 ){
                $selected_content = completed( array( 'zh-cn'=>'支付成功。您的帐户余额为： '.$remain_amount, 'zh-tw'=>'支付成功。您的帳戶餘額為： '.$remain_amount, 'en-us'=>'Payment Success.Your account amount is: '.$remain_amount ));
            }
            else{
                $selected_content = smsg(t(array( 'zh-cn'=>'支付成功。您的帐户余额为： '.$remain_amount, 'zh-tw'=>'支付成功。您的帳戶餘額為： '.$remain_amount, 'en-us'=>'Payment Success.Your account amount is: '.$remain_amount )));
            }
        }
    }


    tran_out:
        $conn->CompleteTrans();

    return $selected_content;
}

function smsg( $msg ){
    return '(success) '.$msg;
}

function fmsg( $msg ){
    return '(fail) '.$msg;
}

function success( $msg ){
    echo smsg( $msg );
}

function fail( $msg ){
    echo fmsg( $msg );
}

?>
