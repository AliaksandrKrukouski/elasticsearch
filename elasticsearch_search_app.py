import csv
import json
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
    print(f"Name: {idx_name}\nSchema: {json.dumps(idx_mapping, indent=2)}")
    if es.indices.exists(index=idx_name):
        print(f"The index already exists. Drop it...")
        es.indices.delete(index=idx_name)

    es.indices.create(index=idx_name, mappings=idx_mapping)
    print(f"The index created")

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

    while True:
        prompt = "Choose search condition (0 to exit):"
        prompt += "\n1 - Search by title (match query)"
        prompt += "\n2 - Search by title (reqexp query)"
        prompt += "\n3 - Search by title (wildcard query)"
        prompt += "\n4 - Search by country (term query)"
        prompt += "\n5 - Search by release date interval (range query)"
        prompt += "\n6 - Search by several columns (multi-match query)"
        prompt += "\n7 - Search by title, country and release date (boolean query)"
        prompt += "\n>>> "

        in_condition = int(input(prompt))

        if in_condition == 0:
            print("\nFinishing the program.")
            break
        elif in_condition == 1:
            in_query_val = input("\nSearch title: ")
            query = {
                "match": {
                    "title": {"query": in_query_val, "operator": "or"}
                }
            }
        elif in_condition == 2:
            in_reqexp_val = input("\nRegexp title: ")
            query = {
                "regexp": {
                    "title": in_reqexp_val
                }
            }
        elif in_condition == 3:
            in_wildcard_val = input("\nWildcard title: ")
            query = {
                "wildcard": {
                    "title": in_wildcard_val + '*'
                }
            }
        elif in_condition == 4:
            in_query_val = input("\nSearch country: ")
            query = {
                "term": {
                    "country": {"value": in_query_val}
                }
            }
        elif in_condition == 5:
            in_gte_val = input("\nSearch year FROM: ")
            in_lte_val = input("Search year TO: ")
            query = {
                "range": {
                    "release_year": {"gte": in_gte_val,
                                     "lte": in_lte_val}
                }
            }
        elif in_condition == 6:
            in_query_val = input("\nSearch text: ")
            in_fields_val = input("Search fields (separated by comma): ")

            fields = [f.strip() for f in in_fields_val.split(",")]

            query = {
                "multi_match": {
                    "query": in_query_val,
                    "fields": fields
                }
            }
        elif in_condition == 7:
            in_title_val = input("\nSearch title: ")
            in_country_val = input("Search country: ")
            in_date_val = input("Search year: ")

            query = {
                "bool": {
                    "must": [
                        {
                            "match": {
                                "title": {"query": in_title_val, "operator": "or"}
                            }
                        },
                        {
                            "term": {
                                "country": {"value": in_country_val}
                            }
                        },
                        {
                            "term": {
                                "release_year": {"value": in_date_val}
                            }
                        }
                    ]
                }
            }

        print(f"Query: {query}")

        resp = es.search(index=idx_name, query=query)
        print(f"Result: {json.dumps(resp['hits'], indent=2)}")

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