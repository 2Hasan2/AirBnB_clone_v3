#!/usr/bin/python3
"""
starts a Flask web application
"""
from api.v1.views import app_views
from flask import Flask, jsonify, abort, make_response, request
from models import storage
from models.state import *
from models.city import *


@app_views.route('/states/<string:state_id>/cities', methods=['GET'], strict_slashes=False)
def all_cities(state_id):
    """Returns list of Cities in a JSON representation"""
    if storage.get(State, state_id) is None:
        abort(404)

    cities = [city.to_dict() for city in storage.get(State, state_id).cities]
    return jsonify(cities)


@app_views.route('cities/<string:city_id>', methods=['GET'], strict_slashes=False)
def city_state(city_id):
    """Returs JSON representation of city with given ID"""
    if not city_id:
        abort(404)
    else:
        db_list = storage.all(City)
        city_dict = [city.to_dict() for city in db_list.values()]
        for city in city_dict:
            if (city_id == city.get('id')):
                return (jsonify(city))
    return (make_response(jsonify({"error": "not found"}), 404))


@app_views.route('/cities/<string:city_id>', methods=['DELETE'], strict_slashes=False)
def del_city(city_id):
    """Returs JSON representation of city with given ID"""
    if not city_id:
        abort(404)
    else:
        city_delete = storage.get(City, city_id)
        storage.delete(city_delete)
        storage.save()
        return (jsonify({}))


@app_views.route('/states/<string:state_id>/cities', methods=['POST'], strict_slashes=False)
def create_city(state_id):
    """Returs JSON representation of state with given ID"""
    if storage.get(State, state_id) is None:
        abort(404)

    try:
        kwargs = request.get_json()
        kwargs['state_id'] = state_id

        if not kwargs.get('name'):
            return 'Missing name', 400

        city = City(**kwargs)
        city.save()
        return jsonify(city.to_dict()), 201
    except TypeError:
        return "Not a JSON", 400


@app_views.route('/cities/<string:city_id>', methods=['PUT'], strict_slashes=False)
def edit_city(city_id):
    """Returs JSON representation of city with given ID"""
    list_keys = ["state_id", "id", "created_at", "updated_at"]

    try:
        kwargs = request.get_json()
        city_old = storage.get(City, city_id)

        for key, value in kwargs.items():
            if key not in list_keys:
                setattr(city_old, key, value)

        city_old.save()
        return jsonify(city_old.to_dict()), 200
    except ValueError:
        return "Not a JSON", 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', debug=True)
