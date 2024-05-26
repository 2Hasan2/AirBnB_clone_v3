#!/usr/bin/python3
from models.state import State
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def states():
    """Status of API"""
    states = storage.all(State)
    states = [state.to_dict() for state in states.values()]
    return jsonify(states)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def state_id(state_id):
    """Retrieves the number of each objects by type"""
    state = storage.get(State, state_id)
    if not state:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(state.to_dict())


@app_views.route(
        '/states/<state_id>', methods=['DELETE'],
        strict_slashes=False)
def delete_state(state_id):
    """Delete state"""
    state = storage.get(State, state_id)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    """Create a new state"""
    if not request.get_json():
        abort(400, description="Not a JSON")

    if 'name' not in request.get_json():
        abort(400, description="Missing name")

    data = request.get_json()
    instance = State(**data)
    instance.save()
    return jsonify(instance.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_state(state_id):
    """Update a state"""
    state = storage.get(State, state_id)

    if not state:
        abort(404, description="Not found")

    if not request.get_json():
        abort(400, description="Not a JSON")

    data = request.get_json()
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)

    state.save()
    return jsonify(state.to_dict()), 200