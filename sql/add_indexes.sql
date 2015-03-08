USE delay;

ALTER TABLE arrivals ADD INDEX stop_code_lbsl (stop_code_lbsl);

ALTER TABLE arrivals ADD INDEX arrival_time (arrival_time);

ALTER TABLE arrivals ADD INDEX route (route);

ALTER TABLE arrivals ADD INDEX trip_id (trip_id);

ALTER TABLE arrivals ADD INDEX vehicle_id (vehicle_id)