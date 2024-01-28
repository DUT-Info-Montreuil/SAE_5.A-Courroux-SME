from database.config import db
from models.Staff import Staff

# The Teacher class represents the back-end entity corresponding to a teacher
class Teacher(Staff):
    __tablename__= "teacher"
    id_teacher = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    id_user = db.Column(db.Integer, db.ForeignKey('staff.id', ondelete='CASCADE'), nullable=False)

    # Number of hours forecasted for the teacher (nullable)    
    nb_heures_previsionnelles = db.Column(db.Integer, nullable=True)
    
    # Number of hours taught by the teacher (defaulted to 0)    
    nb_heure_effectue = db.Column(db.Integer, nullable=False, default=0)

    # Activation status of the teacher (defaulted to False)
    activated = db.Column(db.Boolean, nullable=False, default=False)
    #disponibilite = db.relationship('Disponibilite', backref='disponibilite_enseignant', lazy='dynamic')
    cours = db.relationship('Cours', backref='enseignant_id', lazy='dynamic')

    # Constructor to initialize the Teacher instance with basic details
    def __init__(self,role="ROLE_TEACHER",activated= True, **kwargs):
        super().__init__(role=role,**kwargs)
        self.activated = activated

    # Method to convert the Teacher instance into a dictionary
    def to_dict(self):
        return {
            'id': self.id_teacher,
            'staff' :super().to_dict(),
            "activated": self.activated,
        }

    