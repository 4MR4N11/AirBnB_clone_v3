#!/usr/bin/python3
"""Users view module"""
from flask import Flask, request, jsonify, abort
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET', 'POST'],
                 strict_slashes=False)
def getUsers():
    """
    Retrieves the list of all Users
    or create a new User object
    """
    if request.method == 'GET':
        users = list(map(lambda x: x.to_dict(), storage.all(User).values()))
        return jsonify(users)

    if request.method == 'POST':
        body = request.get_json()
        if body is None:
            abort(400, {'Not a JSON'})
        if 'email' not in body:
            abort(400, {'Missing email'})
        if 'password' not in body:
            abort(400, {'Missing password'})

        newUser = User(**body)
        storage.new(newUser)
        storage.save()
        return jsonify(newUser.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def getUserById(user_id):
    """
    Retrieves a User object by id,
    deletes a User object by id,
    or update a User object by id
    """
    user = storage.get(User, user_id)
    if (user):
        if request.method == 'GET':
            return jsonify(user.to_dict())

        if request.method == 'DELETE':
            storage.delete(user)
            storage.save()
            return jsonify({}), 200

        if request.method == 'PUT':
            body = request.get_json()
            if body is None:
                abort(400, {'Not a JSON'})
            ignored = ["id", "created_at", "updated_at", "email"]
            for key, value in body.items():
                if key not in ignored:
                    setattr(user, key, value)
            storage.save()
            return jsonify(user.to_dict()), 200
    abort(404)
