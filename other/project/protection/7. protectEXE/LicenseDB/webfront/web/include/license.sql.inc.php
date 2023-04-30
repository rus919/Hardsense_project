<?php
//
// Note: each sql statement here must start with 'create table' and end with ';', 
//       or otherwise will cause incorrect result.
//
function get_license_sql(){
	$sql = <<<SQL_END

CREATE TABLE IF NOT EXISTS `banhardware` (
  `UserID` text,
  `HardwareHash` varchar(32) NOT NULL DEFAULT '',
  PRIMARY KEY (`HardwareHash`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `banlog` (
  `Reason` text,
  `Time` datetime DEFAULT NULL,
  `LicenseHash` varchar(32) DEFAULT NULL,
  `HardwareHash` varchar(32) DEFAULT NULL,
  `Version` text,
  `Type` text,
  `IP` text
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `fail` (
  `Time` datetime DEFAULT NULL,
  `LicenseHash` varchar(32) DEFAULT NULL,
  `HardwareHash` varchar(32) DEFAULT NULL,
  `IP` text
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `licenses` (
  `UserID` text,
  `Remarks` text,
  `LicenseHash` varchar(32) NOT NULL,
  `HardwareHash` varchar(32) DEFAULT NULL,
  `LicenseExpiration` datetime DEFAULT NULL,
  `LicensedCount` int(11) DEFAULT NULL,
  `TotalCount` int(11) NOT NULL DEFAULT '0',
  `Banned` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`LicenseHash`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `log` (
  `Time` datetime DEFAULT NULL,
  `UserID` text,
  `HardwareHash` varchar(32) DEFAULT NULL,
  `IP` text
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

SQL_END;

	return $sql;
}
?>