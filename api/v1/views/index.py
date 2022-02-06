#!/usr/bin/python3

"""Start Flask API"""

from flask import jsonify
from api.v1.views import app_views
from models import storage

Stats_dict = {
    "amenities": "Amenity",
    "cities": "City",
    "places": "Place",
    "reviews": "Review",
    "states": "State",
    "users": "User"
}


@app_views.route('/status', methods=['GET'])
def status_code():
    """Returns API status"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def Stats_code():
    """Returns the number of each objects by type"""
    return_dict = {}
    for key, value in Stats_dict.items():
        return_dict[key] = storage.count(value)
    return jsonify(return_dict)

if __name__ == '__main__':
    pass
