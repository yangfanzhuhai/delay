USE delay;

ALTER TABLE arrivals ADD INDEX stop_code_lbsl (stop_code_lbsl);

ALTER TABLE arrivals ADD INDEX arrival_time (arrival_time);