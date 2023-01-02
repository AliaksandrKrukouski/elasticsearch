import json
import sys

from elasticsearch import Elasticsearch

from elasticsearch_indexing.utils import utils
from elasticsearch_indexing.dsl_builder import query_builder, agg_builder

ES_ENDPOINT = f"http://localhost:9200"

DATA_PATH = "./data/ml-latest-small"

MOVIES_INDEX = "movies"
MOVIES_CSV = "movies.csv"
MOVIES_MAPPING = {
    "movieId": {"type": "keyword"},
    "title": {"type": "text"},
    "genres": {"type": "text"}
}

RATINGS_INDEX = "ratings"
RATINGS_CSV = "ratings.csv"
RATINGS_MAPPING = {
    "userId": {"type": "keyword"},
    "movieId": {"type": "keyword"},
    "rating": {"type": "double"},
    "timestamp": {"type": "date", "format": "epoch_second"}
}

TAGS_INDEX = "tags"
TAGS_CSV = "tags.csv"
TAGS_MAPPING = {
    "userId": {"type": "keyword"},
    "movieId": {"type": "keyword"},
    "tag": {"type": "keyword"},
    "timestamp": {"type": "date", "format": "epoch_second"}
}

MOVIES_DENORMALIZED_INDEX = "movies_denormalized"
MOVIES_DENORMALIZED_JSON = "movies_denormalized.json"
MOVIES_DENORMALIZED_MAPPING = {
    "movieId": {"type": "keyword"},
    "title": {"type": "text",
              "fields": {
                  "raw": {
                      "type":  "keyword"
                  }
              }},
    "genres": {"type": "text"},
    "tags": {"type": "nested",
             "properties":
                 {
                     "userId": {"type": "keyword"},
                     "tag": {"type": "keyword"},
                     "timestamp": {"type": "date", "format": "epoch_second"}
                 }
             },
    "ratings": {"type": "nested",
                "properties":
                    {
                        "userId": {"type": "keyword"},
                        "rating": {"type": "keyword"},
                        "timestamp": {"type": "date", "format": "epoch_second"}
                    }
                }
}

ALL_INDEXES = [
    {"index_name": MOVIES_INDEX, "file_name": MOVIES_CSV, "file_format": "CSV", "mapping": MOVIES_MAPPING},
    {"index_name": RATINGS_INDEX, "file_name": RATINGS_CSV, "file_format": "CSV", "mapping": RATINGS_MAPPING},
    {"index_name": TAGS_INDEX, "file_name": TAGS_CSV, "file_format": "CSV", "mapping": TAGS_MAPPING},
    {"index_name": MOVIES_DENORMALIZED_INDEX, "file_name": MOVIES_DENORMALIZED_JSON, "file_format": "JSON",
     "mapping": MOVIES_DENORMALIZED_MAPPING}
]

def get_movies_by_title(es_client, movie):
    query = query_builder.match_query("title", movie)
    resp = es_client.search(index=MOVIES_INDEX, query=query)
    hits = resp["hits"]["hits"]

    movies = []
    for m in hits:
        movie_id = m["_source"]["movieId"]
        title = m["_source"]["title"]
        movies.append({"movie_id": movie_id, "title": title})

    return movies

def init(es_client):
    for idx in ALL_INDEXES:
        index_name, file_name, file_foramt, mapping = idx.values()
        file_path = DATA_PATH + "/" + file_name

        print(f"Create {index_name} index...")
        utils.create_index(index_name, mapping, es_client)

        print(f"Ingest data for {index_name} index...")
        if file_foramt == "CSV":
            utils.ingest_data(data=utils.parse_csv(index_name, file_path), es_client=es_client)
        elif file_foramt == "JSON":
            utils.ingest_data(data=utils.parse_json(index_name, file_path), es_client=es_client)
        else:
            raise Exception("ERROR: Unsupported file format. Should be CSV or JSON.")

def run_search(es_client):
    while True:
        prompt = "Choose search condition (0 to exit):"
        prompt += "\n1 - Search movie by title (match query)"
        prompt += "\n2 - Search movie by title (fuzzy query)"
        prompt += "\n3 - Search movie by rate (sub agg query)"
        prompt += "\n4 - Top 10 tags for the movie (bucket agg query)"
        prompt += "\n5 - Top 10 tags for the movie (nested query/denorm data)"
        prompt += "\n6 - Top rated movies by the user (boolean query)"
        prompt += "\n7 - Top rated movies by the user (nested query/denorm data)"
        prompt += "\n>>> "

        in_condition = int(input(prompt))

        query, aggs = None, None
        if in_condition == 0:
            print("\nFinishing the program.")
            break
        elif in_condition == 1:
            in_query_val = input("\nMatch phrase: ")
            index = MOVIES_INDEX
            query = query_builder.match_query("title", in_query_val, 0)
        elif in_condition == 2:
            in_query_val = input("\nMatch fuzzy phrase: ")
            index = MOVIES_INDEX
            query = query_builder.match_query("title", in_query_val, 2)
        elif in_condition == 3:
            in_avg_from = input("\nAvg rate from: ")
            in_avg_to = input("Avg rate to: ")
            index = RATINGS_INDEX
            aggs = agg_builder.sub_agg("avg", "movieId", "rating", in_avg_from, in_avg_to, "desc")
        elif in_condition == 4:
            in_movie = input("\nMovie title to search: ")
            movies = get_movies_by_title(es_client, in_movie)

            if len(movies) == 0:
                print("Movie not found...\n")
                continue
            elif len(movies) > 1:
                print(f"Choose the exact movie title: {[m['title'] for m in movies]}\n")
                continue

            movie_id = movies[0]["movie_id"]

            index = TAGS_INDEX
            query = query_builder.match_query("movieId", movie_id)
            aggs = agg_builder.terms_agg("tag", 10)
        elif in_condition == 5:
            in_movie = input("\nMovie title to search: ")

            tag_terms_agg = agg_builder.terms_agg("tag", path="tags")
            nested_tag_terms_agg = agg_builder.nested_agg("tags", tag_terms_agg)

            index = MOVIES_DENORMALIZED_INDEX
            query = query_builder.match_query("title", in_movie)
            aggs = agg_builder.terms_agg("title.raw", sub_agg=nested_tag_terms_agg)
        elif in_condition == 6:
            in_user_id = input("\nUserID to search: ")

            user_filter = query_builder.term_query("userId", in_user_id)
            rate_filter = query_builder.range_query("rating", 5)

            index = RATINGS_INDEX
            query = query_builder.bool_query(filter=[user_filter, rate_filter])
        elif in_condition == 7:
            in_user_id = input("\nUserID to search: ")

            path = "ratings"
            user_filter = query_builder.term_query("userId", in_user_id, path=path)
            rate_filter = query_builder.range_query("rating", 5, path=path)
            bool_query = query_builder.bool_query(filter=[user_filter, rate_filter])

            index = MOVIES_DENORMALIZED_INDEX
            query = query_builder.nested_query(path=path, query=bool_query)

        print(f"Query: {json.dumps(query, indent=2)}")
        print(f"Aggs: {json.dumps(aggs, indent=2)}")

        resp = es_client.search(index=index, query=query, aggs=aggs)
        if query:
            print(f"Query result: {json.dumps(resp['hits'], indent=2)}")
        if aggs:
            print(f"Aggs result: {json.dumps(resp['aggregations'], indent=2)}")

def main(argv):
    print("\nInit ES client...")
    es_client = Elasticsearch(hosts=ES_ENDPOINT, request_timeout=600)

    print("\nPrepare environment...")
    init(es_client)

    print("\nRun search...")
    run_search(es_client)

if __name__ == "__main__":
    main(sys.argv)