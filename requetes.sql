create table station(
    stop_id numeric(5,0)
    latitude TEXT,
    longitude TEXT,
    name varchar(150),
    constraint PK_station primary key(stop_id)
);

CREATE TABLE registered (
    name varchar(50),
    from_station varchar(150),
    to_station varchar(150),
    constraint PK_registered primary key(from_station, to_station)
)

create table travel_mode(
    route_type numeric(2,0),
    mode_name varchar(30),
    constraint PK_travel_mode primary key(route_type)
);


create table route(
    route_id numeric(10,0),
    route_name varchar(30),
    route_type numeric(2,0),
    constraint PK_route primary key(route_id),
    constraint FK_route_travel_mode foreign key(route_type) references travel_mode
);

create table network(
    from_stop numeric(5,0),
    to_stop numeric(5,0),
    dep_time_ut numeric(12,0),
    arr_time_ut numeric(12,0),
    route_type numeric(2,0),
    trip_I numeric(7,0),
    seq numeric(5),
    route_id numeric(10,0),
    distance numeric(10, 5),
    duration_avg numeric(30, 20),
    constraint PK_network primary key(from_stop, to_stop,dep_time_ut, arr_time_ut, route_id, trip_I),
    constraint FK_network_from_station foreign key(from_stop) references station,
    constraint FK_network_to_station foreign key(to_stop) references station,
    constraint FK_network_route foreign key(route_id) references route
);

create table walk(
    from_stop numeric(5,0),
    to_stop numeric(5,0),
    distance_walk numeric(10, 5),
    distance_osm_walk numeric(10,0),
    constraint PK_walk primary key(from_stop, to_stop),
    constraint FK_walk_from_station foreign key(from_stop) references station
);


create table disturb(
    d_id SERIAL primary key,
    route_id numeric(10,0),
    d_type varchar(150),
    d_message  TEXT,
    start_at date,
    end_at date,
    constraint FK_disturb_route foreign key(route_id) references route
);


-- create table network_bis(
--     from_stop numeric(5,0),
--     to_stop numeric(5,0),
--     distance numeric(10, 5),
--     duration_avg numeric(30, 20),
--     nb_vehicules numeric(5,0),
--     route_id numeric(10,0),
--     constraint PK_networkbis primary key(from_stop, to_stop,route_id)
--     );
