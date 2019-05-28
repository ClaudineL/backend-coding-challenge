from flask import Flask, request, jsonify
from text_matching import text_match
from scoring import score_results
import pprint

app = Flask(__name__)


@app.route('/suggestions')
def index():
    query = request.args['q']
    loc = None
    lat = request.args.get('latitude')
    lon = request.args.get('longitude')
    if lat and lon:
        loc = (lat, lon)
    matches = text_match(query)
    scored_matches = score_results(matches, query, loc)
    return jsonify(scored_matches)


if __name__ == '__main__':
    app.run(debug=True)
