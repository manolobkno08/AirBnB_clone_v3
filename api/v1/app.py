#!/usr/bin/python3

"""Start Flask API"""

from flask import Flask
import os
from models import storage
from api.v1.views import app_views

app = Flask(__name__)

app.register_blueprint(app_views)


@app.teardown_appcontext
def close(self):
    """Close session"""
    storage.close()


if __name__ == '__main__':
    if 'HBNB_API_HOST' and 'HBNB_API_PORT':
        app.run(host=os.getenv('HBNB_API_HOST'), port=int(os.getenv('HBNB_API_PORT')),
                threaded=True, debug=True)
    else:
        app.run(host='0.0.0.0', port='5000', threaded=True, debug=True)
