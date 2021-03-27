DROP DATABASE logistics IF EXISTS;
CREATE DATABSE logistics;
USE logistics;

-- Creating date and time dimensions
--- Credit to http://www.dwhworld.com/2010/08/date-dimension-sql-scripts-mysql/
-- Small-numbers table
DROP TABLE IF EXISTS numbers_small;
CREATE TABLE numbers_small (number INT);
INSERT INTO numbers_small VALUES (0),(1),(2),(3),(4),(5),(6),(7),(8),(9);

-- Main-numbers table
DROP TABLE IF EXISTS numbers;
CREATE TABLE numbers (number BIGINT);
INSERT INTO numbers
SELECT thousands.number * 1000 + hundreds.number * 100 + tens.number * 10 + ones.number
FROM numbers_small thousands, numbers_small hundreds, numbers_small tens, numbers_small ones
LIMIT 1000000;

-- Create Date Dimension table
DROP TABLE IF EXISTS date_d;
CREATE TABLE date_d (
date_key          BIGINT PRIMARY KEY,
date             DATE NOT NULL,
year             INT,
month            CHAR(10),
month_of_year    CHAR(2),
day_of_month     INT,
day              CHAR(10),
day_of_week      INT,
weekend          CHAR(10) NOT NULL DEFAULT "Weekday",
day_of_year      INT,
week_of_year     CHAR(2),
quarter  INT,
previous_day     date NOT NULL default '0000-00-00',
next_day         date NOT NULL default '0000-00-00',
UNIQUE KEY `date` (`date`));

-- First populate with ids and Date
-- Change year start and end to match your needs. The above sql creates records for year 2010.
INSERT INTO date_d (date_key, date)
SELECT number, DATE_ADD( '2014-01-01', INTERVAL number DAY )
FROM numbers
WHERE DATE_ADD( '2014-01-01', INTERVAL number DAY ) BETWEEN '2014-01-01' AND '2024-12-31'
ORDER BY number;

-- Update other columns based on the date.
UPDATE date_d SET
year            = DATE_FORMAT( date, "%Y" ),
month           = DATE_FORMAT( date, "%M"),
month_of_year   = DATE_FORMAT( date, "%m"),
day_of_month    = DATE_FORMAT( date, "%d" ),
day             = DATE_FORMAT( date, "%W" ),
day_of_week     = DAYOFWEEK(date),
weekend         = IF( DATE_FORMAT( date, "%W" ) IN ('Saturday','Sunday'), 'Weekend', 'Weekday'),
day_of_year     = DATE_FORMAT( date, "%j" ),
week_of_year    = DATE_FORMAT( date, "%V" ),
quarter         = QUARTER(date),
previous_day    = DATE_ADD(date, INTERVAL -1 DAY),
next_day        = DATE_ADD(date, INTERVAL 1 DAY);

-- credit to Akom's Tech Ruminations
-- http://tech.akom.net/archives/36-Creating-A-Basic-Date-Dimension-Table-in-MySQL.html
DROP TABLE IF EXISTS  time_d;
CREATE TABLE IF NOT EXISTS time_d  (
    time_key INT NOT NULL auto_increment,
    fulltime time,
    hour int,
    minute int,
    ampm varchar(2),
    PRIMARY KEY(time_key)
) ENGINE=InnoDB AUTO_INCREMENT=1000;


delimiter //

DROP PROCEDURE IF EXISTS timedimbuild;
CREATE PROCEDURE timedimbuild ()
BEGIN
    DECLARE v_full_date DATETIME;

    DELETE FROM time_d;

    SET v_full_date = '2009-03-01 00:00';
    WHILE v_full_date < '2009-03-02 00:00' DO

        INSERT INTO time_d (
            fulltime ,
            hour ,
            minute ,
            ampm
        ) VALUES (
            TIME(v_full_date),
            HOUR(v_full_date),
            MINUTE(v_full_date),
            DATE_FORMAT(v_full_date,'%p')
        );

        SET v_full_date = DATE_ADD(v_full_date, INTERVAL 1 MINUTE);
    END WHILE;
END;

//
delimiter ;

-- call the stored procedure
call timedimbuild();


-- Creating the database fact and dimensions

DROP TABLE IF EXISTS  truck_run_f;
DROP TABLE IF EXISTS shipper_d;
DROP TABLE IF EXISTS  carrier_d;
DROP TABLE IF EXISTS  lane_d;
DROP TABLE IF EXISTS  on_time_d;
DROP TABLE IF EXISTS  sourcing_channel_d;
DROP TABLE IF EXISTS  equipment_type_d;
DROP TABLE IF EXISTS  load_d;
DROP TABLE IF EXISTS  tracking_d;


CREATE TABLE shipper_d (
    shipper_key int NOT NULL PRIMARY KEY AUTO_INCREMENT,
    shipper_name varchar(255) NOT NULL
);

CREATE TABLE carrier_d (
    carrier_key int NOT NULL PRIMARY KEY AUTO_INCREMENT,
    carrier_name varchar(255) NOT NULL,
    vip_indicator varchar(255) NOT NULL,
    carrier_rating smallint,
    carrier_dropped smallint
);

CREATE TABLE lane_d (
    lane_key int NOT NULL PRIMARY KEY AUTO_INCREMENT,
    origin_city varchar(255) NOT NULL,
    origin_state varchar(255) NOT NULL,
    origin_country varchar(255) NOT NULL,
    mileage float not null,
    destination_city varchar(255) NOT NULL,
    destination_state varchar(255) NOT NULL,
    destination_country varchar(255) NOT NULL,
    city_pair varchar(255) NOT NULL
);

CREATE TABLE on_time_d (
    on_time_key int NOT NULL PRIMARY KEY AUTO_INCREMENT,
    pickup_indicator varchar(255) NOT NULL,
    delivery_indicator varchar(255) NOT NULL,
    overall_indicator varchar(255) NOT NULL
);

CREATE TABLE sourcing_channel_d (
  sourcing_channel_key int NOT NULL PRIMARY KEY AUTO_INCREMENT,
  sourcing_channel_indicator varchar(255) NOT NULL
);

CREATE TABLE equipment_type_d (
    equipment_type_key int NOT NULL PRIMARY KEY AUTO_INCREMENT,
    equipment_type_indicator varchar(255) NOT NULL
);

CREATE TABLE load_d (
  load_key int NOT NULL PRIMARY KEY AUTO_INCREMENT,
  contracted_indicator varchar(255) NOT NULL,
  booked_indicator varchar(255) NOT NULL,
  sourced_indicator varchar(255) NOT NULL,
  cancelled_indicator varchar(255) NOT NULL
);

CREATE TABLE tracking_d (
    tracking_key int NOT NULL PRIMARY KEY AUTO_INCREMENT,
    mobile_app_indicator varchar(255) NOT NULL,
    macro_point_indicator varchar(255) NOT NULL,
    edi_indicator varchar(255) NOT NULL
);

CREATE TABLE truck_run_f (
    quote_date bigint not null,
    FOREIGN KEY (quote_date) REFERENCES date_d(date_key),
    quote_time int not null,
    FOREIGN KEY (quote_time) REFERENCES time_d(time_key),
    book_date bigint not null,
    FOREIGN KEY (book_date) REFERENCES date_d(date_key),
    book_time int not null,
    FOREIGN KEY (book_time) REFERENCES time_d(time_key),
    source_date bigint,
    FOREIGN KEY (source_date) REFERENCES date_d(date_key),
    source_time int,
    FOREIGN KEY (source_time) REFERENCES time_d(time_key),
    pickup_appointment_date bigint not null,
    FOREIGN KEY (pickup_appointment_date) REFERENCES date_d(date_key),
    pickup_appointment_time int not null,
    FOREIGN KEY (pickup_appointment_time) REFERENCES time_d(time_key),
    pickup_date bigint not null,
    FOREIGN KEY (pickup_date) REFERENCES date_d(date_key),
    pickup_time int not null,
    FOREIGN KEY (pickup_time) REFERENCES time_d(time_key),
    delivery_appointment_date bigint not null,
    FOREIGN KEY (delivery_appointment_date) REFERENCES date_d(date_key),
    delivery_appointment_time int not null,
    FOREIGN KEY (delivery_appointment_time) REFERENCES time_d(time_key),
    delivery_date bigint not null,
    FOREIGN KEY (delivery_date) REFERENCES date_d(date_key),
    delivery_time int not null,
    FOREIGN KEY (delivery_time) REFERENCES time_d(time_key),
    lane_key int not null,
    FOREIGN KEY (lane_key) REFERENCES lane_d(lane_key),
    book_price float not null,
    source_price float not null,
    profit_and_loss float not null,
    shipper_key int NOT NULL,
    carrier_key int NOT NULL,
    on_time_key int NOT NULL,
    sourcing_channel_key int NOT NULL,
    equipment_type_key int NOT NULL,
    load_key int NOT NULL,
    tracking_key int NOT NULL,
    FOREIGN KEY (shipper_key) REFERENCES shipper_d(shipper_key),
    FOREIGN KEY (carrier_key) REFERENCES carrier_d(carrier_key),
    FOREIGN KEY (on_time_key) REFERENCES on_time_d(on_time_key),
    FOREIGN KEY (sourcing_channel_key) REFERENCES sourcing_channel_d(sourcing_channel_key),
    FOREIGN KEY (equipment_type_key) REFERENCES equipment_type_d(equipment_type_key),
    FOREIGN KEY (load_key) REFERENCES load_d(load_key),
    FOREIGN KEY (tracking_key) REFERENCES tracking_d(tracking_key)
);

INSERT INTO equipment_type_d (equipment_type_indicator) VALUES ('Unknown');
INSERT INTO equipment_type_d (equipment_type_indicator) VALUES ('DRV');
INSERT INTO equipment_type_d (equipment_type_indicator) VALUES ('RFR');
INSERT INTO equipment_type_d (equipment_type_indicator) VALUES ('FBE');

INSERT INTO sourcing_channel_d (sourcing_channel_indicator) VALUES ('Unknown');
INSERT INTO sourcing_channel_d (sourcing_channel_indicator) VALUES ('Carrier Capacity');
INSERT INTO sourcing_channel_d (sourcing_channel_indicator) VALUES ('Ts In');
INSERT INTO sourcing_channel_d (sourcing_channel_indicator) VALUES ('Ts Out');
INSERT INTO sourcing_channel_d (sourcing_channel_indicator) VALUES ('Source List');
INSERT INTO sourcing_channel_d (sourcing_channel_indicator) VALUES ('Dat Out');
INSERT INTO sourcing_channel_d (sourcing_channel_indicator) VALUES ('Dat In');
INSERT INTO sourcing_channel_d (sourcing_channel_indicator) VALUES ('Live Jobs');
INSERT INTO sourcing_channel_d (sourcing_channel_indicator) VALUES ('External Source List');
