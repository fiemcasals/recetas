#!/bin/sh

echo 'Running collecstatic...'
python manage.py collectstatic --no-input production

echo 'Applying migrations...'
#python manage.py wait_for_db 
python manage.py makemigrations 
python manage.py migrate 

echo 'Running server...'

gunicorn --env DJANGO_SETTINGS_MODULE=mysite.settings mysite.wsgi:application --bind 0.0.0.0:8000 #--workers=2