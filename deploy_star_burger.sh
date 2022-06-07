#!/bin/bash

set -e

echo "Update from repo"
git pull

echo "Install requirements"
./venv/bin/pip install -r requirements.txt

echo "Install node.js libs"
npm ci --dev

echo "Rebuild JS-code"
./node_modules/.bin/parcel build bundles-src/index.js --dist-dir bundles --public-url="./"

echo "Collect Django static"
./venv/bin/python manage.py  collectstatic --noinput

echo "Make migrations"
./venv/bin/python manage.py makemigrations
./venv/bin/python manage.py migrate

echo "restart Systemd service"
systemctl restart django-burger.service

echo  "Send info about deploy to rollbar.com"
comit_number=$(git rev-parse --short HEAD)
curl -H "X-Rollbar-Access-Token: ffd0c1e6e6d44392be42d0e83821f8d4" -H "Content-Type: application/json" -X POST 'https://api.rollbar.com/api/1/deploy' -d '{"environment": "production", "status": "succeeded","revision": $comit_number, "user": "Toshiharu"}'

echo "----------------"
echo "Deploy complete!"
echo "----------------"

