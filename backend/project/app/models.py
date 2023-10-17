from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from app import app
import os

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

model = SQLAlchemy()
model.init_app(app)

class User(model.Model):
    id = model.Column(model.Integer, primary_key = True)
    name = model.Column(model.String(100))
    last_name = model.Column(model.String(100))
    email = model.Column(model.String(100), unique = True)
    password = model.Column(model.String(100))
    parcel_groups = model.relationship("Parcel", backref = 'user', cascade="all, delete-orphan")
    date = model.Column(model.Date, default = datetime.utcnow)



class Parcel(model.Model):
    id = model.Column(model.Integer, primary_key = True)
    name = model.Column(model.String(50))
    location = model.Column(model.String(50))
    surface = model.Column(model.Integer)
    user_id = model.Column(model.Integer, model.ForeignKey('user.id'), nullable=False)
    vans = model.relationship("Van", backref = 'parcel', cascade="all, delete-orphan")
    date = model.Column(model.Date, default = datetime.utcnow)


class Van(model.Model):
    id = model.Column(model.Integer, primary_key = True)
    name = model.Column(model.String(100), nullable = False)
    device_id = model.Column(model.String(100), nullable = False)
    parcel_id = model.Column(model.Integer, model.ForeignKey('parcel.id'), nullable=False)
    records = model.relationship("Record", backref = 'van', cascade="all, delete-orphan")
    command = model.relationship("Command", backref = 'van', cascade="all, delete-orphan")
    date = model.Column(model.Date, default = datetime.utcnow)
    
    
class Record(model.Model):
    id = model.Column(model.Integer, primary_key = True)
    state = model.Column(model.Boolean, default = True)
    flow = model.Column(model.Integer)
    quantity = model.Column(model.Integer)
    battery = model.Column(model.Integer)
    van_id = model.Column(model.Integer, model.ForeignKey('van.id'), nullable = False)
    date = model.Column(model.DateTime, default = datetime.utcnow)
    
class Command(model.Model):
    id = model.Column(model.Integer, primary_key = True)
    state = model.Column(model.Boolean, default = True)
    van_id = model.Column(model.Integer, model.ForeignKey('van.id'), nullable = False)
    date = model.Column(model.DateTime, default = datetime.utcnow)

with app.app_context():
    model.create_all()