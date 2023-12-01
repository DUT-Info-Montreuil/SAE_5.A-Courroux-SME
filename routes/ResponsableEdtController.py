from flask import Blueprint, jsonify, send_from_directory, request
from functools import wraps
from flask_jwt_extended import (jwt_required, create_access_token, get_jwt_identity)
from services.ResponsableEdtService import ResponsableEdtService

responsable_edt_bp = Blueprint('responsable_edt', __name__)

@responsable_edt_bp.route('/responsables', methods=['GET'])
def get_all_responsable_edt():
    try:
        responsables_edt = ResponsableEdtService.get_all_responsable_edt()
        responsables_edt_dict = [responsable_edt.to_dict() for responsable_edt in responsables_edt]
        # Récupérer tous les enseignants
        return jsonify(responsables_edt_dict),200
    except Exception as e:
        # En cas d'erreur, annulez la transaction et renvoyez un message d'erreur
        # db.session.rollback()
        return jsonify({'error': str(e)}),403


@responsable_edt_bp.route('/responsable/<id>', methods=['GET'])
def get_by_responsable_edt(id):
    try:
        # Récupérer un enseignant avec son ID
        responsables_edt = ResponsableEdtService.get_by_id(id)
        if not responsables_edt:
            return jsonify({'error': 'Responsable Edt not found'}),403

        return jsonify(responsables_edt.to_dict()),200
    except Exception as e:
        # En cas d'erreur, annulez la transaction et renvoyez un message d'erreur
        # db.session.rollback()
        return jsonify({'error': str(e)}),403
    

@responsable_edt_bp.route('/responsable', methods=['POST'])
def create_responsable():
    data = request.json
    try:
        responsable_edt = ResponsableEdtService.create_responsable_edt(data)
        return jsonify(responsable_edt.to_dict()),200
    except Exception as e:
        return jsonify({'error': str(e)}),403



@responsable_edt_bp.route('/responsable/<id>', methods=['DELETE'])
def delete_responsable(id):
    try:
        responsable_edt = ResponsableEdtService.delete_responsable_edt(id)
        if not responsable_edt:
            return jsonify({'error': 'Responsable Edt not found'}),403
        
        return jsonify(responsable_edt.to_dict()),200
    except Exception as e:
  
        return jsonify({'error': str(e)}),403
    
@responsable_edt_bp.route('/responsable/<id>', methods=['PUT'])
def update_responsable_edt(id):
    data = request.json
    try:
        responsable_edt = ResponsableEdtService.update_responsableEdt(id, **data)
        if not responsable_edt:
            return jsonify({'error': 'Responsable edt not found'}),403
        
        return jsonify(responsable_edt.to_dict()),200
    except Exception as e:
  
        return jsonify({'error': str(e)}),403