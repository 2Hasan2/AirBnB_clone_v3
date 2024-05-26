#!/usr/bin/python3
""" places_reviews API"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.review import Review


@app_views.route(
        '/places/<place_id>/reviews', methods=['GET'],
        strict_slashes=False)
def reviews(place_id):
    """Retrieves the list of all Review objects"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    reviews = storage.all(Review)
    reviews = [
        review.to_dict() for review in reviews.values()
        if review.place_id == place_id
    ]
    return jsonify(reviews), 200


@app_views.route(
        '/reviews/<review_id>',
        methods=['GET'], strict_slashes=False)
def review_id(review_id):
    """Retrieves a Review object"""
    review = storage.get(Review, review_id)
    if not review:
        return abort(404)
    return jsonify(review.to_dict()), 200


@app_views.route(
        '/reviews/<review_id>',
        methods=['DELETE'], strict_slashes=False)
def delete_review(review_id):
    """Deletes a Review object"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route(
        '/places/<place_id>/reviews',
        methods=['POST'], strict_slashes=False)
def post_review(place_id):
    """Creates a Review"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'user_id' not in request.get_json():
        abort(400, description="Missing user_id")
    if 'text' not in request.get_json():
        abort(400, description="Missing text")
    data = request.get_json()
    user_id = data.get('user_id')
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    data['place_id'] = place_id
    instance = Review(**data)
    instance.save()
    return jsonify(instance.to_dict()), 201


@app_views.route(
        '/reviews/<review_id>',
        methods=['PUT'], strict_slashes=False)
def put_review(review_id):
    """Updates a Review object"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    data = request.get_json()
    for key, value in data.items():
        if key not in [
                'id', 'user_id', 'place_id', 'created_at', 'updated_at']:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict()), 200
