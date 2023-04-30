<?php

// prevent user directly accessing this page.
if( !defined('VALID_ENTRY_POINT') ){
    exit;
}
//
// page container
//
ob_start();
?>
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <title><?php
echo t( array( 'zh-cn'=>'Safengine 网络授权平台', 'zh-tw'=>'Safengine 网路授权平台', 'en-us'=>'Safengine Net Authorization Platform' ));
?></title>
    <link rel="stylesheet" type="text/css" href="<?php echo $template_path;?>page.css">
</head>
<body>
    <table width="800" cellspacing="0" cellpadding="0" id="page-container" align="center">
        <tr><td colspan="2" background="<?php echo $template_path;?>top.png" width="800" height="80" style="position:relative"><div id="select_lang"><?php 

        echo '<a href="'. url( implode('/',$selector_array), 'zh-cn') . '">简体中文</a> '; 
        echo '<a href="'. url( implode('/',$selector_array), 'zh-tw') . '">繁體中文</a> '; 
        echo '<a href="'. url( implode('/',$selector_array), 'en-us') . '">English</a> '; 

?></div></td></tr>
        <tr><td colspan="2" class="bcbar"><div id="breadcrumb"><?php

echo t( array( 'zh-cn'=>'当前位置', 'zh-tw'=>'當前位置', 'en-us'=>'Location' )) .'： '. $breadcrumb; 

?></div></td></tr>
        <tr><td width="150" valign="top"><?php 

			if( ROOT_PATH == '' ){
		        include(ROOT_PATH.'include/menu.inc.php');
			}
			else{
		        include('menu.inc.php');
			}

?></td><td width="650" valign="top"><div id="panel"><?php 
if(!empty($intro_pic)){
	echo '<img src="'.$template_path.$intro_pic.'" border="0"/><br/>'; 
}
?>{content}</div></td></tr>
		<tr><td colspan="2" id="footer" background="<?php echo $template_path;?>btm.png"></td></tr>
        <tr><td colspan="2" id="footer2"><span id="copyright"><?php

echo t( array( 'zh-cn'=>'版权所有(C)2009-2010, Safengine', 'zh-tw'=>'版權所有(C)2009-2010, Safengine', 'en-us'=>'Copyright(C)2009-2010, Safengine' ));

?></span> <span class="spp">|</span> <span id="icp"><a href="http://www.miibeian.gov.cn" target="_blank"><?php echo $icp;?></a></span><div id="footer-text"><?php

echo '<a href="http://www.safengine.com" target="_blank">'.                      t( array( 'zh-cn'=>'官方网站', 'zh-tw'=>'官方網站', 'en-us'=>'Official Website' )) .'</a> <span class="spp">|</span> ';
echo '<a href="http://www.safengine.com/products/netlicensor" target="_blank">'. t( array( 'zh-cn'=>'产品系列', 'zh-tw'=>'產品系列', 'en-us'=>'Products' ))                .'</a> <span class="spp">|</span> ';
echo '<a href="http://www.safengine.com/downloads/get-demo" target="_blank">'. t( array( 'zh-cn'=>'下载产品', 'zh-tw'=>'下載產品', 'en-us'=>'Downloads' ))                .'</a> <span class="spp">|</span> ';
echo '<a href="http://www.safengine.com/downloads/get-demo" target="_blank">'. t( array( 'zh-cn'=>'安全技术介绍', 'zh-tw'=>'安全技術介紹', 'en-us'=>'Features' ))                .'</a> <span class="spp">|</span> ';
echo '<a href="http://www.safengine.com/support/contact-us" target="_blank">'.   t( array( 'zh-cn'=>'技术与销售服务', 'zh-tw'=>'技術與銷售服務', 'en-us'=>'Support' ))                 .'</a>';

?></div></td></tr>
    </table>
</body>
</html>
<?php
$page_content = ob_get_contents();
ob_end_clean();

?>