import logging
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from logging.handlers import TimedRotatingFileHandler

from app.globalDebugVer import GlobalVar
from app.tools.LedTask.ledTaskThread import LedTaskThread
from .config import Config
from flask import jsonify
from flask_restful import Api,Resource

import os
 
import json
def to_pretty_json(value):
    return json.dumps(value, sort_keys=True,
                      indent=4, separators=(',', ': '), ensure_ascii=False)


app = Flask(__name__)
app.config.from_object(Config)
app.config["JSON_AS_ASCII"] = False

app.jinja_env.filters['to_pretty_json'] = to_pretty_json

db = SQLAlchemy(app)

def init(curAppPath):
    app.config["LOGGER_PATH"]=f"{curAppPath}/logs/"
    app.config["UPLOAD_FOLDER"]=f"{curAppPath}/upload/"
    app.config["TASK_FOLDER"]=f"{curAppPath}/tasks/"
    app.config["BACKGROUND_IMG_PATH"]=f'{curAppPath}/123.jpg'
        

    if not os.path.exists(app.config["UPLOAD_FOLDER"]):
        os.makedirs(app.config["UPLOAD_FOLDER"])  

    if not os.path.exists(app.config["TASK_FOLDER"]):
        os.makedirs(app.config["TASK_FOLDER"])  

    if not os.path.exists(app.config["LOGGER_PATH"]):
        os.makedirs(app.config["LOGGER_PATH"]) 

        
    logging.basicConfig(filename=f'{app.config["LOGGER_PATH"]}flask.log',
                        level=logging.DEBUG, format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')


    formatter = logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    rfhandler = TimedRotatingFileHandler(f'{app.config["LOGGER_PATH"]}Rotatingflask.log', 
                            when='midnight', backupCount=7)
    rfhandler.setLevel(logging.DEBUG)
    rfhandler.setFormatter(formatter)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    

    logger = logging.getLogger("Tlog")
    logger.setLevel(logging.DEBUG)
    logger.addHandler(rfhandler)
    logger.addHandler(ch)

    app.globalVar=GlobalVar()
    if app.globalVar.ledTaskThread==None:
        app.globalVar.ledTaskThread = LedTaskThread(app.config)
        app.globalVar.ledTaskThread.start()

def stopAll():
    app.globalVar.ledTaskThread.stopTask()

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
def show_allRoutes():
    
    return render_template('all_routers.html',sorted_rules=app.url_map.iter_rules())



@app.route('/l', methods=['GET'])
@app.route('/list', methods=['GET'])
def index():
    routes=[]
    for rule in app.url_map.iter_rules():
        routes.append(f'{rule.methods} {rule.rule}')
    return jsonify(routes)


if __name__ == '__main__':
    app.run(debug=True)