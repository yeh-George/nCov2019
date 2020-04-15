from flask import Blueprint, render_template

from nCov2019.models import Bless
from nCov2019.extensions import db

bless_bp = Blueprint('bless', __name__)


@bless_bp.route('/bless')
def index():
    all_count = Bless.query.count()
    items = Bless.query.order_by(Bless.timestamp.desc()).all()
    return render_template('_bless.html', all_count=all_count, items=items)


@bless_bp.route('/bless/new')
def new_bless():
    pass

