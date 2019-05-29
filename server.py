from flask import render_template, request, jsonify
import connexion

app = connexion.App(__name__, specification_dir='./')

app.add_api('swagger.yml')


@app.route('/')
def home():
    return render_template('home.html')


# FIXME: remember to turn off!
if __name__ == '__main__':
    app.run(debug=False)