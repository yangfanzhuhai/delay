#!/bin/sh

filename=arrival-$(date +"%Y-%m-%d-%H:%M:%S").sql

mysqldump delay > /home/delay/db/$filename
scp /home/delay/db/$filename yz10111@shell1.doc.ic.ac.uk:/vol/automed/data/tfl_bus/
rm /home/delay/db/$filename

