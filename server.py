import flask, os
from flask import jsonify, Flask

app = Flask(__name__)

@app.route('/getTitles')
def getTitles():
    return jsonify([18])

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
