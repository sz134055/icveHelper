from flask import Blueprint, request, jsonify, session
from web.core import User

api_bp = Blueprint('api', __name__)


class CourseStatus:
    def __init__(self):
        self.info = {}


@api_bp.route('/login')
def login():
    try:
        form_load = {
            'userName': request.form['user'],
            'userPwd': request.form['pswd'],
            'equipmentApiVersion': request.form['osVer'],
            'equipmentModel': request.form['osName'],
            'appVersion': '2.8.28',
            'equipmentAppVersion': '2.8.48',
            'clientId': request.form['clientId']
        }
    except KeyError:
        return jsonify({'code': '0', 'info': '登陆信息不完善'})

    user = User(form_load)
    login_status = user.login()
    if login_status['code'] == '1':
        # 登陆成功，装载SESSION
        session.update(user.user_info)
    return login_status


@api_bp.route('/logins')
def sess():
    try:
        session['cookies']
    except KeyError:
        return jsonify({'code': '0', 'msg': 'SESSION不完整'})
    user = User(session[:])
    login_status = user.login_from_session()
    if login_status['code'] == 1:
        session.update(user.user_info)

    return jsonify(login_status)


@api_bp.route('/course/nowStatus')
def courseStatus():
    pass


@api_bp.route('/course/allComplete')
def courseComplete():
    pass
