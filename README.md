# Elasticsearch applications
This repository contains elasticsearch applications:
- elastcsearch_index_app
- elasticsearch_analyzer_app

## Prerequisites
Before running the applications: 
- Navigate to the project directory - *cd elasticsearch*
- Install Elasticsearch - *./scripts/es_install.ksh*
- Install Kibana - *./scripts/kibana_install.ksh*
- Create Python virtual environment - *./scripts/venv_create.ksh*

## Applications
### elasticsearch_index_app
This application parses provided CSV file and post the data into Elasticsearch.

**Run application** \
To run the application pride a path to CSV file - *python3 elasticsearch_index_app.py ./data/soccer-standings.csv*

**Check results:**
- Connect to DevTools in Kibana - http://localhost:5601/app/dev_tools 
- Search for the data - *GET soccer-standings/_search*

You can process any CSV file with different structure. \
The application will create an index with the same name as the file and populate it with the data from provided CSV.

### elasticsearch_analyzer_app
This application utilizes custom analyzer which replaces Roman numbers with its Arabic variation and remove HTML tags in provided HTML document.

**Run application** \
To run the application provide a path to HTML document to be analyzed - *python3 elasticsearch_analyzer_app.py ./data/british-monarchy.html*

**Check results** \
In console output Roman numbers should be replaced with its Arabic variation and HTML tags should be removed from provided HTML document.

##Clean up
After finishing with running the applications:
- Delete Elasticsearch - *./scripts/es_drop.ksh*
- Delete Kibana - *./scripts/kibana_drop.ksh*
- Delete Python virtual environment - *./scripts/venv_drop.ksh*

