import json

from collections import defaultdict

# from bson import ObjectId
from flask import Flask, request
from werkzeug.wrappers import Response

app = Flask(__name__)


def create_response(error=False, message="", status_code=200, extra_response=None):
    response = {
        "error": error,
        "message": message
    }
    if extra_response:
        response.update(extra_response)

    r = Response(json.dumps(response), mimetype='application/json')
    r.status_code = status_code

    return r


with app.app_context():

    @app.route('/', methods=["GET"])
    def check():
        '''
        serving index
        '''
        return create_response(message="[data gathering] Hello i'm working. GIVE ME DATA")
