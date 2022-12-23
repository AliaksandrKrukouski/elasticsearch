#Number of flights with less than 1000 miles distance
GET /kibana_sample_data_flights/_search
{
  "size": 0,
  "query": {
    "range": {
      "DistanceKilometers": {
        "gt": 0,
        "lt": 1000
      }
    }
  },
  "aggs": {
    "flights_count": {
      "value_count": {
        "field": "FlightNum"
      }
    }
  }
}

#How many flights that do not fly to International airport with Clear and Sunny weather
GET /kibana_sample_data_flights/_search
{
  "size": 0,
  "query": {
    "bool": {
      "filter": [
        {"script": {
          "script": "doc['OriginCountry'].value != doc['DestCountry'].value"
        }
        },
        {"term": {
          "Cancelled": true
        }},
        {"terms": {
          "DestWeather": ["Clear", "Cloudy"]
        }
        }
      ]
    }
  },
  "aggs": {
    "flights_count": {
      "value_count": {
        "field": "FlightNum"
      }
    }
  }
}

#How many flights were delayed by at least an hour on Monday?
GET /kibana_sample_data_flights/_search
{"size": 0,
  "query": {
      "bool": {
        "filter": [
          {"term": {
            "dayOfWeek": 0
            }
          },
          {"range": {
            "FlightDelayMin": {
              "gt": 60
            }
          }}
        ]
      }
  },
  "aggs": {
    "flights_count": {
      "value_count": {
        "field": "FlightNum"
      }
    }
  }
}
