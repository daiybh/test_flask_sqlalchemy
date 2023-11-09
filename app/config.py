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
    LED_SERVER_UPDATE_EMPTY_PLOT = LED_SERVER_BASEURL+"/empty_plot"
    LED_SERVER_UPDATE_CONTENT = LED_SERVER_BASEURL+"/updatecontent"

    UPLOAD_FOLDER = f'{curAppPath}/upload/'

    LOGGER_PATH=f'{curAppPath}/logs/'
    TASK_FOLDER = f'{curAppPath}/tasks/'

    BACKGROUND_IMG_PATH=f'{curAppPath}/123.jpg'

    ACTIVETASK_EVERYSECONDS=60

