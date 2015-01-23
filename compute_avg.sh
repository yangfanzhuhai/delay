#!/bin/sh

mysql < add_indexes.sql

mysql < avg_time.sql > output.txt
