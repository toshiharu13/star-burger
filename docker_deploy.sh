#!/bin/bash

set -e

echo "Update from repo"
git pull

echo "Rebuild docker containers"
docker-compose up --build -d

echo  "Send info about deploy to rollbar.com"
http POST https://api.rollbar.com/api/1/deploy X-Rollbar-Access-Token:ffd0c1e6e6d44392be42d0e83821f8d4 environment=production revision=$(git rev-parse --short HEAD) rollbar_name=FirstProject local_username=Toshiharu

echo "----------------"
echo "Deploy complete!"
echo "----------------"
