#!/usr/bin/python3
"""
starts a Flask web application
"""
from flask import Flask, jsonify
from api.v1.views import app_views
from models import storage
from models.amenity import *
from models.city import *
from models.user import *
from models.place import *
from models.state import *
from models.review import *


classes = {
    "amenity": Amenity,
    "city": City,
    "place": Place,
    "review": Review,
    "state": State,
    "user": User,
}
@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """returns Hello HBNB!"""
    status_dict = {"status": "OK"}
    return jsonify(status_dict)


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stats():
    """returns product of the count method"""
    stats_dict = {}

    for key, value in classes.items():
        stats_dict[key] = storage.count(value)

    return jsonify(stats_dict)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
