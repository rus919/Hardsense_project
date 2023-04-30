<?php


// prevent user directly accessing this page.
if( !defined('VALID_ENTRY_POINT') ){
    exit;
}

$is_new = false;
$is_del = false;
$key = 0;

if( count( $param ) == 0 ){
missing:
    $selected_content = t( array( 'zh-cn'=>'缺失参数。', 'zh-tw'=>'缺失參數。', 'en-us'=>'Missing parameters.' ) ); 
    goto end_of_page;
}
else{
    include('./include/adodb5/adodb.inc.php');

    $conf = 'default';
    $conn = newConn($conf);

    $table_name = 'Orders';

    // check connection.
    if (!$conn){
        $selected_content = t( array( 'zh-cn'=>'连接数据库失败。', 'zh-tw'=>'連接數據庫失敗。', 'en-us'=>'Unable to connect database.' ) ); 
        goto end_of_page;
    }

    switch( strtolower( $param[0] ) ){
        //
        // add
        //
        case 'add':
            if( count( $param ) == 1 ){
                goto missing;
            }
            $is_new = true;
            $key = (int)$param[1];

            // add to cart
            if( is_post() ){

                /*
                if( !isset( $_POST['Number'] ) ){
                    $selected_content = t(array( 'zh-cn'=>'拒绝访问。', 'zh-tw'=>'拒絕訪問。', 'en-us'=>'Access denied.' ));
                    goto end_of_page;
                }

                $number = $_POST['Number'];
                if( empty($number) ){
                    $selected_content = t(array( 'zh-cn'=>'Number 不能为空', 'zh-tw'=>'Number 不能為空。', 'en-us'=>'Number cannot be empty.' ));
                    goto end_of_page;
                }

                if( $number < 1 ){
                    $selected_content = t(array( 'zh-cn'=>'购买数量必须大于1', 'zh-tw'=>'購買數量必須大於1', 'en-us'=>'You must buy more than 1 quantity.' ));
                    goto end_of_page;
                }
                */

                $number = 1;

                if( $conn->GetOne('select count(*) from Products where PID='.$key ) == 0 ){
					$selected_content = t(array('zh-cn'=>'无效访问','zh-tw'=>'無效訪問','en-us'=>'Invalid Accessing.'));
					goto end_of_page;
				}

                $sql='insert into '.$table_name.' (UID,PID,Number,Time,IP,PaidTime,PaidIP) values ('.
                    get_uid($conf).','.
                    $key.','.
                    $number.','.
                    time().','.
                    $conn->qstr(get_real_ip()).','.
                    '0,'.
                    "''".
                    ')';

                $conn->Execute($sql);
                if ($conn->ErrorNo() != 0){ 
                    $selected_content = $conn->ErrorMsg();
                }
                else{
                    $selected_content = completed( array( 'zh-cn'=>'已添加到您的购物车。', 'zh-tw'=>'已添加到您的購物車。', 'en-us'=>'This product has been added to your shopping cart.' ) );
                }
                goto end_of_page;
            }
            else{
                $rs = &$conn->Execute('select PID,Name,Pic,Description,Url,Price,PriceVersion,Time,Published from Products where PID='.$key );
                if (!$rs){ 
                    $selected_content = $conn->ErrorMsg();
                    goto end_of_page;
                }
				if(  $rs->RecordCount() == 0 ){
					$selected_content = t(array('zh-cn'=>'无效访问','zh-tw'=>'無效訪問','en-us'=>'Invalid Accessing.'));
					goto end_of_page;
				}
                $selected_content = '<table cellspacing="1" cellpadding="5" width="600">';
                $selected_content .= '<tr>';
                $selected_content .= '<td width="150"><img border="0" src="'.$rs->fields[2].'"/></td>';
                $selected_content .= '<td>';
                $selected_content .=    '<div class="ptitle">'.$rs->fields[1].'</div>';
                $selected_content .=    '<div class="pintro">'.$rs->fields[3].'</div>';
                $selected_content .=    '<div class="pmore"><a href="'.$rs->fields[4].'" target="_blank">'.t(array('zh-cn'=>'了解更多','zh-tw'=>'了解更多','en-us'=>'More')).'</a></div>';
                $selected_content .= '</td>';
                $selected_content .= '</tr>';
                $selected_content .= '</table>';

                $selected_content .= '<form method="post" action="'.url( implode( '/', $selector_array ) ).'">';
                $selected_content .= '<table cellspacing="1" cellpadding="5" width="600" class="dg">';

                $selected_content .= '<tr><td class="dg-cell">'.t( array( 'zh-cn'=>'产品名称', 'zh-tw'=>'產品名稱', 'en-us'=>'Product Name' ) ).'</td><td class="dg-cell">';
                $selected_content .= htmlspecialchars( $rs->fields[1] ).'</td></tr>';

                $selected_content .= '<tr><td class="dg-cell">'.t( array( 'zh-cn'=>'单价', 'zh-tw'=>'單價', 'en-us'=>'Price' ) ).'</td><td class="dg-cell">';
                $selected_content .= htmlspecialchars( $rs->fields[5] ).'</td></tr>';

            /*
                $selected_content .= '<tr><td class="dg-cell">'.t( array( 'zh-cn'=>'购买数量', 'zh-tw'=>'購買數量', 'en-us'=>'Number' ) ).'</td><td class="dg-cell">';
                $selected_content .= '<input name="Number" class="lnum" type="text" value="1" maxlength="10"/></td></tr>';
            */
                $selected_content .= '</table><br/>';
            }
            break;

        //
        // delete
        //
        case 'delete':
            if( count( $param ) == 1 ){
                goto missing;
            }
            $is_del = true;
            $key = (int)$param[1];

            $conn->Execute('delete from '.$table_name.' where PaidTime=0 and UID='.get_uid($conf).' and OID='. $key );
            if ($conn->ErrorNo() != 0){ 
                $selected_content = $conn->ErrorMsg();
            }
            else{
                $selected_content = completed( array( 'zh-cn'=>'删除成功。', 'zh-tw'=>'刪除成功。', 'en-us'=>'Deleting Success.' ) );
            }
            goto end_of_page;
            break;

        //
        // edit
        //
        case 'edit':
            if( count( $param ) == 1 ){
                goto missing;
            }
            $key = (int)$param[1];

            // edit(view only) mode
            if( is_post() ){
				if( isset( $_POST['mc'] ) ){
					$mc = trim($_POST['mc']);
					if( strlen( $mc ) == 0 ){
	                    $selected_content = t(array( 'zh-cn'=>'请输入机器码。', 'zh-tw'=>'請輸入機器碼。', 'en-us'=>'Please enter the machine code.' ));
						goto end_of_page;
					}
					else if( strlen( $mc ) > 40 ){
	                    $selected_content = t(array( 'zh-cn'=>'机器码最长４０位。', 'zh-tw'=>'機器碼最長４０位。', 'en-us'=>'The maximun length of the machine code is only 40.' ));
						goto end_of_page;
					}
					else{
						$conn->Execute('update '.$table_name.' set HardwareID='.$conn->qstr($mc).' where HardwareID=\'\' and OID='.$key);
						update_license_key( 'default', $key );
					}
				}
				else{
                    $selected_content = gen_order($conf, $_SESSION['Username'], get_uid($conf), $key, 0);
                    update_license_key( 'default', $key );
                    goto end_of_page;
				}
            }
            else{

            }
            break;
    }
}


$mc = false;

// view only
if( !$is_new ){
    $rs = &$conn->Execute('select a.OID,a.UID,c.Username,a.PID,b.Name,b.Price,a.Number,a.Time,a.IP,a.PaidTime,a.PaidIP,b.Keyname,b.DataName,b.OutPath,'.
                'c_LockHardwareID,'. //14
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
                'c_TotalExecTime,'.
                'a.ExpDate aExpDate,'.
				'a.HardwareID'.     //32
        ' from '. $table_name .' as a left join Products as b on a.PID=b.PID, Users as c where a.UID=c.UID and a.UID='.get_uid($conf).' and a.OID=' .$key);
    if (!$rs){ 
        $selected_content = $conn->ErrorMsg();
        goto end_of_page;
    }
	if(  $rs->RecordCount() == 0 ){
        $selected_content = t(array('zh-cn'=>'无效访问','zh-tw'=>'無效訪問','en-us'=>'Invalid Accessing.'));
        goto end_of_page;
	}

    if( $rs->fields[9] > 0 && $rs->fields[14] > 0 && strlen(trim($rs->fields[32])) == 0 ){
		$mc = true;
        $selected_content  = '<form method="post" action="'.url( implode( '/', $selector_array ) ).'">';
	}
	else{
        $selected_content  = '<form method="post" action="'.url( implode( '/', $selector_array ) ).'" onsubmit="return confirm(\''.t(array( 'zh-cn'=>'您确认要支付本订单吗？', 'zh-tw'=>'您確認要支付本訂單嗎？', 'en-us'=>'Do you confirm to pay for this order?' )).'\')">';
	}

    $selected_content .= '<table cellspacing="1" cellpadding="5" width="600" class="dg"><caption>'.t( array( 'zh-cn'=>'首付记录', 'zh-tw'=>'首付記錄', 'en-us'=>'First Order' ) ).'</cation>';

    $selected_content .= '<tr><td width="100" class="dg-cell">ID</td><td class="dg-cell">';
    $selected_content .= htmlspecialchars( $rs->fields[0] ).'</td></tr>';

    $selected_content .= '<tr><td class="dg-cell">'.t( array( 'zh-cn'=>'产品名称', 'zh-tw'=>'產品名稱', 'en-us'=>'Product Name' ) ).'</td><td class="dg-cell">';
    $selected_content .= htmlspecialchars( $rs->fields[4] ).'</td></tr>';

    $selected_content .= '<tr><td class="dg-cell">'.t( array( 'zh-cn'=>'单价', 'zh-tw'=>'單價', 'en-us'=>'Price' ) ).'</td><td class="dg-cell">';
    $selected_content .= htmlspecialchars( $rs->fields[5] ).'</td></tr>';
    /*
    $selected_content .= '<tr><td class="dg-cell">'.t( array( 'zh-cn'=>'购买数量', 'zh-tw'=>'購買數量', 'en-us'=>'Number' ) ).'</td><td class="dg-cell">';
    $selected_content .= htmlspecialchars( $rs->fields[6] ).'</td></tr>';
    */
    $selected_content .= '<tr><td class="dg-cell">'.t( array( 'zh-cn'=>'下单时间', 'zh-tw'=>'下單時間', 'en-us'=>'Adding Time' ) ).'</td><td class="dg-cell">';
    $selected_content .= htmlspecialchars( date('Y-n-j G:i:s',$rs->fields[7]) ).'</td></tr>';

    if( $rs->fields[9] > 0 ){
        $selected_content .= '<tr><td class="dg-cell">'.t( array( 'zh-cn'=>'首付时间', 'zh-tw'=>'首付時間', 'en-us'=>'Paying Time' ) ).'</td><td class="dg-cell">';
        $selected_content .= htmlspecialchars( date('Y-n-j',$rs->fields[9]) ).'</td></tr>';
    }

    if( $rs->fields[23]>0 && $rs->fields[31]>0 ){
        $selected_content .= '<tr><td class="dg-cell">'.t( array( 'zh-cn'=>'截止日期', 'zh-tw'=>'截止日期', 'en-us'=>'Expiration Date' ) ).'</td><td class="dg-cell">';
        $selected_content .= htmlspecialchars( date('Y-n-j',$rs->fields[31]) ).'</td></tr>';
    }

    if( $mc ){
		$selected_content .= '<tr><td class="dg-cell">'.t(array('zh-cn'=>'机器码','zh-tw'=>'機器碼', 'en-us'=>'Machine Code')).'</td><td class="dg-cell"><input class="lbtn" type="text" name="mc" value="" maxlength="40" size="40"/><br/><div style="line-height:150%;margin-top:5px;">'.t(array('zh-cn'=>'您已经付款成功，只需要再提交注册码就可以立即下载授权文件。','zh-tw'=>'您已經付款成功，只需要再提交註冊碼就可以立即下載授權文件。', 'en-us'=>'You had been paid successfully, after submit the machine code, you can download the license file instantly.')).'</div></td></tr>';
	}
	else{
		if( $rs->fields[9]>0 && $rs->fields[14]>0){
			$selected_content .= '<tr><td class="dg-cell">'.t(array('zh-cn'=>'机器码','zh-tw'=>'機器碼', 'en-us'=>'Machine Code')).'</td><td class="dg-cell">'.$rs->fields[32].'</td></tr>';
		}
	}

    $selected_content .= '</table><br/>';

    $selected_content .= renews($conf,$key);

    if( $rs->fields[9]>0 && !$mc ){
        $keyname = $rs->fields[11];
        $selected_content .= '<div id="downkey"><h4>'.t( array('zh-cn'=>'下载产品授权文件','zh-tw'=>'下載產品授權文件', 'en-us'=>'Download Product Licensing File.') ).'</h4>';
        if( !$urlrewrite ){
			/*
            $selected_content .= t( array(
                'zh-cn'=>"注：点击下载后，浏览器会提示您保存index.php文件，请下载后将其改名为{$keyname}即可。",
                'zh-tw'=>"注：點擊下載後，瀏覽器會提示您保存index.php文件，請下載後將其改名為{$keyname}即可。",
                'en-us'=>"Note: After you clicked the download link, browser will prompt you to save the index.php file, download it and simply rename it to {$keyname}.") );
				*/
        }

        $selected_content .= '</div><div id="keys">';

        $num = $rs->fields[6];
        for( $i = 0 ; $i < $num ; $i ++ ){
            $selected_content .= '<div class="key"><img src="'. $path_root . '/images/key.png' .'" border="0"/><div><a href="'.url('/members/download-key/'.$rs->fields[0].'/'.($i+1)).'/'.$keyname.'" target="_blank">';
            $selected_content .= $keyname . ' ('.($i+1).')';
            $selected_content .= '</a></div></div>';
        }

        $selected_content .= '</div>';
        $selected_content .= gen_license_key( $conf, $_SESSION['Username'], get_uid($conf), $key );
    }

}

$selected_content .= '<div id="form_toolbar">';
$selected_content .= '<div id="form_toolbar_left">';

if( $is_new ){

    $sql = 'select b.OID from Products as a right join Orders as b on a.PID=b.PID where b.RenewID=0 and b.UID='.get_uid($conf).' and a.PID='.$key;
    $cnt = $conn->GetOne($sql);

    if( empty($cnt) ){
        $selected_content .= '<input class="lbtn" type="submit" value="'.t( array('zh-cn'=>'添加到购物车','zh-tw'=>'添加到購物車', 'en-us'=>'Add to cart') ) .'"/>';
    }
    else{
        $selected_content .= '<a style="color:blue;" href="'.str_replace("'","\'",url( implode( '/', get_path_array() ). '/edit/'. $cnt )).'">'.t( array('zh-cn'=>'查看我的订单','zh-tw'=>'查看我的訂單', 'en-us'=>'View My Order') ) .'</a>';
    }

}
else{
	if( $mc ){
		$selected_content .= '<input class="lbtn" type="submit" value="'.t( array('zh-cn'=>'提交机器码','zh-tw'=>'提交機器碼', 'en-us'=>'Submit Machine Code') ) .'"/>';
	}
	else{
		$sql = 'select b.PaidTime,a.c_ExpDateEn from Products as a right join Orders as b on a.PID=b.PID where b.RenewID=0 and b.UID='.get_uid($conf).' and b.OID='.$key;
		$rs = $conn->Execute($sql);
		$cnt = $rs->fields[0];

		if( $cnt == 0 ){
			$selected_content .= '<input class="lbtn" type="submit" value="'.t( array('zh-cn'=>'立即付款','zh-tw'=>'立即付款', 'en-us'=>'Pay Now') ) .'"/>';
		}
		else{
			if( $rs->fields[1] > 0 ){
				$selected_content .= '<input class="lbtn" type="submit" value="'.t( array('zh-cn'=>'立即续费','zh-tw'=>'立即續費', 'en-us'=>'Renew Now') ) .'"/>';
			}
		}
	}
}

$selected_content .= '</div>';
$selected_content .= '<div id="form_toolbar_right">';

if( !$is_new && !$mc && $cnt == 0){
    $selected_content .= '<input class="lbtn" type="button" value="'.t( array('zh-cn'=>'删除订单','zh-tw'=>'刪除訂單', 'en-us'=>'Delete this order') ) .'" ';
    $selected_content .= 'onclick="document.location=\''.str_replace("'","\'",url( implode( '/', get_path_array() ). '/delete/'. implode( '/', array_slice( $param, 1) ) )).'\';"/>';
}

$selected_content .= '</div>';

$selected_content .= '<div id="edit-return"><a href="'.url( implode( '/', get_path_array() ). '/'. implode( '/', array_slice( $param, $is_new? 1:2 ) ) ).'">'.t( array( 'zh-cn'=>'返回', 'zh-tw'=>'返回', 'en-us'=>'Return' ) ).'</a></div>';
$selected_content .= '</form>';

// renew records
function renews($conf,$key){
    $selected_content = '';

    $conn=newConn($conf);
	$key = (int)$key;

    $sql = 'select Type,PaidTime,RenewId,OID from orders where RenewID!=0 and RenewID='.$key.' order by PaidTime asc';
    $rs = $conn->Execute( $sql );

    if( $rs && $rs->RecordCount() > 0 ){

        $selected_content .= '<table cellspacing="1" cellpadding="5" width="600" class="dg"><caption>'.t( array( 'zh-cn'=>'续费记录', 'zh-tw'=>'續費記錄', 'en-us'=>'Renew Orders' ) ).'</cation>';

        $selected_content .= '<tr><td width="40" class="dg-cell">'.t( array( 'zh-cn'=>'序列号', 'zh-tw'=>'序列號', 'en-us'=>'OID' ) ).'</td><td width="100" class="dg-cell">'.t( array( 'zh-cn'=>'时间', 'zh-tw'=>'時間', 'en-us'=>'Time' ) ).'</td><td class="dg-cell">';
        $selected_content .= t( array( 'zh-cn'=>'方式', 'zh-tw'=>'方式', 'en-us'=>'Type' ) ).'</td></tr>';
        
        do{
            $selected_content .= '<tr><td class="dg-cell">'.$rs->fields[3].'</td><td class="dg-cell">'.date('Y-n-j G:i:s',$rs->fields[1]).'</td><td class="dg-cell">';
            if( $rs->fields[2] == 0 ){
                switch( $rs->fields[0] ){
                    case 0:
                        $selected_content .= t(array( 'zh-cn'=>'从网站添加订单', 'zh-tw'=>'從網站添加訂單', 'en-us'=>'From website' ));
                        break;
                    case 1:
                        $selected_content .= t(array( 'zh-cn'=>'从客户端软件添加订单', 'zh-tw'=>'從客戶端軟件添加訂單', 'en-us'=>'From client side software' ));
                        break;
                }
            }
            else{
                switch( $rs->fields[0] ){
                    case 0:
                        $selected_content .= t(array( 'zh-cn'=>'从网站续费', 'zh-tw'=>'從網站續費', 'en-us'=>'Renew from website' ));
                        break;
                    case 1:
                        $selected_content .= t(array( 'zh-cn'=>'从客户端软件续费', 'zh-tw'=>'從客戶端軟件續費', 'en-us'=>'Renew from client side software' ));
                        break;
                }
            }
            $selected_content .= '</td></tr>';
            $rs->MoveNext();
        }
        while( !$rs->EOF );

        $selected_content .= '</table><br/>';

    }
    return $selected_content;
}

function completed( $t ){
    global $is_new, $param;
    $text  = t( $t ); 
    $text .= '<br/><br/><input type="button" value="'.t( array( 'zh-cn'=>'返回', 'zh-tw'=>'返回', 'en-us'=>'Return' ) ).'" ';
    $text .= 'onclick="document.location=\''.str_replace("'","\'",url( implode( '/', get_path_array() ). '/'. implode( '/', array_slice( $param, $is_new? 1:2 ) ) )).'\';"/>';
    return $text;
}

end_of_page:
?>