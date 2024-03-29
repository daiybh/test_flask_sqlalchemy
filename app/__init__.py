import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from app.globalDebugVer import GlobalVar
from app.tools.timerThread import TimerThread
from .config import Config
from flask import jsonify
from flask_restful import Api,Resource

import os
 


app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

def init(curAppPath):
    app.config["LOGGER_PATH"]=f"{curAppPath}/logs/"
    app.config["UPLOAD_FOLDER"]=f"{curAppPath}/upload/"
        

    if not os.path.exists(app.config["UPLOAD_FOLDER"]):
        os.makedirs(app.config["UPLOAD_FOLDER"])  

    if not os.path.exists(app.config["LOGGER_PATH"]):
        os.makedirs(app.config["LOGGER_PATH"]) 

    logging.basicConfig(filename=f'{app.config["LOGGER_PATH"]}flask.log',
                        level=logging.DEBUG, format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

    app.globalVar=GlobalVar()
    if app.globalVar.timerThread==None:
        app.globalVar.timerThread = TimerThread(app.logger)
        app.globalVar.timerThread.start()

# Import models
from .models.user import User
from .models.led import Led
from .models.park import Park

# Import routers
from .routers.user_router import user_router
from .routers.index_router import index_router
from .routers.led_router import led_router
from .routers.park_router import park_router
from .routers.api_updateLed_router import api_updateLed_router

# Register routers
app.register_blueprint(user_router)
app.register_blueprint(index_router)
app.register_blueprint(led_router)
app.register_blueprint(park_router)
app.register_blueprint(api_updateLed_router)

@app.route('/', methods=['GET'])
@app.route('/l', methods=['GET'])
@app.route('/list', methods=['GET'])
def index():
    routes=[]
    for rule in app.url_map.iter_rules():
        routes.append(f'{rule.methods} {rule.rule}')
    return jsonify(routes)


if __name__ == '__main__':
    app.run(debug=True)