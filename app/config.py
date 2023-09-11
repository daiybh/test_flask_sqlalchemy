import os

curAppPath=os.path.split(os.path.realpath(__file__))[0]

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///example.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SERVER_PORT = 18080

    LED_SERVER_BASEURL = "http://t.hyman.store:11007"
    LED_SERVER_NEIMA_URL = LED_SERVER_BASEURL+"/neima?key="
    LED_SERVER_UPDATE_WITH_IMAGE = LED_SERVER_BASEURL+"/update_with_image"

    UPLOAD_FOLDER = f'{curAppPath}/upload/'

    LOGGER_PATH=f'{curAppPath}/logs/'

    ACTIVETASK_EVERYSECONDS=20

