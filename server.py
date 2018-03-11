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
us_code = load_diffs(BACKEND.DIFF_SOURCE) ## Doesn't work if put in run block below.

@app.route('/getTitles')
def getTitles():
    return jsonify({API.KEYS.GET_TITLES: us_code.keys()})

@app.route('/getTitle', methods=['GET'])
def getTitle():
    try:
        data = json.loads(request.data)
    except:
        data = {}

    if API.KEYS.TITLE not in data:
        ## Bad request
        return jsonify(data)

    if data[API.KEYS.TITLE] not in us_code:
        ## Missing data
        return jsonify(data)

    return jsonify(us_code[data[API.KEYS.TITLE]].to_json())

@app.route('/getDiffs', methods=['GET', 'POST'])
def getDiffs():
    ## Refactor this and above.
    try:
        data = json.loads(request.data)
    except:
        data = {}

    if API.KEYS.TITLE not in data:
        ## Bad request
        return jsonify(data)

    if data[API.KEYS.TITLE] not in us_code:
        ## Missing data
        return jsonify(data)
    
    return jsonify(us_code[12].get_text_at(datetime.datetime.now()).to_json())

if __name__ == '__main__':
    # Startup file load goes here.
    # Probably add some logging too.
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', Server.PORT))
    app.run(host=Server.HOST, port=port, debug=debug)
