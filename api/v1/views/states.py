#!/usr/bin/python3
"""new view for State objects that handles all default RESTFul API actions"""

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models.state import State
from models import storage


@app_views.route('/states', strict_slashes=False, methods=['GET'])
def get_all_states():
    states = storage.all(State).values()
    return jsonify([state.to_dict() for state in states]), 200


@app_views.route('/states/<state_id>',
                 strict_slashes=False, methods=['GET'])
def get_state_by_id(state_id):
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict()), 200


@app_views.route('/states',
                 strict_slashes=False, methods=['POST'])
def create_state():
    state_json = request.get_json(silent=True)
    if not state_json:
        return jsonify({'error': 'Not a JSON'}), 400
    if 'name' not in state_json:
        return jsonify({'error': 'Missing name'}), 400
    state = State(**state_json)
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>',
                 strict_slashes=False, methods=['PUT'])
def update_state(state_id):
    state_json = request.get_json(silent=True)
    if not state_json:
        return jsonify({'error': 'Not a JSON'}), 400
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    for key, val in state_json.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, val)
    state.save()
    return jsonify(state.to_dict()), 200


@app_views.route('/states/<state_id>',
                 strict_slashes=False, methods=['DELETE'])
def delete_state(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200
