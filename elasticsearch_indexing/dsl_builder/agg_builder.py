def terms_agg(bucket_field, limit):
    return {
        "agg_bucket": {
            "terms": {
                "field": bucket_field,
                "size": limit
            }
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
