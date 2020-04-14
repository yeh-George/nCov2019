from datetime import datetime

from nCov2019.extensions import db


class EverydayData(db.Model):
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
