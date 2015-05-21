USE delay;

TRUNCATE recent_arrivals;

INSERT INTO recent_arrivals
SELECT *
FROM delay_arrivals
WHERE recorded_time >= DATE_SUB(NOW(),INTERVAL 1 HOUR);

TRUNCATE current_travel_time_log;

INSERT INTO current_travel_time_log
SELECT t1.stop_code_lbsl start_stop,
       t2.stop_code_lbsl end_stop,
       t1.route route,
       t1.trip_id trip_id,
       t1.vehicle_id vehicle_id,
       t1.arrival_time start_time,
       t2.arrival_time end_time,
       TIME_TO_SEC(TIMEDIFF(t2.arrival_time, t1.arrival_time)) travel_time
FROM delay_neighbours AS neighbours
INNER JOIN recent_arrivals AS t1
  ON t1.stop_code_lbsl = neighbours.start_stop
  AND t1.route = neighbours.route
INNER JOIN recent_arrivals AS t2
  ON t2.stop_code_lbsl = neighbours.end_stop
  AND t2.route = neighbours.route
  AND t1.trip_id = t2.trip_id
  AND t1.vehicle_id = t2.vehicle_id;

TRUNCATE delay_current_timetable;

INSERT INTO delay_current_timetable
SELECT start_stop, end_stop, TRUNCATE(AVG(travel_time), 1) average_travel_time
FROM current_travel_time_log
WHERE travel_time > 0 AND travel_time < 1800
GROUP BY start_stop, end_stop;

