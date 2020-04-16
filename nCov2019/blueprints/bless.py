import logging

from flask import Blueprint, render_template, request, jsonify, current_app

from nCov2019.models import Bless
from nCov2019.extensions import db

bless_bp = Blueprint('bless', __name__)


@bless_bp.route('/bless')
def index():
    data = request.args
    if not data.get('page'):
        page = 1
    elif int(data.get('page')) < 1:
        page = 1
    else:
        page = int(data.get('page'))

    per_page = current_app.config.get('NCOV2019_BLESS_PER_PAGE')
    pagination = Bless.query.order_by(Bless.timestamp.desc()).paginate(page=page, per_page=per_page)
    items = pagination.items
    bless_count = Bless.query.count()
    return render_template('_bless.html', items=items, bless_count=bless_count, pagination=pagination)


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


@bless_bp.route('/bless/thumb-up', methods=['GET'])
def thumb_up():
    data = request.args
    if not data.get('id'):
        return jsonify(message='Id 不存在！'), 400
    bless = Bless.query.get(int(data.get('id')))
    if not bless:
        return jsonify(message='Id 不存在！'), 400

    bless.thumb_up = bless.thumb_up + 1
    db.session.commit()

    num = bless.thumb_up

    return jsonify(num=num, message='点赞 +1')

