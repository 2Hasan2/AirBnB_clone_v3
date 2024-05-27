#!/usr/bin/python3
"""
starts a Flask web application
"""
from api.v1.views import app_views
# from api.v1.app import not_found
from flask import Flask, jsonify, abort, make_response, request
from models import storage
from models.user import *


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def all_users():
    """Returns list of users in a JSON representation"""
    db_list = storage.all(User)
    user_dict = [user.to_dict() for user in db_list.values()]

    return jsonify(user_dict)


@app_views.route('/users/<string:user_id>', methods=['GET'], strict_slashes=False)
def fetch_user(user_id):
    """Returs JSON representation of user with given ID"""
    if not user_id:
        abort(404)
    else:
        db_list = storage.all(User)
        user_dict = [user.to_dict() for user in db_list.values()]
        for user in user_dict:
            if (user_id == user.get('id')):
                return (jsonify(user))
    return (make_response(jsonify({"error": "not found"}), 404))


@app_views.route('/users/<string:user_id>', methods=['DELETE'], strict_slashes=False)
def del_user(user_id):
    """Returs JSON representation of user with given ID"""
    if storage.get(User, user_id) is None or not user_id:
        abort(404)
    else:
        user_delete = storage.get(User, user_id)
        storage.delete(user_delete)
        storage.save()
        return (jsonify({}))


@app_views.route('/users/', methods=['POST'], strict_slashes=False)
def create_user():
    """Returs JSON representation of user with given ID"""
    try:
        kwargs = request.get_json()
        attrs = ["email", "password"]

        for attribute in attrs:
            if kwargs.get(attribute) is None:
                return 'Missing {}'.format(attribute), 400

        user = User(**kwargs)
        user.save()
        return make_response(jsonify(user.to_dict()), 201)
    except TypeError:
        return "Not a JSON", 400


@app_views.route('/users/<string:user_id>', methods=['PUT'], strict_slashes=False)
def edit_user(user_id):
    """Returs JSON representation of user with given ID"""
    list_keys = ["email", "id", "created_at", "updated_at"]

    try:
        kwargs = request.get_json()
        user_old = storage.get(User, user_id)

        for key, value in kwargs.items():
            if key not in list_keys:
                setattr(user_old, key, value)

        user_old.save()
        return jsonify(user_old.to_dict()), 200
    except ValueError:
        return "Not a JSON", 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', debug=True)
