#!/bin/bash

docker network create elastic
docker pull docker.elastic.co/elasticsearch/elasticsearch:8.4.3
docker run -d --name elasticsearch --net elastic -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" -e xpack.security.enabled=false -it docker.elastic.co/elasticsearch/elasticsearch:8.4.3