#!/usr/bin/python3
""" Index """
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage
from api.v1.views import app_views
from flask import jsonify

classes = {
    "amenities": Amenity, "cities": City,
    "places": Place, "reviews": Review,
    "states": State, "users": User
}


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """ Status of API """
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def number_objects():
    """ Retrieves the number of each objects by type """

    new_dict = {}
    for key, value in classes.items():
        new_dict[key] = storage.count(value)
    return jsonify(new_dict)


@app_views.route('/stats/<object>', methods=['GET'], strict_slashes=False)
def number_objects_by_object(object):
    """ Retrieves the number of each objects by type """

    new_dict = {}
    for key, value in classes.items():
        if key == object:
            new_dict[key] = storage.count(value)
            return jsonify(new_dict)
    return jsonify({"error": "Not found"}), 404
