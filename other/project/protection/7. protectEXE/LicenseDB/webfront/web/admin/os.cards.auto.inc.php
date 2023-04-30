<?php


// prevent user directly accessing this page.
if( !defined('VALID_ENTRY_POINT') ){
    exit;
}


include('../include/adodb5/adodb.inc.php');

$conf = 'default';
$conn = newConn($conf);

$table_name = 'Cards';

$post = is_post();

if( $post ){
    $cnt = $_POST['Count'];
    $amt = $_POST['Amount'];

    if( $amt <= 0 || $cnt <=0 || $cnt > 1000 ){
        $selected_content = t( array( 'zh-cn'=>'充值卡金额必须大于0或生成数量必须在1000以内。', 'zh-tw'=>'充值卡金額必須大於0或生成數量必須在1000以內。', 'en-us'=>'Amount must be larger than 0 or generating number must less or equal to 1000.' ) );
        goto end_of_page;
    }

    $cards = gen_card( get_db_start_number( $conf ), $cnt );
    $passs = gen_pass( $cnt );

    $sql = 'insert into '.$table_name.' (CardNumber,Password,Amount,GeneratedTime) values ';
    $save = '';

    for( $i = 0, $cnt = count($cards); $i < $cnt; $i ++ ){
        if( $i > 0 ) $sql.=',';
        $sql .= '('.
            $conn->qstr( $cards[ $i ] ). ','.
            $conn->qstr( $passs[ $i ] ). ','.
            $amt.','.
            $conn->sysTimeStamp.
            ')';
        $save .= $cards[ $i ] .', '.$passs[ $i ]."\r\n";
    }

    $conn->Execute($sql);
    if ($conn->ErrorNo() != 0){ 
        $selected_content = $conn->ErrorMsg();
    }
    else{
        $selected_content = completed( array( 'zh-cn'=>'生成成功。', 'zh-tw'=>'生成成功。', 'en-us'=>'Generating Success.' ) );

        $selected_content .= '<br/><br/><table cellspacing="1" cellpadding="5" width="600" class="dg">';

        $selected_content .= '<tr>';
        $selected_content .= '<td class="dg-cell">'.t(array( 'zh-cn'=>'请复制并保存生成的卡和密码', 'zh-tw'=>'請複製並保存生成的卡和密碼', 'en-us'=>'Please copy and save generated cards and passwords.' )).'</td>';
        $selected_content .= '</tr>';

        $selected_content .= '<tr>';
        $selected_content .= '<td class="dg-cell"><textarea name="Amount" cols="80" rows="30" class="lremark">'.htmlspecialchars( $save ).'</textarea></td>';
        $selected_content .= '</tr>';

        $selected_content .= '</table><br/>';

    }
    goto end_of_page;
}
else{

    $selected_content  = '<form method="post" action="'.url( implode( '/', $selector_array ) ).'">';
    $selected_content .= '<table cellspacing="1" cellpadding="5" width="600" class="dg">';

    $selected_content .= '<tr>';
    $selected_content .= '<td class="dg-cell">'.t(array( 'zh-cn'=>'充值卡金额', 'zh-tw'=>'充值卡金額', 'en-us'=>'Prepaid card amount' )).'</td>';
    $selected_content .= '<td class="dg-cell"><input name="Amount" type="text" value="" maxlength="10" class="ledit"/></td>';
    $selected_content .= '</tr>';

    $selected_content .= '<tr>';
    $selected_content .= '<td class="dg-cell">'.t(array( 'zh-cn'=>'生成数量', 'zh-tw'=>'生成數量', 'en-us'=>'Generating number' )).'( <= 1000 )</td>';
    $selected_content .= '<td class="dg-cell"><input name="Count" type="text" value="" maxlength="10" class="ledit"/></td>';
    $selected_content .= '</tr>';

    $selected_content .= '</table>';
    $selected_content .= '<br/><div id="form_toolbar">';
    $selected_content .= '<div id="form_toolbar_left"><input class="lbtn" type="submit" value="'.t( array('zh-cn'=>'生成','zh-tw'=>'生成', 'en-us'=>'Generate') ) .'"/></div>';
    $selected_content .= '<div id="form_toolbar_right"></div><div id="edit-return"><a href="'.url( implode( '/', get_path_array() ). '/'. implode( '/', array_slice( $param, 1 ) ) ).'">'.t( array( 'zh-cn'=>'返回', 'zh-tw'=>'返回', 'en-us'=>'Return' ) ).'</a></div>';
    $selected_content .= '</form>';

}

function get_db_start_number( $conf ){
    // get max id
    $conn = newConn($conf);
    $max = $conn->GetOne('select max(CardId) from Cards');

    if( $max <= 0 ){
        return 0;
    }

    return $max;
}

function gen_card( $seed, $num ){
    global $prepaid_card_format, $prepaid_card_start_number;
    $seed += $prepaid_card_start_number;

    $result = array();    
    for( $i = 0 ; $i < $num ; $i++ ){
        $result[] = xformat( $prepaid_card_format, ++$seed );
    }

    return $result;
}

// seed with microseconds
function make_seed()
{
  list($usec, $sec) = explode(' ', microtime());
  return (float) $sec + ((float) $usec * 100000);
}

function gen_pass( $num ){
    global $prepaid_card_password_length;
    $prepaid_card_password_length = $prepaid_card_password_length > 32 ? 32 : $prepaid_card_password_length;

    $min = $prepaid_card_password_length > 10 ? pow(10, 9 ) : pow(10, $prepaid_card_password_length - 1 );
    $max = $prepaid_card_password_length > 10 ? pow(10, 10 ) - 1 : pow(10, $prepaid_card_password_length ) - 1;
    mt_srand(make_seed());

    $min2 = pow( 10,$prepaid_card_password_length % 10 - 1 );
    $max2 = pow( 10,$prepaid_card_password_length % 10 ) - 1;

    $result = array();    
    for( $i = 0 ; $i < $num ; $i++ ){
        $len = $prepaid_card_password_length;
        $s = '';
        do{
            if( $len > 10 || $prepaid_card_password_length<= 10 ){
                $s .= (string)mt_rand($min,$max);
            }
            else{
                $s .= (string)mt_rand( $min2 , $max2 );
            }
            $len -= 10;
        }while( $len > 0 );
        $result[] = $s;
    }
    return $result;
}

function xformat( $fmt, $n ){
    $n = (string)$n;
    $result = '';

    for( $i = strlen( $fmt ) - 1, $j = strlen( $n ) - 1 ; $i >=0 ; $i-- ){
        $c = $fmt[ $i ];
        if( $c == '?' ){
            if( $j >= 0 ){
                $result = $n[ $j-- ]. $result;
            }
            else{
                $result = '0' . $result;
            }
        }
        else{
            $result = $c . $result;
        }
    }
    return $result;
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