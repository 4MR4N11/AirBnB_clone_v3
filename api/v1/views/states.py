#!/usr/bin/python3
"""States view module"""
from flask import Flask, request, jsonify, abort
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET', 'POST'], strict_slashes=False)
def getStates():
    """ Retrieves the list of all State objects or create a new State object"""
    if request.method == 'GET':
        states = []
        for state in storage.all(State).values():
            states.append(state.to_dict())
        return jsonify(states)
    if request.method == 'POST':
        body = request.get_json()
        if body is None:
            abort(400, {'Not a JSON'})
        if 'name' not in body:
            abort(400, {'Missing name'})
        newState = State(name=body['name'])
        storage.new(newState)
        storage.save()
        return jsonify(newState.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def getStateById(state_id):
    """ Retrieves a State object by id, delete a State object by id,
    or update a State object by id """
    state = storage.get(State, state_id)
    if (state):
        if request.method == 'GET':
            return jsonify(state.to_dict())
        if request.method == 'DELETE':
            storage.delete(state)
            storage.save()
            return jsonify({}), 200
        if request.method == 'PUT':
            body = request.get_json()
            if body is None:
                abort(400, {'Not a JSON'})
            ignored = ["id", "created_at", "updated_at"]
            for key, value in body.items():
                if key not in ignored:
                    setattr(state, key, value)
            storage.save()
            return jsonify(state.to_dict()), 200
    abort(404)
