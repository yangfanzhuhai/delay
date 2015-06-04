USE delay;

CREATE TABLE arrivals_new LIKE current_arrivals;
RENAME TABLE current_arrivals TO arrivals_yesterday;
RENAME TABLE arrivals_new TO current_arrivals;

SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;
INSERT INTO delay_arrivals_archive (stop_code_lbsl,
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
FROM arrivals_yesterday
COMMIT;

Drop TABLE arrivals_yesterday;

