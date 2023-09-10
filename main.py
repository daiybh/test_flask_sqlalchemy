from app import app,db,init
from flask_migrate import Migrate
import logging
import os
migrate=Migrate(app,db)


if __name__ == '__main__':    
    curAppPath=os.path.split(os.path.realpath(__file__))[0]
              
    init(curAppPath)
    app.run(debug=False,host='0.0.0.0',port=18080)