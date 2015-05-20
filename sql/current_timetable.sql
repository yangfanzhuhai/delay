USE delay;

DROP TABLE IF EXISTS recent_arrivals;

CREATE TABLE recent_arrivals (
  SELECT *
  FROM delay_arrivals
  WHERE recorded_time >= DATE_SUB(NOW(),INTERVAL 1 HOUR)
);

ALTER TABLE recent_arrivals ADD INDEX stop_code_lbsl (stop_code_lbsl);

ALTER TABLE recent_arrivals ADD INDEX arrival_time (arrival_time);

ALTER TABLE recent_arrivals ADD INDEX route (route);

ALTER TABLE recent_arrivals ADD INDEX trip_id (trip_id);

ALTER TABLE recent_arrivals ADD INDEX vehicle_id (vehicle_id);

DROP TABLE IF EXISTS current_travel_time_log;

CREATE TABLE current_travel_time_log
(
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
    AND t1.vehicle_id = t2.vehicle_id
);

ALTER TABLE current_travel_time_log ADD INDEX stops (start_stop, end_stop);

DROP TABLE IF EXISTS delay_current_timetable;

CREATE TABLE delay_current_timetable (
    SELECT start_stop, end_stop, TRUNCATE(AVG(travel_time), 1) average_travel_time
    FROM current_travel_time_log
    WHERE travel_time > 0 AND travel_time < 1800
    GROUP BY start_stop, end_stop
);

