from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from services.AffiliationRespEdtService import AffiliationRespEdtService
from services.ResponsableEdtService import ResponsableEdtService
from services.UserService import UserService
from models.User import User

affiliationrespedt_bp = Blueprint('affiliationrespedt', __name__)



@affiliationrespedt_bp.route('/affiliateRespEdt', methods=['POST'])
def affiliate_respedt_to_promo():

    idResp = request.json["id_resp"]
    idPromo = request.json["id_promo"]
    
    try:
        # Associer un respEdt à une promo
        affiliate_respEdt = AffiliationRespEdtService.affiliate_respedt_to_promo(idResp,idPromo)

        return jsonify(affiliate_respEdt.to_dict()),200
    except Exception as e:
        # En cas d'erreur, annulez la transaction et renvoyez un message d'erreur
        # db.session.rollback()
        return jsonify({'error': str(e)}),403


@affiliationrespedt_bp.route('/affiliateRespEdt/getPromosByResp/<idResp>', methods=['GET'])
def get_promos_for_respedt(idResp):

    try:
        # Associer un respEdt à une promo
        promotions = AffiliationRespEdtService.get_promos_for_respedt(idResp)

        if not promotions:
            return jsonify({'error': 'Promotions not found'}),201

        return jsonify([promotion.to_dict() for promotion in promotions]),200
    except Exception as e:
        return jsonify({'error': str(e)}),403



@affiliationrespedt_bp.route('/affiliateRespEdt/delete/<idResp>', methods=['DELETE'])
def delete_affiliate_respedt_to_promo(idResp):
    
    try:
        # Associer un respEdt à une promo
        affiliate_respEdt = AffiliationRespEdtService.delete_respEdt_promo(idResp)
        
        return jsonify({"message": "RespEdtPromo supprimé du groupe avec succès"}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 403
    

@affiliationrespedt_bp.route('/responsable/promos', methods=['GET'])
@jwt_required()
def get_promos_for_respedt_by_user(idUser):

    try:
        # Associer un respEdt à une promo
        current_user = get_jwt_identity()
        user : User = UserService.get_by_id(current_user)
        respEdt= ResponsableEdtService.get_by_userId(user.id)
        promotions = AffiliationRespEdtService.get_promos_for_respedt(respEdt.id_resp)

        if not promotions:
            return jsonify({'error': 'Promotions not found'}),201

        return jsonify([promotion.to_dict() for promotion in promotions]),200
    except Exception as e:
        return jsonify({'error': str(e)}),403

