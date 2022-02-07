#!/usr/bin/python3
"""The controller for the api"""

from flask import Flask, make_response, jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)

app.register_blueprint(app_views)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage on teardown"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == "__main__":
    HBNB_API_HOST = getenv('HBNB_API_HOST') if not None else '0.0.0.0'
    HBNB_API_PORT = getenv('HBNB_API_PORT') if not None else '5000'

    app.run(host=HBNB_API_HOST,
            port=HBNB_API_PORT,
            threaded=True,
            debug=True)
