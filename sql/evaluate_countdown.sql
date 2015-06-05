CREATE table predictions_25_30_minutes(
SELECT snapshot.stop_code_lbsl,
     snapshot.route,
     snapshot.vehicle_id,
     snapshot.trip_id,
     snapshot.arrival_time predicted_arrival_time,
     current_arrivals.arrival_time actual_arrival,
     TIME_TO_SEC(TIMEDIFF(snapshot.arrival_time, current_arrivals.arrival_time)) delta,
     snapshot.recorded_time prediction_recorded_time,
     current_arrivals.recorded_time actual_arrival_recorded_time,
     current_arrivals.expire_time

FROM
(
SELECT * from delay_arrivals_full
WHERE arrival_time BETWEEN '2015-06-04 11:24:37' + INTERVAL 25 MINUTE
           AND '2015-06-04 11:24:37' + INTERVAL 30 MINUTE
) AS snapshot
JOIN

current_arrivals

ON snapshot.stop_code_lbsl = current_arrivals.stop_code_lbsl
AND snapshot.route = current_arrivals.route
AND snapshot.trip_id = current_arrivals.trip_id
AND snapshot.vehicle_id = current_arrivals.vehicle_id
AND snapshot.arrival_date = current_arrivals.arrival_date)


select * from

(select AVG(delta)
from predictions_0_3_minutes

UNION

select AVG(delta)
from predictions_0_5_minutes

UNION

select AVG(delta)
from predictions_5_10_minutes

UNION

select AVG(delta)
from predictions_10_15_minutes

UNION

select AVG(delta)
from predictions_15_20_minutes

UNION

select AVG(delta)
from predictions_20_25_minutes

UNION

select AVG(delta)
from predictions_25_30_minutes) c
