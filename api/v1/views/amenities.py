#!/usr/bin/python3
"""amenities view module"""
from flask import Flask, request, jsonify, abort
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET', 'POST'], strict_slashes=False)
def getAmenities():
    """
    Retrieves the list of all Amenity objects
    or create a new Amenity object
    """
    if request.method == 'GET':
        amenities = storage.all(Amenity)
        amenities_dicts = list(map(lambda x: x.to_dict(), amenities.values()))
        return jsonify(amenities_dicts)
    if request.method == 'POST':
        body = request.get_json()
        if body is None:
            abort(400, {'Not a JSON'})
        if 'name' not in body:
            abort(400, {'Missing name'})
        newAmenity = Amenity(name=body['name'])
        storage.new(newAmenity)
        storage.save()
        return jsonify(newAmenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def getAmenityById(amenity_id):
    """
    Retrieves a Amenity object by id,
    delete a Amenity object by id,
    or update a Amenity object by id
    """
    amenity = storage.get(Amenity, amenity_id)
    if (amenity):
        if request.method == 'GET':
            return jsonify(amenity.to_dict())
        if request.method == 'DELETE':
            storage.delete(amenity)
            storage.save()
            return jsonify({}), 200
        if request.method == 'PUT':
            body = request.get_json()
            if body is None:
                abort(400, {'Not a JSON'})
            ignored = ["id", "created_at", "updated_at"]
            for key, value in body.items():
                if key not in ignored:
                    setattr(amenity, key, value)
            storage.save()
            return jsonify(amenity.to_dict()), 200
    abort(404)
