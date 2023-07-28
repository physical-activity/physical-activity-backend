#!/bin/bash
echo "Make database migrations"
python manage.py makemigrations --noinput

echo "Apply database migrations"
python manage.py migrate --noinput

echo "Creating superuser"
python manage.py createsuperuser --noinput

echo "Collecting static"
python manage.py collectstatic --noinput

echo "Starting gunicorn"
gunicorn physact.wsgi:application --bind 0:8000


