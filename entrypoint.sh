#!/bin/sh

set -euo pipefail

cp /tmp/jwt_public_key/ec_public.key /app/ec_public.key

python manage.py makemigrations && python manage.py migrate && python manage.py loaddata initial_data.json && python manage.py runserver 0.0.0.0:9001
