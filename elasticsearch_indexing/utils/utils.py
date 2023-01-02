import csv
import json
import os
import uuid

from elasticsearch import Elasticsearch, helpers as es_helper

from elasticsearch_indexing import ES_ENDPOINT, ES_TIMEOUT_SEC

def create_index(index, mapping=None, es_client=None):
    print(f"Input parameters:")
    print(f"- index = {index}")
    print(f"- mapping = {json.dumps(mapping, indent=2)}")

    es = es_client if es_client else _es_client()

    if es.indices.exists(index=index):
        print(f"Recreate index")
        es.indices.delete(index=index)

    index_mapping = {"properties": mapping} if mapping else None

    es.indices.create(index=index, mappings=index_mapping)
    print(f"Index successfully created")

def parse_csv(index, csv_file_path):
    print(f"Input parameters:")
    print(f"- index = {index}")
    print(f"- csv_file_path = {csv_file_path}")

    with open(csv_file_path, mode="r", encoding='utf-8-sig') as csv_file:
        csv_reader = csv.DictReader(csv_file)

        for row in csv_reader:
            doc = {
                "_index": index,
                "_id": str(uuid.uuid4()),
                "_source": row
            }
            yield doc

def parse_json(index, json_file_path):
    print(f"Input parameters:")
    print(f"- index = {index}")
    print(f"- json_file_path = {json_file_path}")

    with open(json_file_path, mode="r", encoding='utf-8-sig') as json_file:
        for row in json_file:
            source = json.loads(row)
            doc = {
                "_index": index,
                "_id": str(uuid.uuid4()),
                "_source": source
            }
            yield doc

def ingest_data(data, es_client=None):
    es = es_client if es_client else _es_client()

    es_resp = es_helper.bulk(client=es, actions=data)
    print(f"{es_resp[0]} document/-s ingested.")

def _es_client():
    return Elasticsearch(hosts=ES_ENDPOINT, request_timeout=ES_TIMEOUT_SEC)
