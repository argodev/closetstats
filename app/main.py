#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, Response, request, render_template, send_from_directory, jsonify
import os
import json
import datetime
import pymongo

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
mongo_conn_str = os.getenv('MONGODB_URI', 'notset')

@app.route('/api/visit', methods=["POST"])
def stripeTest():
    if request.method == "POST":
        try:
            json_dict = request.get_json()
            if 'timestamp' not in json_dict:
                json_dict['timestamp'] = datetime.datetime.now()

            # we don't have a high volume, so we open/close on each request
            myclient = pymongo.MongoClient("mongodb+srv://%s:%s@%s/%s?retryWrites=true&w=majority" % (db_user, db_pass, db_url, db_name))
            #myclient = pymongo.MongoClient(mongo_conn_str)
            mydb = myclient["closet_stats"]
            mycol = mydb["visits"]
            mycol.insert_one(json_dict)
            myclient.close()
            return {'status': 'ok'}, 201
        except:
            return json.dumps({ "error": "Unexpected Error" }), 500
    else:
        return json.dumps({ "error": "wrong request type" }), 500


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Compassion Closet Checkin')

if __name__ == '__main__':
    app.run(host=WEB_HOST, port=WEB_PORT, debug=WEB_DEBUG)
