<?php

// prevent user directly accessing this page.
if( !defined('VALID_ENTRY_POINT') ){
    exit;
}

if( count( $param ) != 3 ){
    $selected_content = 'Invalid download page.';
    goto end_of_page;
}

$key = (int)$param[0];
$num = (int)$param[1];

include('./include/adodb5/adodb.inc.php');

$conf = 'default';
$conn = newConn($conf);

$table_name = 'Orders';

$rs = &$conn->Execute('select a.OID,a.UID,c.Username,a.PID,b.Name,b.Price,a.Number,a.Time,a.IP,a.PaidTime,a.PaidIP,b.Keyname,b.DataName,b.OutPath from '. $table_name .' as a left join Products as b on a.PID=b.PID, Users as c where a.UID=c.UID and a.UID='.get_uid($conf).' and a.OID=' .$key);
if (!$rs || $conn->ErrorNo() != 0 ){ 
    $selected_content = 'You do not have permission to download this file.';
    goto end_of_page;
}

if( !( $num >= 1 && $num <= $rs->fields[6] ) ){
    $selected_content = 'You don\'t have permissions to download the unauthorized key file.';
    goto end_of_page;
}

$outPath = $rs->fields[13];
$c = $outPath[ strlen($outPath) - 1 ];
$outPath .= $c == "\\" ? '': "\\";
$outPath .= $_SESSION['Username']."\\";

if( !file_exists( $outPath ) ){
    $selected_content = 'System error: key path not found,  please contact the administrator.';
    goto end_of_page;
}

$keyname = $rs->fields[11];

$name = get_uid($conf) .'-'.$rs->fields[0].'-'.$num;
$fn = $outPath.$name.'-'.$keyname;

if( !file_exists( $fn ) ){
    $selected_content = 'System error: key file not found,  please contact the administrator.';
    goto end_of_page;
}

$rs->Close();
$conn->Close();


$prevent_output = true;

header('Content-Type: application/octet-stream;');
header('Content-Disposition: attachment; filename='.$keyname);

ob_clean();
readfile( $fn );
exit;
end_of_page:
?>