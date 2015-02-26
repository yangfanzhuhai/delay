SELECT COUNT(*)
FROM neighbours
JOIN arrivals AS t1
ON t1.stop_code_lbsl = neighbours.start_stop 
AND t1.route = neighbours.route