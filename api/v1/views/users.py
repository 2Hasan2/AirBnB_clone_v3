#!/usr/bin/python3
""" this contains the views for users """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def users():
    """Retrieves the list of all User objects"""
    users = storage.all(User)
    data = []
    for user in users.values():
        user = user.to_dict()
        data.append(user)
    return jsonify(data)


@app_views.route(
        '/users/<user_id>',
        methods=['GET'], strict_slashes=False)
def user_id(user_id):
    """Retrieves a User object"""
    user = storage.get(User, user_id)
    if not user:
        return abort(404)
    return jsonify(user.to_dict())


@app_views.route(
        '/users/<user_id>',
        methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """Deletes a User object"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route(
        '/users',
        methods=['POST'], strict_slashes=False)
def post_user():
    """Creates a User"""
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    if 'email' not in data:
        abort(400, "Missing email")
    if 'password' not in data:
        abort(400, "Missing password")
    instance = User(**data)
    storage.new(instance)
    instance.save()
    return jsonify(instance.to_dict()), 201


@app_views.route(
        '/users/<user_id>',
        methods=['PUT'], strict_slashes=False)
def put_user(user_id):
    """Updates a User object"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    data = request.get_json()
    for key, value in data.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict()), 200
