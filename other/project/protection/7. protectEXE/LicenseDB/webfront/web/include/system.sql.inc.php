<?php

function get_system_intialized_sql($user, $password, $ip){
	$user = addslashes( $user );
	$password = md5( $password );
	return "insert into users (Username,Password,RegTime,RegIP,LastTime,LastIP,LoginCount,IsAdmin,Amount) values ('$user','$password',now(),'$ip',now(),'$ip',0,1,0)";
}

function get_system_sql(){
	$sql = <<<SQL_END

CREATE TABLE IF NOT EXISTS `cards` (
  `CardId` int(10) NOT NULL AUTO_INCREMENT,
  `CardNumber` varchar(32) DEFAULT NULL,
  `Password` varchar(32) DEFAULT NULL,
  `Amount` int(10) DEFAULT '0',
  `GeneratedTime` datetime DEFAULT NULL,
  `UsedTime` datetime DEFAULT NULL,
  `Discard` tinyint(4) DEFAULT '0',
  PRIMARY KEY (`CardId`),
  UNIQUE KEY `CardNumber` (`CardNumber`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AUTO_INCREMENT=2938744;


CREATE TABLE IF NOT EXISTS `charge` (
  `CID` int(10) NOT NULL AUTO_INCREMENT,
  `UID` int(10) DEFAULT NULL,
  `Type` tinyint(4) DEFAULT '0',
  `CardID` int(10) DEFAULT NULL,
  `Credential` tinytext,
  `Amount` int(10) DEFAULT '0',
  `Remarks` text,
  `Time` datetime DEFAULT NULL,
  PRIMARY KEY (`CID`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AUTO_INCREMENT=1884737;


CREATE TABLE IF NOT EXISTS `lockip` (
  `LID` int(10) NOT NULL AUTO_INCREMENT,
  `Type` tinyint(4) DEFAULT '0',
  `IP` varchar(15) DEFAULT NULL,
  `Time` int(10) DEFAULT '0',
  `Count` int(10) DEFAULT '0',
  PRIMARY KEY (`LID`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;


CREATE TABLE IF NOT EXISTS `orders` (
  `OID` int(10) NOT NULL AUTO_INCREMENT,
  `UID` int(10) DEFAULT NULL,
  `PID` int(10) DEFAULT NULL,
  `Type` tinyint(4) DEFAULT '0',
  `Number` int(10) DEFAULT NULL,
  `Time` int(10) DEFAULT NULL,
  `IP` varchar(15) DEFAULT NULL,
  `PaidTime` int(10) DEFAULT NULL,
  `PaidIP` varchar(15) DEFAULT NULL,
  `RenewID` int(10) DEFAULT '0',
  `ExpDate` int(10) DEFAULT '0',
  `HardwareID` varchar(40) DEFAULT '',
  PRIMARY KEY (`OID`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AUTO_INCREMENT=2134663;


CREATE TABLE IF NOT EXISTS `products` (
  `PId` int(10) NOT NULL AUTO_INCREMENT,
  `Name` tinytext,
  `Identifier` tinytext,
  `Version` tinytext,
  `Pic` tinytext,
  `Description` text,
  `Url` tinytext,
  `Price` int(10) DEFAULT '0',
  `PriceVersion` int(10) DEFAULT '0',
  `Time` datetime DEFAULT NULL,
  `Published` tinyint(4) DEFAULT '0',
  `Keyname` tinytext,
  `DataName` tinytext,
  `OutPath` tinytext,
  `c_LockHardwareID` tinyint(4) DEFAULT '0',
  `c_LockCPU` tinyint(4) DEFAULT '0',
  `c_LockMAC` tinyint(4) DEFAULT '0',
  `c_LockBIOS` tinyint(4) DEFAULT '0',
  `c_LockHDD` tinyint(4) DEFAULT '0',
  `c_NumDaysEn` tinyint(4) DEFAULT '0',
  `c_NumDays` int(10) unsigned DEFAULT '0',
  `c_NumExecEn` tinyint(4) DEFAULT '0',
  `c_NumExec` int(10) unsigned DEFAULT '0',
  `c_ExpDateEn` tinyint(4) DEFAULT '0',
  `c_ExpDate` int(10) unsigned DEFAULT '0',
  `c_CountryIdEn` tinyint(4) DEFAULT '0',
  `c_CountryId` int(10) unsigned DEFAULT '0',
  `c_ExecTimeEn` tinyint(4) DEFAULT '0',
  `c_ExecTime` int(10) unsigned DEFAULT '0',
  `c_TotalExecTimeEn` tinyint(4) DEFAULT '0',
  `c_TotalExecTime` int(10) unsigned DEFAULT '0',
  `d_host` varchar(64) DEFAULT '',
  `d_database` varchar(64) DEFAULT '',
  `d_username` varchar(64) DEFAULT '',
  `d_password` varchar(64) DEFAULT '',
  PRIMARY KEY (`PId`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AUTO_INCREMENT=1299833;

CREATE TABLE IF NOT EXISTS `users` (
  `UId` int(10) NOT NULL AUTO_INCREMENT,
  `Username` varchar(64) DEFAULT NULL,
  `Password` varchar(32) DEFAULT NULL,
  `RegTime` datetime DEFAULT NULL,
  `RegIP` varchar(15) DEFAULT NULL,
  `LastTime` datetime DEFAULT NULL,
  `LastIP` varchar(15) DEFAULT NULL,
  `LoginCount` int(10) DEFAULT '0',
  `IsAdmin` tinyint(4) DEFAULT '0',
  `Amount` int(10) DEFAULT '0',
  PRIMARY KEY (`UId`),
  UNIQUE KEY `Username` (`Username`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AUTO_INCREMENT=5283837;

CREATE TABLE IF NOT EXISTS `sessions` (
  `sesskey` varchar(64) NOT NULL DEFAULT '',
  `expiry` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `expireref` varchar(250) DEFAULT '',
  `created` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `modified` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `sessdata` longtext,
  PRIMARY KEY (`sesskey`),
  KEY `sess2_expiry` (`expiry`),
  KEY `sess2_expireref` (`expireref`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

SQL_END;

	return $sql;
}
?>