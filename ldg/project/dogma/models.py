from dogma import db

from sqlalchemy.orm import declarative_base

base = declarative_base()

class Input(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Lot = db.Column(db.Integer, nullable=False)
    Time = db.Column(db.DateTime, nullable=False)
    pH = db.Column(db.Float, nullable=False)
    Temp = db.Column(db.Float, nullable=False)
    Voltage = db.Column(db.Float, nullable=False)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    number = db.Column(db.Integer, unique=True, nullable=False)

class Imginfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    imgname = db.Column(db.String(200), nullable=False)
    predictdate = db.Column(db.DateTime, nullable=False)
    prediction = db.Column(db.Text(), nullable=False)


class Imginfo2(base):
    __tablename__ = "Imginfo"
    id = db.Column(db.Integer, primary_key=True)
    imgname = db.Column(db.String(200), nullable=False)
    predictdate = db.Column(db.DateTime, nullable=False)
    prediction = db.Column(db.Text(), nullable=False)