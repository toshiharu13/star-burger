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
./venv/bin/python manage.py migrate
# Перезапустит сервисы Systemd
systemctl restart django-burger.service
# Сообщит об успешном завершении деплоя
echo "----------------"
echo "Deploy complite!"
echo "----------------"

