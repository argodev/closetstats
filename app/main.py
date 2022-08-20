#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, Response, request, render_template, send_from_directory, jsonify
import os
import json
import datetime
import pymongo
import dateutil.parser
import logging
import sys

# should get these from the environment?
WEB_HOST = '0.0.0.0'
WEB_PORT = 8083
WEB_DEBUG = True

app = Flask(__name__)

# get password from environment variables
db_name = 'closet_stats'
db_url = os.getenv('CSTATS_DATABASE_SERVER', 'example.com')
db_user = os.getenv('CSTATS_DATABASE_USER', 'user')
db_pass = os.getenv('CSTATS_DATABASE_PWD', 'pass')


@app.route('/api/visit', methods=["POST"])
def postData():
    logging.debug("In method bubba")
    print ("hello complicated world!")
    sys.stdout.flush()
    if request.method == "POST":
        try:
            json_dict = request.get_json()
            if 'timestamp' not in json_dict:
                json_dict['timestamp'] = datetime.datetime.now()
            else:
                # take the string timestamp and convert to proper type
                json_dict['timestamp'] = dateutil.parser.parse(json_dict['timestamp'])

            # we need to adapt some of the data so it is in the proper type
            if 'numKidsServed' in json_dict and json_dict['numKidsServed']:
                json_dict['numKidsServed'] = int(json_dict['numKidsServed'])
            else:
                json_dict['numKidsServed'] = 0

            if 'numGirlsServed' in json_dict and json_dict['numGirlsServed']:
                json_dict['numGirlsServed'] = int(json_dict['numGirlsServed'])
            else:
                json_dict['numGirlsServed'] = 0

            if 'numBoysServed' in json_dict and json_dict['numBoysServed']:
                json_dict['numBoysServed'] = int(json_dict['numBoysServed'])
            else:
                json_dict['numBoysServed'] = 0

            print(json_dict)
            sys.stdout.flush()
            # we don't have a high volume, so we open/close on each request
            myclient = pymongo.MongoClient("mongodb+srv://%s:%s@%s/%s?retryWrites=true&w=majority" % (db_user, db_pass, db_url, db_name))
            mydb = myclient[db_name]
            mycol = mydb["visits"]
            mycol.insert_one(json_dict)
            myclient.close()
            print("done")
            sys.stdout.flush()
            return {'status': 'ok'}, 201
        except Exception as e:
            print(e)
            sys.stdout.flush()
            return json.dumps({"error": "Unexpected Error"}), 500
    else:
        return json.dumps({"error": "wrong request type"}), 500


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Compassion Closet Checkin')


if __name__ == '__main__':
    #flaskapp.run(debug=True)
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

    app.logger.addHandler(logging.StreamHandler(sys.stdout))
    app.logger.setLevel(logging.debug)

    app.run(host=WEB_HOST, port=WEB_PORT, debug=WEB_DEBUG)

