#!/usr/bin/python3
""" Flask Application """
from api.v1.views import app_views
from models import storage
from flask import Flask, abort, make_response, jsonify, request
from os import environ
from flask_cors import CORS


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
    return make_response(jsonify({'error': "Not found"}), 404)


# @app.before_request
# def before_request():
#     """ Before Request """
#     if request.content_type != 'application/json':
#         abort(400, 'Content-Type is not application/json')


if __name__ == "__main__":
    """ Main Function """
    PORT = environ.get('HBNB_API_PORT') or '0.0.0.0'
    HOST = environ.get('HBNB_API_HOST') or 5000
    app.run(host=HOST, port=PORT, threaded=True, debug=True)
