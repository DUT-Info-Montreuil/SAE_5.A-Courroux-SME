from database.config import db
from models.User import User

# The Student class represents the back-end entity corresponding to a student
class Student(User):
    __tablename__= "student"
    id_student = db.Column(db.BigInteger, primary_key=True, autoincrement=True)

    # User identifier associated with the student (foreign key referencing the User table)    
    id_user = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    INE = db.Column(db.String(64), unique=True, nullable=False)
    # etudiantGroupe = db.relationship('EtudiantGroupe', backref='etudiant_appartient_groupe', lazy='dynamic')
    # absence = db.relationship('Absence', backref='idUser', lazy='dynamic')


    # Constructor to initialize the Student instance with basic details
    def __init__(self,INE, role="ROLE_STUDENT", **kwargs):
        super().__init__(role=role,**kwargs)
        self.INE = INE

    # Method to convert the Student instance into a dictionary
    def to_dict(self):
        return {
            'id': self.id_student,
            'user' :super().to_dict()
        }

    