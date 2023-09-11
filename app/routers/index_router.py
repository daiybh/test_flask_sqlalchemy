from flask import Blueprint, jsonify, request  ,render_template

from app import db

from app.models.user import User
from app.models.led import Led
from app.models.park import Park


index_router = Blueprint('index_router', __name__,url_prefix='/index')



@index_router.route('/', methods=['GET'])
def index():
    msg="Hello World!python"    
    return render_template('index.html',data=msg)

@index_router.route('/all', methods=['GET'])
def all():
    leds = Led.query.all()
    ledsJson= ([led.to_dict() for led in leds])

    parks = Park.query.all()
    parksJson= ([l.to_dict() for l in parks])

    return render_template('park_led.html',PARKS_DATA=parks,LEDS_DATA=ledsJson)

@index_router.route('/product', methods=['GET'])
def product():
    msg="Hello World!python"    
    return render_template('product.html',data=msg)



@index_router.route("/createdb", methods=["GET"])
def createdb():
    db.create_all()
    return "Database created"

