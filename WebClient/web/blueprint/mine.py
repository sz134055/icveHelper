from crypt import methods
from distutils.log import info
from tkinter import E
from flask import Blueprint,render_template,request,jsonify,session
from web.datebase import get_info

mine_bp = Blueprint('mine',__name__)

@mine_bp.route('/')
def index():
    return render_template('mine.html')

@mine_bp.route('/login')
def login():
    try:
        my_account = request.form['account']
        my_pswd = request.form['pswd']

        my_info = get_info(account=my_account)
        
        if my_info:
            if my_pswd == my_info['userPwd']:
                # 通过验证
                session['logined'] = my_account

                return jsonify({'code':'1','info':'通过验证'})
        
        return jsonify({'code':'0','info':'账号或密码错误！'})


    except KeyError:
        return jsonify({'code':'0','info':'缺少必要信息'})

@mine_bp.route('/info',methods=['POST'])
def get_my_header():


    #my_id = request.form.get('id')
    #my_user_id = request.form.get('userId')
    try:
        my_account = request.form['account']

        if my_account and my_account == session['logined']:
            my_info = get_info(account=my_account)

            info = {
                'id':my_info['id'],
                'userType':my_info['type'],
                'userId':my_info['userId'],
                'account':my_info['userName'],
                'name':my_info['displayName'],
                'header':my_info['url'],
                'schoolName':my_info['schoolName'],
                'schoolId':my_info['schoolId'],
                'device':my_info['equipmentModel'],
                'os':my_info['equipmentApiVersion'],
                'app':my_info['appVersion'],
                'clientId':my_info['clientId'],
                'email':my_info['email'],
                'star':my_info['comment_star'],
                'content':my_info['comment_content']
            }


            return jsonify({'code':'1','info':info})
        return jsonify({'code':'0','info':'请先验证你的信息'})
    except KeyError:
            return jsonify({'code':'0','info':'缺少必要信息'})
