#!/usr/bin/python3
""" places_amenities API """
from api.v1.views import app_views
from flask import jsonify, abort
from models import storage
from models.place import Place
from models.amenity import Amenity
from models import storage_t as storage_type


@app_views.route(
        '/places/<place_id>/amenities',
        methods=['GET'], strict_slashes=False)
def get_place_amenities(place_id):
    """Retrieves the list of all Amenity objects of a Place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    result = []

    if storage_type == "db":
        for amenity in place.amenities:
            result.append(amenity.to_dict())
    else:
        result = place.amenities

    return jsonify(result), 200


@app_views.route(
        '/places/<place_id>/amenities/<amenity_id>',
        methods=['DELETE'], strict_slashes=False)
def delete_place_amenity(place_id, amenity_id):
    """Deletes an Amenity object from a Place"""
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if place is None or amenity is None:
        abort(404)
    if amenity not in place.amenities:
        abort(404)

    if storage_type == "db":
        place.amenities.remove(amenity)
    else:
        place.amenity_ids.remove(amenity)
    storage.save()

    return jsonify({}), 200


@app_views.route(
        '/places/<place_id>/amenities/<amenity_id>',
        methods=['POST'], strict_slashes=False)
def link_place_amenity(place_id, amenity_id):
    """Links an Amenity object to a Place"""
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if place is None or amenity is None:
        abort(404)
    if amenity in place.amenities:
        return jsonify(amenity.to_dict()), 200

    if storage_type == "db":
        place.amenities.append(amenity)
    else:
        place.amenity_ids.append(amenity.id)
    storage.save()

    return jsonify(amenity.to_dict()), 201
