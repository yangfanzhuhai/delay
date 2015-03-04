SELECT COUNT(*)
FROM neighbours
JOIN arrivals AS t1
ON t1.stop_code_lbsl = neighbours.start_stop 
AND t1.route = neighbours.route
JOIN arrivals AS t2
ON neighbours.end_stop = t2.stop_code_lbsl
AND t2.route = neighbours.route
AND t1.trip_id = t2.trip_id
AND t1.vehicle_id = t2.vehicle_id;