#!/usr/bin/python3
from models.city import City
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request


@app_views.route(
        '/states/<state_id>/cities', methods=['GET'],
        strict_slashes=False)
def cities(state_id):
    """Status of API"""
    cities = storage.all(City)
    cities = [city.to_dict() for city in cities.values()]
    return jsonify(cities)


@app_views.route(
        '/cities/<city_id>', methods=['GET'],
        strict_slashes=False)
def city_id(city_id):
    """Retrieves the number of each objects by type"""
    city = storage.get(City, city_id)
    if not city:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(city.to_dict())


@app_views.route(
        '/cities/<city_id>', methods=['DELETE'],
        strict_slashes=False)
def delete_city(city_id):
    """Delete city"""
    city = storage.get(City, city_id)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route(
        '/states/<state_id>/cities', methods=['POST'],
        strict_slashes=False)
def post_city(state_id):
    """Create a new city"""
    if not request.get_json():
        abort(400, description="Not a JSON")

    if 'name' not in request.get_json():
        abort(400, description="Missing name")

    data = request.get_json()
    instance = City(**data)
    instance.save()
    return jsonify(instance.to_dict()), 201


@app_views.route(
        '/cities/<city_id>', methods=['PUT'],
        strict_slashes=False)
def put_city(city_id):
    """Update a city"""
    city = storage.get(City, city_id)

    if not city:
        abort(404, description="Not found")

    if not request.get_json():
        abort(400, description="Not a JSON")

    data = request.get_json()
    for key, value in data.items():
        setattr(city, key, value)

    city.save()

    return jsonify(city.to_dict()), 200