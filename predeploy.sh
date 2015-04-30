#!/bin/bash
source ~/.virtualenvs/delay/bin/activate
python delaysite/manage.py makemigrations
pip freeze > requirements.txt
