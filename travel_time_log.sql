USE delay; 

DROP PROCEDURE IF EXISTS rowperrow;
delimiter //
CREATE PROCEDURE rowperrow() 
BEGIN
	DECLARE n INT DEFAULT 0;
	DECLARE i INT DEFAULT 0;
	DECLARE start VARCHAR(64) DEFAULT NULL;
	DECLARE end VARCHAR(64) DEFAULT NULL;
	DECLARE r VARCHAR(64) DEFAULT NULL;	

	-- SELECT COUNT(*) FROM neighbours INTO n;
	SET n=50;
	SET i=50;
	WHILE i<=n DO 
		SELECT start_stop FROM neighbours LIMIT i,1 INTO start;
		SELECT end_stop FROM neighbours LIMIT i,1 INTO end;
		SELECT route FROM neighbours LIMIT i,1 INTO r;
	  	INSERT INTO travel_time_log
	  	-- DROP TABLE IF EXISTS tmp_log;
	  	-- create table tmp_log
	  	-- 	(SELECT * FROM arrivals WHERE stop_code_lbsl = (SELECT start) 
	  	-- 		AND route = (SELECT route));
	  		(SELECT t1.stop_code_lbsl start_stop,
	       		   t2.stop_code_lbsl end_stop, 
	               t1.route, 
	       		   t1.trip_id, 
	               t1.vehicle_id,
	               DAYNAME(t1.arrival_time) day, 
	               DATE(t1.arrival_time) date,
	               HOUR(t1.arrival_time) hour,
	               TIME_TO_SEC(TIMEDIFF(t2.arrival_time, t1.arrival_time)) travel_time
            FROM (SELECT * 
            	  FROM arrivals 
            	  WHERE stop_code_lbsl = 10002 
            	  AND route = 19) AS t1 
            INNER JOIN (SELECT * 
            	        FROM arrivals 
            	        WHERE stop_code_lbsl = 11469
            	        AND route = 19) AS t2
				ON t1.trip_id = t2.trip_id
				AND t1.vehicle_id = t2.vehicle_id
				AND DATE(t1.arrival_time) = DATE(t2.arrival_time)
			WHERE t1.arrival_time < t2.arrival_time);

	    SET i = i + 1;
	END WHILE;
End//
delimiter ;

CALL rowperrow();
