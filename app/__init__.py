from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config
from flask import jsonify
from flask_restful import Api,Resource

import os
 



app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)



# Import models
from .models.user import User
from .models.led import Led
from .models.park import Park

# Import routers
from .routers.user_router import user_router
from .routers.index_router import index_router
from .routers.led_router import led_router
from .routers.park_router import park_router

# Register routers
app.register_blueprint(user_router)
app.register_blueprint(index_router)
app.register_blueprint(led_router)
app.register_blueprint(park_router)

@app.route('/l', methods=['GET'])
@app.route('/list', methods=['GET'])
def index():
    routes=[]
    for rule in app.url_map.iter_rules():
        routes.append(f'{rule.methods} {rule.rule}')
    return jsonify(routes)


if __name__ == '__main__':
    app.run(debug=True)