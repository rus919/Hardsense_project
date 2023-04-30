CREATE DATABASE `licensedb` DEFAULT CHARACTER SET utf8;

USE licensedb;

GRANT SELECT,INSERT,UPDATE ON licensedb.* TO 'user'@'%' IDENTIFIED BY 'password';

CREATE TABLE `Licenses`
(
       UserID TEXT,
       Remarks TEXT,
       LicenseHash VARCHAR(32) NOT NULL,
       HardwareHash VARCHAR(32) NULL DEFAULT NULL,
       LicenseExpiration DATETIME,
       LicensedCount INTEGER,
       TotalCount INTEGER NOT NULL DEFAULT "0" ,
       Banned BOOLEAN NOT NULL DEFAULT FALSE ,
       PRIMARY KEY (LicenseHash)
);

CREATE TABLE `Fail`
(
       Time DATETIME,
       LicenseHash VARCHAR(32),
       HardwareHash VARCHAR(32) NULL DEFAULT NULL,
       `IP`  TEXT
);

CREATE TABLE `Log`
(
       Time DATETIME,
       UserID TEXT,
       HardwareHash VARCHAR(32) NULL DEFAULT NULL,
       `IP`  TEXT
);

CREATE TABLE `BanHardware`
(
       UserID TEXT,
       HardwareHash VARCHAR(32),
PRIMARY KEY (HardwareHash)
);

CREATE TABLE `BanLog`
(
       Reason TEXT,
       Time DATETIME,
       LicenseHash VARCHAR(32),
       HardwareHash VARCHAR(32),
       Version TEXT, `Type`  TEXT, `IP`  TEXT);

