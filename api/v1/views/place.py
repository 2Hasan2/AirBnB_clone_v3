#!/usr/bin/python3
"""
starts a Flask web application
"""
from api.v1.views import app_views
from flask import Flask, jsonify, abort, make_response, request
from models import storage
from models.city import *
from models.state import *
from models.place import *
from models.user import *


@app_views.route('/cities/<string:city_id>/places', methods=['GET'], strict_slashes=False)
def all_places(city_id):
    """Returns list of places in a JSON representation"""
    if storage.get(City, city_id) is None:
        abort(404)

    places = [place.to_dict() for place in storage.get(City, city_id).places]
    return jsonify(places)


@app_views.route('places/<string:place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Returs JSON representation of place with given ID"""
    if not place_id:
        abort(404)
    else:
        db_list = storage.all(Place)
        place_dict = [place.to_dict() for place in db_list.values()]
        for place in place_dict:
            if (place_id == place.get('id')):
                return (jsonify(place))
    return (make_response(jsonify({"error": "not found"}), 404))


@app_views.route('/places/<string:place_id>', methods=['DELETE'], strict_slashes=False)
def del_place(place_id):
    """Returs JSON representation of place with given ID"""
    if not place_id or storage.get(Place, place_id) is None:
        abort(404)
    else:
        place_delete = storage.get(Place, place_id)
        storage.delete(place_delete)
        storage.save()
        return (jsonify({}))


@app_views.route('/cities/<string:city_id>/places', methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """Returs JSON representation of place with given ID"""
    try:
        kwargs = request.get_json()
        kwargs['city_id'] = city_id

        dict_id = {kwargs.get("user_id"): User, city_id: City}
        for key, value in dict_id.items():
            if storage.get(value, key) is None:
                abort(404)

        list_keys = ["user_id", "name"]
        for key in list_keys:
            if not kwargs.get(key):
                return 'Missing {}'.format(key), 400

        place = Place(**kwargs)
        place.save()
        return jsonify(place.to_dict()), 201
    except TypeError:
        return "Not a JSON", 400


@app_views.route('/places/<string:place_id>', methods=['PUT'], strict_slashes=False)
def edit_place(place_id):
    """Returs JSON representation of place with given ID"""
    if storage.get(Place, place_id) is None:
        abort(404)
    list_keys = ["user_id", "city_id", "id", "created_at", "updated_at"]

    try:
        kwargs = request.get_json()
        place_old = storage.get(Place, place_id)

        for key, value in kwargs.items():
            if key not in list_keys:
                setattr(place_old, key, value)

        place_old.save()
        return jsonify(place_old.to_dict()), 200
    except ValueError:
        return "Not a JSON", 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', debug=True)
