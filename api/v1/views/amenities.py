#!/usr/bin/python3
"""new view for Amenity objects that handles all default RESTFul API actions"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models.amenity import Amenity
from models import storage


@app_views.route('/amenities', strict_slashes=False, methods=['GET'])
"""Retrieves the list of all Amenity objects: GET /api/v1/amenities"""
def get_all_amenities():
    amenities = storage.all(Amenity).values()
    return jsonify([amenity.to_dict() for amenity in amenities]), 200


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 method=['GET'])
"""Retrieves a Amenity object: GET /api/v1/amenities/<amenity_id>
If the amenity_id is not linked to any Amenity object, raise a 404 error"""
def get_amenity_by_id(amenity_id):
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict()), 200


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 method=['GET'])
"""Deletes a Amenity object:: DELETE /api/v1/amenities/<amenity_id>
If the amenity_id is not linked to any Amenity object, raise a 404 error
Returns an empty dictionary with the status code 200"""
def delete_amenity(amenity_id):
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', strict_slashes=False, method=['POST'])
"""Creates a Amenity: POST /api/v1/amenities
You must use request.get_json from Flask to transform 
the HTTP request to a dictionary
If the HTTP request body is not valid JSON, raise a 400
error with the message Not a JSON
If the dictionary doesn’t contain the key name, raise a 400
error with the message Missing name
Returns the new Amenity with the status code 201"""
def create_amenity():
    amenity_json = request.get_json(silent=True)
    if not amenity_json:
        return jsonify({'error': 'Not a JSON'}), 400
    if 'name' not in amenity_json:
        return jsonify({'error': 'Missing name'}), 400
    amenity = Amenity(**amenity_json)
    amenity.save()
    return jsonify(amenity.to_dict()), 201


@app_vies.route('/amenities/<amenity_id>', strict_slashes=False, method=['PUT'])
"""Updates a Amenity object: PUT /api/v1/amenities/<amenity_id>
If the amenity_id is not linked to any Amenity object, raise a 404 error
You must use request.get_json from Flask to transform the HTTP reques to a dic
If the HTTP request body is not valid JSON, raise a 400 error
with the message Not a JSON
Update the Amenity object with all key-value pairs of the dictionary
Ignore keys: id, created_at and updated_at
Returns the Amenity object with the status code 200"""
def update_amenity(amenity_id):
    amenity_json = request.get_json(silent=True)
    if not amenity_json:
        return jsonify({'error': 'Not a JSON'}), 400
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    for key, val in amenity_json items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, val)
    amenity.save()
    return jsonify(amenity.to dict()), 200
0"""
