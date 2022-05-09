from datetime import timedelta
from re import I
from flask import Flask, render_template, session
from web import logger
from web import coon
from web import FIRST_USE

from web.blueprint.login import login_bp
from web.blueprint.api import api_bp
from web.blueprint.mine import mine_bp

app = Flask(__name__)

app.config['SECRET_KEY'] = 'ICVE-FLASK-WEB'
app.config['ENV'] = 'development'
#app.config['ENV'] = 'production'
app.config['DEBUG'] = True
# session.permanent = True
app.config['PERMANENT_SESSION_LIFETIM'] = timedelta(days=3)  # SESSION保质期

# BP
app.register_blueprint(login_bp, url_prefix='/login')
app.register_blueprint(api_bp, url_prefix='/api')
app.register_blueprint(mine_bp,url_prefix='/mine')

@app.route('/')
def index():
    if FIRST_USE:
        pass
    else:
        pass
    return render_template('index.html')


if __name__ == '__main__':
    logger.info('正在启动WEB...')
    app.run('0.0.0.0', 5000)
