from flask import Blueprint, jsonify, request
from app.models.led import Led
from app import db

led_router = Blueprint('led_router', __name__)

@led_router.route('/leds', methods=['GET'])
def get_leds():
    leds = Led.query.all()
    return jsonify([led.to_dict() for led in leds])

@led_router.route('/leds/<int:led_id>', methods=['GET'])
def get_led(led_id):
    led = Led.query.get(led_id)
    if led:
        return jsonify(led.to_dict())
    else:
        return jsonify({'error': 'Led not found'})

@led_router.route('/leds', methods=['POST'])
def create_led():
    try:
        data = request.get_json()
    except:
        data = request.values
    led = Led(ledid=data['ledid'], park_id=data['park_id'])
    db.session.add(led)
    db.session.commit()
    return jsonify(led.to_dict())

@led_router.route('/leds/<int:led_id>', methods=['PUT'])
def update_led(led_id):
    led = Led.query.get(led_id)
    if led:
        data = request.get_json()
        led.ledid = data['ledid']
        led.park_id = data['park_id']
        db.session.commit()
        return jsonify(led.to_dict())
    else:
        return jsonify({'error': 'Led not found'})

@led_router.route('/leds/<int:led_id>', methods=['DELETE'])
def delete_led(led_id):
    led = Led.query.get(led_id)
    if led:
        db.session.delete(led)
        db.session.commit()
        return jsonify({'message': 'Led deleted successfully'})
    else:
        return jsonify({'error': 'Led not found'})
