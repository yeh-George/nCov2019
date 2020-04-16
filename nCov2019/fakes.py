import random

from faker import Faker

from nCov2019.extensions import db
from nCov2019.models import Bless

fake = Faker()

def fake_bless():
    for i in range(50):
        body = fake.text(200)
        thumb_up = random.randint(10, 1000)
        item = Bless(body=body, thumb_up=thumb_up)
        db.session.add(item)
    db.session.commit()
