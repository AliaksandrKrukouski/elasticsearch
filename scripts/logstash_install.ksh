#!/bin/bash

docker pull docker.elastic.co/logstash/logstash:8.4.3
docker run --rm --name logstash --net elastic -p 5000:5000 -v "$(pwd)/logstash/pipeline":/usr/share/logstash/pipeline -it docker.elastic.co/logstash/logstash:8.4.3