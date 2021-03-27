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
