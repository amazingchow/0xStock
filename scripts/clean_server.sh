#!/bin/bash

docker_container_id=`docker container ls | grep mysql-deploy | awk '{print $1}'`
docker exec -i ${docker_container_id} /bin/bash -c 'mysql -u root -p"Pwd123!@" < /mysql/migrations/create_database_down.sql'

docker-compose -f "$PWD/storetool/mysql-deploy/docker-compose.yml" down
