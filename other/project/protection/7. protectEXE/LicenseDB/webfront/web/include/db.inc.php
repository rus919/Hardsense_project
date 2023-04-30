<?php

function is_database_consistent( $type, $host, $username, $password, $database, $sql ){
	$conn = &ADONewConnection( $type ); 
	$conn->Connect( $host, $username, $password, $database );
	$conn->Execute('set names utf8');

	$tables = get_table_names( $sql );

	$sql = "SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = '$database' AND (";
	
	for( $i = 0, $n = count( $tables ) ; $i < $n ; $i ++ ){
		if( $i > 0 ) $sql .= ' OR ';
		$sql .= 'TABLE_NAME = \''.$tables[ $i ].'\' ';
	}

	$sql .= ")";
	return $conn->GetOne( $sql ) == $n;
}

function check_table_exists( $database, $table, $conf = 'default' ){
	$conn = newConn($conf);

	$sql = "SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = '$database' AND TABLE_NAME = '$table'";

	$count = $conn->GetOne( $sql );
	return $count > 0;
}


function check_db_exists( $database, $conf = 'default' ){
	$conn = newConn($conf);

	$sql = "SELECT COUNT(*) FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = '$database'";

	return $conn->GetOne( $sql ) > 0;
}

function newConn2($conf){
    global $sqlConf;
    $conn = &ADONewConnection($sqlConf[$conf]['type']); 
    if($sqlConf[$conf]['persist']){
        @$conn->PConnect($sqlConf[$conf]['host'],$sqlConf[$conf]['username'],$sqlConf[$conf]['password'],$sqlConf[$conf]['database']);
    }
    else{
        $conn->Connect($sqlConf[$conf]['host'],$sqlConf[$conf]['username'],$sqlConf[$conf]['password'],$sqlConf[$conf]['database']);
    }
	$conn->Execute('set names utf8');
    return $conn;
}

function is_post2(){
    return $_SERVER['REQUEST_METHOD']=='POST';
}

function get_table_names( $sql ){
	$num = preg_match_all( '/IF\s+NOT\s+EXISTS\s+`([0-9a-zA-Z_]+)`/i', $sql, $out, PREG_SET_ORDER );
	$result = array();
	foreach( $out as $val ){
		$result[] = $val[1];
	}
	return $result;
}

function get_table_sqls( $sql ){
	$num = preg_match_all( '/(CREATE\s+TABLE\s[^;]*;)/i', $sql, $out, PREG_SET_ORDER );
	$result = array();
	foreach( $out as $val ){
		$result[] = $val[1];
	}
	return $result;
}

function get_page_state(){
	return isset( $_GET['n'] ) ? (int)$_GET['n'] : 0 ;
}

?>