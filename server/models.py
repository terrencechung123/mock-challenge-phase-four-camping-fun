from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from sqlalchemy import func
from sqlalchemy.ext.associationproxy import association_proxy

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
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
    signups = db.relationship('Signup', back_populates='camper')
    activities = association_proxy('signups', 'activity')

    serialize_rules = ('-signups', '-created_at','-updated_at','-activities.created_at','-activities.updated_at', '-activities.campers')

class Activity(db.Model, SerializerMixin):
    __tablename__ = 'activities'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    difficulty = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    signups = db.relationship(
        'Signup', back_populates='activity', cascade="all,delete, delete-orphan")
    campers = association_proxy('signups', 'camper')
    serialize_rules = ('-signups', '-updated_at', '-created_at', '-campers.activities')

class Signup(db.Model, SerializerMixin):
    __tablename__ = 'signups'

    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.Integer)
    activity_id = db.Column(db.Integer, db.ForeignKey('activities.id'), nullable=False)
    camper_id = db.Column(db.Integer, db.ForeignKey('campers.id'), nullable=False)
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    camper = db.relationship('Camper', back_populates='signups')
    activity = db.relationship('Activity', back_populates='signups')

    serialize_rules = ('-camper.signups', '-activity.signups',
                        '-camper.activities', '-activity.campers', '-created_at', '-updated_at')

    @validates('time')
    def validate_time(self,key,value):
        if not (0 <= value <= 23):
            raise ValueError('Time must be between 0 and 23')
        return value

    @validates('camper_id')
    def validates_camper_id(self, key, value):
        campers = Camper.query.all()
        camper_ids = [camper.id for camper in campers]
        if not value in camper_ids:
            raise ValueError("Not a camper.")
        return value

    @validates('activity_id')
    def validates_activity_id(self, key, value):
        activities = Activity.query.all()
        activity_ids = [activity.id for activity in activities]
        if not value in activity_ids:
            raise ValueError("Not an activity.")
        return value