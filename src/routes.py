import datetime
import json
import os
import re
import sys

from collections import defaultdict
from pymongo import MongoClient

# from bson import ObjectId
from flask import Flask, request, redirect, render_template
from werkzeug.datastructures import ImmutableMultiDict
from werkzeug.wrappers import Response

app = Flask(__name__)
client = MongoClient('mongo', 27017)
db = client.data


class FormatException(Exception):
    pass


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


def format_happiness_data(raw_data):
    '''
    raw happiness data {'happy-level': ['3'], 'happy-reason': ['other'], 'other-happy': ['gloubi'], 'unhappy-reason': ['projects'], 'other-unhappy': [''], 'date': ['2018-09-20']}
    '''
    # TODO these should be put in a common file and the html template should take from the same source
    scores_whitelist = ['1', '2', '3', '4', '5']
    reasons_whitelist = ["ff", "work", "projects", "learning", "entertainment", "other"]

    formatted_data = dict()

    # score
    score = raw_data.get("happy-level", [])
    if len(score) != 1 or score[0] not in scores_whitelist:
        raise FormatException("happy-level is not well formatted")
    formatted_data["level"] = int(score[0])

    # reasons
    for reason_type in ["happy", "unhappy"]:
        reasons = raw_data.get("%s-reason" % reason_type, [])
        if len(reasons) != 1 or reasons[0] not in reasons_whitelist:
            raise FormatException("%s-reason: unknown reason" % reason_type)
        formatted_data["%s_reason" % reason_type] = reasons[0]

        if reasons[0] == "other":
            details = raw_data.get("other-%s" % reason_type, [''])[0]  # meh
            formatted_data["%s_reason_detail" % reason_type] = re.sub(r'[\W_]+', ' ', details) 

    return formatted_data


def format_dozen_data(raw_data):
    return {}


with app.app_context():

    @app.route('/', methods=["GET"])
    def hello():
        return create_response(message="Hello i'm working")


    @app.route('/day', methods=["GET"])
    def index():
        '''
        serving index
        '''
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        return redirect("/%s" % today, code=302)


    @app.route('/day/<date>', methods=["GET"])
    def get_summary(date):
        '''
        serving index for the day
        '''
        datetime_object = datetime.datetime.strptime(date, '%Y-%m-%d')
        if datetime_object > datetime.datetime.now():
            return create_response(error=True, message=str("can't see in the future!"), status_code=400)

        # check for existing data
        data = {}
        stored_day = db.monitoring_days.find_one({"date": date})
        if stored_day:
            data = stored_day.get("happiness_data", {})

        return render_template('index.html', date=date, data=data)    


    @app.route('/insert/happiness', methods=["POST"])
    def happiness_check():
        '''
        process hapiness data
        the monitoring_days collection has a unique index on date
        '''
        content = request.form.to_dict(flat=False)
        print("raw happiness data %s" % str(content), file=sys.stderr)

        if not re.match(r'[0-9]{4}-[0-9]{2}-[0-9]{2}', content["date"][0]):  # TODO valid date
            return create_response(error=True, message="date %s doesn't match a date!" % content["date"][0], status_code=400)

        try:
            happiness_data = format_happiness_data(content)
            print("formatted happiness data %s" % str(happiness_data), file=sys.stderr)
            db.monitoring_days.update_one({"date": content["date"][0]}, {"$set": {"happiness_data": happiness_data}}, upsert=True)
        except FormatException as e:
            return create_response(error=True, message=str(e), status_code=400)

        return create_response()


    @app.route('/insert/dozen', methods=["POST"])
    def dozen_check():
        '''
        process daily dozen data
        '''
        content = request.form.to_dict(flat=False)
        print("Dozen content %s" % str(content))

        dozen_data = format_dozen_data(content)
        db.monitoring_days.update_one({"date": content["date"]}, {"$set": {"dozen_data": dozen_data}}, upsert=True)

        return create_response()

