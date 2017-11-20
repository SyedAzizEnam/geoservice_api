# Geoservices API

Here is a service that can can resolve the lat, lng coordinates for an address
by using third party geocoding services. 

# Start up service

The app was developed on python 3+ so please make sure python 3.0+ is installed.
To install all required libraries run the line: `pip install -r requirements.txt`

To run the service locally run the line: `python app.py`

The service will now be running on the local machine and can be reached though HTTP accepting either GET or POST requests.

# Using the service
For POST requests add `{'Content-Type': 'application/json'}` to the request header and then the input json is as follows:

```javascript
{
  "address": "1222 Harrison san francisco ca 94103"
}
```
For GET request you can use the following format: 
`http://localhost/geoservices/?address=1222%20Harrison%20san%20francisco%20ca%2094103`

This is an example of a successful output from the service.
```javascript
{
  "result": {
    "geo_location": {
      "lat": 37.7736106,
      "lng": -122.4092483
    },
    "search_address": "1222 Harrison san francisco ca 94103"
  },
  "status": 200
}
```

# Adding Third Party Services
Currently there are two geolocations services that are configured (Google, HERE). The services are configured in 'service_config.yaml' the services are used in the order that they appear in the configuration file. The api attempts to use the geolocation services in order until it successfully retreives a lat/lng pair. Additional services can be added to the file by following this format:
```yaml
  - name: name_of_service
    URL: url_of_service
    address_field: request_param_that_accepts_address_search_text
    request_param:
      (key:value of any request params that are required)
    response_paths:
      lat: path_to_lat_in_the_response_json 
      lng: path_to_lng_in_the_response_json
      (any paths that require traversing through list can be indentified by using the "list__(index)" key)
```
