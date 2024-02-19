#!/bin/bash

echo "Starting backend..."

python manage.py makemigrations --noinput
python manage.py migrate --noinput
python manage.py loaddata ./fixtures/fixtures.json

exec "$@"