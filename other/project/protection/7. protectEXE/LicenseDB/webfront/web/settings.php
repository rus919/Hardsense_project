<?php


$sqlConf= array(
    'default'=>array(
        'type'     => 'mysql',
        'database' => 'licensedb',
        'host'     => '127.0.0.1:3306',
        'username' => 'root',
        'password' => 'password',
        'persist'  => true
    ),
);

// system default language.
$lang = 'zh-cn';

// 1, 2
$template = '1' ; 

//icp
$icp = '';

// path of virtual directory
$path_root = '';

// change browsing products' page size.
$product_page_size = 5; 

// chnage user shopping cart's default page size.
$shopping_cart_page_size = 10;

// allow url rewrite
$urlrewrite = false;

// must end with "\" or "/"
$keygen_dat_uploaded_dir = "C:\\LicenseDB\\webfront\\output\\";

// sekeygen.exe filename.
$keygen_filename = "C:\\LicenseDB\\webfront\\sekeygen_wrapper\\sekeygen_wrapper.exe";

// prepaid card start number.
$prepaid_card_start_number = 10000000;

// prepaid card format, ? indicate a number, alignment from right, left overflow digits will be discarded. max lengh is 32.
$prepaid_card_format = 'SE-???-???-???';


// min length is 1, max length is 32.
$prepaid_card_password_length = 10;

// allow to register a user in a specified time from same ip. 0 is not restriction.
$register_interval = 60 ; // only allow to register a user in 60 minutes.

// if a user fail to login over a specified times, will be banned temporarily.
$max_login_count = 3;   // only allow to try logining 3 time, 0 is not restriction.
$login_interval  = 60;  // user will be banned during this time.

// if a user fail to invoke a general service over a specified times, will be banned temporarily.
$max_try_count = 5; // 0 is not restriction.
$try_interval = 60;

?>