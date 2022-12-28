# Elasticsearch applications
This repository contains elasticsearch applications:
- [elastcsearch_index_app](#elasticsearch_index_app)
- [elasticsearch_analyzer_app](#elasticsearch_analyzer_app)
- [elasticsearch_search_app](#elasticsearch_search_app)
- [elasticsearch_agg_app](#elasticsearch_agg_app)
- [logstash http_poller pipeline](#logstash http_poller pipeline) 

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

### elasticsearch_search_app
This application provides ability to search data loaded from data/netflix_titles.csv into Elasticsearch. It uses different types of queries for search like match, term, range etc.

**Run application** \
To run the application execute in command line - *python3 elasticsearch_search_app.py*.\
Follow the instructions on screen to choose required query type and provide input values for search parameters.

**Check results** \
In console output see documents matched with provided criteria.

### elasticsearch_agg_app
This application provides ability to analyze movie related data loaded from data/ml-latest-small. It uses different types of analytical queries.

**Run application** \
To run the application execute in command line - *python3 elasticsearch_agg_app.py*.\
Follow the instructions on screen to choose required query and provide input values for search parameters.

**Check results** \
In console output see the results.

### logstash http_poller pipeline
This pipeline loads data from REST API endpoint into Elasticsearch using Logstash.

**Run pipeline** \
To start the pipeline execute in command line - *source ./scripts/logstash_install.ksh*.

**Check results** \
Navigate to Dev Tools in Elasticsearch UI and execute a query below to see loaded documents:
```
GET /logstash_http_poller/_search
{
    "query": {
        "match_all": {}
    }
}
```
To stop the pipeline run in command line - *docker stop logstash* 

## Clean up
After finishing with running the applications:
- Delete Elasticsearch - *./scripts/es_drop.ksh*
- Delete Kibana - *./scripts/kibana_drop.ksh*
- Delete Python virtual environment - *./scripts/venv_drop.ksh*

