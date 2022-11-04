import csv
import os
import sys
import uuid

from elasticsearch import Elasticsearch

ES_ENDPOINT=f"http://localhost:9200"

def read_csv(csv_file_path):
    print(f"Input file: {csv_file_path}")

    with open(csv_file_path, mode="r", encoding='utf-8-sig') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        data = list(csv_reader)

    print(f"Total lines read: {len(data)}")
    return data

def index_csv(index, data):
    es = Elasticsearch(hosts=ES_ENDPOINT, request_timeout=600)
    docs_created = 0

    print(f"Create index: {index}")
    for item in data:
        response = es.index(index=index, id=str(uuid.uuid4()), document=item)

        if response.get('result') == 'created':
            docs_created += 1

    print(f"Total documents created: {docs_created}")

def main(argv):
    csv_file_path = argv[1]
    index = os.path.basename(csv_file_path).split('.')[0]

    print("\nRead CSV...")
    data = read_csv(csv_file_path)

    print("\nIndex CSV...")
    index_csv(index, data)

if __name__ == "__main__":
    main(sys.argv)
