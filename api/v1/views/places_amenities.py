#!/usr/bin/python3
""" places_amenities API """
from api.v1.views import app_views
from flask import jsonify, abort, make_response
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

    if storage_type == "db":
        amenities = [amenity.to_dict() for amenity in place.amenities]
    else:
        amenities = [amenity.to_dict() for amenity in place.amenity_ids]
    return jsonify(amenities), 200


@app_views.route(
        '/places/<place_id>/amenities/<amenity_id>',
        methods=['DELETE'], strict_slashes=False)
def delete_place_amenity(place_id, amenity_id):
    """Deletes an Amenity object from a Place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    for amenityDb in place.amenities:
        if amenityDb.id == amenity.id:
            if storage_type == "db":
                place.amenities.remove(amenityDb)
            else:
                place.amenity_ids.remove(amenityDb)
            storage.save()
            return jsonify({}), 200


@app_views.route(
        '/places/<place_id>/amenities/<amenity_id>',
        methods=['POST'], strict_slashes=False)
def link_place_amenity(place_id, amenity_id):
    """Links an Amenity object to a Place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    if amenity in place.amenities:
        return jsonify(amenity.to_dict()), 200
    if storage_type == "db":
        if amenity not in place.amenities:
            place.amenities.append(amenity)
    else:
        if amenity.id not in place.amenity_ids:
            place.amenity_ids.append(amenity.id)
    storage.save()
    return jsonify(amenity.to_dict()), 201
