<?php


// prevent user directly accessing this page.
if( !defined('VALID_ENTRY_POINT') ){
    exit;
}

$is_new = false;
$is_del = false;
$key = '';

if( count( $param ) == 0 ){
missing:
    $selected_content = t( array( 'zh-cn'=>'缺失参数。', 'zh-tw'=>'缺失參數。', 'en-us'=>'Missing parameters.' ) ); 
    goto end_of_page;
}
else{
    switch( strtolower( $param[0] ) ){
        case 'add':
            $is_new = true;
            if( !is_post() ){
                goto new_begin;
            }
            break;
        case 'delete':
            if( count( $param ) == 1 ){
                goto missing;
            }
            $is_del = true;
            $key = (int)$param[1];
            break;
        case 'edit':
            if( count( $param ) == 1 ){
                goto missing;
            }
            $key = (int)$param[1];
            break;
    }
}

include('../include/adodb5/adodb.inc.php');

$conn = newConn('default');

$table_name = 'orders';

// check connection.
if (!$conn){
    $selected_content = t( array( 'zh-cn'=>'连接数据库失败。', 'zh-tw'=>'連接數據庫失敗。', 'en-us'=>'Unable to connect database.' ) ); 
    goto end_of_page;
}

if( $is_new ){
    if( empty($_POST['UID']) || empty($_POST['PID']) || empty($_POST['Number']) ){
        $selected_content = t(array( 'zh-cn'=>'UID,PID,Number 不能为空。', 'zh-tw'=>'UID,PID,Number 不能為空。', 'en-us'=>'UID,PID,Number cannot be empty.' ));
        goto end_of_page;
    }
    $sql='insert into '.$table_name.' (UID,PID,Number,Time,IP,PaidTime,PaidIP) values ('.
        (int)($_POST['UID']).",".
        (int)($_POST['PID']).",".
        (int)($_POST['Number']).",".
        strptime('Y-n-j G:i:s',$_POST['Time']).",".
        $conn->qstr($_POST['IP']).','.
        (empty($_POST['PaidTime'])?'0':strptime('Y-n-j G:i:s',$_POST['PaidTime'])).','.
        $conn->qstr($_POST['PaidIP']).
        ')';

    $conn->Execute($sql);
    if ($conn->ErrorNo() != 0){ 
        $selected_content = $conn->ErrorMsg();
    }
    else{
        $selected_content = completed( array( 'zh-cn'=>'添加成功。', 'zh-tw'=>'添加成功。', 'en-us'=>'Adding Success.' ) );
    }
    goto end_of_page;
}

if( $is_del ){
    $conn->Execute('delete from '.$table_name.' where oid='. $key );
    if ($conn->ErrorNo() != 0){ 
        $selected_content = $conn->ErrorMsg();
    }
    else{
        $selected_content = completed( array( 'zh-cn'=>'删除成功。', 'zh-tw'=>'刪除成功。', 'en-us'=>'Deleting Success.' ) );
    }
    goto end_of_page;
}
else{
    if( is_post() ){
		if( isset( $_POST['mc'] ) ){
			$sql = 'update '.$table_name.' set '.
				'HardwareID='.$conn->qstr($_POST['mc']).
				' where OID='.$key;
			$conn->Execute($sql);
			if ($conn->ErrorNo() != 0){ 
				$selected_content = $conn->ErrorMsg();
			}
			else{
				if (!update_license_key('default', $key)){ 
					$selected_content = t(array( 'zh-cn'=>'无法删除旧的ＫＥＹ文件。', 'zh-tw'=>'無法刪除舊的ＫＥＹ文件', 'en-us'=>'Unable to delete the old keys.' ));
					goto end_of_page;
				}
				$selected_content = completed( array( 'zh-cn'=>'更新成功。', 'zh-tw'=>'更新成功。', 'en-us'=>'Updating Success.' ) );
			}
			goto end_of_page;
		}
		else{
			$sql = 'update '.$table_name.' set '.
				'Number='.(int)($_POST['Number']).','.
				'Time='.strptime('Y-n-j G:i:s',$_POST['Time']).','.
				'IP='.$conn->qstr($_POST['IP']).','.
				'PaidTime='. (empty($_POST['PaidTime'])?'0':strptime('Y-n-j G:i:s',$_POST['PaidTime'])).','.
				'PaidIP='.$conn->qstr($_POST['PaidIP']).
				' where OID='.$key;
			$conn->Execute($sql);
			if ($conn->ErrorNo() != 0){ 
				$selected_content = $conn->ErrorMsg();
			}
			else{
				$selected_content = completed( array( 'zh-cn'=>'更新成功。', 'zh-tw'=>'更新成功。', 'en-us'=>'Updating Success.' ) );
			}
			goto end_of_page;
		}
    }
    else{
		//hardwareid 12
		//c_LockHardwareID 13
        $rs = &$conn->Execute('select a.OID,a.UID,a.PID,b.Name,a.Number,a.Time,a.IP,a.PaidTime,a.PaidIP,c.Username,a.Type,a.RenewId,a.HardwareID,b.c_LockHardwareID from Orders as a left join Products as b on a.PID=b.PID, Users as c where a.oid=' .$key .' and a.UID=c.UID');
        if (!$rs){ 
            $selected_content = $conn->ErrorMsg();
            goto end_of_page;
        }
    }
}

$mc =  $rs->fields[13]>0 ;

new_begin:

$selected_content  = '<form method="post" action="'.url( implode( '/', $selector_array ) ).'">';
$selected_content .= '<table cellspacing="1" cellpadding="5" width="600" class="dg">';

$selected_content .= '<tr><td width="100" class="dg-cell">ID</td><td class="dg-cell">';
$selected_content .= ($is_new?'': htmlspecialchars( $rs->fields[0] )).'</td></tr>';

$selected_content .= '<tr><td width="100" class="dg-cell">'.t(array( 'zh-cn'=>'用户名', 'zh-tw'=>'用戶名', 'en-us'=>'Username' )).'</td><td class="dg-cell">';
$selected_content .= ($is_new?
                       '<input name="UID" class="ledit" type="text" value="1" maxlength="10"/>'
                       :'<a href="'.url('/order-system/customers/edit/'.$rs->fields[1]).'">'.htmlspecialchars($rs->fields[9]).'</a>'
                      ).
                      '</td></tr>';

$selected_content .= '<tr><td width="100" class="dg-cell">'.t(array( 'zh-cn'=>'产品名称', 'zh-tw'=>'產品名稱', 'en-us'=>'Product Name' )).'</td><td class="dg-cell">';
$selected_content .= ($is_new?
                        '<input name="PID" class="ledit" type="text" value="1" maxlength="10"/>'
                       :'<a href="'.url('/order-system/products/edit/'.$rs->fields[2]).'">'.htmlspecialchars($rs->fields[3]).'</a>').
                      '</td></tr>';
if( !$is_new ){
    if( $rs->fields[11] == 0 ){
	    $selected_content .= '<tr><td class="dg-cell">'.t(array( 'zh-cn'=>'订单来源', 'zh-tw'=>'訂單來源', 'en-us'=>'Order From' )).'</td><td class="dg-cell">';
        switch( $rs->fields[10] ){
            case 0:
                $selected_content .= t(array( 'zh-cn'=>'从网站添加订单', 'zh-tw'=>'從網站添加訂單', 'en-us'=>'From website' ));
                break;
            case 1:
                $selected_content .= t(array( 'zh-cn'=>'从客户端软件添加订单', 'zh-tw'=>'從客戶端軟件添加訂單', 'en-us'=>'From client side software' ));
                break;
        }
    }
    else{
	    $selected_content .= '<tr><td class="dg-cell">'.t(array( 'zh-cn'=>'充值方式', 'zh-tw'=>'充值方式', 'en-us'=>'Charging Method' )).'</td><td class="dg-cell">';
        switch( $rs->fields[10] ){
            case 0:
                $selected_content .= t(array( 'zh-cn'=>'从网站续费', 'zh-tw'=>'從網站續費', 'en-us'=>'Renew from website' ));
                break;
            case 1:
                $selected_content .= t(array( 'zh-cn'=>'从客户端软件续费', 'zh-tw'=>'從客戶端軟件續費', 'en-us'=>'Renew from client side software' ));
                break;
        }
    }
    $selected_content .= '</td></tr>';
}

$selected_content .= '<tr><td class="dg-cell">'.t(array( 'zh-cn'=>'购买数量', 'zh-tw'=>'購買數量', 'en-us'=>'Number' )).'</td><td class="dg-cell">';
$selected_content .= htmlspecialchars( $rs->fields[4] ) .'</td></tr>';

$selected_content .= '<tr><td class="dg-cell">'.t(array( 'zh-cn'=>'下单时间', 'zh-tw'=>'下單時間', 'en-us'=>'Order Time' )).'</td><td class="dg-cell">';
$selected_content .= htmlspecialchars( date('Y-n-j G:i:s',$rs->fields[5]) ) .'</td></tr>';

$selected_content .= '<tr><td class="dg-cell">'.t(array( 'zh-cn'=>'下单时IP', 'zh-tw'=>'下單時IP', 'en-us'=>'Ordering IP' )).'</td><td class="dg-cell">';
$selected_content .= htmlspecialchars( $rs->fields[6] ) .'</td></tr>';

$selected_content .= '<tr><td class="dg-cell">'.t(array( 'zh-cn'=>'付款时间', 'zh-tw'=>'付款時間', 'en-us'=>'Paid Time' )).'</td><td class="dg-cell">';
$selected_content .= htmlspecialchars( $rs->fields[7]==0?'': date('Y-n-j G:i:s',$rs->fields[7]) ).'</td></tr>';

$selected_content .= '<tr><td class="dg-cell">'.t(array( 'zh-cn'=>'付款时IP', 'zh-tw'=>'付款時IP', 'en-us'=>'Renewing IP' )).'</td><td class="dg-cell">';
$selected_content .= htmlspecialchars( $rs->fields[8] ) .'</td></tr>';

if( !$is_new && $mc ){
	$selected_content .= '<tr><td class="dg-cell">'.t(array( 'zh-cn'=>'机器码', 'zh-tw'=>'機器碼', 'en-us'=>'Machine Code' )).'</td><td class="dg-cell">';
	$selected_content .= '<input name="mc" type="text" class="lbtn" value="'.htmlspecialchars( $rs->fields[12] ) .'" maxlength="40" size="40"/>';
	$selected_content .= '</td></tr>';
}

$selected_content .= '</table>';
$selected_content .= '<br/><div id="form_toolbar">';
$selected_content .= '<div id="form_toolbar_left"><input class="lbtn" type="submit" '.(!$is_new && $mc?'':'disabled="disabled" ').'value="'.t( $is_new? array('zh-cn'=>'添加','zh-tw'=>'添加', 'en-us'=>'Add') : array('zh-cn'=>'更新','zh-tw'=>'更新', 'en-us'=>'Update') ) .'"/></div>';
$selected_content .= '<input class="lbtn" type="button" disabled="disabled" value="'.t( array('zh-cn'=>'删除','zh-tw'=>'刪除', 'en-us'=>'Delete') ) .'" ';
$selected_content .= 'onclick="document.location=\''.str_replace("'","\'",url( implode( '/', get_path_array() ). '/delete/'. implode( '/', array_slice( $param, 1) ) )).'\';"/></div><div id="edit-return"><a href="'.url( implode( '/', get_path_array() ). '/'. implode( '/', array_slice( $param, $is_new? 1:2 ) ) ).'">'.t( array( 'zh-cn'=>'返回', 'zh-tw'=>'返回', 'en-us'=>'Return' ) ).'</a></div>';
$selected_content .= '</form>';

function completed( $t ){
    global $is_new, $param;
    $text  = t( $t ); 
    $text .= '<br/><br/><input type="button" value="'.t( array( 'zh-cn'=>'返回', 'zh-tw'=>'返回', 'en-us'=>'Return' ) ).'" ';
    $text .= 'onclick="document.location=\''.str_replace("'","\'",url( implode( '/', get_path_array() ). '/'. implode( '/', array_slice( $param, $is_new? 1:2 ) ) )).'\';"/>';
    return $text;
}

end_of_page:
?>