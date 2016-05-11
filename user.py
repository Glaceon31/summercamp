#-*- coding: utf-8 -*-
from flask import request
from app import app, db
import traceback
import json
import random
from tools import *

userdb = db.user

userinfolist = ['username', 'name', 'email', 'college', 'department'\
                'identity', 'mobile', 'address', 'postcode']

@app.route('/userregister', methods=['POST'])
def userregister():
    jsondata = request.form
    data = immutabledict2dict(jsondata)
    result = {'success' :0}
    if len(data['username']) < 3:
        result['message'] = u'用户名过短'
        return json.dumps(result)
    #db
    try:
        #same username
        tmp = userdb.find_one({"username": data["username"]})
        if tmp:
            result['message'] = u'用户名已存在'
            return json.dumps(result)
        else:
            '''
            if not savelog(data['username'], 'register', ''):
                result['message'] = u'后台错误'
                return json.dumps(result)
            '''
            user_id = userdb.insert_one(dict(data)).inserted_id
            result['success'] = 1
            result['message'] = u'注册成功'
            return json.dumps(result)
    except:
        traceback.print_exc()
        result['message'] = u'后台错误'
        return json.dumps(result)

@app.route('/userlogin', methods=['POST'])
def userlogin():
    jsondata = request.form
    data = immutabledict2dict(jsondata)
    result = {'success': 0}
    #db
    try:
        tmp = userdb.find_one({"username": data["username"]})
        if not tmp:
            result['message'] = u'用户不存在'
            return json.dumps(result)
        else:
            if tmp['password'] == data['password']:
                tokenlength = random.randrange(16,32)
                token = ''
                for i in range(0, tokenlength):
                    token += random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
                result['success'] = 1
                result['userid'] = str(tmp['_id'])
                result['username'] = tmp['username']
                result['token'] = token
                userdb.update_one({'_id': tmp['_id']}, {'$set':{'token' : token}})
                return json.dumps(result)
            else:
                result['message'] = u'密码错误'
                return json.dumps(result)
    except:
        traceback.print_exc()
        result['message'] = u'后台错误'
        return json.dumps(result)

@app.route('/userchecklogin', methods=['POST'])
def userchecklogin():
    jsondata = request.form
    data = immutabledict2dict(jsondata)
    result = {'success': 0}
    #db
    try:
        tmp = userdb.find_one({'username': data['username']})
        if tmp['token'] == data['token']:
            result['success'] = 1
        return json.dumps(result)
    except:
        traceback.print_exc()
        return json.dumps(result)
    #
    return '1'

@app.route('/getuserinfo', methods=['POST'])
def getuserinfo():
    jsondata = request.form
    data = immutabledict2dict(jsondata)
    result = {'success': 0}
    try:
        tmp = userdb.find_one({'username': data['username']})
        if tmp['token'] != data['token']:
            result['message'] = u'请重新登录'
            return json.dumps(result)
        for i in userinfolist:
            if not tmp.has_key(i):
                tmp[i] = ''
            result[i] = tmp[i]
        result['success'] = 1
        return json.dumps(result)
    except:
        traceback.print_exc()
        return json.dumps(result)

@app.route('/userlogout', methods=['POST'])
def userlogout(jsondata):
    data = json.loads(jsondata)
    #db
    try:
        tmp = userdb.find_one({'username': data['username']})
        if tmp['token'] == data['token']:
            if not savelog(data['username'], 'logout', data['token']):
                return u'后台错误'
            userdb.update_one({'username': data['username']}, {'$set':{'token' : ''}})
    except:
        traceback.print_exc()
        return '0'
    #
    return '1'

@app.route('/usergetinfo', methods=['POST'])
def getinfo(jsondata):
    data = json.loads(jsondata)
    result = {}
    try:
        a = 1
    except:
        print 'dberror'
        return 0
    #
    if data['token'] != token:
        return 0
    result = ''
    return result

@app.route('/usermodify', methods=['POST'])
def modify(jsondata):
    data = json.loads(jsondata)
    result = {'success': 0 }
    #db
    try:
        tmp = userdb.find_one({'username': data['username']})
    except:
        traceback.print_exc()
        result['message'] = u'后台错误'
        return json.dumps(result)
    #
    if data['token'] != tmp['token']:
        result['message'] = u'登录已失效，请重新登录'
        return json.dumps(result)
    else:
        try:
            if not savelog(data['username'], 'modify', data['token'], message=data['name']):
                return u'后台错误'
            userdb.update_one({'username': data['username']}, {'$set':{'name' : data['name']}})
        except:
            traceback.print_exc()
            result['message'] = u'后台错误'
            return json.dumps(result)
        result['message'] = u'修改成功'
        result['success'] = 1
        return json.dumps(result)

@app.route('/usermodifypassword', methods=['POST'])
def modifypassword(jsondata):
    data = json.loads(jsondata)
    result = {'success':0}
    #db
    try:
        tmp = userdb.find_one({'username': data['username']})
    except:
        traceback.print_exc()
        result['message'] = u'后台错误'
        return json.dumps(result)
    #
    if data['token'] != tmp['token']:
        result['message'] = u'登录已失效，请重新登录'
        return json.dumps(result)
    elif data['oldpass'] != tmp['password']:
        result['message'] = u'原密码错误'
        return json.dumps(result)
    else:
        try:
            if not savelog(data['username'], 'modifypassword', data['token']):
                return u'后台错误'
            userdb.update_one({'username': data['username']}, {'$set':{'password' : data['newpass']}})
        except:
            traceback.print_exc()
            result['message'] = u'后台错误'
            return json.dumps(result)
        result['success'] = 1
        result['message'] = u'修改成功'
        return json.dumps(result)