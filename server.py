### REST API server which hosts version history for the U.S. Code

## Library imports
import flask, json, os
from flask import jsonify, Flask, request

## Project imports
from lib.constants import *
from lib.server_init import *
import lib.structure

app = Flask(__name__)
debug = True

us_code = {}
us_code = load_diffs() ## Doesn't work if put in run block below.

@app.route('/getTitles')
def getTitles():
    return jsonify({API.GET_TITLES_KEY: us_code.keys()})

@app.route('/getTitle', methods=['GET'])
def getTitle():
    try:
        data = json.loads(request.data)
    except:
        data = {}

    if API.TITLE_KEY not in data:
        ## Bad request
        return jsonify(data)

    if data[API.TITLE_KEY] not in us_code:
        ## Missing data
        return jsonify(data)

    return jsonify(us_code[data[API.TITLE_KEY]].to_json())

@app.route('/getDiffs', methods=['GET', 'POST'])
def getDiffs():
    request_json = request.get_json(silent=not debug)
    return jsonify([18])

if __name__ == '__main__':
    # Startup file load goes here.
    # Probably add some logging too.
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', Server.PORT))
    app.run(host=Server.HOST, port=port, debug=debug)
