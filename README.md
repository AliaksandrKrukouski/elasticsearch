# Elasticsearch applications
This repository contains elasticsearch applications:
- elastcsearch_index_app

## elasticsearch_index_app
This application parses provided CSV file and post the data into Elasticsearch.

Run application:
- Navigate to the project directory - cd elasticsearch
- Install Elasticsearch - ./scripts/es_install.ksh
- Install Kibana - ./scripts/kibana_install.ksh
- Create Python virtual environment - ./scripts/venv_create.ksh
- Run the application providing a path to CSV file - python3 elasticsearch_index_app.py ./data/soccer-standings.csv

Check results:
- Connect to DevTools in Kibana - http://localhost:5601/app/dev_tools 
- Search for the data - GET soccer-standings/_search

Clean up:
- Delete Elasticsearch - ./scripts/es_drop.ksh
- Delete Kibana - ./scripts/kibana_drop.ksh
- Delete Python virtual environment - ./scripts/venv_drop.ksh

You can process any CSV file with different structure. The application will create an index with the same name as the file and populate it with the data from provided CSV.



