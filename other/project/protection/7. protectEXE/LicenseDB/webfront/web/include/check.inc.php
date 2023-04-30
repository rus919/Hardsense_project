<?php
/*
   注：check前面可以加语言标识： zh-cn, zh-tw, en-us 用于返回特定语言的消息，不加则按系统默认设置。
      例如：　 index.php?p=/en-us/check/get-key/product/username/password-md5/hardware-id-base64/
 
   get-key: index.php?p=/check/get-key/product/username/password-md5/hardware-id-base64/
            返回KEY的内容,hardware_id 是可选的。

   query:   index.php?p=/check/query/product/username/password-md5/
            返回帐户相关信息的内容
   
   version: index.php?p=/check/version/product/
            返回版本号

   charge:  index.php?p=/check/charge/product/username/card-number/card-password/
            先充值，再用帐户余额添加订单或续费

   renew:   index.php?p=/check/renew/product/username/
            用账户余额添加订单或续费

   正确返回消息格式　"(success) ..."
   错误返回消息格式 "(fail) ..."

*/

// prevent user directly accessing this page.
if( !defined('VALID_ENTRY_POINT') ){
    exit;
}
$prevent_output = true;

$conf = 'default';
$conn = newConn($conf);
$lock_type = 100;

if( $max_try_count > 0 && check_ip_lock( $conf, $lock_type, $max_try_count ) ){
    fail( 'Multiple failure operations, temporarily deny any operation, please try later.' );
    exit;
}

ensure_parameter_quantity( 2 );

$action  = $param[0];
$product = $param[1];

$param = array_slice( $param, 2 );

switch( $action ){
    case 'get-key':
        ensure_parameter_quantity( 2 );

        $hardware_id = '';
        if( count( $param ) == 2 ){
            list( $username, $password ) = $param;
        }
        else if( count( $param ) == 3 ){
            list( $username, $password, $hardware_id ) = $param;
        }

        $sql = 'select UID from users where username='.$conn->qstr($username).' and password='.$conn->qstr($password);
        $uid = $conn->GetOne( $sql );
        if( $uid > 0 ){
            $sql = 'select OID from orders as a left join products as b on a.PID=b.PID where a.UID='.$uid.' and a.RenewID=0 and b.Identifier='.$conn->qstr($product);
            $oid = $conn->GetOne( $sql );
            if( $oid > 0 ){
                gen_license_key($conf, $username, $uid, $oid, false, base64_decode($hardware_id));
                downkey2( $conf, $oid, $username, $uid );
                exit;
            }
            else{
                fail( t( array( 'zh-cn'=>'无效产品或无此记录。', 'zh-tw'=>'無效產品或無此記錄。', 'en-us'=>'Invalid product or no records.' ) ) );
            }
        }
        else{
            fail( t( array( 'zh-cn'=>'无效用户。', 'zh-tw'=>'無效用戶。', 'en-us'=>'Invalid User.' ) ) );
        }
        break;
    case 'query':
        ensure_parameter_quantity( 2 );
        list( $username, $password ) = $param;
        //
        // get amount
        //
        $sql = 'select uid,amount from users where username='.$conn->qstr($username).' and password='.$conn->qstr($password);
        $rs = $conn->Execute( $sql );
        if(!$rs || $rs->RecordCount()==0 || $conn->ErrorNo() != 0 ){
            fail( t( array( 'zh-cn'=>'无效用户。', 'zh-tw'=>'無效用戶。', 'en-us'=>'Invalid User.' ) ) );
        }
        else{
            $uid = $rs->fields[0];
            $amount = $rs->fields[1];
            // get expDate
            $sql = 'select a.Pid,Name,Pic,Description,Url,Price,PriceVersion,a.Time,Published,Keyname,DataName,OutPath,Identifier,Version,'.
                        'c_LockHardwareID,'. //14
                        'c_LockCPU,'.
                        'c_LockMAC,'.
                        'c_LockBIOS,'.
                        'c_LockHDD,'.
                        'c_NumDaysEn,'.
                        'c_NumDays,'.
                        'c_NumExecEn,'.
                        'c_NumExec,'.
                        'c_ExpDateEn,'. //23
                        'c_ExpDate,'.
                        'c_CountryIdEn,'.
                        'c_CountryId,'.
                        'c_ExecTimeEn,'.
                        'c_ExecTime,'.
                        'c_TotalExecTimeEn,'.
                        'c_TotalExecTime,'.
                        'b.ExpDate as bExpDate'. //31
                ' from Products as a left join Orders as b on a.PID=b.PID where Identifier=' .$conn->qstr($product). ' and b.UID='.$uid.' and b.RenewID=0 limit 0,1';
            $rs = &$conn->Execute( $sql );
            if (!$rs || $rs->RecordCount() == 0 ){ 
                fail( t( array( 'zh-cn'=>'无效产品或无此记录。', 'zh-tw'=>'無效產品或無此記錄。', 'en-us'=>'Invalid product or no records.' ) ) );
            }
            else{
                success( t(array( 'zh-cn'=>'余额', 'zh-tw'=>'餘額', 'en-us'=>'Amount' )).': '.$amount. ' '.t(array( 'zh-cn'=>'到期时间', 'zh-tw'=>'到期時間', 'en-us'=>'Expiration Date' )).': '. date('Y-n-j',$rs->fields[31]) );
            }
        }
        break;
    case 'version':
        $sql = 'select Version from Products where Identifier='.$conn->qstr($product).' order by pid desc limit 0,1';
        $rs = $conn->Execute( $sql );
        if( !$rs || $rs->RecordCount() < 1 ){
            fail( t(array( 'zh-cn'=>'无效产品', 'zh-tw'=>'無效產品', 'en-us'=>'Invalid Product' )) );
        }
        else{
            success( $rs->fields[0] );
        }
        break;
    case 'charge':
        ensure_parameter_quantity( 3 );
        list( $username, $cardNumber, $password ) = $param;

        $sql = 'select uid,amount from users where username='.$conn->qstr($username);
        $rs = $conn->Execute( $sql );
        if(!$rs || $rs->RecordCount()==0 || $conn->ErrorNo() != 0 ){
            fail( t( array( 'zh-cn'=>'无效用户。', 'zh-tw'=>'無效用戶。', 'en-us'=>'Invalid User.' ) ) );
        }
        else{
            $uid = $rs->fields[0];

            $text = charge( $conf,$uid, $cardNumber, $password );
            if( strpos( $text, '(success)' ) !== false ){

                $oid = ensure_add_order( $conf, $uid, $product );
                if( $oid > 0 ){
                    echo gen_order($conf, $username, $uid, $oid, 1);
                }
                else{
                    echo( $oid. t( array( 'zh-cn'=>'（已充值金额保留在系统中，请联系管理员）。', 'zh-tw'=>'（已充值金額保留在系統中，請聯繫管理員）。', 'en-us'=>'(Charged amount is reserved in system, please contact your administrator).' ) ) );
                }
            }
            else{
                echo $text;
            }
        }
        break;
    case 'renew':
        ensure_parameter_quantity( 2 );
        list( $username, $password ) = $param;

        $sql = 'select uid,amount from users where username='.$conn->qstr($username).' and password='.$conn->qstr($password);
        $rs = $conn->Execute( $sql );
        if(!$rs || $rs->RecordCount()==0 || $conn->ErrorNo() != 0 ){
            fail( t( array( 'zh-cn'=>'无效用户。', 'zh-tw'=>'無效用戶。', 'en-us'=>'Invalid User.' ) ) );
        }
        else{
            $uid = $rs->fields[0];

            $oid = ensure_add_order( $conf, $uid, $product );
            if( $oid > 0 ){
                echo gen_order($conf, $username, $uid, $oid, 1);
            }
            else{
                echo $oid;
            }
        }
        break;
    default:
        if( $max_try_count > 0 ){
            lock_ip( $conf, $lock_type, $try_interval );
        }
        fail('Undefined behavior.');
        break;
}

function ensure_add_order($conf, $uid, $product){
    $conn = newConn($conf);

    $sql = 'select OID from orders as a left join products as b on a.PID=b.PID where a.UID='.$uid.' and a.RenewID=0 and b.Identifier='.$conn->qstr($product);
    $oid = $conn->GetOne( $sql );
    if( $oid > 0 ){
        return $oid;
    }
    else{
        $sql = 'select PID from Products where Identifier='.$conn->qstr($product).' order by pid desc limit 0,1';
        $rs = $conn->Execute( $sql );
        if( !$rs || $rs->RecordCount() < 1 ){
            return fmsg( t(array( 'zh-cn'=>'无效产品', 'zh-tw'=>'無效產品', 'en-us'=>'Invalid Product' )) );
        }
        $pid = $rs->fields[0];

        $sql='insert into Orders (UID,PID,Type,Number,Time,IP,PaidTime,PaidIP) values ('.
            $uid.','.
            $pid.','.
            '1,'.
            '1,'.
            time().','.
            $conn->qstr(get_real_ip()).','.
            '0,'.
            "''".
            ')';

        $conn->Execute($sql);
        if ($conn->ErrorNo() != 0){ 
            return fmsg( $conn->ErrorMsg() );
        }
        return $conn->Insert_ID();
    }
}

function ensure_parameter_quantity( $n ){
    global $param, $conf, $lock_type, $try_interval,$max_try_count,$error_prefix;

    if( count( $param ) < $n ){
        if( $max_try_count > 0 ){
            lock_ip( $conf, $lock_type, $try_interval );
        }
        fail('Missing parameters.');
        exit;
    }
}

function charge( $conf, $uid, $cardNumber, $password ){
    global $conn;

    $selected_content = '';
    $table_name='charge';

    $conn=newConn($conf);

    $conn->BeginTrans();

    $sql = 'select CardId,CardNumber,Password,Amount,GeneratedTime,UsedTime,Discard from Cards where CardNumber='.$conn->qstr( $cardNumber ).' and Password='. $conn->qstr( $password );

    $rs = $conn->Execute( $sql );
    if( $conn->ErrorNo() != 0 ){
        $selected_content =　fmsg( $conn->ErrorMsg() );
        $conn->FailTrans();goto tran_out;
    }
    else{
        if( ! $rs || $rs->RecordCount()<1 ){
            $selected_content = fmsg( t(array( 'zh-cn'=>'无效卡号或密码错误。', 'zh-tw'=>'無效卡號或密碼錯誤。', 'en-us'=>'Invalid card number or wrong password.' )) );
            $conn->FailTrans();goto tran_out;
        }
        else{
            // discard 
            if( $rs->fields[6] == 1 ){
                $selected_content = fmsg( t(array( 'zh-cn'=>'该卡已失效。', 'zh-tw'=>'該卡已失效。', 'en-us'=>'This card had beed discarded.' )) );
                $conn->FailTrans();goto tran_out;
            }
            elseif( !is_null( $rs->fields[5] ) ){
                $selected_content = fmsg( t(array( 'zh-cn'=>'该卡已被使用。', 'zh-tw'=>'該卡已被使用。', 'en-us'=>'This card had been used.' )) );
                $conn->FailTrans();goto tran_out;
            }
            else{
                $cardId = $rs->fields[0];
                $amount = $rs->fields[3];
                $rs->Close();

                $sql = 'update Cards set UsedTime='.$conn->sysTimeStamp.' where CardID='.$cardId;
                $conn->Execute( $sql );
                if( $conn->ErrorNo() != 0 ){
                    $selected_content = fmsg( $conn->ErrorMsg() );
                    $conn->FailTrans();goto tran_out;
                }
                else{
                    $sql = 'insert into '.$table_name.' (UID,Type,CardID,Amount,Remarks,Time) values ('.
                        $uid.','.
                        '1,'.
                        $cardId .','.
                        $amount .','.
                        '\'\','.
                        $conn->sysTimeStamp.
                        ')';
                    $conn->Execute( $sql );
                    if( $conn->ErrorNo() != 0 ){
                        $selected_content = fmsg( $conn->ErrorMsg() );
                        $conn->FailTrans();goto tran_out;
                    }
                    else{
                        $sql = "update Users set Amount=Amount+".$amount.' where UID='.$uid;
                        $conn->Execute( $sql );
                        if( $conn->ErrorNo() != 0 ){
                            $selected_content = fmsg( $conn->ErrorMsg() );
                            $conn->FailTrans();goto tran_out;
                        }
                        else{
                            $selected_content = smsg( t(array( 'zh-cn'=>'充值已成功，您本次充值', 'zh-tw'=>'充值已成功，您本次充值', 'en-us'=>'Charging successfully.You had  charged:' )).' '.$amount );
                        }
                    }
                }
            }
        }
    }
    tran_out:
        $conn->CompleteTrans();
        return $selected_content;
}

function downkey( $conf, $key, $username, $uid ){
    $conn = newConn($conf);
    $table_name = 'Orders';

    $rs = &$conn->Execute('select a.OID,a.UID,c.Username,a.PID,b.Name,b.Price,a.Number,a.Time,a.IP,a.PaidTime,a.PaidIP,b.Keyname,b.DataName,b.OutPath from '. $table_name .' as a left join Products as b on a.PID=b.PID, Users as c where a.UID=c.UID and c.Uid='.$uid.' and a.OID=' .$key);
    if (!$rs || $conn->ErrorNo() != 0 ){ 
        return fmsg( t(array( 'zh-cn'=>'没有权限下载此文件', 'zh-tw'=>'沒有權限下載此文件。', 'en-us'=>'You do not have permission to download this file.' )) );
    }

    $num = 1;
    if( !( $num >= 1 && $num <= $rs->fields[6] ) ){
        return fmsg( t(array( 'zh-cn'=>'没有权限下载此文件', 'zh-tw'=>'沒有權限下載此文件。', 'en-us'=>'You don\'t have permissions to download the unauthorized key file.' )) );
    }

    $outPath = $rs->fields[13];
    $c = $outPath[ strlen($outPath) - 1 ];
    $outPath .= $c == "\\" ? '': "\\";
    $outPath .= $username."\\";

    if( !file_exists( $outPath ) ){
        return fmsg( t(array( 'zh-cn'=>'系统错误，未找到ＫＥＹ路径，请联系管理员。', 'zh-tw'=>'系統錯誤，未找到ＫＥＹ路徑，請聯繫管理員。', 'en-us'=>'System error: key path not found,  please contact the administrator.' )) );
    }

    $keyname = $rs->fields[11];

    $name = $uid .'-'.$rs->fields[0].'-'.$num;
    $fn = $outPath.$name.'-'.$keyname;

    if( !file_exists( $fn ) ){
        return fmsg( t(array( 'zh-cn'=>'系统错误，ＫＥＹ文件未找到，请联系管理员。', 'zh-tw'=>'系統錯誤，ＫＥＹ文件未找到，請聯繫管理員。', 'en-us'=>'System error: key file not found,  please contact the administrator.' )) );
    }

    $rs->Close();
    $conn->Close();

    header('Content-Type: application/octet-stream;');
    echo file_get_contents( $fn );
}

function downkey2( $conf, $key, $username, $uid ){
    $conn = newConn($conf);
    $table_name = 'Orders';

    $rs = &$conn->Execute('select a.OID,a.UID,c.Username,a.PID,b.Name,b.Price,a.Number,a.Time,a.IP,a.PaidTime,a.PaidIP,b.Keyname,b.DataName,b.OutPath from '. $table_name .' as a left join Products as b on a.PID=b.PID, Users as c where a.UID=c.UID and c.Uid='.$uid.' and a.OID=' .$key);
    if (!$rs || $conn->ErrorNo() != 0 ){ 
        return fmsg( t(array( 'zh-cn'=>'没有权限下载此文件', 'zh-tw'=>'沒有權限下載此文件。', 'en-us'=>'You do not have permission to download this file.' )) );
    }

    $num = 1;
    if( !( $num >= 1 && $num <= $rs->fields[6] ) ){
        return fmsg( t(array( 'zh-cn'=>'没有权限下载此文件', 'zh-tw'=>'沒有權限下載此文件。', 'en-us'=>'You don\'t have permissions to download the unauthorized key file.' )) );
    }

    $outPath = $rs->fields[13];
    $c = $outPath[ strlen($outPath) - 1 ];
    $outPath .= $c == "\\" ? '': "\\";
    $outPath .= $username."\\";

    if( !file_exists( $outPath ) ){
        return fmsg( t(array( 'zh-cn'=>'系统错误，未找到ＫＥＹ路径，请联系管理员。', 'zh-tw'=>'系統錯誤，未找到ＫＥＹ路徑，請聯繫管理員。', 'en-us'=>'System error: key path not found,  please contact the administrator.' )) );
    }

    $keyname = $rs->fields[11];

    $name = $uid .'-'.$rs->fields[0].'-'.$num;
    $fn = $outPath.$name.'-'.$keyname;

    if( !file_exists( $fn ) ){
        return fmsg( t(array( 'zh-cn'=>'系统错误，ＫＥＹ文件未找到，请联系管理员。', 'zh-tw'=>'系統錯誤，ＫＥＹ文件未找到，請聯繫管理員。', 'en-us'=>'System error: key file not found,  please contact the administrator.' )) );
    }

    $rs->Close();
    $conn->Close();

    echo '<html><body><input type="hidden" ID="szKeyName" value="' . $keyname . '">';
    echo '<input type="hidden" ID="szKeyData" value="' . base64_encode(file_get_contents( $fn )) . '">';
    echo '<BUTTON STYLE="WIDTH:100" ID="btOK">确定</BUTTON><body></html>';
}

end_of_page:
?>