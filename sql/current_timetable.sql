USE delay;

TRUNCATE arrivals_last_hour;

INSERT INTO arrivals_last_hour
SELECT *
FROM current_arrivals
WHERE recorded_time >= DATE_SUB(NOW(),INTERVAL 1 HOUR);

TRUNCATE current_travel_time_log;

SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;
INSERT INTO current_travel_time_log
SELECT t1.stop_code_lbsl start_stop,
       t2.stop_code_lbsl end_stop,
       t1.route route,
       t1.trip_id trip_id,
       t1.vehicle_id vehicle_id,
       t1.arrival_time start_time,
       t2.arrival_time end_time,
       TIME_TO_SEC(TIMEDIFF(t2.arrival_time, t1.arrival_time)) travel_time,
       t2.arrival_date `date`,
       DAYNAME(t2.arrival_time) day,
       HOUR(t2.arrival_time) hour
FROM delay_neighbours AS neighbours
INNER JOIN arrivals_last_hour AS t1
  ON t1.stop_code_lbsl = neighbours.start_stop
  AND t1.route = neighbours.route
INNER JOIN arrivals_last_hour AS t2
  ON t2.stop_code_lbsl = neighbours.end_stop
  AND t2.route = neighbours.route
  AND t1.trip_id = t2.trip_id
  AND t1.vehicle_id = t2.vehicle_id;
COMMIT;


TRUNCATE delay_current_timetable_new;

SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;
INSERT INTO delay_current_timetable_new
(start_stop, end_stop, average_travel_time, `date`, day, hour)
SELECT start_stop, end_stop, TRUNCATE(AVG(travel_time), 1) average_travel_time, `date`, day, hour
FROM current_travel_time_log
WHERE travel_time > 0 AND travel_time < 1800
GROUP BY start_stop, end_stop;
COMMIT;

DROP TABLE IF EXISTS delay_current_timetable_old;

RENAME TABLE delay_current_timetable TO delay_current_timetable_old,
             delay_current_timetable_new TO delay_current_timetable;

SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;
INSERT INTO delay_current_timetable_log
(start_stop, end_stop, average_travel_time, `date`, day, hour)
SELECT start_stop, end_stop, average_travel_time, `date`, day, hour
FROM delay_current_timetable_old;
COMMIT;

RENAME TABLE delay_current_timetable_old TO
  delay_current_timetable_new;


