# How many customers from Birmingham which bought products that costs up to 100$?
GET /kibana_sample_data_ecommerce/_search
{
  "size": 0,
  "query": {
    "bool": {
      "must": [
        {"term": {"geoip.city_name": {"value": "Birmingham"}}},
        {"range": {"products.price": {"lte": 100}}}
      ]
    }
  },
  "aggs": {
    "customer_count": {
      "value_count": {
        "field": "customer_id"
      }
    }
  }
}

# How many purchases have double E or double B in their customer’s names?
GET /kibana_sample_data_ecommerce/_search
{
  "size": 0,
  "query": {
    "regexp": {
      "customer_full_name": ".*(bb|cc).*"
    }
  },
  "aggs": {
    "order_count": {
      "value_count": {
        "field": "order_id"
      }
    }
  }
}

# How many purchases contains only 1 manufacturer, even though there are multiple purchases?
GET /kibana_sample_data_ecommerce/_search
{
  "size": 0,
  "query": {
    "bool": {
      "filter": [
        {
          "script": {
            "script": {
              "source":
              """
              def manufacturer_arr = doc['manufacturer.keyword'];
              def one_manufacturer_bool = true;
              for(int i = 0; i < manufacturer_arr.length-1; i++) {
                for(int j = i+1; j < manufacturer_arr.length; j++) {
                  if(manufacturer_arr[i] != manufacturer_arr[j]) {
                    one_manufacturer_bool = false;
                    break
                  }
                }
                if (!one_manufacturer_bool) {
                  break
                }
              }
              return one_manufacturer_bool;
              """
            }
          }
        }
      ]
    }
  },
  "aggs": {
    "order_count": {
      "value_count": {
        "field": "order_id"
      }
    }
  }
}
