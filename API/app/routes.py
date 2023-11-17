from flask import request, jsonify
from . import db
from run import app
from models import Voltage
from datetime import datetime

BAD_REQUEST = 400
OK = 200
NOT_FOUND = 404

@app.route('/energy_meter/voltage', methods=['POST'])
def receive_voltage():
    data = request.get_json()

    voltage_value = data['voltage']

    return jsonify({'message': 'Success'}), OK

@app.route('/voltage/closest', methods=['GET'])
def get_voltage_closest():
    timestamp = request.args.get('timestamp')

    if timestamp:
        try:
            requested_time = datetime.fromisoformat(timestamp)
        except ValueError:
            return jsonify({'error': 'Invalid argument'}), BAD_REQUEST
    else:
        return jsonify({'error': 'timestamp required'}), BAD_REQUEST
    
    closest_before = Voltage.query.filter(Voltage.meas_time <= requested_time)\
                                  .order_by(Voltage.meas_time.desc())\
                                  .first()
    closest_after = Voltage.query.filter(Voltage.meas_time >= requested_time)\
                                 .order_by(Voltage.meas_time.asc())\
                                 .first()

    if closest_before and closest_after:
        diff_before = requested_time - closest_before.meas_time
        diff_after = closest_after.meas_time - requested_time
        closest_reading = closest_before if diff_before < diff_after else closest_after
    else:
        return jsonify({'message': 'Not found'}), NOT_FOUND

    return jsonify({
        'id': closest_reading.id,
        'meas': closest_reading.meas,
        'meas_time': closest_reading.meas_time,
        'device_id': closest_reading.device_id
    })
