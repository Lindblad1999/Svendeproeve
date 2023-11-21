from flask import request, jsonify
from . import db
from .models import Voltage, Current
from datetime import datetime

OK          = 200
CREATED     = 201
BAD_REQUEST = 400
NOT_FOUND   = 404

def register_routes(app):
    @app.route('/', methods=['GET'])
    def home():
        return "Test!"

    # Route that returns the voltage measurement 
    # closest to the date and time given in the 
    # GET request
    @app.route('/voltage/closest', methods=['GET'])
    def get_voltage_closest():
        timestamp = request.args.get('timestamp')

        # Check that a timestamp argument has been given in the request
        # and check that timestamp is valid
        if timestamp:
            try:
                requested_time = datetime.fromisoformat(timestamp)
            except ValueError:
                return jsonify({'error': 'Invalid argument'}), BAD_REQUEST
        else:
            return jsonify({'error': 'timestamp required'}), BAD_REQUEST
        
        # Query the database for the closest timstamp above and below 
        # the timestamp given in the request
        closest_before = Voltage.query.filter(Voltage.meas_time <= requested_time)\
                                    .order_by(Voltage.meas_time.desc())\
                                    .first()
        closest_after = Voltage.query.filter(Voltage.meas_time >= requested_time)\
                                    .order_by(Voltage.meas_time.asc())\
                                    .first()

        # Get the closest timestamp of the two
        if closest_before and closest_after:
            diff_before = requested_time - closest_before.meas_time
            diff_after = closest_after.meas_time - requested_time
            closest_reading = closest_before if diff_before < diff_after else closest_after
        else:
            return jsonify({'message': 'Not found'}), NOT_FOUND

        # Return the reading in JSON format
        return jsonify({
            'id': closest_reading.id,
            'meas': closest_reading.meas,
            'meas_time': closest_reading.meas_time,
            'device_id': closest_reading.device_id
        })


    # Route that returns the current measurement 
    # closest to the date and time given in the 
    # GET request
    @app.route('/current/closest', methods=['GET'])
    def get_current_closest():
        timestamp = request.args.get('timestamp')

        # Check that a timestamp argument has been given in the request
        # and check that timestamp is valid
        if timestamp:
            try:
                requested_time = datetime.fromisoformat(timestamp)
            except ValueError:
                return jsonify({'error': 'Invalid argument'}), BAD_REQUEST
        else:
            return jsonify({'error': 'timestamp required'}), BAD_REQUEST
        
        # Query the database for the closest timstamp above and below 
        # the timestamp given in the request
        closest_before = Current.query.filter(Current.meas_time <= requested_time)\
                                    .order_by(Current.meas_time.desc())\
                                    .first()
        closest_after = Current.query.filter(Current.meas_time >= requested_time)\
                                    .order_by(Current.meas_time.asc())\
                                    .first()

        # Get the closest timestamp of the two
        if closest_before and closest_after:
            diff_before = requested_time - closest_before.meas_time
            diff_after = closest_after.meas_time - requested_time
            closest_entry = closest_before if diff_before < diff_after else closest_after
        else:
            return jsonify({'message': 'Not found'}), NOT_FOUND

        # Return the reading in JSON format
        return jsonify({
            'id': closest_entry.id,
            'meas': closest_entry.meas,
            'meas_time': closest_entry.meas_time,
            'device_id': closest_entry.device_id
        })

    # Route to POST a voltage measurement
    @app.route('/voltage', methods=['POST'])
    def post_voltage():
        data = request.get_json()

        try:
            voltage = Voltage(meas=float(data['meas']), meas_time=datetime.now(), device_id=data['device_id'])
            db.session.add(voltage)
            db.session.commit() 
        except:
            return jsonify({'message': 'Inalid request'}), BAD_REQUEST

        return jsonify({'message': 'Success'}), CREATED

    # Route to POST a current measurement
    @app.route('/current', methods=['POST'])
    def post_current():
        data = request.get_json()

        try:
            voltage = Current(meas=float(data['meas']), meas_time=datetime.now(), device_id=data['device_id'])
            db.session.add(voltage)
            db.session.commit() 
        except:
            return jsonify({'message': 'Inalid request'}), BAD_REQUEST

        return jsonify({'message': 'Success'}), CREATED