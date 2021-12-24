#!/usr/bin/env bash

source ".venv/bin/activate"

rm db.sqlite3
rm -r empl_database/migrations

python manage.py makemigrations empl_database
python manage.py migrate

python manage.py createsuperuser --username omer --email ''

python manage.py runserver
