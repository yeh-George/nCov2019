from faker import Faker

from nCov2019.extensions import db
from nCov2019.models import Bless

fake = Faker()

def fake_bless():
    for i in range(20):
        body = fake.text(200)
        item = Bless(body=body)
        db.session.add(item)
    db.session.commit()
