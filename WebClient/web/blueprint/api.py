from flask import Blueprint, request, jsonify, session
from web.core import User
#from web.courseLaunch import currentInfo, currentId, currentUserId, currentProcess, currentTotalProcess
from web.datebase import get_one,get_info

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


@api_bp.route('/info',methods=['POST'])
def get_my_header():
    my_id = request.form.get('id')
    my_user_id = request.form.get('userId')
    my_account = request.form.get('account')

    if my_id or my_user_id or my_account:
        my_info = get_info(my_id,my_user_id,my_account)

        info = {
            'id':my_info['id'],
            'userType':my_info['type'],
            'userId':my_info['userId'],
            #'account':my_info['userName'],
            #'name':my_info['displayName'],
            'header':my_info['url'],
            #'schoolName':my_info['schoolName'],
            #'schoolId':my_info['schoolId'],
            #'device':my_info['equipmentModel'],
            #'os':my_info['equipmentApiVersion'],
            #'app':my_info['appVersion'],
            #'clientId':my_info['clientId'],
            #'email':my_info['email'],
            #'star':my_info['comment_star'],
            #'content':my_info['comment_content']
        }


        return jsonify({'code':'1','info':info})
    else:
        return jsonify({'code':'0','info':'缺少必要信息'})

