#!/bin/sh
# 10 users randomly loading pages for 5 minutes with 0-3 seconds delay between loads

siege -c 10 -i -t 5m -d 3 -f random_prediction_urls.txt
# ab -n 100 -c 10 http://www.yahoo.com/ > test1.txt &
# ab -n 100 -c 10 http://www.yahoo.com/ > test2.txt &
