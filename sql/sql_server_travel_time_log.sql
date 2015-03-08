
SET SHOWPLAN_TEXT ON

IF OBJECT_ID('dbo.travel_time_log_main', 'U') IS NOT NULL
  DROP TABLE dbo.travel_time_log_main

SELECT t1.stop_code_lbsl start_stop,
	   t2.stop_code_lbsl end_stop, 
       t1.route route,
       t1.trip_id trip_id, 
       t1.vehicle_id vehicle_id,
       DATENAME(weekday, t1.arrival_time) day,
       t1.arrival_date arrival_date,
       DATENAME(hour, t1.arrival_time) hour,
       DATEDIFF(second, t1.arrival_time, t2.arrival_time) travel_time
INTO travel_time_log_main
FROM arrivals AS t1
INNER JOIN neighbours 
ON t1.stop_code_lbsl = neighbours.start_stop_code_lbsl 
AND t1.route = neighbours.route
INNER JOIN arrivals AS t2
ON t2.stop_code_lbsl = neighbours.end_stop_code_lbsl
AND t2.route = neighbours.route
AND t1.trip_id = t2.trip_id
AND t1.vehicle_id = t2.vehicle_id
AND t1.arrival_date = t2.arrival_date
WHERE t1.arrival_time < t2.arrival_time

