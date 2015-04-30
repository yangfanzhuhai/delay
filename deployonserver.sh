#!/bin/bash
source /home/delay/.virtualenvs/delay/bin/activate     # Activate the virtualenv
cd /home/delay/delay/
pip install -r requirements.txt           # Install or upgrade dependencies
cd /home/delay/delay/delaysite
python manage.py migrate                  # Apply South's database migrations
python manage.py compilemessages          # Create translation files
python manage.py collectstatic --noinput  # Collect static files
supervisorctl restart gunicorn
supervisorctl start arrival

