#!/bin/bash
python delaysite/manage.py makemigrations
pip freeze > requirements.txt
