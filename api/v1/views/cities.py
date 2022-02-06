#!/usr/bin/python3
"""new view for City objects that handles all default RESTFul API actions"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models.state import State
from models.city import City
from models import storage


@app_views.route('/states/<state_id>/cities',
                 strict_slashes=False, methods=['GET'])
def get_all_cities_from_state(state_id):
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    cities = state.cities
    return jsonify([city.to_dict() for city in cities]), 200


@app_views.route('/cities/<city_id>',
                 strict_slashes=False, methods=['GET'])
def get_city_by_id(city_id):
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict()), 200


@app_views.route('/states/<state_id>/cities',
                 strict_slashes=False, methods=['POST'])
def create_city(state_id):
    city_json = request.get_json(silent=True)
    if not city_json:
        return jsonify({'error': 'Not a JSON'}), 400
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if 'name' not in city_json:
        return jsonify({'error': 'Missing name'}), 400
    city_json['state_id'] = state_id
    city = City(**city_json)
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>',
                 strict_slashes=False, methods=['PUT'])
def update_city(city_id):
    city_json = request.get_json(silent=True)
    if not city_json:
        return jsonify({'error': 'Not a JSON'}), 400
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    for key, val in city_json.items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, key, val)
    city.save()
    return jsonify(city.to_dict()), 200


@app_views.route('/cities/<city_id>',
                 strict_slashes=False, methods=['DELETE'])
def delete_city(city_id):
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200
