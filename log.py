#-*- coding: utf-8 -*-
import pymongo
import datetime
import traceback
from pymongo import MongoClient
import json
from app import db

logdb = db.log

'''
def log(url):
	logdata = {}
	logdata['url'] = url
	logdata['time'] = datetime.datetime.now()
	try:
		logdb.insert(logdata)
		return 1
	except:
		traceback.print_exc()
		return 0
'''
