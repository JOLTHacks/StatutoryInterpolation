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
## Doesn't work if put in run block below.
us_code = load_us_code(BACKEND.US_CODE_SOURCE)
us_code = load_diffs(BACKEND.DIFF_SOURCE, us_code)

@app.route('/getTitles')
def getTitles():
    ## May just want to cache this data.
    return json.dumps({API.KEYS.GET_TITLES: us_code.get_subsection_keys()})

@app.route('/getTitle', methods=['GET'])
def getTitle():
    try:
        data = json.loads(request.data)
    except:
        data = {}

    if API.KEYS.TITLE not in data:
        ## Bad request
        return json.dumps(data)

    title_data = us_code.get_subsection(data[API.KEYS.TITLE])
    if title_data is None:
        ## Bad request
        return json.dumps(data)
    
    return json.dumps(title_data.to_json())

@app.route('/getDiffs', methods=['GET', 'POST'])
def getDiffs():
    ## Refactor this and above.
    try:
        data = json.loads(request.data)
    except:
        data = {}

    if API.KEYS.TITLE not in data:
        ## Bad request
        return json.dumps(data)

    title_data = us_code.get_subsection(data[API.KEYS.TITLE])
    if title_data is None:
        ## Bad request
        return json.dumps(data)
    
    return json.dumps(us_code.get_subsection(12).get_text_at(datetime.datetime.now().date()).to_json())

if __name__ == '__main__':
    # Startup file load goes here.
    # Probably add some logging too.
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', Server.PORT))
    app.run(host=Server.HOST, port=port, debug=debug)
