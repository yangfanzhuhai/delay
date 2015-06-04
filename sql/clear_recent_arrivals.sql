USE delay;

SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;
INSERT INTO delay_arrivals (stop_code_lbsl,
                            route,
                            vehicle_id,
                            trip_id,
                            arrival_date,
                            arrival_time,
                            expire_time,
                            recorded_time,
                            run)
SELECT stop_code_lbsl,
        route,
        vehicle_id,
        trip_id,
        arrival_date,
        arrival_time,
        expire_time,
        recorded_time,
        run
FROM recent_arrivals;
COMMIT;

TRUNCATE recent_arrivals;
RENAME TABLE recent_arrivals TO empty_arrivals;
