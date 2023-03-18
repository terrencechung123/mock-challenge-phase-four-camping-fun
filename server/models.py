from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from sqlalchemy import func

db = SQLAlchemy()


class Camper(db.Model, SerializerMixin):
    __tablename__ = 'campers'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String)
    age = db.Column(db.Integer)
    @validates('name')
    def validate_name(self,key,value):
        if not value:
            raise ValueError('Name is required')
        return value
    @validates('age')
    def validate_age(self,key,value):
        if not (8 <= value <= 18):
            raise ValueError('Age must be between 8 and 18')
        return value

    created_at = db.Column(db.DateTime,server_default=func.now())
    updated_at = db.Column(db.DateTime, onupdate=func.now())
    signups = db.relationship('Signup', backref='camper', lazy=True)
    # activities = db.relationship('Activity', secondary='signups', backref='campers', lazy=True)
    serialize_rules = ('-signups', '-created_at','-updated_at',)

class Activity(db.Model, SerializerMixin):
    __tablename__ = 'activities'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    difficulty = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, onupdate=func.now())

    signups = db.relationship('Signup', backref='activity', lazy=True)
    # campers = db.relationship('Camper', secondary='signups', backref='activities', lazy=True)
    serialize_rules = ('-signups',)

class Signup(db.Model, SerializerMixin):
    __tablename__ = 'signups'

    id = db.Column(db.Integer, primary_key=True)
    camper_id = db.Column(db.Integer, db.ForeignKey('campers.id'), nullable=False)
    activity_id = db.Column(db.Integer, db.ForeignKey('activities.id'), nullable=False)

    time = db.Column(db.Integer)
    @validates('time')
    def validate_time(self,key,value):
        if not (0 <= value <= 23):
            raise ValueError('Time must be between 0 and 23')
        return value
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, onupdate=func.now())
