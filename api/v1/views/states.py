#!/usr/bin/python3
"""
starts a Flask web application
"""
from api.v1.views import app_views
# from api.v1.app import not_found
from flask import Flask, jsonify, abort, make_response, request
from models import storage
from models.base_model import *
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
        state_dict = {}
        for state in state_dict:
            if (state_id == state.get('id')):
                storage.delete(state_id)
                return (jsonify({}))
    abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state(state_id):
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

    # if not state_id:
    #     abort(404)
    # else:
    #     try:
    #         kwargs = request.get_json()
    #         if (name not in kwargs.keys()):
    #             return(make_response("Missing name"), 400)
    #         else:
    #             new_state = State(**kwargs)
    #             new_state.save()
    #             return (make_response(jsonify(new_state.to_dict()), 201))
    #     except ValueError:
    #         abort(404)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', debug=True)
