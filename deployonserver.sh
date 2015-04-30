#!/bin/bash
source /home/delay/.virtualenvs/delay/bin/activate     # Activate the virtualenv
git pull
pip install -r REQUIREMENTS.txt           # Install or upgrade dependencies
python manage.py migrate                  # Apply South's database migrations
python manage.py compilemessages          # Create translation files
python manage.py collectstatic --noinput  # Collect static files
