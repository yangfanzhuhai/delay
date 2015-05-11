#!/usr/bin/env bash
cd generated/tfl_timetables/
for f in *.csv
do
  mysql -e "LOAD DATA LOCAL INFILE '"$f"'INTO TABLE delay_tfl_timetable FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n' IGNORE 1 LINES (@col1, @col2, @col3, @col4, @col5, @col6, @col7, @col8, @col9, @col10) set route=@col1, day=@col2, run=@col3, sequence=@col4, naptan_atco=@col5, stop_name=@col6, departure_time_from_origin=@col7, arrival_time=@col8, travel_time=@col9, cummulative_travel_time=@col10" delay
echo "Done: '"$f"' at $(date)"
done
