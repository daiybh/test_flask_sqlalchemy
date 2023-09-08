from app import app,db
from flask_migrate import Migrate
import logging
import os
migrate=Migrate(app,db)


if __name__ == '__main__':    
    curAppPath=os.path.split(os.path.realpath(__file__))[0]
    app.config["LOGGER_PATH"]=f"{curAppPath}/logs/"
    app.config["UPLOAD_FOLDER"]=f"{curAppPath}/upload/"
        

    if not os.path.exists(app.config["UPLOAD_FOLDER"]):
        os.makedirs(app.config["UPLOAD_FOLDER"])  

    if not os.path.exists(app.config["LOGGER_PATH"]):
        os.makedirs(app.config["LOGGER_PATH"])   
        
    handler = logging.FileHandler(f'{app.config["LOGGER_PATH"]}flask.log')
    handler.setLevel(logging.DEBUG)
    logging_format= logging.Formatter('%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
    handler.setFormatter(logging_format)
    app.logger.addHandler(handler)

    app.run(debug=True)