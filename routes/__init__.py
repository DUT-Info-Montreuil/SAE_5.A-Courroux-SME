from flask import Flask
from .authentificationController import auth_bp
from .api_routes import api_bp
from .CoursController import cours_bp
from .UserController import user_bp
from .TeacherController import teacher_bp
from .SalleController import salle_bp
from .RessourceController import ressource_bp
from .GroupeController import groupe_bp
from .StudentController import student_bp
from .PromotionController import promotion_bp
from .ResponsableEdtController import responsable_edt_bp


def register_routes(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(cours_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(teacher_bp)
    app.register_blueprint(salle_bp)
    app.register_blueprint(ressource_bp)
    app.register_blueprint(groupe_bp)
    app.register_blueprint(promotion_bp)
    app.register_blueprint(responsable_edt_bp)
    app.register_blueprint(student_bp)

# Exportez la fonction pour l'utiliser dans app.py