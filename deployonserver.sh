#!/bin/bash
source /home/delay/.virtualenvs/delay/bin/activate     # Activate the virtualenv
git pull
pip install -r delaysite/requirements.txt           # Install or upgrade dependencies
python delaysite/manage.py migrate                  # Apply South's database migrations
python delaysite/manage.py compilemessages          # Create translation files
python delaysite/manage.py collectstatic --noinput  # Collect static files
