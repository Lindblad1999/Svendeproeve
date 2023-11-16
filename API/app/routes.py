from flask import request, jsonify
from . import db
from run import app

@app.route('/energy_meter/voltage', methods=['POST'])
def receive_voltage():
    data = request.get_json()

    voltage_value = data['voltage']

    return jsonify({'message': 'Success'}), 200