#-*- coding: utf-8 -*-
from flask import request, redirect, url_for, send_from_directory
from app import app, db
import traceback
import json
import random
from tools import *
import os
from werkzeug import secure_filename
import datetime

activitydb = db.activity
applydb = db.apply
userdb = db.user

UPLOAD_FOLDER='applications'
ALLOWED_EXTENSIONS = set(['zip', 'rar', 'gz'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
	return '.' in filename and \
		filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def activity_available(activity):
	return True
'''
@app.route('/getapplylist', methods=['POST'])
def getapplylist():
	jsondata = request.form
	data = immutabledict2dict(jsondata)
	result = {'success' :0}
	print data
	try:
		tmp = userdb.find_one({'username': data['username']})
		if tmp['token'] != data['token']:
			result['message'] = u'请先登录'
			return json.dumps(result)
		activitylist = []
		tmp = applydb.find({'username':data['username']})
		for i in tmp:
			tmpac = activitydb.find_one({'title': i['title']})
			if activity_available(tmpac):
				new = {}
				new['status'] = i['status']
				new['title'] = i['title']
				new['newsdetail'] = tmpac['newsdetail'] 
				new['end'] = str(tmpac['end'])
				activitylist.append(new)
		result['applylist'] = activitylist
		result['success'] = 1
		return json.dumps(result)
	except:
		traceback.print_exc()
		result['message'] = u'后台错误'
		return json.dumps(result)

def getactivity():
	try:
		activitylist = []
		tmp = activitydb.find()
		for i in tmp:
			if activity_available(i):
				new = {}
				new['title'] = i['title']
				new['start'] = str(i['start'])
				new['end'] = str(i['end'])
				new['newsdetail'] = i['newsdetail']
				activitylist.append(new)
		return activitylist
	except:
		traceback.print_exc()
		return []
'''
@app.route('/cancel', methods=['POST'])
def cancel():
	jsondata = request.form
	data = immutabledict2dict(jsondata)
	result = {'success' :0}
	try:
		tmp = userdb.find_one({'username': data['username']})
		if tmp['token'] != data['token']:
			result['message'] = u'请先登录'
			return json.dumps(result)
		if tmp['applied']:
			userdb.update({'username': data['username']},{'$set':{
				'applied' : False,
				'applydate' : '',
				'lastmodify' : '',
				'filename' : ''
				}})
		else:
			result['message'] = u'尚未申请'
			return json.dumps(result)
	except:
		traceback.print_exc()
		result['message'] = u'后台错误'
		return json.dumps(result)
	result['success'] = 1
	return json.dumps(result)

@app.route('/upload', methods=['POST'])
def upload():
	jsondata = request.form
	data = immutabledict2dict(jsondata)
	result = {'success' :0}
	try:
		a = 1
	except:
		traceback.print_exc()
		result['message'] = u'后台错误'
		return json.dumps(result)
	return json.dumps(result)

@app.route('/submit', methods=['GET', 'POST'])
def submit():
	jsondata = request.form
	data = immutabledict2dict(jsondata)
	result = {'success' :0}
	try:
		applydata = {}
		#validate the availability of user and activity
		tmp = userdb.find_one({'username': data['username']})
		if tmp['token'] != data['token']:
			result['message'] = u'请先登录'
			return result['message']
		if tmp.has_key('applied'):
			if tmp['applied']:
				result['message'] = u'已经申请过了<br><a href="/mainpage">返回首页</a>'
				return result['message']
		'''
		tmpap = applydb.find_one({'title': data['title'],'username':data['username']})
		if tmpap:
			result['message'] = u'已经申请过了'

			return result['message']
		tmpac = activitydb.find_one({'title': data['title']})
		'''
		if True:#activity_available(tmpac):
			#save material
			file = request.files['file']
			if file and allowed_file(file.filename):
				'''
				filename = secure_filename(file.filename)
				print filename, file.filename
				if filename != file.filename:
					result['message'] = u'文件名不符合要求'
					return result['message']
				'''
				filename = tmp['identity']+os.path.splitext(file.filename)[1]
				directory=os.path.join(app.config['UPLOAD_FOLDER'], data['username'])
				try:
					os.makedirs(directory)
				except:
					a = 1
				file.save(os.path.join(app.config['UPLOAD_FOLDER'], data['username'],filename))
				applydata['filename'] = filename
			else:
				result['message'] = u'上传文件失败，请检查文件类型是否满足要求'
				return result['message']

			#save to db
			'''
			applydata['username'] = data['username']
			applydata['title'] = data['title']
			applydata['status'] = u'等待处理'
			apply_id = applydb.insert_one(applydata).inserted_id
			'''
			userdb.update({'username': data['username']},{'$set':{
				'applied' : True,
				'applydate' : datetime.datetime.utcnow(),
				'lastmodify' : datetime.datetime.utcnow(),
				'filename' : filename 
				}})

			result['success'] = 1
			return u'申请成功！<br><a href="/mainpage">返回首页</a>'
	except:
		traceback.print_exc()
		result['message'] = u'后台错误'
		return result['message']
	return result['message']

@app.route('/applymodifysubmit', methods=['GET', 'POST'])
def applymodifysubmit():
	jsondata = request.form
	data = immutabledict2dict(jsondata)
	result = {'success' :0}
	try:
		applydata = {}
		#validate the availability of user and activity
		tmp = userdb.find_one({'username': data['username']})
		if tmp['token'] != data['token']:
			result['message'] = u'请先登录'
			return result['message']
		if not tmp['applied']:
			result['message'] = u'尚未申请'
			return result['message']
		#tmpac = activitydb.find_one({'title': data['title']})
		if True:#activity_available(tmpac):
			#save material
			file = request.files['file']
			if file and allowed_file(file.filename):
				'''
				filename = secure_filename(file.filename)
				print filename, file.filename
				if filename != file.filename:
					result['message'] = u'文件名不符合要求'
					return result['message']
				'''
				filename = tmp['identity']+os.path.splitext(file.filename)[1]
				directory=os.path.join(app.config['UPLOAD_FOLDER'], data['username'])
				try:
					os.makedirs(directory)
				except:
					a = 1
				file.save(os.path.join(app.config['UPLOAD_FOLDER'], data['username'],filename))
				applydata['filename'] = filename
			else:
				result['message'] = u'上传文件失败，请检查文件类型是否满足要求'
				return result['message']

			#save to db
			'''
			applydata['username'] = data['username']
			apply_id = applydb.update_one({'username': applydata['username']}, {'$set':{'filename' : applydata['filename']}})
			os.remove(os.path.join(app.config['UPLOAD_FOLDER'], data['title'], data['username'],tmpap['filename']))
			'''
			os.remove(os.path.join(app.config['UPLOAD_FOLDER'], data['username'],tmp['filename']))
			userdb.update({'username': data['username']},{'$set':{
				'lastmodify' : datetime.datetime.utcnow(),
				'filename' : filename 
				}})

			result['success'] = 1
			return u'修改成功！<br><a href="/mainpage">返回首页</a>'
	except:
		traceback.print_exc()
		result['message'] = u'后台错误'
		return result['message']
	return result['message']

@app.route('/getapplymaterial/<jsondata>', methods=['GET','POST'])
def getapplymaterial(jsondata):
	data = json.loads(jsondata)
	result = {'success' :0}
	try:
		tmp = userdb.find_one({'username': data['username']})
		if tmp['token'] != data['token']:
			result['message'] = u'请先登录'
			return json.dumps(result)
		if not tmp['applied']:
			result['message'] = u'尚未申请'
			return result['message']
		directory=os.path.join('applications',data['username'])
		result['success'] = 1
		return send_from_directory(directory=directory,filename=tmp['filename'], as_attachment=True)
	except:
		traceback.print_exc()
		result['message'] = u'后台错误'
		return json.dumps(result)