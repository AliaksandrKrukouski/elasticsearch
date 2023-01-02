def terms_agg(bucket_field, limit=1000, path=None, sub_agg=None):
    bucket_field = f"{path}.{bucket_field}" if path else bucket_field
    sub_agg = sub_agg if sub_agg else {}
    return {
        "agg_bucket": {
            "terms": {
                "field": bucket_field,
                "size": limit
            },
            "aggs": sub_agg
        }
    }

def sub_agg(agg_type, bucket_field, metric_field, agg_from=0, agg_to=999999999, sort_order="asc", limit=1000):
    return {
        "agg_bucket": {
            "terms": {
                "field": bucket_field
            },
            "aggs": {
                "agg_metric": {
                    agg_type: {
                        "field": metric_field
                    }
                },
                "agg_filter": {
                    "bucket_selector": {
                        "buckets_path": {
                            "rate": "agg_metric"
                        },
                        "script": f"params.rate >= {agg_from} && params.rate <= {agg_to}"
                    }
                },
                "agg_sort": {
                    "bucket_sort": {
                        "sort": [
                            {"agg_metric": {"order": sort_order}}
                        ],
                        "size": limit
                    }
                }
            }
        }
    }

def nested_agg(path, aggs):
    return {
        "nested_agg": {
            "nested": {"path": path},
            "aggs": aggs
        }
    }