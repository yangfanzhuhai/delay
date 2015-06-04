USE delay;


TRUNCATE delay_timetable_updated;

SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;
INSERT INTO delay_timetable_updated (start_stop, end_stop, day, hour, average_travel_time)
(
  SELECT start_stop, end_stop, day, hour, AVG(average_travel_time) AS average_travel_time
  FROM delay_current_timetable_log
  GROUP BY start_stop, end_stop, day, hour
);

INSERT INTO delay_timetable (start_stop, end_stop, day, hour, average_travel_time)
SELECT start_stop, end_stop, day, hour, average_travel_time
FROM delay_timetable_updated
ON DUPLICATE KEY UPDATE delay_timetable.average_travel_time = delay_timetable_updated.average_travel_time;
COMMIT;

