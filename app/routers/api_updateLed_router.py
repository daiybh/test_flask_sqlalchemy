from flask import Blueprint, jsonify, request
from app.models.user import User
from app import db

api_updateLed_router = Blueprint('api_updateLed_router', __name__,url_prefix='/api')
@api_updateLed_router.route('/updates', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])
