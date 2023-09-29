#!/usr/bin/python3
"""Cities view module"""
from flask import Flask, request, jsonify, abort
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET', 'POST'],
                 strict_slashes=False)
def getCitiesOfState(state_id):
    """
    Retrieves the list of all Cities in a State
    or create a new City object
    """
    if request.method == 'GET':
        state = storage.get(State, state_id)
        cities = state.cities
        cities_dicts = list(map(lambda x: x.to_dict(), cities))
        return jsonify(cities_dicts)
    if request.method == 'POST':
        body = request.get_json()
        if body is None:
            abort(400, {'Not a JSON'})
        if 'name' not in body:
            abort(400, {'Missing name'})
        if state_id not in list(map(lambda x: x.id,
                                    storage.all(State).values())):
            abort(404)

        newCity = City(name=body['name'], state_id=state_id)
        storage.new(newCity)
        storage.save()
        return jsonify(newCity.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def getCityById(city_id):
    """
    Retrieves a Cityobject by id,
    delete a State object by id,
    or update a State object by id
    """
    city = storage.get(City, city_id)
    if (city):
        if request.method == 'GET':
            return jsonify(city.to_dict())
        if request.method == 'DELETE':
            storage.delete(city)
            storage.save()
            return jsonify({}), 200
        if request.method == 'PUT':
            body = request.get_json()
            if body is None:
                abort(400, {'Not a JSON'})
            ignored = ["id", "created_at", "updated_at"]
            for key, value in body.items():
                if key not in ignored:
                    setattr(city, key, value)
            storage.save()
            return jsonify(city.to_dict()), 200
    abort(404)
