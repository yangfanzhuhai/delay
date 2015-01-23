#!/bin/sh

filename=arrival-$(date +"%Y-%m-%d-%H:%M:%S").sql

mysqldump delay > /home/delay/db/$filename
scp /home/delay/db/$filename yz10111@shell1.doc.ic.ac.uk:/homes/yz10111/Documents/delaybackup


