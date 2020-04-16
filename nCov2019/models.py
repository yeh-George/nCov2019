from datetime import datetime

from nCov2019.extensions import db


class EverydayData(db.Model):
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.Integer, primary_key=True)
    confirmedCount_zh = db.Column(db.Integer)
    curedCount_zh  = db.Column(db.Integer)
    deadCount_zh =  db.Column(db.Integer)
    confirmedCountIncr_zh = db.Column(db.Integer)
    curedCountIncr_zh =  db.Column(db.Integer)
    deadCountIncr_zh =  db.Column(db.Integer)
    confirmedCount_USA = db.Column(db.Integer)
    confirmedCount_UK = db.Column(db.Integer)
    confirmedCount_Italy = db.Column(db.Integer)

    data_day = db.Column(db.Integer, unique=True)


class Bless(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    thumb_up = db.Column(db.Integer, default=0)
    timestamp = db.Column(db.DateTime, default=datetime.now, index=True)