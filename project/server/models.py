# project/server/models.py


import datetime

from flask import current_app

from project.server import db, bcrypt


class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    racer = db.relationship("Racer", uselist=False, backref="user")

    def __init__(self, email, password, admin=False):
        self.email = email
        self.password = bcrypt.generate_password_hash(
            password, current_app.config.get('BCRYPT_LOG_ROUNDS')
        ).decode('utf-8')
        self.registered_on = datetime.datetime.now()
        self.admin = admin

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def __repr__(self):
        return '<User {0}>'.format(self.email)

class Sponsor(db.Model):

    __tablename__ = 'sponsors'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))

    def __init__(self, name):
        self.name = name
    
    def __repr__(self):
        return '<Sponsor {0}>'.format(self.name)

class RaceClass(db.Model):

    __tablename__ = 'raceclasses'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)

    def __init__(self, name):
        self.name = name
    
    def __repr__(self):
        return '<RaceClass {0}>'.format(self.name)

class Track(db.Model):

    __tablename__ = 'tracks'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    #lap_distance = db.Column(db.Float)

    def __init__(self, name, event_id):
        self.name = name
        self.event_id = event_id
    
    def __repr__(self):
        return '<Track {0}>'.format(self.name)

class Event(db.Model):
    
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    tracks = db.relationship('Track', backref='event')
    date = db.Column(db.Date, nullable=False)

    def __init__(self, name, date):
        self.name = name
        self.date = date
    
    def __repr__(self):
        return '<Event {0}>'.format(self.name)

class Car(db.Model):

    __tablename__ = 'cars'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    make = db.Column(db.String(255), nullable=False)
    model = db.Column(db.String(255), nullable=False)
    year = db.Column(db.String(255), nullable=False)
    color = db.Column(db.String(255), nullable=False)
    number = db.Column(db.String(255), nullable=False)
    racer_id = db.Column(db.Integer, ForeignKey('racers.id'))

    def __init__(self, make=None, model=None, year=None, color=None, number=None, racer_id):
        self.make = make
        self.model = model
        self.year = year
        self.color = color
        self.number = number
        self.racer_id = racer_id
    
    def __repr__(self):
        return "<Car(make='%s', model='%s', number='%s')>" % (self.make, self.model, self.number)

class Racer(db.Model):

    __tablename__ = 'racers'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True)
    user_id = db.Column(db.Integer, ForeignKey('users.id'))
    user = db.relationship("User", backref="racer")
    name = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(255))
    state = db.Column(db.String(255))
    points = db.Column(db.Integer)
    car = db.relationship('Car', backref='racer')
    sponsor = db.relationship('Sponsor', backref='racer')
    #Picture

    def __init__(self, email, user_id, name, city, state, points, car, sponsor):
        self.email = email
        self.user_id = user_id
        self.name = name
        self.city = city
        self.state = state
        self.points = points
        self.car = car
        self.sponsor = sponsor
    
    def __repr__(self):
        return '<Racer {0}>'.format(self.name)

class Race(db.Model):

    __tablename__ = 'races'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    driver = db.relationship('Racer', backref='race')
    track = db.relationship('Track', backref='race')
    event = db.relationship('Event', backref='race')
    time = db.Column(db.String(255))

    def __init__(self, driver, track, event, time):
        self.driver = driver
        self.track = track
        self.event = event
        self.time = time
    
    def __repr__(self):
        return "<Race(driver='%s', track='%s', event='%s')>" % (self.driver, self.track, self.event)

class BestLap(db.Model):

    __tablename__ = 'bestlaps'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    driver = db.relationship('Racer', backref='bestlap')
    raceclass = db.relationship('RaceClass', backref='bestlap')
    event = db.relationship('Event', backref='bestlap')
    track = db.relationship('Track', backref='bestlap')
    time = db.Column(db.Float)
    isBest = db.Column(db.Boolean)

    def __init__(self, driver, raceclass, event, track, time, isBest):
        self.driver = driver
        self.raceclass = raceclass
        self.event = event
        self.track = track
        self.time = time
        self.isBest = isBest

    def __repr__(self):
        return "<BestLap(driver='%s', raceclass='%s', track='%s', time='%s')>" % (self.driver, self.raceclass, self.track, self.time)


class Record(db.Model):
    
    __tablename__ = 'records'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    csv = db.Column(db.Blob)

    def __init__(self, csv):
        self.csv = csv

    def __repr__(self):
        return '<Record {0}>'.format(self.csv)
