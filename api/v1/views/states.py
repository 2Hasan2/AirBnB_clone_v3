#!/usr/bin/python3
"""
starts a Flask web application
"""
from api.v1.views import app_views
# from api.v1.app import not_found
from flask import Flask, jsonify, abort, make_response, request
from models import storage
from models.state import *


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def all_states():
    """Returns list of States in a JSON representation"""
    db_list = storage.all(State)
    state_dict = [state.to_dict() for state in db_list.values()]

    return jsonify(state_dict)


@app_views.route('/states/<string:state_id>', methods=['GET'], strict_slashes=False)
def fetch_state(state_id):
    """Returs JSON representation of state with given ID"""
    if not state_id:
        abort(404)
    else:
        db_list = storage.all(State)
        state_dict = [state.to_dict() for state in db_list.values()]
        for state in state_dict:
            if (state_id == state.get('id')):
                return (jsonify(state))
    return (make_response(jsonify({"error": "not found"}), 404))


@app_views.route('/states/<string:state_id>', methods=['DELETE'], strict_slashes=False)
def del_state(state_id):
    """Returs JSON representation of state with given ID"""
    if not state_id:
        abort(404)
    else:
        state_delete = storage.get(State, state_id)
        storage.delete(state_delete)
        storage.save()
        return jsonify({}), 200


@app_views.route('/states/', methods=['POST'], strict_slashes=False)
def create_state():
    """Returs JSON representation of state with given ID"""
    if request.get_json:
        kwargs = request.get_json()
    else:
        return "Not a JSON", 400

    if kwargs:
        if 'name' not in kwargs.keys():
            return 'Missing name', 400

    try:
        state = State(**kwargs)
        state.save()
    except TypeError:
        return "Not a JSON", 400

    return make_response(jsonify(state.to_dict()), 201)


@app_views.route('/states/<string:state_id>', methods=['PUT'], strict_slashes=False)
def edit_state(state_id):
    """Returs JSON representation of state with given ID"""
    list_keys = ["id", "created_at", "updated_at"]

    try:
        kwargs = request.get_json()
        state_old = storage.get(State, state_id)

        for key, value in kwargs.items():
            if key not in list_keys:
                setattr(state_old, key, value)

        state_old.save()
        return jsonify(state_old.to_dict()), 200
    except ValueError:
        return "Not a JSON", 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', debug=True)
