import json
import os

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


def get_file(filename):
    try:
        root_dir = os.path.abspath(os.path.dirname(__file__))
        src_file = os.path.join(root_dir, filename)
        with open(src_file, "r") as f_in:
            return f_in.read()
    except IOError as exc:
        return str(exc)


with app.app_context():

    @app.route('/', methods=["GET"])
    def check():
        '''
        serving index
        '''
        content = get_file('index.html')
        return Response(content, mimetype="text/html")

