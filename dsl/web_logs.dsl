#Number of requests with tags success or login for Windows machines
GET /kibana_sample_data_logs/_search
{
  "size": 0,
  "query": {
    "bool": {
      "filter": [
        {
          "terms": {
              "tags": [
                "login",
                "success"
              ]
          }
        },
        {
          "term": {
            "machine.os": "win"
          }
        }
      ]
    }
  },
  "aggs": {
    "request_count": {
      "value_count": {
        "field": "ip"
      }
    }
  }
}

#Find total number of logs with IP in range from 176.0.0.0 to 179.255.255.254 with request size being between 1000 and 10000 bytes
GET /kibana_sample_data_logs/_search
{
  "size": 0,
  "query": {
    "bool": {
      "filter": [
        {
          "range": {
            "ip": {
              "gte": "176.0.0.0",
              "lte": "179.255.255.254"
            }
          }
        },
        {
          "range": {
            "bytes": {
              "gte": 1000,
              "lte": 10000
            }
          }
        }
      ]
    }
  },
  "aggs": {
    "request_count": {
      "value_count": {
        "field": "ip"
      }
    }
  }
}

#Number of requests with some value of memory field and Firefox based agent
GET /kibana_sample_data_logs/_search
{
  "size": 0,
  "query": {
    "bool": {
      "filter": [
        {
          "match": {
            "agent": "firefox"
          }
        },
        {
          "exists": {
            "field": "memory"
          }
        }
      ]
    }
  },
  "aggs": {
    "request_count": {
      "value_count": {
        "field": "ip"
      }
    }
  }
}