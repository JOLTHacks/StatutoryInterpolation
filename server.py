### REST API server which hosts version history for the U.S. Code
import flask, os
from flask import jsonify, Flask

app = Flask(__name__)

@app.route('/getTitles')
def getTitles():
    return jsonify([18])

@app.route('/getTitle/<int:title>')
def getTitle(title):
    return jsonify([title])

@app.route('/getDiffs')
def getDiffs():
    return jsonify([18])

if __name__ == '__main__':
    # Startup file load goes here.
    # Probably add some logging too.
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
