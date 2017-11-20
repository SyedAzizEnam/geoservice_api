from flask import Flask, request, jsonify
import yaml
import traceback
import urllib
import urllib.request
import json

with open('config.yaml') as f:
    config = yaml.load(f)
    services = config["Services"]

app = Flask(__name__)


@app.route('/geoservices/', methods=['GET','POST'])
def geoservice_method():

        if request.method == 'GET':
            data = request.args

        if request.method == 'POST':
            data = request.json

        output = {}
        output["result"] = {}

        for service in services:
            try:
                url = service['URL']
                request_data = {}
                request_data[service["address_field"]] = data["address"]
                for param in service["request_param"]:
                    request_data[param] = service["request_param"][param]

                request_url = url + urllib.parse.urlencode(request_data)
                response = urllib.request.urlopen(request_url)
                response_json = json.loads(response.read().decode(response.info().get_param('charset') or 'utf-8'))

                output_data = {}
                for param, path in service["reponse_paths"].items():
                    result = response_json
                    for entry in path.split('.'):
                        if 'list__' in entry:
                            index = int(entry.split('__')[1])
                            result = result[index]
                        else:
                            result = result[entry]

                    output_data[param] = result

                output["result"]["geo_location"] = output_data
                output["result"]["search_address"] = data["address"]
                output["status"] = 200

                return jsonify(output)

            except Exception as e:
                print("UNEXPECTED SERVICE ERROR TRACEBACK:")
                print(traceback.format_exc())
                continue

        output["status"] = 503
        output["result"]["message"] = "Unable to reach geoservices"

        return jsonify(output)

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True, threaded=True, port=80)
