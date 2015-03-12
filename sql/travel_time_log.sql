USE delay; 

DROP TABLE IF EXISTS travel_time_log_main2; 

CREATE TABLE travel_time_log_main2
(
	SELECT t1.stop_code_lbsl start_stop,
	       t2.stop_code_lbsl end_stop, 
	       t1.route route, 
	       t1.trip_id trip_id, 
	       t1.vehicle_id vehicle_id,
	       DAYNAME(t1.arrival_time) day, 
	       t1.arrival_date date,
	       HOUR(t1.arrival_time) hour,
	       t1.arrival_time start_time,
	       t2.arrival_time end_time,
	       TIME_TO_SEC(TIMEDIFF(t2.arrival_time, t1.arrival_time)) travel_time
	FROM neighbours 
	INNER JOIN arrivals AS t1 
		ON t1.stop_code_lbsl = neighbours.start_stop 
		AND t1.route = neighbours.route
	INNER JOIN arrivals AS t2
		ON t2.stop_code_lbsl = neighbours.end_stop 
		AND t2.route = neighbours.route
		AND t1.trip_id = t2.trip_id
		AND t1.vehicle_id = t2.vehicle_id
		AND t1.arrival_date = t2.arrival_date
	-- WHERE t1.arrival_time < t2.arrival_time
);

