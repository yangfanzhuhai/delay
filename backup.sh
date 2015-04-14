#!/bin/sh

filename=/data/tmp/delay-$(date +"%Y-%m-%d-%H:%M:%S").sql

mysqldump --extended-insert=FALSE delay > $filename

sed -i 's/`//g' $filename

scp $filename yz10111@shell1.doc.ic.ac.uk:/vol/automed/data/tfl_bus/
rm $filename

