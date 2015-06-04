#!/bin/bash

python3 random_url.py tfl 1000 > random_urls.txt
siege -c 50 -i -t 1m -d 1 -f random_urls.txt
