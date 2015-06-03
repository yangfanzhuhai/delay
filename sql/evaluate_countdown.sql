CREATE table predictions_0_5_minutes(
SELECT snapshot.stop_code_lbsl,
     snapshot.route,
     snapshot.vehicle_id,
     snapshot.trip_id,
     snapshot.arrival_time 20_minute_prediction,
     delay_arrivals.arrival_time actual_arrival,
     TIME_TO_SEC(TIMEDIFF(snapshot.arrival_time, delay_arrivals.arrival_time)) delta,
     snapshot.recorded_time prediction_recorded_time,
     delay_arrivals.recorded_time actual_arrival_recorded_time,
     delay_arrivals.expire_time

FROM
(
SELECT * from delay_arrivals_full
WHERE recorded_time = '2015-06-02 08:59:37'
AND arrival_time BETWEEN '2015-06-02 08:59:37' + INTERVAL 0 MINUTE
           AND '2015-06-02 08:59:37' + INTERVAL 5 MINUTE
) AS snapshot
JOIN

delay_arrivals

ON snapshot.stop_code_lbsl = delay_arrivals.stop_code_lbsl
AND snapshot.route = delay_arrivals.route
AND snapshot.trip_id = delay_arrivals.trip_id
AND snapshot.vehicle_id = delay_arrivals.vehicle_id
AND snapshot.arrival_date = delay_arrivals.arrival_date)
