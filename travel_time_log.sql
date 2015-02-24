USE delay; 

DROP TABLE IF EXISTS travel_time_log; 

CREATE TABLE travel_time_log
(
	SELECT t1.stop_code_lbsl start_stop,
	       t2.stop_code_lbsl end_stop, 
	       t1.route, 
	       t1.trip_id, 
	       DAYNAME(t1.arrival_time) day, 
	       DATE(t1.arrival_time) date,
	       HOUR(t1.arrival_time) hour,
	       TIME_TO_SEC(TIMEDIFF(t2.arrival_time, t1.arrival_time)) travel_time
	FROM neighbours 
	INNER JOIN arrivals_part_2 AS t1 
		ON t1.stop_code_lbsl = neighbours.start_stop 
		AND t1.route = neighbours.route
	INNER JOIN arrivals_part_2 AS t2
		ON t2.stop_code_lbsl = neighbours.end_stop 
		AND t2.route = neighbours.route
		AND t1.trip_id = t2.trip_id
		AND DATE(t1.arrival_time) = DATE(t2.arrival_time)
	WHERE t1.arrival_time < t2.arrival_time
	ORDER BY day, hour, start_stop, end_stop
);

