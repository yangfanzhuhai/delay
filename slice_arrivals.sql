USE delay; 

DROP TABLE IF EXISTS arrivals_part; 

CREATE TABLE arrivals_part 
(SELECT * FROM arrivals LIMIT 1000000)