#!/bin/bash

mkdir -p ~/0xStock-data/history-data
mkdir -p ~/0xStock-data/curr-date-data
mkdir -p ~/0xStock-db/data
mkdir -p ~/0xStock-db/migrations
cp $PWD/store_tools/migrations/*.sql ~/0xStock-db/migrations
mkdir -p ~/0xStock-logs

docker-compose -f "$PWD/store_tools/mysql-deploy/docker-compose.yml" up -d --build
docker_container_id=`docker container ls | grep mysql-deploy | awk '{print $1}'`
sleep 2
docker exec -i ${docker_container_id} /bin/bash -c 'mysql -uroot -p"Pwd123Pwd" < /mysql/migrations/create_database_up.sql'
sleep 2
docker exec -i ${docker_container_id} /bin/bash -c 'mysql -uroot -p"Pwd123Pwd" < /mysql/migrations/create_stock_code_prefix_000_table_up.sql'
sleep 2
docker exec -i ${docker_container_id} /bin/bash -c 'mysql -uroot -p"Pwd123Pwd" < /mysql/migrations/create_stock_code_prefix_600_table_up.sql'
sleep 2
docker exec -i ${docker_container_id} /bin/bash -c 'mysql -uroot -p"Pwd123Pwd" < /mysql/migrations/create_stock_code_prefix_601_table_up.sql'
sleep 2
docker exec -i ${docker_container_id} /bin/bash -c 'mysql -uroot -p"Pwd123Pwd" < /mysql/migrations/create_stock_code_prefix_603_table_up.sql'
sleep 2
docker exec -i ${docker_container_id} /bin/bash -c 'mysql -uroot -p"Pwd123Pwd" < /mysql/migrations/create_stock_code_prefix_605_table_up.sql'
