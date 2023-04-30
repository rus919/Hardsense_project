<?php

// prevent user directly accessing this page.
if( !defined('VALID_ENTRY_POINT') ){
    exit;
}

?>
<dl class="menu">
<dt><?php echo t( array( 'zh-cn'=>'我的登录', 'zh-tw'=>'我的登錄', 'en-us'=>'My Login' ) );?></dt>
<dd>
    <div id="login_box"><?php
    
echo htmlspecialchars( $_SESSION['Username'] );

?></div>
    <ul>
        <li><a href="<?php echo user_url('/'); ?>"><?php echo t( array( 'zh-cn'=>'切换前台',     'zh-tw'=>'切換前台',    'en-us'=>'Goto Front-End' ) );?></a></li>
        <li><a href="<?php echo user_url('/logout'); ?>"><?php echo t( array( 'zh-cn'=>'退出登录',     'zh-tw'=>'退出登錄',    'en-us'=>'Logout' ) );?></a></li>
    </ul>
</dd>
<dt><?php echo t( array( 'zh-cn'=>'订单系统', 'zh-tw'=>'訂單系統', 'en-us'=>'Order System' ) );?></dt>
<dd>
    <ul>
        <li><a href="<?php echo url('order-system/customers'); ?>"><?php echo t( array( 'zh-cn'=>'客户管理',     'zh-tw'=>'客戶管理',    'en-us'=>'Customers' ) );?></a></li>
        <li><a href="<?php echo url('order-system/products'); ?>"><?php echo t( array( 'zh-cn'=>'产品设置',     'zh-tw'=>'產品設置',    'en-us'=>'Products' ) );?></a></li>
        <li><a href="<?php echo url('order-system/cards'); ?>"><?php echo t( array( 'zh-cn'=>'充值卡管理', 'zh-tw'=>'充值卡管理', 'en-us'=>'Card management' ) );?></a></li>
        <li><a href="<?php echo url('order-system/charges'); ?>"><?php echo t( array( 'zh-cn'=>'充值记录', 'zh-tw'=>'充值記錄', 'en-us'=>'Charges' ) );?></a></li>
        <li><a href="<?php echo url('order-system/orders'); ?>"><?php echo t( array( 'zh-cn'=>'订单记录', 'zh-tw'=>'訂單記錄', 'en-us'=>'Orders' ) );?></a></li>
		<li><a href="<?php echo url('licensing-records'); ?>"><?php echo t( array( 'zh-cn'=>'授权记录', 'zh-tw'=>'授權記錄', 'en-us'=>'Licensing Records' ) );?></a></li>
    </ul>
</dd>
</dl>
