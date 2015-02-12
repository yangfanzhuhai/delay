#!/bin/sh

filename=/home/delay/db/arrivals-$(date +"%Y-%m-%d-%H:%M:%S").sql

mysqldump --extended-insert=FALSE --no-create-info --tables delay arrivals > $filename

sed -i 's/`//g' $filename

scp $filename yz10111@shell1.doc.ic.ac.uk:/vol/automed/data/tfl_bus/
rm $filename

