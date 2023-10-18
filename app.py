from flask import Flask, request, jsonify
from flask_jwt_extended import (JWTManager, jwt_required, create_access_token, get_jwt_identity)
import os
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
import bcrypt
from flask_migrate import Migrate
from sqlalchemy import text, Row
from sqlalchemy.orm import session
import sqlalchemy




#Import personnalisé
#import model


load_dotenv()

app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = 'votre_clé_secrète'  # Remplacez 'votre_clé_secrète' par une clé secrète forte et sécurisée
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')

db = SQLAlchemy(app)
jwt = JWTManager(app)
migrate = Migrate(app, db)


@app.route('/user', methods=['POST'])
def register():
    identifier = request.json.get('identifier')
    password = request.json.get('password')
    role = request.json.get('role')
    name = request.json.get('name')
    lastname = request.json.get('lastname')

    try:
        # Créez un nouvel utilisateur
        new_user = User(identifier=identifier, password=password, role=role, name=name, lastname=lastname)
        
        # Ajoutez le nouvel utilisateur à la session et commettez les changements
        db.session.add(new_user)
        db.session.commit()

        # La transaction a réussi, renvoyez une réponse de succès
        return jsonify({'message': 'Nouvel utilisateur ajouté avec succès'})
    except Exception as e:
        # En cas d'erreur, annulez la transaction et renvoyez un message d'erreur
        db.session.rollback()
        return jsonify({'error': str(e)})

@app.route('/login', methods=['POST'])
def login():
    identifier = request.json.get('identifier')
    password = request.json.get('password')

    user = get_user_by_identifier(identifier)
    if (user is not None):
        # Vérifiez le nom d'utilisateur et le mot de passe (par exemple, dans une base de données)
        # Si la vérification est réussie, générez un jeton d'accès JWT
        if (user.check_password(password)):
            access_token = create_access_token(identity=identifier)
            return {'access_token': access_token}, 200
    else:
        return {'message': 'Authentification échouée'}, 401
    
@app.route('/test', methods=['GET'])
@jwt_required()
def ressource_protégée():
    current_user = get_jwt_identity()
    return {'message': 'Ceci est une ressource protégée', 'user': current_user}


@app.route('/<string:groupe_tp_user>', methods=['GET'])
def get_schedule(groupe_tp_user):

    engine = sqlalchemy.create_engine(os.environ.get('DATABASE_URL'))
    get_lessons_query = text('SELECT * FROM cours WHERE groupe = :groupe')

    # Create a connection and execute the query
    with engine.connect() as connection:
        result = connection.execute(get_lessons_query, {'groupe':groupe_tp_user})
        lessons = result.fetchall()

    return str(lessons)

def row_to_dict(row: Row) -> dict:
    """Converts a SQLAlchemy Row object to a Python dictionary."""

    try:
        columns = row.__table__.columns
    except AttributeError:
        columns = []

    return {col.name: getattr(row, col.name) for col in columns}

class User(db.Model):
    __tablename__= "user"

    id = db.Column(db.Integer, primary_key=True)
    identifier = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(64), nullable=False)
    name = db.Column(db.String(64), nullable=False)
    lastname = db.Column(db.String(64), nullable=False)


    def __init__(self, identifier, password, role, name, lastname):
        self.identifier = identifier
        self.role = role
        self.name = name
        self.lastname = lastname


        self.set_password(password)  # Utilisez la méthode pour définir le mot de passe
        
    def set_password(self, password):
        # Utilisez hashlib pour hacher le mot de passe en MD5
        salt = bcrypt.gensalt()
        self.password = bcrypt.hashpw(password.encode('utf-8'), salt)
    def check_password(self, password):
        # Vérifiez si le mot de passe fourni correspond au hachage dans la base de données
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

def get_user_by_identifier(identifier):
    user = User.query.filter_by(identifier=identifier).first()
    return user

class Enseignant(db.Model):
    __tablename__= "enseignant"

    initial = db.Column(db.String(15), primary_key=True)
    cours = db.relationship('Cours', backref='enseignant_initial', lazy='dynamic')
    

    def __init__(self, name, lastname):
        self.initial = self.set_initial(name, lastname)

    def set_initial(self, name, lastname):
        namelist=name.split(" ")
        lastnamelist=lastname.split(" ")
        initial=""
        indexChar = 0
        for c in namelist:
            initial+=c[indexChar]
        for c in lastnamelist:
            initial+=c[indexChar] 
        
        initialExist = Enseignant.query.filter_by(initial=initial).first()

        while initialExist is not None:
            indexChar+=1
            initial = ""

            for c in namelist:
                for i in range(indexChar):
                    initial+=c[i]
            for c in lastnamelist:
                initial+=c[0]
            
            initialExist = Enseignant.query.filter_by(initial=initial).first()
        
        return initial
    
class Etudiant(db.Model):
    __tablename__= "etudiant"

    id = db.Column(db.Integer, primary_key=True)

    def __init__(self, id):
        self.id = id
    
class Ressources(db.Model):
    __tablename__= "ressources"

    initial = db.Column(db.String(5), primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    cours = db.relationship('Cours', backref='ressource_initial', lazy='dynamic')

    def __init__(self, name):
        self.name=name
        self.initial = set_initial(name)

    def set_initial(name):
        namelist = name.split(" ")
        initial=""

        if namelist.length>1:
            for c in namelist:
                initial+=c[0]
        else:
            initial+=name[0]+name[1]

        return initial

class Salle(db.Model):
    __tablename__= "salle"

    nom = db.Column(db.String(64), primary_key=True)
    ordi = db.Column(db.Integer, nullable=True)
    tableauNumerique = db.Column(db.Integer, nullable=True)
    videoProjecteur = db.Column(db.Integer, nullable=True)
    cours = db.relationship('Cours', backref='salle_name', lazy='dynamic')


    def __init__(self, name, ordi, tableauNumerique, videoProjecteur):
        self.nom = name
        self.ordi = ordi
        self.tableauNumerique = tableauNumerique
        self.videoProjecteur = videoProjecteur

class Promotion(db.Model):
    __tablename__= "promotion"

    name = db.Column(db.String(64), primary_key=True)
    cours = db.relationship('Cours', backref='promotion_name', lazy='dynamic')

    def __init__(self, name):
        self.name = name

class Groupe(db.Model):
    __tablename__= "groupe"

    idGroupe = db.Column(db.String(64), primary_key=True)
    cours = db.relationship('Cours', backref='groupe_name', lazy='dynamic')

    def __init__(self, idGroupe):
        self.idGroupe =idGroupe
    
class Cours(db.Model):

    __tablename__= "cours"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    heureDebut = db.Column(db.Time, nullable=False)
    heureFin = db.Column(db.Time, nullable=False)
    enseignant = db.Column(db.String(15), db.ForeignKey('enseignant.initial'))
    ressource = db.Column(db.String(64), db.ForeignKey('ressources.initial'))
    promotion = db.Column(db.String(64), db.ForeignKey('promotion.name'))
    groupe = db.Column(db.String(64), db.ForeignKey('groupe.idGroupe'))
    salle = db.Column(db.String(64), db.ForeignKey("salle.nom"))
    appelEffectue = db.Column(db.Boolean, nullable=True)

    def __init__(self, date, heureDebut, heureFin, enseignant_initial, ressource, promotion, groupe, salle, appelEffectue):
        self.date = date
        self.heureDebut = heureDebut
        self.heureFin = heureFin
        self.enseignant_initial = enseignant_initial
        self.ressource = ressource
        self.promotion = promotion
        self.groupe = groupe
        self.salle = salle
        self.appelEffectue = appelEffectue

    def appelFait(self, appelFait):
        self.appelEffectue = appelFait 

class Absence(db.Model):
    __tablename__= "absence"

    idEtudiant = db.Column(db.Integer, primary_key=True)
    idCour = db.Column(db.Integer, primary_key=True)

    def __init__(self, idEtudiant, idCour):
        self.idEtudiant = idEtudiant
        self.idCour = idCour

with app.app_context():
    db.create_all()
    
if __name__ == '__main__':
    app.run(debug=True)