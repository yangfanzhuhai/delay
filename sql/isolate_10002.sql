use delay;
SELECT * FROM `arrivals` 
  WHERE expire_time = 0
  AND (stop_code_lbsl = 11469 
  OR stop_code_lbsl = 10002)
INTO OUTFILE '/home/delay/delay/10002.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n';
