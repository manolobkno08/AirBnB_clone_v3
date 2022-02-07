#!/usr/bin/python3
"""new view for Amenity objects that handles all default RESTFul API actions"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models.amenity import Amenity
from models import storage


@app_views.route('/amenities', strict_slashes=False, methods=['GET'])
def get_all_amenities():
    """Retrieves the list of all Amenity objects"""
    amenities = storage.all(Amenity).values()
    return jsonify([amenity.to_dict() for amenity in amenities]), 200


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 method=['GET'])
def get_amenity_by_id(amenity_id):
    """Retrieves a Amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict()), 200


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 method=['GET'])
def delete_amenity(amenity_id):
    """Deletes a Amenity object:: DELETE"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', strict_slashes=False, method=['POST'])
def create_amenity():
    """Creates a Amenity: POST"""
    amenity_json = request.get_json(silent=True)
    if not amenity_json:
        return jsonify({'error': 'Not a JSON'}), 400
    if 'name' not in amenity_json:
        return jsonify({'error': 'Missing name'}), 400
    amenity = Amenity(**amenity_json)
    amenity.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 method=['PUT'])
def update_amenity(amenity_id):
    """Updates a Amenity object"""
    amenity_json = request.get_json(silent=True)
    if not amenity_json:
        return jsonify({'error': 'Not a JSON'}), 400
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    for key, val in amenity_json.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, val)
    amenity.save()
    return jsonify(amenity.to dict()), 200
