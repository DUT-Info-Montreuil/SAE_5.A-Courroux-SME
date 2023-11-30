from database.config import db
from models.Salle import Salle

class SalleService:

    @staticmethod
    def create_salle(nom, ordi, tableauNumerique, videoProj):
        salle = Salle(nom=nom, ordi=ordi, tableauNumerique=tableauNumerique, videoProjecteur=videoProj)

        db.session.add(salle)
        db.session.commit()

        return salle
    
    @staticmethod
    def isExist(nom):
        return Salle.query.filter_by(nom=nom).first() is not None
    
    @staticmethod
    def get_all_salles():
        return Salle.query.all()
    
    @staticmethod
    def get_salle_by_name(nom):
        return Salle.query.filter_by(nom=nom).first()
    
    @staticmethod
    def delete_salle(nom):
        salle = SalleService.get_salle_by_name(nom)
        db.session.delete(salle)
        db.session.commit()