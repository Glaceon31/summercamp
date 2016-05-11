#-*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, url_for
from werkzeug import secure_filename

app = Flask(__name__)
app.debug = True

import pymongo
import traceback
from pymongo import MongoClient

client = MongoClient(connect=False)

db = client.thusummercamp

@app.route('/')
@app.route('/entrance')
def entrance():
	return render_template('entrance.html')

@app.route('/register')
def register():
	return render_template('register.html')

@app.route('/login')
def login():
	return render_template('login.html')

@app.route('/mainpage')
def mainpage():
	newslist = getnews(0,3)
	activitylist = getactivity()
	return render_template('mainpage.html', newslist = newslist, activitylist = activitylist)

@app.route('/apply')
def apply():
	activitylist = getactivity()
	return render_template('apply.html', activitylist = activitylist)

@app.route('/applymodify')
def applymodify():
	return render_template('applymodify.html')

@app.route('/activity')
def activity():
	#appliedlist = get
	activitylist = getactivity()
	print activitylist
	return render_template('activity.html', activitylist = activitylist)

@app.route('/newsdetail/<newsname>')
def newsdetail(newsname):
	return render_template('news/'+newsname)

@app.route('/news')
def news():
	newslist = getnews(0,10)
	return render_template('news.html', newslist = newslist)

@app.route('/news/<page>')
def newspage(page):
	newslist = getnews(10*page,10*(page+1))
	return render_template('news.html', newslist = newslist)

@app.route('/account')
def account():
	return render_template('account.html')

@app.route('/fonts/<path>')
def fonts(path):
	return redirect('/static/fonts/'+path)

'''
@app.route('/adminloginpage')
def adminloginpage():
	return render_template('adminlogin.html')

@app.route('/adminnews')
def adminnews():
	return render_template('adminnews.html')

@app.route('/adminactivity')
def adminactivity():
	return render_template('adminactivity.html')
'''

from user import *
from news import *
from admin import *
from activity import *

if __name__ == '__main__':
    app.run('0.0.0.0', port = 7654)