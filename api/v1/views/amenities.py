#!/usr/bin/python3
"""
starts a Flask web application
"""
from api.v1.views import app_views
# from api.v1.app import not_found
from flask import Flask, jsonify, abort, make_response, request
from models import storage
from models.amenity import *


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def all_amenities():
    """Returns list of amenities in a JSON representation"""
    db_list = storage.all(Amenity)
    amenity_dict = [amenity.to_dict() for amenity in db_list.values()]

    return jsonify(amenity_dict)


@app_views.route('/amenities/<string:amenity_id>', methods=['GET'], strict_slashes=False)
def fetch_amenity(amenity_id):
    """Returs JSON representation of amenity with given ID"""
    if not amenity_id:
        abort(404)
    else:
        db_list = storage.all(Amenity)
        amenity_dict = [amenity.to_dict() for amenity in db_list.values()]
        for amenity in amenity_dict:
            if (amenity_id == amenity.get('id')):
                return (jsonify(amenity))
    return (make_response(jsonify({"error": "not found"}), 404))


@app_views.route('/amenities/<string:amenity_id>', methods=['DELETE'], strict_slashes=False)
def del_amenity(amenity_id):
    """Returs JSON representation of amenity with given ID"""
    if not amenity_id:
        abort(404)
    else:
        amenity_delete = storage.get(Amenity, amenity_id)
        storage.delete(amenity_delete)
        storage.save()
        return (jsonify({}))


@app_views.route('/amenities/', methods=['POST'], strict_slashes=False)
def create_amenity():
    """Returs JSON representation of amenity with given ID"""
    if request.get_json:
        kwargs = request.get_json()
    else:
        return "Not a JSON", 400

    if kwargs:
        if 'name' not in kwargs.keys():
            return 'Missing name', 400

    try:
        amenity = Amenity(**kwargs)
        amenity.save()
    except TypeError:
        return "Not a JSON", 400

    return make_response(jsonify(amenity.to_dict()), 201)


@app_views.route('/amenities/<string:amenity_id>', methods=['PUT'], strict_slashes=False)
def edit_amenity(amenity_id):
    """Returs JSON representation of amenity with given ID"""
    list_keys = ["id", "created_at", "updated_at"]

    try:
        kwargs = request.get_json()
        amenity_old = storage.get(Amenity, amenity_id)

        for key, value in kwargs.items():
            if key not in list_keys:
                setattr(amenity_old, key, value)

        amenity_old.save()
        return jsonify(amenity_old.to_dict()), 200
    except ValueError:
        return "Not a JSON", 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', debug=True)
