USE delay; 

CREATE TABLE time_table (
    SELECT day, HOUR(start_time) hour, TRUNCATE(AVG(travel_time), 1) average_travel_time
    FROM travel_time_log_main
    WHERE travel_time > 0
    GROUP BY day, hour
); 