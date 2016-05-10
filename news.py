#-*- coding: utf-8 -*-
from flask import request
from app import app, db
import traceback
import json
import random
from tools import *

newsdb = db.news


def getnews(start, end):
	try:
		newslist = []
		tmp = newsdb.find()
		for i in tmp:
			new = {}
			new['date'] = str(i['date'])
			new['title'] = i['title']
			new['newsdetail'] = i['newsdetail']
			newslist.append(new)
		newslist = newslist[::-1]
		print newslist
		if start >= len(newslist):
			return []
		if end > len(newslist):
			end = len(newslist)
		return newslist[start:end]
	except:
		traceback.print_exc()
		return []

