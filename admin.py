#-*- coding: utf-8 -*-
from flask import request
from app import app, db
import traceback
import json
import random
from tools import *

admindb = db.admin

@app.route('/adminlogin', methods=['POST'])
def adminlogin():
    jsondata = request.form
    data = immutabledict2dict(jsondata)
    result = {'success': 0}
    #db
    try:
        tmp = admindb.find_one({"username": data["username"]})
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
                admindb.update_one({'_id': tmp['_id']}, {'$set':{'token' : token}})
                return json.dumps(result)
            else:
                result['message'] = u'密码错误'
                return json.dumps(result)
    except:
        traceback.print_exc()
        result['message'] = u'后台错误'
        return json.dumps(result)

@app.route('/adminchecklogin', methods=['POST'])
def adminchecklogin():
    jsondata = request.form
    data = immutabledict2dict(jsondata)
    result = {'success': 0}
    #db
    try:
        tmp = admindb.find_one({'username': data['username']})
        if tmp['token'] == data['token']:
            result['success'] = 1
        return json.dumps(result)
    except:
        traceback.print_exc()
        return json.dumps(result)
    #
    return '1'