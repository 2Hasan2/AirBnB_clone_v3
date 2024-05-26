#!/usr/bin/python3
"""
starts a Flask web application
"""
from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage
from models.base_model import *
from models.state import *


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def all_states():
    """returns Hello HBNB!"""
    db_list = storage.all(State)
    state_dict = [state.to_dict() for state in db_list.values()]

    return jsonify(state_dict)


@app_views.route('/states/<str:state_id>', methods=['GET'], strict_slashes=False)
def fetch_state(state_id):
    """returns Hello HBNB!"""
    result_list = (storage.all(State))
    for state in result_list.values().to_dict():
        if (state_id == state.get(id)):
            return (jsonify())
    return jsonify(state_dict)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', debug=True)
