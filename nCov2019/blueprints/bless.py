from flask import Blueprint, render_template, request, jsonify

from nCov2019.models import Bless
from nCov2019.extensions import db

bless_bp = Blueprint('bless', __name__)


@bless_bp.route('/bless')
def index():
    all_count = Bless.query.count()
    items = Bless.query.order_by(Bless.timestamp.desc()).all()
    bless_count = Bless.query.count()
    return render_template('_bless.html', all_count=all_count, items=items, bless_count=bless_count)


@bless_bp.route('/bless/new', methods=['POST'])
def new_bless():
    data = request.get_json()
    if data is None or data['body'].strip() == '':
        return jsonify(message='祝福语错误，请重新输入'), 400

    bless = Bless(body=data['body'])
    db.session.add(bless)
    db.session.commit()

    bless_count = Bless.query.count()

    return jsonify(html=render_template('_bless_item.html', item=bless), bless_count=bless_count,
                   message='发送祝福成功')



