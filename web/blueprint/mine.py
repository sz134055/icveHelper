from flask import Blueprint,render_template

mine_bp = Blueprint('mine',__name__)

@mine_bp.route('/')
def index():
    return render_template('mine.html')