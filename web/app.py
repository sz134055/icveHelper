from datetime import timedelta
from flask import Flask, render_template, session
from web import logger
from web import coon
from web import FIRST_USE
import webbrowser

app = Flask(__name__)

app.config['SECRET_KEY'] = 'ICVE-FLASK-WEB'
# app.config['ENV'] = 'development'
app.config['ENV'] = 'production'
app.config['DEBUG'] = True
session.permanent = True
app.config['PERMANENT_SESSION_LIFETIM'] = timedelta(days=3)  # SESSION保质期


@app.route('/')
def index():
    if FIRST_USE:
        pass
    else:
        pass
    return render_template('index.html')


if __name__ == '__main__':
    logger.info('正在启动WEB...')
    webbrowser.open('http://127.0.0.1:5000/')
    app.run()
