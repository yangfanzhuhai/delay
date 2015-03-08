ALTER TABLE travel_time_log_part
ADD CONSTRAINT fk_travel_time_log
FOREIGN KEY (start_stop) 
REFERENCES neighbours(start_stop)
ON UPDATE CASCADE
ON DELETE CASCADE;


ALTER TABLE users 
ADD CONSTRAINT fk_grade_id FOREIGN KEY (grade_id) references grades(id);



SELECT t1.start_stop, neighbours.end_stop, t1.route, t1.trip_id, t1.arrival_time
FROM (

SELECT stop_code_lbsl AS start_stop, route, trip_id, arrival_time
FROM arrivals_part_2
) AS t1
INNER JOIN neighbours ON 
( t1.start_stop = neighbours.start_stop
AND t1.route = neighbours.route ) 
INNER JOIN (SELECT stop_code_lbsl AS end_stop, route, trip_id, arrival_time
FROM arrivals_part_2
) AS t2 ON (t2.end_stop = neighbours.end_stop AND t2.route = neighbours.route)
ORDER BY  `t1`.`arrival_time` DESC 
LIMIT 0 , 30


ALTER TABLE travel_time_log_part ENGINE = INNODB;

DROP PROCEDURE IF EXISTS ROWPERROW;
DELIMITER ;;
CREATE PROCEDURE ROWPERROW()
BEGIN
DECLARE n INT DEFAULT 0;
DECLARE i INT DEFAULT 0;
SELECT COUNT(*) FROM table_A INTO n;
SET i=0;
WHILE i<n DO 
  INSERT INTO table_B(ID, VAL) VALUES(ID, VAL) FROM table_A LIMIT i,1;
  SET i = i + 1;
END WHILE;
End;
;;

DELIMITER ;
CALL ROWPERROW();


 --innodb_thread_concurrency=0 --innodb_read_io_threads=64 --innodb_write_io_threads=64