#!/bin/sh

set -euo pipefail

curl -o global-bundle.pem https://truststore.pki.rds.amazonaws.com/global/global-bundle.pem

python manage.py makemigrations && python manage.py migrate && python manage.py loaddata initial_data.json && python manage.py runserver 0.0.0.0:9001
