#!/usr/bin/python3
"""
starts a Flask web application
"""
from api.v1.views import app_views
from flask import Flask, jsonify, abort, make_response, request
from models import storage
from models.city import *
from models.state import *
from models.place import *
from models.user import *
from models.review import *


@app_views.route('/places/<string:place_id>/reviews', methods=['GET'], strict_slashes=False)
def all_reviews(place_id):
    """Returns list of reviews in a JSON representation"""
    if storage.get(Place, place_id) is None:
        abort(404)

    reviews = [review.to_dict() for review in storage.get(Place, place_id).reviews]
    return jsonify(reviews)


@app_views.route('reviews/<string:review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """Returs JSON representation of review with given ID"""
    if storage.get(Review, review_id) is None or not review_id:
        abort(404)
    else:
        db_list = storage.all(Review)
        review_dict = [review.to_dict() for review in db_list.values()]
        for review in review_dict:
            if (review_id == review.get('id')):
                return (jsonify(review))
    return (make_response(jsonify({"error": "not found"}), 404))


@app_views.route('/reviews/<string:review_id>', methods=['DELETE'], strict_slashes=False)
def del_review(review_id):
    """Returs JSON representation of review with given ID"""
    if not review_id or storage.get(Review, review_id) is None:
        abort(404)
    else:
        review_delete = storage.get(Review, review_id)
        storage.delete(review_delete)
        storage.save()
        return jsonify({}), 200


@app_views.route('/places/<string:place_id>/reviews', methods=['POST'], strict_slashes=False)
def create_review(place_id):
    """Returs JSON representation of review with given ID"""
    try:
        kwargs = request.get_json()
        kwargs['place_id'] = place_id

        dict_id = {kwargs.get("user_id"): User, place_id: Place}
        for key, value in dict_id.items():
            if storage.get(value, key) is None:
                abort(404)

        list_keys = ["user_id", "text"]
        for key in list_keys:
            if not kwargs.get(key):
                return 'Missing {}'.format(key), 400

        review = Review(**kwargs)
        review.save()
        return jsonify(review.to_dict()), 201
    except TypeError:
        return "Not a JSON", 400


@app_views.route('/reviews/<string:review_id>', methods=['PUT'], strict_slashes=False)
def edit_review(review_id):
    """Returs JSON representation of review with given ID"""
    if storage.get(Review, review_id) is None:
        abort(404)
    list_keys = ["user_id", "place_id", "id", "created_at", "updated_at"]

    try:
        kwargs = request.get_json()
        review_old = storage.get(Review, review_id)

        for key, value in kwargs.items():
            if key not in list_keys:
                setattr(review_old, key, value)

        review_old.save()
        return jsonify(review_old.to_dict()), 200
    except ValueError:
        return "Not a JSON", 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', debug=True)
