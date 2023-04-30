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
include('../include/db.inc.php');
include('../include/license.sql.inc.php');

$conn = newConn('default');

$table_name = 'Products';

// check connection.
if (!$conn){
    $selected_content = t( array( 'zh-cn'=>'连接数据库失败。', 'zh-tw'=>'連接數據庫失敗。', 'en-us'=>'Unable to connect database.' ) ); 
    goto end_of_page;
}

if( $is_new ){
    if( empty($_POST['Name']) || empty($_POST['Description']) || empty($_POST['Price']) || empty($_POST['Identifier']) || empty($_POST['Version']) ){
        $selected_content = t(array( 'zh-cn'=>'Name, Description, Price 不能为空', 'zh-tw'=>'Name, Description, Price 不能為空。', 'en-us'=>'Name, Description, Price  cannot be empty.' ));
        goto end_of_page;
    }

	$datName = '';
	if( empty( $_FILES['dat']['name'] ) ){
		$selected_content = t(array( 'zh-cn'=>'DAT文件不能为空', 'zh-tw'=>'DAT文件不能為空。', 'en-us'=>'DAT file cannot be empty.' ));
        goto end_of_page;
	}

    ensure_output_dir($_POST['OutPath']);

	if( empty( $_POST['DbHost'] ) || empty( $_POST['DbName'] ) || empty( $_POST['DbUsername'] ) || empty( $_POST['DbPassword'] ) ){
		$selected_content = t(array( 'zh-cn'=>'数据库配置不能为空', 'zh-tw'=>'數據庫配置不能為空。', 'en-us'=>'Database configuration cannot be empty.' ));
        goto end_of_page;
	}

	if( !make_db( $_POST['DbHost'], $_POST['DbName'], $_POST['DbUsername'], $_POST['DbPassword'] ) ){
		$selected_content = t(array( 'zh-cn'=>'生成数据库错误，请检查配置是否正确。', 'zh-tw'=>'生成數據庫錯誤，請檢查配置是否正確。', 'en-us'=>'Generated database error, please check your configuration.' ));
        goto end_of_page;
	}

    $sql='insert into '.$table_name.' (Name,Identifier,Version,Pic,Description,Url,Price,PriceVersion,Time,Published,Keyname,DataName,OutPath,'.
                    'c_LockHardwareID,'.
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
					'd_host,'.
					'd_database,'.
					'd_username,'.
					'd_password'.
               ') values ('.
        $conn->qstr($_POST['Name']).",".
        $conn->qstr($_POST['Identifier']).",".
        $conn->qstr($_POST['Version']).",".
        $conn->qstr($_POST['Pic']).",".
        $conn->qstr($_POST['Description']).",".
        $conn->qstr($_POST['Url']).",".
        (int)$_POST['Price'].",".
        (int)$_POST['PriceVersion'].",".
        $conn->sysTimeStamp.",".
        (isset($_POST['Published'])?'1':'0').','.
        $conn->qstr($_POST['Keyname']).','.
        $conn->qstr($datName).','.
        $conn->qstr($_POST['OutPath']).','.

        (isset($_POST['LockHardwareID'])?'1':'0').','.
        (isset($_POST['LockCPU'])?'1':'0').','.
        (isset($_POST['LockMAC'])?'1':'0').','.
        (isset($_POST['LockBIOS'])?'1':'0').','.
        (isset($_POST['LockHDD'])?'1':'0').','.

        (isset($_POST['NumDaysEn'])?'1':'0').','.
        (int)$_POST['NumDays'].','.

        (isset($_POST['NumExecEn'])?'1':'0').','.
        (int)$_POST['NumExec'].','.

        (isset($_POST['ExpDateEn'])?'1':'0').','.
        (int)$_POST['ExpDate'].','.

        (isset($_POST['CountryIdEn'])?'1':'0').','.
        (int)$_POST['CountryId'].','.

        (isset($_POST['ExecTimeEn'])?'1':'0').','.
        (int)$_POST['ExecTime'].','.

        (isset($_POST['TotalExecTimeEn'])?'1':'0').','.
        (int)$_POST['TotalExecTime'].','.

		$conn->qstr($_POST['DbHost']).','.
		$conn->qstr($_POST['DbName']).','.
		$conn->qstr($_POST['DbUsername']).','.
		$conn->qstr($_POST['DbPassword']).

        ')';

    $conn->Execute($sql);
    if ($conn->ErrorNo() != 0){ 
        $selected_content = $conn->ErrorMsg();
    }
    else{
		$id = $conn->Insert_ID();
		$datName = upload('dat', $id );
		if( empty( $datName ) ){
			$selected_content = t(array( 'zh-cn'=>'上传文件失败。', 'zh-tw'=>'上傳文件失敗。', 'en-us'=>'Upload file failed.' ));
			goto end_of_page;
		}
		else{
			$conn->Execute('update '.$table_name.' set DataName='.$conn->qstr($datName).' where pid='.$id );
		}

        $selected_content = completed( array( 'zh-cn'=>'添加成功。', 'zh-tw'=>'添加成功。', 'en-us'=>'Adding Success.' ) );
    }

    goto end_of_page;
}

if( $is_del ){
    $cnt = $conn->GetOne( 'select count(*) from Orders where PID='.$key );
    if( $cnt > 0 ){
         $selected_content = t( array( 'zh-cn'=>'用户订单已产生，不允许删除。', 'zh-tw'=>'用戶訂單已產生，不允許刪除。', 'en-us'=>'Not allow to delete the user ordered product.' ) );
    }
    else{
        $conn->Execute('delete from '.$table_name.' where PID='. $key );
        if ($conn->ErrorNo() != 0){ 
            $selected_content = $conn->ErrorMsg();
        }
        else{
            $selected_content = completed( array( 'zh-cn'=>'删除成功。', 'zh-tw'=>'刪除成功。', 'en-us'=>'Deleting Success.' ) );
        }
    }
    goto end_of_page;
}
else{
    if( is_post() ){

		ensure_output_dir($_POST['OutPath']);

		$datName = '';
		if( !empty( $_FILES['dat']['name'] ) ){
			$id = $key;
			$datName = upload('dat', $id );
			if( empty( $datName ) ){
				$selected_content = t(array( 'zh-cn'=>'上传文件失败。', 'zh-tw'=>'上傳文件失敗。', 'en-us'=>'Upload file failed.' ));
				goto end_of_page;
			}
		}

		if( empty( $_POST['DbHost'] ) || empty( $_POST['DbName'] ) || empty( $_POST['DbUsername'] ) || empty( $_POST['DbPassword'] ) ){
			$selected_content = t(array( 'zh-cn'=>'数据库配置不能为空', 'zh-tw'=>'數據庫配置不能為空。', 'en-us'=>'Database configuration cannot be empty.' ));
			goto end_of_page;
		}

		if( !make_db( $_POST['DbHost'], $_POST['DbName'], $_POST['DbUsername'], $_POST['DbPassword'] ) ){
			$selected_content = t(array( 'zh-cn'=>'生成数据库错误，请检查配置是否正确。', 'zh-tw'=>'生成數據庫錯誤，請檢查配置是否正確。', 'en-us'=>'Generated database error, please check your configuration.' ));
			goto end_of_page;
		}

        $sql = 'update '.$table_name.' set '.
            'Name='.$conn->qstr($_POST['Name']).','.
            'Identifier='.$conn->qstr($_POST['Identifier']).','.
            'Version='.$conn->qstr($_POST['Version']).','.
            'Pic='.$conn->qstr($_POST['Pic']).','.
            'Description='.$conn->qstr($_POST['Description']).','.
            'Url='.$conn->qstr($_POST['Url']).','.
            'Published='. (isset($_POST['Published'])?'1':'0').','.
            'Keyname='.$conn->qstr($_POST['Keyname']).','.
            ( empty( $datName ) ? '': 'DataName='.$conn->qstr($datName).',' ).
            'OutPath='.$conn->qstr($_POST['OutPath']).','.

            'c_LockHardwareID='.(isset($_POST['LockHardwareID'])?'1':'0').','.
            'c_LockCPU='.(isset($_POST['LockCPU'])?'1':'0').','.
            'c_LockMAC='.(isset($_POST['LockMAC'])?'1':'0').','.
            'c_LockBIOS='.(isset($_POST['LockBIOS'])?'1':'0').','.
            'c_LockHDD='.(isset($_POST['LockHDD'])?'1':'0').','.

            'c_NumDaysEn='.(isset($_POST['NumDaysEn'])?'1':'0').','.
            'c_NumDays='.(int)$_POST['NumDays'].','.

            'c_NumExecEn='.(isset($_POST['NumExecEn'])?'1':'0').','.
            'c_NumExec='.(int)$_POST['NumExec'].','.

            'c_ExpDateEn='.(isset($_POST['ExpDateEn'])?'1':'0').','.
            'c_ExpDate='.(int)$_POST['ExpDate'].','.

            'c_CountryIdEn='.(isset($_POST['CountryIdEn'])?'1':'0').','.
            'c_CountryId='.(int)$_POST['CountryId'].','.

            'c_ExecTimeEn='.(isset($_POST['ExecTimeEn'])?'1':'0').','.
            'c_ExecTime='.(int)$_POST['ExecTime'].','.

            'c_TotalExecTimeEn='.(isset($_POST['TotalExecTimeEn'])?'1':'0').','.
            'c_TotalExecTime='.(int)$_POST['TotalExecTime'].','.

			'd_host='.$conn->qstr($_POST['DbHost']).','.
			'd_database='.$conn->qstr($_POST['DbName']).','.
			'd_username='.$conn->qstr($_POST['DbUsername']).','.
			'd_password='.$conn->qstr($_POST['DbPassword']).

            ' where PID='.$key;
        $conn->Execute($sql);
        if ($conn->ErrorNo() != 0){ 
            $selected_content = $conn->ErrorMsg();
        }
        else{
            $selected_content = completed( array( 'zh-cn'=>'更新成功。', 'zh-tw'=>'更新成功。', 'en-us'=>'Updating Success.' ) );
        }
        //$selected_content .= ensure_output_dir($_POST['OutPath']);
        goto end_of_page;
    }
    else{
        $cnt = $conn->GetOne('select count(*) from orders where PID='.$key);
        $rs = &$conn->Execute('select Pid,Name,Pic,Description,Url,Price,PriceVersion,Time,Published,Keyname,DataName,OutPath,Identifier,Version,'.
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
                    'c_TotalExecTime,'. //30
				    'd_host,'.
					'd_database,'.
					'd_username,'.
					'd_password'.
            ' from '. $table_name . ' where PId=' .$key);
        if (!$rs){ 
            $selected_content = $conn->ErrorMsg();
            goto end_of_page;
        }
    }
}


new_begin:

$selected_content  = '<form enctype="multipart/form-data" method="post" action="'.url( implode( '/', $selector_array ) ).'">';
$selected_content .= '<table cellspacing="1" cellpadding="5" width="600" class="dg">';

$selected_content .= '<tr><td width="100" class="dg-cell">ID</td><td class="dg-cell">';
$selected_content .= ($is_new? '' : htmlspecialchars( $rs->fields[0] ) ).'</td></tr>';

$selected_content .= '<tr><td class="dg-cell">'.t( array( 'zh-cn'=>'产品名称', 'zh-tw'=>'產品名稱', 'en-us'=>'Name' ) ).'</td><td class="dg-cell">';
$selected_content .= '<input name="Name" class="ledit" type="text" value="'.  ($is_new?'': htmlspecialchars( $rs->fields[1] ) ).'" maxlength="256"/></td></tr>';

$usage = t( array( 'zh-cn'=>'用于客户端检测', 'zh-tw'=>'用於客戶端檢測', 'en-us'=>'For client detection' ) );
$usage = '<br/>('.$usage.')';

$selected_content .= '<tr><td class="dg-cell">'.t( array( 'zh-cn'=>'内部标识', 'zh-tw'=>'內部標識', 'en-us'=>'Internal Identifier' ) ).$usage.'</td><td class="dg-cell">';
$selected_content .= '<input name="Identifier" class="ledit" type="text" value="'.  ($is_new?'': htmlspecialchars( $rs->fields[12] ) ).'" maxlength="256"/></td></tr>';

$selected_content .= '<tr><td class="dg-cell">'.t( array( 'zh-cn'=>'产品版本', 'zh-tw'=>'產品版本', 'en-us'=>'Version' ) ).$usage.'</td><td class="dg-cell">';
$selected_content .= '<input name="Version" class="ledit" type="text" value="'.  ($is_new?'': htmlspecialchars( $rs->fields[13] ) ).'" maxlength="256"/></td></tr>';

$selected_content .= '<tr><td class="dg-cell">'.t( array( 'zh-cn'=>'产品图片', 'zh-tw'=>'產品圖片', 'en-us'=>'Picture' ) ).'</td><td class="dg-cell">';
$selected_content .= '<input name="Pic" class="ledit" type="text" value="'.  ($is_new?'': htmlspecialchars( $rs->fields[2] ) ).'" maxlength="256"/></td></tr>';

$selected_content .= '<tr><td class="dg-cell" valign="top">'.t( array( 'zh-cn'=>'产品描述<br/><br/>预定标签：', 'zh-tw'=>'產品描述<br/><br/>預定標籤：', 'en-us'=>'Description<br/><br/>Predefined tags:' ) ).'<br/>'.htmlspecialchars('<p>description</p>').'</td><td class="dg-cell">';
$selected_content .= '<textarea name="Description" class="lremark" rows="10" cols="80">'.($is_new?'': htmlspecialchars( $rs->fields[3] ) ).'</textarea></td></tr>';

$selected_content .= '<tr><td class="dg-cell">'.t( array( 'zh-cn'=>'详情URL', 'zh-tw'=>'詳情URL', 'en-us'=>'Detail Url' ) ).'</td><td class="dg-cell">';
$selected_content .= '<input name="Url" class="ledit" type="text" value="'.  ($is_new?'': htmlspecialchars( $rs->fields[4] ) ).'" maxlength="256"/></td></tr>';

$selected_content .= '<tr><td class="dg-cell">'.t( array( 'zh-cn'=>'产品价格', 'zh-tw'=>'產品價格', 'en-us'=>'Price' ) ).'</td><td class="dg-cell">';
$selected_content .= $is_new ? '<input name="Price" class="ledit" type="text" value="" maxlength="10"/></td></tr>': htmlspecialchars( $rs->fields[5] );

$selected_content .= '<tr><td class="dg-cell">'.t( array( 'zh-cn'=>'价格版本', 'zh-tw'=>'價格版本', 'en-us'=>'PriceVersion' ) ).'</td><td class="dg-cell">';
$selected_content .= $is_new ? '<input name="PriceVersion" class="ledit" type="text" value="1" maxlength="10"/></td></tr>': htmlspecialchars( $rs->fields[6] );

$selected_content .= '<tr><td class="dg-cell">'.t( array( 'zh-cn'=>'创建时间', 'zh-tw'=>'創建時間', 'en-us'=>'Time' ) ).'</td><td class="dg-cell">';
$selected_content .= ($is_new? '' : htmlspecialchars( $rs->fields[7] ) ).'</td></tr>';

$selected_content .= '<tr><td class="dg-cell">'.t( array( 'zh-cn'=>'已发布', 'zh-tw'=>'已發布', 'en-us'=>'Published' ) ).'</td><td class="dg-cell">';
$selected_content .= '<input name="Published" type="checkbox" '.     ($is_new?'':( ((int)$rs->fields[8])>0? 'checked="checked"':'') ).'/></td></tr>';

$selected_content .= '<tr><td class="dg-cell">'.t( array( 'zh-cn'=>'授权文件名称（必须）', 'zh-tw'=>'授權文件名稱(必須)', 'en-us'=>'Licensing Key Filename(Required)' ) ).'</td><td class="dg-cell">';
$selected_content .= '<input name="Keyname" class="ledit" type="text" value="'.  ($is_new?'': htmlspecialchars( $rs->fields[9] ) ).'" maxlength="256"/></td></tr>';

$selected_content .= '<tr><td class="dg-cell">'.t( array( 'zh-cn'=>'SEKeygen.Dat磁盘路径（必须）', 'zh-tw'=>'SEKeygen.Dat硬碟路徑(必須)', 'en-us'=>'SEKeygen.Dat drive path(Required)' ) ).'</td><td class="dg-cell"><input type="hidden" name="MAX_FILE_SIZE" value="1024000" />';
$selected_content .= ($is_new?'': '<div class="lbb">'.htmlspecialchars( $rs->fields[10] ).'</div>' ).'<input name="dat" type="file" /></td></tr>';

$selected_content .= '<tr><td class="dg-cell">'.t( array( 'zh-cn'=>'授权文件输出磁盘路径（不存在则创建）', 'zh-tw'=>'授權文件輸出硬碟路徑(不存在則創建)', 'en-us'=>'Key output drive path(Create if it doesn\'t exist)' ) ).'</td><td class="dg-cell">';
$selected_content .= '<input name="OutPath" class="ledit" type="text" value="'.  ($is_new?'': htmlspecialchars( $rs->fields[11] ) ).'" maxlength="256"/></td></tr>';

$selected_content .= '<tr><td class="dg-cell" valign="top">'.t( array( 'zh-cn'=>'授权配置（必须）', 'zh-tw'=>'授權配置(必須)', 'en-us'=>'Licensing Configuration(Required)' ) ).'</td><td class="dg-cell">';

$selected_content .= '<table cellspacing="1" cellpadding="5" width="480">'.
                     '<tr><td>'.
                        '<input type="checkbox" name="LockHardwareID" id="LockHardwareID"'.($is_new?'':( ((int)$rs->fields[14])>0? ' checked="checked"':'') ).'/><label for="LockHardwareID">'.t(array( 'zh-cn'=>'锁定机器码 （需客户端软件支持）', 'zh-tw'=>'鎖定機器碼 （需客戶端軟件支持）', 'en-us'=>'Lock Hardware ID (Required client side software support)' )).'</label><br/>'.

                        '<span style="padding-left:50px;"><input type="checkbox" name="LockCPU" id="LockCPU" '.($is_new?'':( ((int)$rs->fields[15])>0? ' checked="checked"':'') ).'/><label for="LockCPU">'.t(array( 'zh-cn'=>'锁定CPU', 'zh-tw'=>'鎖定CPU', 'en-us'=>'CPU' )).'</label> '.

                        '<input type="checkbox" name="LockMAC" id="LockMAC"'.($is_new?'':( ((int)$rs->fields[16])>0? ' checked="checked"':'') ).'/><label for="LockMAC">'.t(array( 'zh-cn'=>'锁定网卡MAC地址', 'zh-tw'=>'鎖定網卡MAC地址', 'en-us'=>'MAC Address' )).'</label> '.

                        '<input type="checkbox" name="LockBIOS" id="LockBIOS"'.($is_new?'':( ((int)$rs->fields[17])>0? ' checked="checked"':'') ).'/><label for="LockBIOS">'.t(array( 'zh-cn'=>'锁定BIOS信息', 'zh-tw'=>'鎖定BIOS信息', 'en-us'=>'BIOS' )).'</label> '.

                        '<input type="checkbox" name="LockHDD" id="LockHDD"'.($is_new?'':( ((int)$rs->fields[18])>0? 'checked="checked"':'') ).'/><label for="LockHDD">'.t(array( 'zh-cn'=>'锁定硬盘序列号', 'zh-tw'=>'鎖定硬盤序列號', 'en-us'=>'Hard drive' )).'</label></span>'.
                     '</td></tr>'.
                     '<tr><td>'.
                        '<input type="checkbox" name="NumDaysEn" id="NumDaysEn"'.($is_new?'':( ((int)$rs->fields[19])>0? ' checked="checked"':'') ).'/><label for="NumDaysEn">'.t(array( 'zh-cn'=>'限制试用天数', 'zh-tw'=>'限制試用天數', 'en-us'=>'Lock Trail Days' )).'</label><br/> '.

                        '<span class="ileft">'.t(array( 'zh-cn'=>'试用天数', 'zh-tw'=>'試用天數', 'en-us'=>'Trail Days' )).'</span> <span class="right"><input type="text" name="NumDays" value="'.($is_new?'': htmlspecialchars( $rs->fields[20] ) ).'" maxlength="10" size="10"/></span>'.
                     '</td></tr>'.
                     '<tr><td>'.
                        '<input type="checkbox" name="NumExecEn" id="NumExecEn"'.($is_new?'':( ((int)$rs->fields[21])>0? ' checked="checked"':'') ).'/><label for="NumExecEn">'.t(array( 'zh-cn'=>'限制运行次数', 'zh-tw'=>'限制運行次數', 'en-us'=>'Lock Execution Count' )).'</label><br/>'.

                        '<span class="ileft">'.t(array( 'zh-cn'=>'运行次数', 'zh-tw'=>'運行次數', 'en-us'=>'Execution Count' )).'</span><span class="iright"><input type="text" name="NumExec" value="'.($is_new?'': htmlspecialchars( $rs->fields[22] ) ).'" maxlength="10" size="10"/></span>'.
                     '</td></tr>'.
                     '<tr><td>'.
                        '<input type="checkbox" name="ExpDateEn" id="ExpDateEn"'.($is_new?'':( ((int)$rs->fields[23])>0? ' checked="checked"':'') ).'/><label for="ExpDateEn">'.t(array( 'zh-cn'=>'锁定截止日期 ( 截止日期 ＝ 用户付款时间 + 天数 )', 'zh-tw'=>'鎖定截止日期 （ 截止日期 ＝ 用戶付款時間 + 天數 ）', 'en-us'=>'Lock Expiration Date ( ExpirationDate = UserPiadOrderTime + Days )' )).'</label><br/> '.

                        '<span class="ileft">'.t(array( 'zh-cn'=>'天数', 'zh-tw'=>'天數', 'en-us'=>'Days' )).'</span><span class="iright"><input type="text" name="ExpDate" value="'.($is_new?'': htmlspecialchars( $rs->fields[24] ) ).'" maxlength="10" size="10"/></span>'.
                     '</td></tr>'.
                     '<tr><td>'.
                        '<input type="checkbox" name="CountryIdEn" id="CountryIdEn"'.($is_new?'':( ((int)$rs->fields[25])>0? ' checked="checked"':'') ).'/><label for="CountryIdEn">'.t(array( 'zh-cn'=>'锁定系统语言ID', 'zh-tw'=>'鎖定系統語言ID', 'en-us'=>'Lock System Language ID' )).'</label><br/> '.
                        '<span class="ileft">'.t(array( 'zh-cn'=>'系统语言ID', 'zh-tw'=>'系統語言ID', 'en-us'=>'System Language ID' )).'</span><span class="iright"><input type="text" name="CountryId" value="'.($is_new?'': htmlspecialchars( $rs->fields[26] ) ).'" maxlength="10" size="10"/></span>'.
                     '</td></tr>'.
                     '<tr><td>'.
                        '<input type="checkbox" name="ExecTimeEn" id="ExecTimeEn"'.($is_new?'':( ((int)$rs->fields[27])>0? ' checked="checked"':'') ).'/><label for="ExecTimeEn">'.t(array( 'zh-cn'=>'限制单次使用时间（分钟）', 'zh-tw'=>'限制單次使用時間(分鐘)', 'en-us'=>'Lock Execution Time(Mins.)' )).'</label><br/> '.
                        '<span class="ileft">'.t(array( 'zh-cn'=>'单次使用时间', 'zh-tw'=>'單次使用時間', 'en-us'=>'Execution Time' )).'</span><span class="iright"><input type="text" name="ExecTime" value="'.($is_new?'': htmlspecialchars( $rs->fields[28] ) ).'" maxlength="10" size="10"/></span>'.
                     '</td></tr>'.
                     '<tr><td>'.
                        '<input type="checkbox" name="TotalExecTimeEn" id="TotalExecTimeEn"'.($is_new?'':( ((int)$rs->fields[29])>0? ' checked="checked"':'') ).'/><label for="TotalExecTimeEn">'.t(array( 'zh-cn'=>'限制总使用时间（分钟）', 'zh-tw'=>'限制總使用時間(分鐘)', 'en-us'=>'Lock Total Execution Time(Mins.)' )).'</label><br/> '.
                        '<span class="ileft">'.t(array( 'zh-cn'=>'总使用时间', 'zh-tw'=>'總使用時間', 'en-us'=>'Total Execution Time' )).'</span><span class="iright"><input type="text" name="TotalExecTime" value="'.($is_new?'': htmlspecialchars( $rs->fields[30] ) ).'" maxlength="10" size="10"/></span>'.
                     '</td></tr>'.
                     '</table>';
$selected_content .= '</td></tr>';

// database
$selected_content .= '<tr><td class="dg-cell" valign="top">'.t( array( 'zh-cn'=>'产品数据库配置（自动安装表）', 'zh-tw'=>'產品數據庫配置（自動安裝表）', 'en-us'=>'Product Database Configuration' ) ).'</td><td class="dg-cell">';
$selected_content .= '<table cellspacing="1" cellpadding="5" width="480">'.
                     '<tr><td width="60">'.t( array( 'zh-cn'=>'主机地址', 'zh-tw'=>'主機地址', 'en-us'=>'Host' ) ).'</td><td><input name="DbHost" type="text" value="'.  ($is_new?'': htmlspecialchars( $rs->fields[31] ) ).'" maxlength="64" size="58" class="ledit2" /></td></tr>'.
                     '<tr><td>'.t( array( 'zh-cn'=>'数据库', 'zh-tw'=>'數據庫', 'en-us'=>'Database' ) ).'</td><td><input name="DbName" type="text" value="'.  ($is_new?'': htmlspecialchars( $rs->fields[32] ) ).'" maxlength="64" size="58" class="ledit2"/></td></tr>'.
                     '<tr><td>'.t( array( 'zh-cn'=>'用户名', 'zh-tw'=>'用戶名', 'en-us'=>'Username' ) ).'</td><td><input name="DbUsername" type="text" value="'.  ($is_new?'': htmlspecialchars( $rs->fields[33] ) ).'" maxlength="64" size="58" class="ledit2"/></td></tr>'.
                     '<tr><td>'.t( array( 'zh-cn'=>'密码', 'zh-tw'=>'密碼', 'en-us'=>'Password' ) ).'</td><td><input name="DbPassword" type="password" value="'.  ($is_new?'': htmlspecialchars( $rs->fields[34] ) ).'" maxlength="64" size="58" class="ledit2"/></td></tr>';
$selected_content .= '</table></td></tr>';

$selected_content .= '</table>';
$selected_content .= '<br/><div id="form_toolbar">';
$selected_content .= '<div id="form_toolbar_left"><input class="lbtn" type="submit" value="'.t( $is_new? array('zh-cn'=>'添加','zh-tw'=>'添加', 'en-us'=>'Add') : array('zh-cn'=>'更新','zh-tw'=>'更新', 'en-us'=>'Update') ) .'"/></div>';
$selected_content .= '</div><div id="edit-return"><a href="'.url( implode( '/', get_path_array() ). '/'. implode( '/', array_slice( $param, $is_new? 1:2 ) ) ).'">'.t( array( 'zh-cn'=>'返回', 'zh-tw'=>'返回', 'en-us'=>'Return' ) ).'</a></div>';
$selected_content .= '</form><br/><div>';

$selected_content .= t(array(
    'zh-cn'=>'注：产品价格一经添加就不允许再更改，若要更改产品价格，请复制添加新项，增大版本号，并把旧版本改为未发布状态。',
    'zh-tw'=>'注：產品價格一經添加就不允許再更改，若要更改產品價格，請複製添加新項，增大版本號，並把舊版本改為未發佈狀態。',
    'en-us'=>'Note: price is unable to change after the entry was added. to change the price, add a new entry & copy it\'s contents, increase version number and change old version to the unpublished state.',
));
$selected_content .= '</div>';

function completed( $t ){
    global $is_new, $param;
    $text  = t( $t ); 
    $text .= '<br/><br/><input type="button" value="'.t( array( 'zh-cn'=>'返回', 'zh-tw'=>'返回', 'en-us'=>'Return' ) ).'" ';
    $text .= 'onclick="document.location=\''.str_replace("'","\'",url( implode( '/', get_path_array() ). '/'. implode( '/', array_slice( $param, $is_new? 1:2 ) ) )).'\';"/>';
    return $text;
}

function ensure_output_dir($outPath){
    if( !file_exists( $outPath ) ){
		mkdir( $outPath, 0777, true );
    }
}

function make_db( $host, $name, $username, $password ){
	$conn = &ADONewConnection('mysql');
	if( null == @$conn->Connect( $host, $username, $password, $name ) ) return false;

	$sqltext = get_license_sql();
	if( !is_database_consistent( 'mysql', $host, $username, $password, $name, $sqltext ) ){

		$sql_group = get_table_sqls( $sqltext );
		foreach( $sql_group as $sql ){
			$conn->Execute( $sql );
			if( $conn->ErrorNo() != 0 )return false;
		}

	}
	return true;
}

function upload($dat, $id){
	global $keygen_dat_uploaded_dir;
	$uploadfile = $keygen_dat_uploaded_dir . $id. '.dat';

	if( $_FILES[$dat]['error'] == UPLOAD_ERR_OK ){
		if (move_uploaded_file($_FILES[$dat]['tmp_name'], $uploadfile)) {
			return $uploadfile;
		} 
	}
	return "";
}

end_of_page:
?>