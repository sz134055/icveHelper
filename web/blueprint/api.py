from flask import Blueprint, request, jsonify, session
from web.core import User
#from web.courseLaunch import currentInfo, currentId, currentUserId, currentProcess, currentTotalProcess
from web.datebase import get_one

api_bp = Blueprint('api', __name__)

'''
@api_bp.route('/nowUser')
def now_user():
    return jsonify({'code': '1', 'info': {'num': currentId, 'id': currentUserId}})


@api_bp.route('/nowInfo')
def now_info():
    return jsonify({'code': '1', 'msg': currentInfo})
'''
@api_bp.route('/nowUser')
def now_user():
    user = get_one()
    if user:
        return jsonify({'code':'1','info':{'num':str(user[0]),'id':user[2]}})
    else:
        # 无用户
        return jsonify({'code':'10','info':{'num':'0','id':'0'}})

@api_bp.route('/nowInfo')
def now_info():
    return {'code':'1','msg':'状态信息暂时不可用'}