#!/bin/sh

docker-compose exec mids pip install -r /w205/proj-3-george-reece-julian-francisco/baseline/requirements.txt
docker-compose exec mids apk add kafkacat
docker-compose exec mids apk add apache2-utils
