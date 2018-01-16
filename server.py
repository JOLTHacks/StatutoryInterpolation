### REST API server which hosts version history for the U.S. Code

## Library imports
import flask, json, os
from flask import jsonify, Flask, request

## Project imports
from lib import constants, structure

app = Flask(__name__)
debug = True

@app.route('/getTitles')
def getTitles():
    return jsonify([18])

@app.route('/getTitle', methods=['GET'])
def getTitle():
    try:
        data = json.loads(request.data)
    except:
        data = {}

    if constants.TITLE_KEY not in data:
        return jsonify(data)
    
    return jsonify(data[constants.TITLE_KEY])

@app.route('/getDiffs', methods=['GET', 'POST'])
def getDiffs():
    request_json = request.get_json(silent=not debug)
    return jsonify([18])

if __name__ == '__main__':
    # Startup file load goes here.
    # Probably add some logging too.
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=debug)
