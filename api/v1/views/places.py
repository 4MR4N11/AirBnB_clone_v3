#!/usr/bin/python3
"""Places view module"""
from flask import Flask, request, jsonify, abort
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET', 'POST'],
                 strict_slashes=False)
def getPlacesOfCity(city_id):
    """
    Retrieves the list of all Places in a City
    or create a new Place object.
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if request.method == 'GET':
        places = city.places
        places_dicts = list(map(lambda x: x.to_dict(), places))
        return jsonify(places_dicts)
    if request.method == 'POST':
        body = request.get_json()
        if body is None:
            abort(400, {'Not a JSON'})
        if 'user_id' not in body:
            abort(400, {'Missing user_id'})
        if 'name' not in body:
            abort(400, {'Missing name'})

        user = storage.get(User, body['user_id'])
        if user is None:
            abort(404)

        newPlace = Place(name=body['name'], user_id=body['user_id'],
                         city_id=city_id)
        storage.new(newPlace)
        storage.save()
        return jsonify(newPlace.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def getPlaceById(place_id):
    """
    Retrieves a Place object by id,
    delete a Place object by id,
    or update a Place object by id
    """
    place = storage.get(Place, place_id)
    if (place):
        if request.method == 'GET':
            return jsonify(place.to_dict())
        if request.method == 'DELETE':
            storage.delete(place)
            storage.save()
            return jsonify({}), 200
        if request.method == 'PUT':
            body = request.get_json()
            if body is None:
                abort(400, {'Not a JSON'})
            ignored = ["id", "created_at", "updated_at", "user_id", "city_id"]
            for key, value in body.items():
                if key not in ignored:
                    setattr(place, key, value)
            storage.save()
            return jsonify(place.to_dict()), 200
    abort(404)
