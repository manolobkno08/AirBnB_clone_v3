#!/usr/bin/python3

"""Start Flask API"""

from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'])
def status_code():
    """Returns API status"""
    return jsonify({"status": "OK"})
