#!/usr/bin/python3
""" Flask Application """
from flask import Flask, make_response, jsonify, request, abort
from flask_cors import CORS
from api.v1.views import app_views
from models import storage
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def close_db(error):
    """ Close Storage """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """ Error 404 """
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    """ Main Function """
    HOST = getenv('HBNB_API_HOST') or '0.0.0.0'
    PORT = getenv('HBNB_API_PORT') or 5000
    app.run(host=HOST, port=PORT, threaded=True)
