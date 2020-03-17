#! /bin/sh

python manage.py makemigrations
python manage.py migrate

gunicorn --workers=4 --reload --bind=web_app:8000 blogs.wsgi:application