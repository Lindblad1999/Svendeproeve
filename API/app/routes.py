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
        return "Home!"

    # Route that returns the voltage measurement 
    # closest to the date and time given in the 
    # GET request
    @app.route('/voltage/closest', methods=['GET'])
    def get_voltage_closest():
        timestamp = request.args.get('timestamp')

        resp = get_closest_meas(Voltage, timestamp)

        if not isinstance(resp, Voltage):
            return resp

        return jsonify({
            'id': resp.id,
            'meas': resp.meas,
            'meas_time': resp.meas_time,
            'device_id': resp.device_id
        }), 200


    # Route that returns the current measurement 
    # closest to the date and time given in the 
    # GET request
    @app.route('/current/closest', methods=['GET'])
    def get_current_closest():
        timestamp = request.args.get('timestamp')

        resp = get_closest_meas(Current, timestamp)

        if not isinstance(resp, Current):
            return resp

        # Return the reading in JSON format
        return jsonify({
            'id': resp.id,
            'meas': resp.meas,
            'meas_time': resp.meas_time,
            'device_id': resp.device_id
        }), 200

    # Route to POST a voltage measurement
    @app.route('/voltage', methods=['POST'])
    def post_voltage():
        data = request.get_json()

        try:
            voltage = Voltage(meas=float(data['meas']), meas_time=datetime.now(), device_id=int(data['device_id']))
            db.session.add(voltage)
            db.session.commit() 
        except Exception as e:
            app.logger.error(f"Error: {str(e)}")
            return jsonify({'message': 'Invalid request'}), 400

        return jsonify({'message': 'Success'}), 201

    # Route to POST a current measurement
    @app.route('/current', methods=['POST'])
    def post_current():
        data = request.get_json()

        try:
            current = Current(meas=float(data['meas']), meas_time=datetime.now(), device_id=int(data['device_id']))
            db.session.add(current)
            db.session.commit() 
        except:
            return jsonify({'message': 'Inalid request'}), 400

        return jsonify({'message': 'Success'}), 201
    

def get_closest_meas(model, timestamp):
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
    closest_before = model.query.filter(model.meas_time <= requested_time)\
                                .order_by(model.meas_time.desc())\
                                .first()
    closest_after = model.query.filter(model.meas_time >= requested_time)\
                                .order_by(model.meas_time.asc())\
                                .first()

    # Get the closest timestamp of the two
    if closest_before and closest_after:
        diff_before = requested_time - closest_before.meas_time
        diff_after = closest_after.meas_time - requested_time
        closest_reading = closest_before if diff_before < diff_after else closest_after
    elif closest_before:
        closest_reading = closest_before
    elif closest_after:
        closest_reading = closest_after
    else:
        return jsonify({'message': 'Not found'}), NOT_FOUND

    # Return the reading in JSON format
    return closest_reading