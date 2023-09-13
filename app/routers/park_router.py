from flask import Blueprint, jsonify, request
from app.models.park import Park
from app import db,app

park_router = Blueprint('park_router', __name__)

@park_router.route('/parks', methods=['GET'])
def get_parks():
    parks = Park.query.all()
    return jsonify([park.to_dict() for park in parks])

@park_router.route('/parks/<int:park_id>', methods=['GET'])
def get_park(park_id):
    park = Park.query.get(park_id)
    if park:
        return jsonify(park.to_dict())
    else:
        return jsonify({'error': 'Park not found'})
import os
@park_router.route('/parks', methods=['POST'])
def create_park():
    lsprjfile=""
    try:
        data = request.get_json()
    except:
        data = request.values
        file = request.files['file']
        if not file:
            return "no file"
        lsprjfile = os.path.join(app.config['UPLOAD_FOLDER'],
                                 f'{data["park_id"]}.lsprj')
        app.logger.warning("create_park lsprjfile:{}".format(lsprjfile))
        file.save(lsprjfile)

    park = Park(name=data['park_name']
                , park_id=data['park_id']
                , pgmfilepath=lsprjfile)
    db.session.add(park)
    db.session.commit()
    return jsonify(park.to_dict())

@park_router.route('/parks/<int:park_id>', methods=['PUT'])
def update_park(park_id):
    park = Park.query.get(park_id)
    if park:
        data = request.get_json()
        park.name = data['name']
        park.park_id = data['park_id']
        park.pgmfilepath = data['pgmfilepath']
        db.session.commit()
        return jsonify(park.to_dict())
    else:
        return jsonify({'error': 'Park not found'})

@park_router.route('/parks/<int:park_id>', methods=['DELETE'])
def delete_park(park_id):
    park = Park.query.get(park_id)
    if park:
        db.session.delete(park)
        db.session.commit()
        return jsonify({'message': 'Park deleted successfully'})
    else:
        return jsonify({'error': 'Park not found'})
