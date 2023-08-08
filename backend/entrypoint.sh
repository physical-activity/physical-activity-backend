#!/bin/bash
echo "Apply database migrations"
python manage.py migrate --noinput

echo "Collecting static"
python manage.py collectstatic --noinput

echo "Starting gunicorn"
gunicorn physact.wsgi:application --bind 0:8000


