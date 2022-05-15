from flask import Blueprint, request, jsonify, render_template
from web.core import User
from web.datebase import insert, get_info

login_bp = Blueprint('login', __name__)


@login_bp.route('/')
def index():
    return render_template('login.html')


@login_bp.route('/add',methods=['POST'])
def add_user():
    try:
        # 空表单检测
        for form_value in request.form.to_dict().values():
            if form_value == '':
                raise KeyError


        me = User({
            'appVersion': request.form['app'],
            'clientId': request.form['clientId'],
            'equipmentApiVersion': request.form['os'],
            'equipmentAppVersion': request.form['app'],
            'equipmentModel': request.form['device'],
            'userName': request.form['account'],
            'userPwd': request.form['pswd']
        })
        user_email = request.form['email']

        # 提前验证查询
        if get_info(account=request.form['account']):
            return jsonify({'code': '1', 'msg': '你已在队列当中，如有需要请自行查询序号等信息'})

        login_status = me.login()
        if login_status['code'] == '1':
            add_status = insert(
                me.type,
                me.id,
                me.account,
                me.login_info['userPwd'],
                me.token,
                me.name,
                me.number,
                me.header_url,
                me.school_info['name'],
                me.school_info['id'],
                me.login_info['equipmentModel'],
                me.login_info['equipmentApiVersion'],
                request.form['app'],
                me.login_info['clientId'],
                user_email,
                request.form.get('star'),
                request.form.get('comment')
            )
            if add_status['code'] == '1':
                return jsonify(add_status)
            else:
                return jsonify({'code': '1', 'msg': '你已在队列当中，如有需要请自行查询序号等信息'})
        else:
            return jsonify({'code': '0', 'msg': login_status['msg']})
    except KeyError:
        return jsonify({'code': '0', 'msg': '缺少必要登陆信息！'})