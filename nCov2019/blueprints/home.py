# -*- coding: utf-8 -*-
import requests

from datetime import datetime
import time

from flask import Blueprint, render_template, jsonify, current_app

from nCov2019.extensions import db
from nCov2019.models import EverydayData

home_bp = Blueprint('home', __name__)


@home_bp.route('/')
def index():
    return render_template('index.html')


@home_bp.route('/intro')
def intro():
    """
        调用的接口：COVID-19/2019-nCoV Realtime Infection Data API
        GitHub：https://github.com/BlankerL/DXY-COVID-19-Crawler
        向接口调数据存在一个问题：间隔时间不能太短，否则会出现503，多次试验，时间大概定在0.4s
        改进方法；把当天的数据写入数据库
    """
    # 国内确诊人数、治愈人数、死亡人数
    headers = {
    }

    if not EverydayData.query.filter_by(data_day=datetime.today().toordinal()).first():
        url_zh = 'https://lab.isaaclin.cn/nCoV/api/overall'
        r = requests.get(url_zh, headers=headers)
        r.encoding = 'utf-8'
        data = r.json()

        if data.get('detail'):
            return jsonify(message=('Data get wrong.')), 400

        confirmedCount_zh = data['results'][0].get('confirmedCount') or 0
        curedCount_zh  = data['results'][0].get('curedCount') or 0
        deadCount_zh =  data['results'][0].get('deadCount') or 0
        confirmedCountIncr_zh =  data['results'][0].get('confirmedIncr') or 0
        curedCountIncr_zh =  data['results'][0].get('curedIncr') or 0
        deadCountIncr_zh =  data['results'][0].get('deadIncr') or 0

        #美国确诊人数及新增确诊人数
        time.sleep(0.5)
        url_USA = "https://lab.isaaclin.cn/nCoV/api/area?latest=true&province=%E7%BE%8E%E5%9B%BD"
        r = requests.get(url_USA, headers=headers)
        r.encoding = 'utf-8'
        data = r.json()
        if data.get('detail'):
            return jsonify(message=('Data get wrong.')), 400

        confirmedCount_USA = data['results'][0]['confirmedCount']

        # 英国确诊人数及新增确诊人数
        time.sleep(0.5)
        url_UK = 'https://lab.isaaclin.cn/nCoV/api/area?province=%E8%8B%B1%E5%9B%BD&latest=true'
        r = requests.get(url_UK, headers=headers)
        r.encoding = 'utf-8'
        data = r.json()
        if data.get('detail'):
            return jsonify(message=('Data get wrong.')), 400

        confirmedCount_UK = data['results'][0]['confirmedCount']

        # 意大利确诊人数及新增确诊人数
        time.sleep(0.5)
        url_Italy = 'https://lab.isaaclin.cn/nCoV/api/area?province=%E6%84%8F%E5%A4%A7%E5%88%A9&latest=true'
        r = requests.get(url_Italy, headers=headers)
        r.encoding = 'utf-8'
        data = r.json()
        if data.get('detail'):
            return jsonify(message=('Data get wrong.')), 400

        confirmedCount_Italy = data['results'][0]['confirmedCount']

        everyday_data = EverydayData(confirmedCount_zh=confirmedCount_zh,
                           confirmedCountIncr_zh=confirmedCountIncr_zh, curedCount_zh=curedCount_zh,
                           curedCountIncr_zh=curedCountIncr_zh, deadCount_zh=deadCount_zh,
                           deadCountIncr_zh=deadCountIncr_zh, confirmedCount_USA=confirmedCount_USA,
                           confirmedCount_Italy=confirmedCount_Italy, confirmedCount_UK=confirmedCount_UK,
                            data_day=datetime.today().toordinal())
        db.session.add(everyday_data)
        db.session.commit()
    else:
        everyday_data = EverydayData.query.filter_by(data_day=datetime.today().toordinal()).first()

    return render_template('_intro.html', everyday_data=everyday_data, nCovToday=datetime.today().strftime('%m -%d'))