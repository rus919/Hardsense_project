<?php

define('VALID_ENTRY_POINT',true);
define('ROOT_PATH','../');

include('../settings.php');
Session::start();
include('selector.inc.php');

if( $urlrewrite ){
	$template_path = '/templates/'.$template.'/';
}
else{
	$template_path = ROOT_PATH.'templates/'.$template.'/';
}
include(ROOT_PATH.'templates/'.$template.'/page.php');


$page_content = str_replace( '{content}', $selected_content, $page_content );

echo $page_content;

class Session{
    public  static $name     = '';
    public  static $database = 'default';
    public  static $table    = 'sessions';
    private static $started  = false;

    public static function start(){
        global $sqlConf;
        if(    self::$started 
            || count(  $sqlConf ) == 0 
            || !isset( $sqlConf[ self::$database ] ) 
          ){   return;  }

        self::$started = true;

        require_once( '../include/adodb5/session/adodb-session2.php' );

        if( ! empty( self::$name ) ){
            session_name( self::$name );
        }
        $conf = $sqlConf[ self::$database ];
        ADOdb_Session::config(
            $conf['type'    ], 
            $conf['host'], 
            $conf['username'], 
            $conf['password'], 
            $conf['database'],
            array('table'=> self::$table )
        );
        ADOdb_session::Persist( $conf['persist'] );
        session_cache_limiter('private, must-revalidate');
        session_start();
    }
}

?>