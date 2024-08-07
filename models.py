#not in use at the moment
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
#from app import db

db = SQLAlchemy()

#Define association for skills - used for matching module possibly?
event_skills = db.Table('event_skills',
    db.Column('event_id', db.Integer, db.ForeignKey('event.id'), primary_key=True),
    db.Column('skill_id', db.Integer, db.ForeignKey('skill.id'), primary_key=True)
)

user_skills = db.Table('user_skills',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('skill_id', db.Integer, db.ForeignKey('skill.id'), primary_key=True)
)


#Database Models WIP : Migrate to new file if possible =========================

#User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    #address2 = db.Column(db.String(100))
    state_id = db.Column(db.Integer, db.ForeignKey('state.id'), nullable=False)
    skills = db.relationship('Skill', secondary=user_skills, backref=db.backref('users', lazy='dynamic'))
    preferences = db.Column(db.String(200), nullable=False)
    availability = db.Column(db.String(200), nullable=False)
    volunteer_histories = db.relationship('VolunteerHistory', backref='volunteer', lazy=True)
    def get_id(self):
        return str(self.id)

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False


#Volunteer History Model
class VolunteerHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    volunteer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    participation_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<VolunteerHistory {self.volunteer_id}-{self.event_id}>'

#Event Model
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    urgency = db.Column(db.String(10), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    state_id = db.Column(db.Integer, db.ForeignKey('state.id'), nullable=False)
    zipcode = db.Column(db.String(10), nullable=False)
    skills = db.relationship('Skill', secondary=event_skills, backref=db.backref('events', lazy='dynamic'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    notifications = db.relationship('Notification', backref='event', lazy=True)

#Notification Model
class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)

#Skill Model
class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

#State Model
class State(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(2), nullable=False, unique=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    users = db.relationship('User', backref='state', lazy=True)
    events = db.relationship('Event', backref='state', lazy=True)