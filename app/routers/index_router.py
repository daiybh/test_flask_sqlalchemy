from flask import Blueprint, jsonify, request  ,render_template

from app import db,app


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


@index_router.route('/insertData', methods=['GET'])
def insertData():
    try:
        data = request.get_json()
    except :
        print("don't have Json use values")
        data = request.values
        print(data)
        app.logger.error(f"insertData   {data}")

    park = Park(name="test"
                , park_id="10045928"
                , pgmfilepath="./upload/10045928.lsprj")
    db.session.add(park)

    led = Led(ledid="860402316010496", park_id="10045928")
    db.session.add(led)
    
    db.session.commit()
    return "success"

@index_router.route("/createdb", methods=["GET"])
def createdb():
    db.create_all()
    
    return "Database created"

