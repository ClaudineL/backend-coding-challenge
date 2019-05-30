from city_api import get_cities, check_inputs, load_md
from flask import render_template, request, jsonify, Markup
import connexion

app = connexion.App(__name__, specification_dir='./')

app.add_api('swagger.yml')

@app.route('/')
def home():
    """ Render Markdown documentation to app homepage. """
    content = Markup(load_md())
    return render_template('home.html', **locals())

@app.route('/form')
def form():
    """ API functionality as a webform. """
    return render_template('form.html')

@app.route('/process', methods=['POST'])
def process():
    """ Code for processing webform query. """
    query = request.form['query']

    latitude = None
    if 'latitude' in request.form:
        latitude = request.form.get('latitude')

    longitude = None
    if 'longitude' in request.form:
        longitude = request.form.get('longitude')

    # Returns False when input is valid, error message otherwise
    if query:
        check = check_inputs(query, latitude, longitude)
        # If any check failed, return error message, otherwise lookup query
        if check:
            return jsonify(check)
        else:
            return jsonify(get_cities(query, latitude, longitude))
    else:
        return jsonify({'error' : 'Missing data!'})


# FIXME: remember to turn off!
if __name__ == '__main__':
    app.run(debug=True)