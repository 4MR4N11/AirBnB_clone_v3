#!/usr/bin/python3
"""flask blueprint module"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route("/status")
def status():
    """returns a json object of status"""
    return jsonify({"status": "OK"})


@app_views.route("/stats")
def stats():
    """returns a json object containing the count of all classes"""
    classes = {"Amenity": "amenities", "City": "cities", "Place": "places",
               "Review": "reviews", "State": "states", "User": "users"}
    dic = {}
    for key, value in classes.items():
        dic[value] = storage.count(key)
    return jsonify(dic)
