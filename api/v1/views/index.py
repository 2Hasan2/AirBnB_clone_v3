#!/usr/bin/python3
"""
starts a Flask web application
"""
from flask import Flask, jsonify
from api.v1.views import app_views


@app_views.route('/status', strict_slashes=False)
def status():
    """returns Hello HBNB!"""
    status_dict = {"status": "OK"}
    return jsonify(**status_dict)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
