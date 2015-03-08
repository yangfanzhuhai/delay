USE delay; 

DROP TABLE IF EXISTS arrivals_part_2; 

CREATE TABLE arrivals_part_2 
(SELECT * FROM arrivals LIMIT 500000)