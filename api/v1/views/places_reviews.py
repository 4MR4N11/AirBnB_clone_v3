#!/usr/bin/python3
"""Place Reviews view module"""
from flask import Flask, request, jsonify, abort
from api.v1.views import app_views
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route('places/<place_id>/reviews', methods=['GET', 'POST'],
                 strict_slashes=False)
def getPlaceReviews(place_id):
    """
    Retrieves the list of all Review objects of a Place
    or creates a new Review object
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    if request.method == 'GET':
        reviews = place.reviews
        reviews_dicts = list(map(lambda x: x.to_dict(), reviews))
        return jsonify(reviews_dicts)

    if request.method == 'POST':
        body = request.get_json()
        if body is None:
            abort(400, {'Not a JSON'})

        if 'user_id' not in body:
            abort(400, {'Missing user_id'})
        if 'text' not in body:
            abort(400, {'Missing text'})

        if storage.get(User, body['user_id']) is None:
            abort(404)

        body['place_id'] = place_id
        newReview = Review(**body)
        storage.new(newReview)
        storage.save()
        return jsonify(newReview.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def getReviewById(review_id):
    """
    Retrieves a Review object by id,
    deletes a Review object by id,
    or update a Review object by id
    """
    review = storage.get(Review, review_id)
    if (review):
        if request.method == 'GET':
            return jsonify(review.to_dict())

        if request.method == 'DELETE':
            storage.delete(review)
            storage.save()
            return jsonify({}), 200

        if request.method == 'PUT':
            body = request.get_json()
            if body is None:
                abort(400, {'Not a JSON'})
            ignored = ["id", "created_at", "updated_at", "user_id", "place_id"]
            for key, value in body.items():
                if key not in ignored:
                    setattr(review, key, value)
            storage.save()
            return jsonify(review.to_dict()), 200
    abort(404)
