from nCov2019.extensions import db


class EverydayData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    confirmed_num = db.Column(db.Integer)
    cure_num = db.Column(db.Integer)
    death_num = db.Column(db.Integer)
    date = db.Column(db.DateTime)
