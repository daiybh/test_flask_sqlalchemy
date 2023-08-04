from flask import Blueprint, jsonify, request  ,render_template

from app import db

index_router = Blueprint('index_router', __name__,url_prefix='/index')



@index_router.route('/', methods=['GET'])
def index():
    msg="Hello World!python"    
    return render_template('index.html',data=msg)

@index_router.route('/product', methods=['GET'])
def product():
    msg="Hello World!python"    
    return render_template('product.html',data=msg)


@index_router.route("/createdb", methods=["GET"])
def createdb():
    db.create_all()
    return "Database created"

