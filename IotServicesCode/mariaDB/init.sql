-- # create database
create database IF NOT EXISTS iot_data;

-- # Create a new user (only with local access) and grant privileges to this user on the new database:
grant all privileges on iot_data.* TO 'iot_user'@'%' identified by '9R[-RP#64nY7*E*H';

-- # After modifying the MariaDB grant tables, execute the following command in order to apply the hanges:
flush privileges;

-- #Change to the created database
use iot_data;

DROP TABLE IF EXISTS sensor_data cascade;
-- # create table for sensor data
CREATE OR REPLACE TABLE sensor_data (
    id MEDIUMINT NOT NULL AUTO_INCREMENT,
    device_id varchar(50) NOt NULL,
    longitude float NOT NULL,
    latitude float NOT NULL,
    time varchar(50) NOT NULL,
    humidity float NOT NULL,
    temperature float NOT NULL,
    PRIMARY KEY (id)
);

TRUNCATE TABLE sensor_data;
-- # query over table sensor_data
SELECT temperature, humidity, time, latitude, longitude, device_id FROM sensor_data ORDER BY id DESC LIMIT 1;

DROP TABLE IF EXISTS devices cascade;
-- # create table for storing device IDs
CREATE OR REPLACE TABLE devices (
    id MEDIUMINT NOT NULL AUTO_INCREMENT,
    longitude float NOT NULL,
    latitude float NOT NULL,
    time varchar(50) NOT NULL,
    device_id varchar(50) NOt NULL,
    state varchar(20) NOT NULL,
    UNIQUE  (device_id),
    PRIMARY KEY (id)
);
TRUNCATE TABLE devices;
-- # query over table sensor_data
SELECT device_id, time, latitude, longitude FROM devices ORDER BY id DESC LIMIT 1;