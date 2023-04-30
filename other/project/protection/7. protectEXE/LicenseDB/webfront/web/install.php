<?php

include('settings.php');
include('./include/adodb5/adodb.inc.php');
include('./include/system.sql.inc.php');
include('./include/db.inc.php');

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

$state = get_page_state();
$title  = '';
$output = '';

$conn = newConn2('default');
if( $conn->ErrorNo() != 0 ){
		$title = 'Configure your settings.php';
		$output = <<< EOT
<div style="border:1px solid red;padding:5px;width:350px;background-color:#ffeeee;text-indent:20px">Your website hasn&apos;t configured or there are some configuration errors. Please change your configuration in settings.php, if you done, click the following button.</div>
<div style="margin:5px;text-align:center;width:340px;">
	<input type="button" value="Done" onclick="go('./');"/>
</div>

EOT;
}else{

if( is_post2() ){

    $username = trim( $_POST['username'] );
    $password = trim( $_POST['password'] );
    $confirmPassword = trim ( $_POST['repassword'] );

	$output = "";

    if( empty( $username ) || empty( $password ) || empty( $confirmPassword ) ){
        $output ='Username or Password cannot be empty.';
    }
    else if( strcasecmp( $password, $confirmPassword ) !== 0 ){
        $output = 'Confirm password mismatch, pelease re-enter password.';
    }
    else if(strlen( $password ) < 6 ){
        $output = 'Password must contains at least 6 digits or numbers.';
    }
    else if( strlen( $username ) > 64 || strlen( $password ) > 32 ){
        $output = 'Username or Password too long.';
    }
    else if( !validate_username( $username ) ){
        $output = 'Username must be letters, digits or e-mail address.';
    }

	if( strlen( $output ) == 0 ){
		$sql_group = get_table_sqls( get_system_sql() );
		foreach( $sql_group as $sql ){
			$conn->Execute( $sql );
			if( $conn->ErrorNo() != 0 )break;
		}
		if( $conn->ErrorNo() == 0 ){
			$sql = get_system_intialized_sql( $username, $password, $_SERVER['REMOTE_ADDR'] );
			$conn->Execute( $sql );
		}
	}

	if( $conn->ErrorNo() != 0 || strlen( $output ) > 0 ){
		if( strlen( $output ) > 0 ){
			$msg = $output;
		}else{
			$msg = '('.$conn->ErrorNo().') '.$conn->ErrorMsg();
		}
		$title = "Installing Issues";
		$output = <<<EOT
<div style="border:1px solid red;padding:5px;width:350px;background-color:#ffeeee;text-indent:20px">
$msg
</div>
<div style="margin:5px;text-align:center;width:340px;">
	<input type="button" value="Go back" onclick="go('install.php?n=1');"/>
</div>
EOT;
	}
	else{
		$title = "Installing Completed";
		$output = <<<EOT
<div style="border:1px solid #66ff66;padding:5px;width:350px;background-color:#eeffee;text-indent:20px">
Configratulations! installing successfully.
</div>
<div style="margin:15px;text-align:center;width:340px;">
	<input type="button" value="OK" onclick="go('install.php');"/>
</div>
EOT;
	}
}
else{
	if (version_compare(PHP_VERSION, '5.3.0') >= 0) {

	if( $state == 0 && is_database_consistent( 
			$sqlConf['default']['type'],
			$sqlConf['default']['host'],
			$sqlConf['default']['username'],
			$sqlConf['default']['password'],
			$sqlConf['default']['database'], 
			get_system_sql() 
							  ) 
	){
		// system is consistent, no need to install.
		header('Location: ./');
	}
	else{ 
$title  = 'Installing Safengine Web Platform';
$output = <<< EOT
<form action="?n=1" method="post">
<div style="padding:5px;font-size:1em;color:#339933;font-weight:bold;">Database Configuration</div>
<table style="width:350px;font-size:1em;">
<tr><td class="left">Host</td><td class="right"><input name="host" value="{$sqlConf['default']['host']}" maxlength="512" size="32" readonly="readonly"/></td></tr>
<tr><td class="left">Database</td><td class="right"><input name="db_name" value="{$sqlConf['default']['database']}" maxlength="64" size="32" readonly="readonly"/></td></tr>
<tr><td class="left">Username</td><td class="right"><input name="db_username" value="{$sqlConf['default']['username']}" maxlength="64" size="32" readonly="readonly"/></td></tr>
<tr><td class="left">Password</td><td class="right"><input name="db_password" type="password" value="{pre-defined}" maxlength="64" size="32" readonly="readonly"/></td></tr>
</table>
<div style="margin-top:15px;padding:5px;font-size:1em;color:#339933;font-weight:bold;">Website Account</div>
<table style="width:350px;font-size:1em;">
	<tr><td class="left">Username</td><td class="right"><input name="username" value="" maxlength="32" size="32" title="At least 6 letters, maximum 32 letters."/></td></tr>
	<tr><td class="left">Password</td><td class="right"><input name="password" type="password" value="" maxlength="32" size="32" title="At least 6 letters, maximum 32 letters."/></td></tr>
	<tr><td class="left">Confirm Password</td><td class="right"><input name="repassword" type="password" value="" maxlength="32" size="32" title="At least 6 letters, maximum 32 letters."/></td></tr>
</table>
<div style="margin:5px;text-align:right;width:340px;">
<input type="submit" value="Install"/>
</div>
</form>
EOT;
	}


}else{
	$v = phpversion();
	$title  = 'PHP Version Requirement';
	$output = <<<EOT
<div style="border:1px solid red;padding:5px;width:350px;background-color:#ffeeee;text-indent:20px">
		Require at least PHP 5.3.0 to support this platform. your current version is $v.
</div>
EOT;
}
}
}
?>
<html>
<head>
<title>Install System</title>
<style>
	.left{
		width:100px;
		text-align:right;
		background-color:#eeeeff;
		padding:5px;
	}
	.right{
		width:250px;
		padding:5px;
		background-color:#eeeeff;
	}
</style>
<script language="javascript">
	function go(url){
		document.location.href=url;
	}
</script>
</head>
<body style="text-align:center;">
<div style="margin:100px auto 0px auto;width:400px;text-align:left;">
	<h3><?php echo $title; ?></h3>
	<?php echo $output; ?>
</div>
</body>
</html>