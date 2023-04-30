<?php


// prevent user directly accessing this page.
if( !defined('VALID_ENTRY_POINT') ){
    exit;
}

$conf = 'default';
$lock_type = 3;
$okay = true;

$is_new = false;
$is_del = false;
$key = 0;

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
        case 'edit':
            if( count( $param ) == 1 ){
                goto missing;
            }
            $key = (int)$param[1];
            break;
    }
}

include('./include/adodb5/adodb.inc.php');


$conn = newConn($conf);


$table_name = 'Charge';

// check connection.
if (!$conn){
    $selected_content = t( array( 'zh-cn'=>'连接数据库失败。', 'zh-tw'=>'連接數據庫失敗。', 'en-us'=>'Unable to connect database.' ) ); 
    goto end_of_page;
}

if( $is_new && is_post() ){
    $okay = false;

    if( !isset( $_POST['CardNumber'] ) || !isset( $_POST['Password'] ) ){
        $selected_content = t(array( 'zh-cn'=>'拒绝访问。', 'zh-tw'=>'拒絕訪問。', 'en-us'=>'Access denied.' ));
        goto end_of_page;
    }

    $cardNumber = $_POST['CardNumber'];
    $password = $_POST['Password'];
    $remarks  = '';

    if( strlen( $cardNumber ) > 32 || strlen( $password ) > 32 ){
        $selected_content = t(array( 'zh-cn'=>'无效卡格式。', 'zh-tw'=>'無效卡格式。', 'en-us'=>'Invalid card format.' ));
        goto end_of_page;
    }

    if( empty( $cardNumber ) || empty( $password ) ){
        $selected_content = t(array( 'zh-cn'=>'卡号或密码不能为空', 'zh-tw'=>'卡號或密碼不能為空。', 'en-us'=>'Card Number or password cannot be empty.' ));
        goto end_of_page;
    }

    if( $max_try_count > 0 && check_ip_lock( $conf, $lock_type, $max_try_count ) ){
        $selected_content = t( array( 'zh-cn'=>'多次充值错误，暂时禁止充值，请过后再试。',     'zh-tw'=>'多次充值錯誤，暫時禁止充值，請過後再試。',    'en-us'=>'You had charging error many times, temporarily refuse to charge, please try later.' ));
        goto end_of_page;
    }

    $sql = 'select CardId,CardNumber,Password,Amount,GeneratedTime,UsedTime,Discard from Cards where CardNumber='.$conn->qstr( $cardNumber ).' and Password='. $conn->qstr( $password );

    $rs = $conn->Execute( $sql );
    if( $conn->ErrorNo() != 0 ){
        $selected_content = '(0)'.$conn->ErrorMsg();
        goto end_of_page;
    }
    else{
        if( ! $rs || $rs->RecordCount()<1 ){
            $selected_content = t(array( 'zh-cn'=>'无效卡号或密码错误。', 'zh-tw'=>'無效卡號或密碼錯誤。', 'en-us'=>'Invalid card number or wrong password.' ));
            goto end_of_page;
        }
        else{
            // discard 
            if( $rs->fields[6] == 1 ){
                $selected_content = t(array( 'zh-cn'=>'该卡已失效。', 'zh-tw'=>'該卡已失效。', 'en-us'=>'This card had beed discarded.' ));
                goto end_of_page;
            }
            elseif( !is_null( $rs->fields[5] ) ){
                $selected_content = t(array( 'zh-cn'=>'该卡已被使用。', 'zh-tw'=>'該卡已被使用。', 'en-us'=>'This card had been used.' ));
                goto end_of_page;
            }
            else{
                $cardId = $rs->fields[0];
                $amount = $rs->fields[3];
                $rs->Close();

                $sql = 'update Cards set UsedTime='.$conn->sysTimeStamp.' where CardID='.$cardId;
                $conn->Execute( $sql );
                if( $conn->ErrorNo() != 0 ){
                    $selected_content = '(1)'.$conn->ErrorMsg();
                    goto end_of_page;
                }
                else{
                    $sql = 'insert into '.$table_name.' (UID,CardID,Amount,Remarks,Time) values ('.
                        get_uid( $conf ).','.
                        $cardId .','.
                        $amount .','.
                        $conn->qstr($remarks).','.
                        $conn->sysTimeStamp.
                        ')';
                    $conn->Execute( $sql );
                    if( $conn->ErrorNo() != 0 ){
                        $selected_content = '(2)'.$conn->ErrorMsg();
                        goto end_of_page;
                    }
                    else{
                        $sql = "update Users set Amount=Amount+".$amount.' where UID='.get_uid($conf );
                        $conn->Execute( $sql );
                        if( $conn->ErrorNo() != 0 ){
                            $selected_content = '(3)'.$conn->ErrorMsg();
                            goto end_of_page;
                        }
                        else{
                            $selected_content = completed(t(array( 'zh-cn'=>'充值已成功，您本次充值', 'zh-tw'=>'充值已成功，您本次充值', 'en-us'=>'Charging successfully.You had been charged:' )).' '.$amount);
                            $okay = true;
                            goto end_of_page;
                        }
                    }
                }
            }
        }
    }
}

new_begin:

$selected_content  = '<form method="post" action="'.url( implode( '/', $selector_array ) ).'">';
$selected_content .= '<table cellspacing="1" cellpadding="5" width="600" class="dg">';

if( $is_new ){
    $selected_content .= '<caption>'.t(array('zh-cn'=>'使用充值卡充值','zh-tw'=>'使用充值卡充值','en-us'=>'Charging by Prepaid Card')).'</caption>';

    $selected_content .= '<tr><td class="dg-cell">'.t(array('zh-cn'=>'充值卡号','zh-tw'=>'充值卡號','en-us'=>'Prepaid Card Number')).'</td><td class="dg-cell">';
    $selected_content .= '<input name="CardNumber" type="text" value="" maxlength="32" class="lsn"/></td></tr>';

    $selected_content .= '<tr><td class="dg-cell">'.t(array('zh-cn'=>'充值卡密码','zh-tw'=>'充值卡密碼','en-us'=>'Prepaid Card Password')).'</td><td class="dg-cell">';
    $selected_content .= '<input name="Password" type="text" value="" maxlength="32" class="lsn"/></td></tr>';

    $selected_content .= '<tr><td class="dg-cell">'.t(array('zh-cn'=>'备注','zh-tw'=>'備註','en-us'=>'Remarks')).'</td><td class="dg-cell">';
    $selected_content .= '<textarea name="Remarks" rows="6" cols="80" class="ledit" disabled="disabled"></textarea></td></tr>';

    $selected_content .= '</table><br/>';

    $selected_content .= '<div id="form_toolbar">';
    $selected_content .= '<div id="form_toolbar_left"><input class="lbtn" type="submit" value="'.t( array('zh-cn'=>'立即充值','zh-tw'=>'立即充值', 'en-us'=>'Charge Now') ) .'"/></div>';
    $selected_content .= '<div id="form_toolbar_right"></div>';
}
else{
    $rs = &$conn->Execute('select a.CID,a.UID,a.CardID,b.CardNumber,a.Credential,a.Amount,a.Remarks,a.Time from '. $table_name .' as a left join Cards as b on a.CardID=b.CardID where a.UID='.get_uid($conf).' and a.CID=' .$key);
    if (!$rs){ 
        $selected_content = $conn->ErrorMsg();
        goto end_of_page;
    }
	if(  $rs->RecordCount() == 0 ){
        $selected_content = t(array('zh-cn'=>'无效访问','zh-tw'=>'無效訪問','en-us'=>'Invalid Accessing.'));
        goto end_of_page;
	}

    $selected_content .= '<tr><td width="100" class="dg-cell">ID</td><td class="dg-cell">';
    $selected_content .= htmlspecialchars( $rs->fields[0] ).'</td></tr>';

    $selected_content .= '<tr><td class="dg-cell">'.t( array( 'zh-cn'=>'充值方式', 'zh-tw'=>'充值方式', 'en-us'=>'Payment Method' ) ).'</td><td class="dg-cell">';
    $selected_content .= ( !empty($rs->fields[2]) ?
            t(array('zh-cn'=>'充值卡','zh-tw'=>'充值卡','en-us'=>'Prepaid Card'))
           :t(array('zh-cn'=>'网银充值','zh-tw'=>'網銀充值','en-us'=>'Online Bank'))
                                                   ).'</td></tr>';

    $selected_content .= '<tr><td class="dg-cell">'.t(array('zh-cn'=>'充值卡号/网银订单号','zh-tw'=>'充值卡號/網銀訂單號','en-us'=>'Card No. / Order No.')).'</td><td class="dg-cell">';
    $selected_content .= ( !empty($rs->fields[2]) ? $rs->fields[3] : $rs->fields[4] ).'</td></tr>';

    $selected_content .= '<tr><td class="dg-cell">'.t(array('zh-cn'=>'金额','zh-tw'=>'金額','en-us'=>'Amount') ).'</td><td class="dg-cell">';
    $selected_content .= htmlspecialchars( $rs->fields[5] ).'</td></tr>';

    $selected_content .= '<tr><td class="dg-cell">'.t( array( 'zh-cn'=>'备注', 'zh-tw'=>'備註', 'en-us'=>'Remarks' ) ).'</td><td class="dg-cell">';
    $selected_content .= htmlspecialchars( $rs->fields[6] ).'</td></tr>';

    $selected_content .= '<tr><td class="dg-cell">'.t(array('zh-cn'=>'充值时间','zh-tw'=>'充值時間','en-us'=>'Charging Time') ).'</td><td class="dg-cell">';
    $selected_content .= htmlspecialchars( $rs->fields[7] ).'</td></tr>';

    $selected_content .= '</table><br/>';
}

$selected_content .= '<div id="edit-return"><a href="'.url( implode( '/', get_path_array() ). '/'. implode( '/', array_slice( $param, $is_new? 1:2 ) ) ).'">'.t( array( 'zh-cn'=>'返回', 'zh-tw'=>'返回', 'en-us'=>'Return' ) ).'</a></div>';
$selected_content .= '</form>';

function completed( $text ){
    global $is_new, $param;
    $text .= '<br/><br/><input type="button" value="'.t( array( 'zh-cn'=>'返回', 'zh-tw'=>'返回', 'en-us'=>'Return' ) ).'" ';
    $text .= 'onclick="document.location=\''.str_replace("'","\'",url( implode( '/', get_path_array() ). '/'. implode( '/', array_slice( $param, $is_new? 1:2 ) ) )).'\';"/>';
    return $text;
}

end_of_page:
    if( !$okay && $max_try_count > 0){
        lock_ip( $conf, $lock_type, $try_interval );
    }
?>