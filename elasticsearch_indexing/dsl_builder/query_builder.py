def match_query(field, query, fuzziness=0):
    return {
        "match": {
            field: {"query": query, "operator": "and", "fuzziness": fuzziness}
        }
    }

def term_query(field, value):
    return {
        "term": {
            field: value
        }
    }

def range_query(field, from_value=0, to_value=999999999):
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
