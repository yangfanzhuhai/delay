USE delay; 

DROP TABLE IF EXISTS time_table_main;

CREATE TABLE time_table_main (
    SELECT start_stop, end_stop, day, hour, TRUNCATE(AVG(travel_time), 1) average_travel_time
    FROM travel_time_log_main
    WHERE travel_time > 0
    GROUP BY start_stop, end_stop, day, hour
); 



