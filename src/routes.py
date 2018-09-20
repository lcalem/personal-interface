import datetime
import json
import os

from collections import defaultdict

# from bson import ObjectId
from flask import Flask, request
from jinja2 import PackageLoader, Environment, select_autoescape
from werkzeug.wrappers import Response

app = Flask(__name__)
env = Environment(
    loader=PackageLoader('src', 'templates'),
    autoescape=select_autoescape(['html', 'xml'])
)


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
        template = env.get_template('index.html')
        return template.render(date=datetime.datetime.now().strftime("%Y-%m-%d"))

    @app.route('/insert/happiness', methods=["POST"])
    def happiness_check():
        '''
        process hapiness data
        '''
        pass

