#!/usr/bin/python3
""" Users API """
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
        data.append(user.to_dict())
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
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'email' not in request.get_json():
        abort(400, description="Missing email")
    if 'password' not in request.get_json():
        abort(400, description="Missing password")
    data = request.get_json()
    instance = User(**data)
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
        abort(400, description="Not a JSON")
    data = request.get_json()
    for key, value in data.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict()), 200
