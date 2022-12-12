import sys

from elasticsearch import Elasticsearch


ES_ENDPOINT = f"http://localhost:9200"

INDEX_DATA_PATH = "./data/netflix_titles.csv"
INDEX_NAME = 'netflix_movies'
INDEX_MAPPING = {
    "mappings": {
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
            "description": {"type": "text"},
        }
    }
}

DSL_MATCH_QUERY_PTRN = {
    "query": {
        "match": {
            "title": {"query": "{match_title}", "operator": "or"},
        }
    }
}
DSL_QUERY_PTRNS = {"MATCH": DSL_MATCH_QUERY_PTRN}

def create_index(es):
    print(f"Index name: {INDEX_NAME}; Schema: {INDEX_MAPPING}.")

    print(f"Index name: {index}")


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

    print("\nCreate index for CSV...")

    print("\nPost docs into ES...")
    post_docs(es_client, gen_docs(csv_file_path))

    print("")

    prompt = "\nChoose search type:"
    prompt += "\n1 - Match query"
    prompt += "\n2 - Term query"
    prompt += "\nEnter 0 to end the program."
    prompt += "\n"

    search_input = int(input(prompt))
    if search_input == 1:
        print("*** MATCH QUERY ***")
        title_input = input("\nInput title for search: ")
        query_ptrn = ES_QUERY_PTRNS("MATCH")
        query = query_ptrn.format(match_title=title_input)

    es_client.search(index=, body=query)



if __name__ == "__main__":
    main(sys.argv)