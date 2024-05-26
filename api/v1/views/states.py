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

@app_views.route('/states', methods=['GET'], strict_slashes=False)
def all_states():
    """returns Hello HBNB!"""
    state_list = to_dict(storage.all(State))
    return jsonify(state_list)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
