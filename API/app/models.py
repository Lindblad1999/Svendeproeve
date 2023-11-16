from . import db

class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    api_key = db.relationship('APIKey', backref='device', uselist=False)
    voltages = db.relationship('Voltage', backref='device')
    currents = db.relationship('Current', backref='device')
    relays = db.relationship('Relay', backref='device')

class Voltage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    meas = db.Column(db.Float, nullable=False)
    meas_time = db.Column(db.DateTime)
    device_id = db.Column(db.Integer, db.ForeignKey(Device.id), nullable=False)
    
class Current(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    meas = db.Column(db.Float, nullable=False)
    meas_time = db.Column(db.DateTime)
    device_id = db.Column(db.Integer, db.ForeignKey(Device.id), nullable=False)

class Relay(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.Boolean, nullable=False)
    log_time = db.Column(db.DateTime)
    device_id = db.Column(db.Integer, db.ForeignKey(Device.id), nullable=False)

class APIKey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    api_key = db.Column(db.String(255), unique=True, nullable=False)
    device_id = db.Column(db.Integer, db.ForeignKey(Device.id), nullable=False)

