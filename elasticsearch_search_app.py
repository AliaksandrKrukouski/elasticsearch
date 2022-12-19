import csv
import os
import sys
import uuid

from elasticsearch import Elasticsearch, helpers as es_helper

ES_ENDPOINT = f"http://localhost:9200"

INDEX_DATA_PATH = "./data/netflix_titles.csv"
INDEX_NAME = 'netflix_movies'
INDEX_MAPPING = {
    "properties": {
        "show_id": {"type": "text"},
        "type": {"type": "keyword"},
        "title": {"type": "text"},
        "director": {"type": "text"},
        "cast": {"type": "text"},
        "country": {"type": "keyword"},
        "date_added": {"type": "text"},
        "release_year": {"type": "short"},
        "rating": {"type": "keyword"},
        "duration": {"type": "text"},
        "listed_in": {"type": "text"},
        "description": {"type": "text"}
    }
}

def create_index(es, idx_name, idx_mapping):
    print(f"Name: {idx_name}\nSchema: {idx_mapping}")
    if not es.indices.exists(index=idx_name):
        es.indices.create(index=idx_name, mappings=idx_mapping)
        print(f"{idx_name} index created")
    else:
        print(f"{idx_name} index already exists")

def gen_docs(idx_name, csv_file_path):
    print(f"Index: {idx_name}\nCSV file: {csv_file_path}")

    with open(csv_file_path, mode="r", encoding='utf-8-sig') as csv_file:
        csv_reader = csv.DictReader(csv_file)

        for row in csv_reader:
            doc = {
                "_index": idx_name,
                "_id": str(uuid.uuid4()),
                "_source": row
            }
            yield doc

def run_search(es, idx_name):
    prompt = "Choose search type:"
    prompt += "\n1 - Match query"
    prompt += "\n2 - Term query"
    prompt += "\nEnter 0 to end the program: "

    search_input = int(input(prompt))

    if search_input == 1:
        print("*** MATCH QUERY ***")
        title_input = input("Input title for search: ")
        query = {
            "query": {
                "match": {
                    "title": {"query": title_input, "operator": "or"},
                }
            }
        }

    print(f"Search query: {query}")
    response = es.search(index=idx_name, body=query)
    print(f"Search result: {response}")

def post_docs(es, docs):
    es_resp = es_helper.bulk(client=es, actions=docs)
    print(f"Docs posted: {es_resp[0]}")

def main(argv):
    print("\nInit ES client...")
    es_client = Elasticsearch(hosts=ES_ENDPOINT, request_timeout=600)

    print("\nCreate index...")
    create_index(es_client, INDEX_NAME, INDEX_MAPPING)

    print("\nLoad CSV...")
    post_docs(es_client, gen_docs(INDEX_NAME, INDEX_DATA_PATH))

    print("\nRun search...")
    run_search(es_client, INDEX_NAME)

if __name__ == "__main__":
    main(sys.argv)