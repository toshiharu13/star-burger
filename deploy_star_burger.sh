#!/bin/bash

set -e
# Обновит код репозитория
git pull
# Установит библиотеки python
./venv/bin/pip install -r requirements.txt
# Установит библиотеки node.js
npm ci --dev
# Пересоберёт JS-код
./node_modules/.bin/parcel build bundles-src/index.js --dist-dir bundles --public-url="./"
# Пересоберёт статику Django
./venv/bin/python manage.py  collectstatic
# Накатит миграции
./venv/bin/python manage.py makemigrations
./venv/bin/python manage.py migrate
# Перезапустит сервисы Systemd
systemctl restart django-burger.service
#  Передача в rollbar.com информации о деплое
comit_number=$(git rev-parse --short HEAD)
curl -H "X-Rollbar-Access-Token: ffd0c1e6e6d44392be42d0e83821f8d4" -H "Content-Type: application/json" -X POST 'https://api.rollbar.com/api/1/deploy' -d '{"environment": "production", "status": "succeeded","revision": $comit_number, "user": "Toshiharu"}'

# Сообщит об успешном завершении деплоя
echo "----------------"
echo "Deploy complete!"
echo "----------------"

