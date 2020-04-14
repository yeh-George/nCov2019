from flask import Blueprint, render_template


bless_bp = Blueprint('bless', __name__, url_prefix='/bless')


@bless_bp.route('/')
def index():
    return render_template('_bless.html')