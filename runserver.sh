#!/bin/bash
source ~/.virtualenvs/delay/bin/activate
python delaysite/manage.py runserver 0.0.0.0:5000
