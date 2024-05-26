#!/usr/bin/python3
"""places"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City
from models.place import Place
from datetime import datetime
import uuid


@app_views.route(
        '/cities/<city_id>/places', methods=['GET'],
        strict_slashes=False)
def places(city_id):
    """Retrieves the list of all Place objects"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    places = storage.all(Place)
    places = [
        place.to_dict() for place in places.values()
        if place.city_id == city_id
    ]
    return jsonify(places), 200


@app_views.route(
        '/places/<place_id>',
        methods=['GET'], strict_slashes=False)
def place_id(place_id):
    """Retrieves a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        return abort(404)
    return jsonify(place.to_dict()), 200


@app_views.route(
        '/places/<place_id>',
        methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """Deletes a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route(
        '/cities/<city_id>/places',
        methods=['POST'], strict_slashes=False)
def post_place(city_id):
    """Creates a Place"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'user_id' not in request.get_json():
        abort(400, description="Missing user_id")
    if 'name' not in request.get_json():
        abort(400, description="Missing name")
    data = request.get_json()
    data['city_id'] = city_id
    instance = Place(**data)
    instance.save()
    return jsonify(instance.to_dict()), 201


@app_views.route(
        '/places/<place_id>',
        methods=['PUT'], strict_slashes=False)
def put_place(place_id):
    """Updates a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    data = request.get_json()
    for key, value in data.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200


@app_views.route(
        '/places_search',
        methods=['POST'], strict_slashes=False)
def search_places():
    """Retrieves the list of all Place objects"""
    if not request.get_json():
        abort(400, description="Not a JSON")
    data = request.get_json()
    places = storage.all(Place)
    places = [
        place.to_dict() for place in places.values()
        if all(
            value in place.to_dict().values()
            for key, value in data.items()
        )
    ]
    return jsonify(places), 200
