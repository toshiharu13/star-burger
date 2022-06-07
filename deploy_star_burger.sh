#!/bin/bash

set -e

echo "Update from repo"
git pull

echo "Install requirements"
./venv/bin/pip install -r  requirements.txt --no-input

echo "Install node.js libs"
npm ci --dev

echo "Rebuild JS-code"
./node_modules/.bin/parcel build bundles-src/index.js --dist-dir bundles --public-url="./"

echo "Collect Django static"
./venv/bin/python manage.py  collectstatic --noinput

echo "Make migrations"
./venv/bin/python manage.py makemigrations --noinput
./venv/bin/python manage.py migrate --noinput

echo "restart Systemd service"
systemctl restart django-burger.service

echo  "Send info about deploy to rollbar.com"
http POST https://api.rollbar.com/api/1/deploy X-Rollbar-Access-Token:ffd0c1e6e6d44392be42d0e83821f8d4 environment=production revision=$(git rev-parse --short HEAD) rollbar_name=FirstProject local_username=Toshiharu

echo "----------------"
echo "Deploy complete!"
echo "----------------"

