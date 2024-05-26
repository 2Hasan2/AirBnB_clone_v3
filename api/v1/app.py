#!/usr/bin/python3
"""
API Module
"""

from flask import Flask, render_template, abort, make_response, jsonify
from models import *
from models import storage
from api.v1.views import app_views
app = Flask(__name__)
app.register_blueprint(app_views)


@app.errorhandler(404)
def not_found(error):
    """Handling 404 Not Found error"""
    not_found = {"error": "Not Found"}
    return make_response(jsonify(not_found), 404)


@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage on teardown"""
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', threaded=True, debug=True)
