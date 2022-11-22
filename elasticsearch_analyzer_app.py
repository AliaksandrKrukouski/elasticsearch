import sys

from elasticsearch import Elasticsearch

ES_ENDPOINT = f"http://localhost:9200"

TOKENIZER = "keyword"
CHAR_FILTER = [
    "html_strip",
    {
        "type": "mapping",
        "mappings": [
            "I => 1",
            "II => 2",
            "III => 3",
            "IV => 4",
            "V => 5",
            "VI => 6",
            "VII => 7",
            "VIII => 8",
            "IX => 9",
            "X => 10"
        ]
    }
]

def read_html_doc(html_doc_path):
    print(f"HTML document: {html_doc_path}")
    with open(html_doc_path, mode="r", encoding='utf-8-sig') as html_doc:
        doc = html_doc.read().rstrip()

    return doc

def run_analyzer(es_client, tokenizer, char_filter, text):
    print(f"Tokenizer: {TOKENIZER}")
    print(f"Char filter: {CHAR_FILTER}")
    print(f"Before analyzing: {text}")

    tokens = es_client.indices.analyze(tokenizer=tokenizer, char_filter=char_filter, text=text)
    text_analyzed = tokens['tokens'][0]['token']
    print(f"After analyzing:\n{text_analyzed.strip()}")

def main(argv):
    html_doc_path = argv[1]

    print("\nInit ES client...")
    es_client = Elasticsearch(hosts=ES_ENDPOINT, request_timeout=600)

    print("\nRead html document...")
    text = read_html_doc(html_doc_path)

    print("\nRun analyzer...")
    run_analyzer(es_client, TOKENIZER, CHAR_FILTER, text)

if __name__ == "__main__":
    main(sys.argv)
