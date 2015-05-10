#!/bin/bash
source ~/.virtualenvs/delay/bin/activate
python delaysite/manage.py makemigrations
python delaysite/manage.py migrate
pip freeze > requirements.txt
