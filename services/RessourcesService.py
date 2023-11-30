from database.config import db
from models.Ressources import Ressources

class RessourcesService:

    @staticmethod
    def create_resource(name, initial, promo):
        ressource = Ressources(name, initial, promo)
        db.session.add(ressource)
        db.session.commit()
        return ressource
    
    def get_resource_by_initial(initial):
        return Ressources.query.filter_by(initial=initial).first()
    
    @staticmethod
    def get_all_ressources():
        ressources = Ressources.query.all()
        return ressources
    
    @staticmethod
    def add_ressource(name):
        return Ressources.query.get(name) is not None
    
    @staticmethod
    def delete_ressource(initial):
        resource = Ressources.query.filter_by(initial=initial).first()
        return resource
    
    @staticmethod
    def update_ressource(name, initial, promo):
        ressource = Ressources.query.filter_by(initial=initial).first()
        ressource.name = name
        ressource.promo = promo
        db.session.commit()
        return ressource
