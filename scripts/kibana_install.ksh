#!/bin/bash

docker pull docker.elastic.co/kibana/kibana:8.4.3
docker run -d --name kibana --net elastic -p 5601:5601 -ti docker.elastic.co/kibana/kibana:8.4.3