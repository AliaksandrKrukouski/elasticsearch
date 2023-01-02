def match_query(field, query, fuzziness=0):
    return {
        "match": {
            field: {"query": query, "operator": "and", "fuzziness": fuzziness}
        }
    }

def term_query(field, value, path=None):
    field = f"{path}.{field}" if path else field
    return {
        "term": {
            field: value
        }
    }

def range_query(field, from_value=0, to_value=999999999, path=None):
    field = f"{path}.{field}" if path else field
    return {
        "range": {
            field: {
                "gte": from_value,
                "lte": to_value
            }
        }
    }

def bool_query(filter):
    return {
        "bool": {
            "filter": filter
        }
    }

def nested_query(path, query):
    return {
        "nested": {
            "path": path,
            "query": query
        }
    }