USE delay;

CREATE TEMPORARY TABLE t1
(
  SELECT * FROM `arrivals` 
  WHERE 
  DAYOFWEEK(arrival_time) = 5
  AND
  HOUR(arrival_time) = 9 
  AND
  (stop_code_lbsl = 11469 OR stop_code_lbsl = 10002)
);

CREATE TEMPORARY TABLE IF NOT EXISTS t2 AS (SELECT * FROM t1);


SELECT t1.stop_code_lbsl start,
       t2.stop_code_lbsl end, 
       t1.route, 
       t1.trip_id, 
       DATE(t1.arrival_time) date,
       DATE_FORMAT(t1.arrival_time, '%T') start_time,
       DATE_FORMAT(t2.arrival_time, '%T') end_time,
       TIME_TO_SEC(TIMEDIFF(t2.arrival_time, t1.arrival_time)) length_in_secs
FROM t1 
JOIN t2
WHERE t1.trip_id = t2.trip_id
AND t1.stop_code_lbsl < t2.stop_code_lbsl
ORDER BY start_time;

SELECT AVG(TIME_TO_SEC(TIMEDIFF(t2.arrival_time, t1.arrival_time))) length
FROM t1 
JOIN t2
WHERE t1.trip_id = t2.trip_id
AND t1.stop_code_lbsl < t2.stop_code_lbsl;