DROP DATABASE IF EXISTS monitoring;
CREATE DATABASE monitoring COLLATE utf8_general_ci;
use monitoring;

CREATE TABLE usb (
	id INT PRIMARY KEY AUTO_INCREMENT,
	computer_name VARCHAR(25),
	time_stamp DATETIME DEFAULT CURRENT_TIMESTAMP,
	device_name VARCHAR(25),
	description VARCHAR(50),
	device_type VARCHAR(25),
	connected VARCHAR(3),
	safe_to_unplug VARCHAR(3),
	disabled VARCHAR(3),
	drive_letter VARCHAR(5),
	serial_number VARCHAR(25),
	firmware_revision VARCHAR(10),
);

CREATE TABLE network (
	id INT PRIMARY KEY AUTO_INCREMENT,
	computer_name VARCHAR(25),
	time_stamp DATETIME DEFAULT CURRENT_TIMESTAMP,
	name VARCHAR(50),
	default_gateway VARCHAR(25),
	ip_address VARCHAR(50),
	mac_address VARCHAR(20),
);

CREATE TABLE product (
	id INT PRIMARY KEY AUTO_INCREMENT,
	computer_name VARCHAR(25),
	time_stamp DATETIME DEFAULT CURRENT_TIMESTAMP,
	name VARCHAR(50),
);

CREATE TABLE os (
	id INT PRIMARY KEY AUTO_INCREMENT,
	computer_name VARCHAR(25),
	time_stamp DATETIME DEFAULT CURRENT_TIMESTAMP,
	os_name VARCHAR(50),
	build_number VARCHAR(15),
	version VARCHAR(15),
	system_directory VARCHAR(50),
	install_date VARCHAR(50),
	service_pack INT,
	distributed CHAR(5),
	number_of_users INT,
	os_type INT,
	windows_directory VARCHAR(50),
);
