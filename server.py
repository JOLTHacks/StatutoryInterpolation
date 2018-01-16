### REST API server which hosts version history for the U.S. Code

## Library imports
import flask, json, os
from flask import jsonify, Flask, request

## Project imports
from lib.constants import *
from lib.logic import *
import lib.structure

app = Flask(__name__)
debug = True

us_code = {}

@app.route('/getTitles')
def getTitles():
    return jsonify({'titles': [12]})

@app.route('/getTitle', methods=['GET'])
def getTitle():
    try:
        data = json.loads(request.data)
    except:
        data = {}

    if API.TITLE_KEY not in data:
        return jsonify(data)

    if data[API.TITLE_KEY] not in us_code:
        return jsonify(data)

    return jsonify(us_code[data[API.TITLE_KEY]])

@app.route('/getDiffs', methods=['GET', 'POST'])
def getDiffs():
    request_json = request.get_json(silent=not debug)
    return jsonify([18])

if __name__ == '__main__':
    # Startup file load goes here.
    # Probably add some logging too.
    # Bind to PORT if defined, otherwise default to 5000.
    us_code = load_diffs()
    port = int(os.environ.get('PORT', Server.PORT))
    app.run(host=Server.HOST, port=port, debug=debug)
