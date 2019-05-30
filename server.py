from city_api import get_cities
from flask import render_template, request, jsonify
import connexion

app = connexion.App(__name__, specification_dir='./')

app.add_api('swagger.yml')

# @app.route('/')
# def home():
#     return render_template('home.html')


@app.route('/')
def index():
	return render_template('form.html')


@app.route('/process', methods=['POST'])
def process():

    query = request.form['query']

    latitude = None
    if 'latitude' in request.form:
        latitude = request.form.get('latitude')

    longitude = None
    if 'longitude' in request.form:
        longitude = request.form.get('longitude')

    if query:
        return jsonify(get_cities(query, latitude, longitude))
    else:
        return jsonify({'error' : 'Missing data!'})


# FIXME: remember to turn off!
if __name__ == '__main__':
    app.run(debug=True)