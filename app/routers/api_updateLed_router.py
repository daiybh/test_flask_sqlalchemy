from flask import Blueprint, jsonify, request
from app.models.user import User
from app.models.park import Park
from app.models.led import Led
from app import db

api_updateLed_router = Blueprint('api_updateLed_router', __name__,url_prefix='/api')
@api_updateLed_router.route('/updates', methods=['GET'])
def get_users():
    
    json_template={
            "service_name":"Receive_LED",
            "park_id":"12345678",
            "sign":"",
            "order_id":"10001",
            "LED_id":"11112312135",
            "data": [
                {
                    "F_id":1,
                    "F_message":"car1 coming",
                    "F_color":1
                },
                {
                    "F_id":2,
                    "F_message":"car2 coming",
                    "F_color":1
                }
            ]
        }
    try:
        rjson= request.json()
        park_id=rjson['park_id']
        led_id = rjson['led_id']
    except:        
        #return jsonify({'error':-1,"msg":"need json body"})
        park_id="10045928"
        led_id="860302250008951"
    result = db.session.query
    (        Led.ledid,Led.park_id,Park.name,Park.pgmfilepath        ).filter
    (        Led.ledid==led_id         ).filter
    (        Park.park_id==park_id     ).filter
    (        Park.park_id==Led.park_id ).all() 

    if len(result)==0:        
        return jsonify({'error':-1,"msg":f"don't find parkid:{park_id},led_id:{led_id}"})
    
    #生成请求JSON

    return jsonify([tuple(row) for row in result])
