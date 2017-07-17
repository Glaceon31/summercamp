#-*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug import secure_filename
import json
import os
import datetime

app = Flask(__name__)
app.debug = True

import pymongo
import traceback
from pymongo import MongoClient

client = MongoClient(connect=False)

db = client.thusummercamp2017
userdb = db.user

@app.route('/viewdata')
def viewdata():
	return render_template('dataviewer.html')

@app.route('/getviewdata')
def getviewdata():
	result = []
	tmp = userdb.find({'applied':True})
	for i in tmp:
		user = {}
		user['username'] = i['username']
		user['name'] = i['name']
		user['college'] = i['college']
		user['identity'] = i['identity']
		user['email'] = i['email']
		user['mobile'] = i['mobile']
		user['department'] = i['department']
		user['lastmodify'] = str(i['lastmodify']+datetime.timedelta(hours=8))[0:19]
		result.append(user)
	return json.dumps(result)

@app.route('/getmaterial/<username>', methods=['GET','POST'])
def getmaterial(username):
	tmp = userdb.find_one({'username': username})
	directory=os.path.join('applications',username)
	return send_from_directory(directory=directory,filename=tmp['filename'], as_attachment=True)

if __name__ == '__main__':
    app.run('0.0.0.0', port = 8552)
