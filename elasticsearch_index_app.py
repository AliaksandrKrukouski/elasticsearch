import csv
import os
import sys
import uuid

from elasticsearch import Elasticsearch, helpers as es_helper

ES_ENDPOINT=f"http://localhost:9200"

def gen_docs(csv_file_path):
    print(f"CSV file: {csv_file_path}")

    index = os.path.basename(csv_file_path).split('.')[0]
    print(f"Index: {index}")

    with open(csv_file_path, mode="r", encoding='utf-8-sig') as csv_file:
        csv_reader = csv.DictReader(csv_file)

        for row in csv_reader:
            doc = {
                "_index": index,
                "_id": str(uuid.uuid4()),
                "_source": row
            }
            yield doc

def post_docs(es_client, docs):
    es_resp = es_helper.bulk(client=es_client, actions=docs)
    print(f"Docs posted: {es_resp[0]}")

def main(argv):
    csv_file_path = argv[1]

    print("\nInit ES client...")
    es_client = Elasticsearch(hosts=ES_ENDPOINT, request_timeout=600)

    print("\nPost docs into ES...")
    post_docs(es_client, gen_docs(csv_file_path))

if __name__ == "__main__":
    main(sys.argv)
