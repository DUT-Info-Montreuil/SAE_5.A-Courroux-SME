# Importation des modules nécessaires de flask
from flask import Blueprint
from flask_jwt_extended import (create_access_token)
from flask import Flask, request, jsonify

# Importation de UserService et du modèle User
from services.UserService import UserService
from models.User import User

# Création d'un nouveau Blueprint. C'est une façon d'organiser les routes dans Flask.
auth_bp = Blueprint('auth', __name__)

# Définition d'une route pour créer un nouvel utilisateur. Cette fonction sera appelée lorsqu'une requête POST est faite à '/user'.
@auth_bp.route('/user', methods=['POST'])
def register():
    # Récupération du nom d'utilisateur, du mot de passe, du prénom et du nom à partir des données de la requête.
    username = request.json.get('identifier')
    password = request.json.get('password')
    name = request.json.get('name')
    lastname = request.json.get('lastname')

    try:
        # Création d'un nouvel utilisateur avec les données fournies.
        UserService.create_user(username=username, password=password, name=name, lastname=lastname)

        # Si l'utilisateur a été créé avec succès, retourne un message de succès.
        return jsonify({'message': 'Nouvel utilisateur ajouté avec succès'}),200
    except Exception as e:
        # Si une erreur s'est produite lors de la création de l'utilisateur, retourne un message d'erreur.
        return jsonify({'error': str(e)}),403

# Définition d'une route pour se connecter. Cette fonction sera appelée lorsqu'une requête POST est faite à '/auth/login'.
@auth_bp.route('/auth/login', methods=['POST'])
def login():
    # Récupération du nom d'utilisateur et du mot de passe à partir des données de la requête.
    username = request.json.get('username')
    password = request.json.get('password')

    # Tentative de récupération d'un utilisateur avec le nom d'utilisateur fourni.
    user = UserService.get_by_username(username)
    if (user is not None):
        # Si un utilisateur a été trouvé et que le mot de passe fourni est correct, crée un token d'accès JWT pour l'utilisateur.
        if (user.check_password(password)):
            additional_claims = {'role': user.role}
            access_token = create_access_token(identity=user.id, additional_claims=additional_claims)
            return {'access_token': access_token}, 200
    else:
        # Si aucun utilisateur n'a été trouvé ou si le mot de passe était incorrect, retourne un message d'échec d'authentification.
        return {'message': 'Authentification échouée'}, 401