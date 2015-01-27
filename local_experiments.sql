USE delay;

DROP TABLE stops_10002_11469;

CREATE TEMPORARY TABLE t1
(
  SELECT * FROM `arrivals` 
  WHERE expire_time = 0
  AND (stop_code_lbsl = 11469 
  OR stop_code_lbsl = 10002)
);

CREATE TEMPORARY TABLE IF NOT EXISTS t2 AS (SELECT * FROM t1);

CREATE TABLE stops_10002_11469 (
SELECT t1.stop_code_lbsl start,
       t2.stop_code_lbsl end, 
       t1.route, 
       t1.trip_id, 
       DATE(t1.arrival_time) date,
       DAYNAME(t1.arrival_time) day, 
       -- DATE_FORMAT(t1.arrival_time, '%T') start_time,
       -- DATE_FORMAT(t2.arrival_time, '%T') end_time,
       t1.arrival_time start_time,
       t2.arrival_time end_time,
       TIME_TO_SEC(TIMEDIFF(t2.arrival_time, t1.arrival_time)) length_in_secs
FROM t1 
JOIN t2
WHERE DATE(t1.arrival_time) = DATE(t2.arrival_time)
AND t1.trip_id = t2.trip_id
AND t1.stop_code_lbsl < t2.stop_code_lbsl
AND t1.arrival_time < t2.arrival_time
ORDER BY start_time );

-- Observations:
-- 1. Order by length_in_secs
-- - when journey time is short, the start_time is usually in odd hours -> between 9pm and 6am

-- 2. There are abnormalies - explanations?
-- - journey time = 1s or 4000s

-- 3. 



SELECT AVG(TIME_TO_SEC(TIMEDIFF(t2.arrival_time, t1.arrival_time))) length
FROM t1 
JOIN t2
WHERE t1.trip_id = t2.trip_id
AND t1.stop_code_lbsl < t2.stop_code_lbsl;





