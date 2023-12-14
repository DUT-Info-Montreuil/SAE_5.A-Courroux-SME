from operator import and_

from database.config import db
from models.Cours import Cours
from datetime import datetime, timedelta

from services.GroupeService import GroupeService

class CoursService:

    @staticmethod
    def create_course(data):

        resp, code = CoursService.can_create_course(**data)
        if code >= 400:
            print(resp)
            return resp, code

        course = Cours(**data)
        
        db.session.add(course)
        db.session.commit()

        result = course.to_dict()
        if code > 200:
            result.update(resp)
            return result, code

        return course, 200
    
    def get_course_by_id(id):
        return Cours.query.get(id)
    
    @staticmethod
    def get_all_courses(args, publish = True):

        query = Cours.query

        if 'date_min' in args:
            date_start = datetime.strptime(args["date_min"], '%Y-%m-%d')
            print(date_start)
            query = query.filter(Cours.end_time >= date_start)

        if 'date_max' in args:
            date_end = datetime.strptime(args["date_max"], '%Y-%m-%d') + timedelta(days=1)
            print(date_end)
            query = query.filter(Cours.start_time < date_end)

        # if publish:
        #     query = query.filter(Cours.is_published == publish)

        if 'room' in args:
            query = query.filter(Cours.name_salle == args["room"])
        if 'teacher' in args:
            query = query.filter(Cours.id_enseignant == args["teacher"])
        if 'group' in args:
            query = query.filter(Cours.id_group == args["group"])
        if 'resource' in args:
            query = query.filter(Cours.initial_ressource == args["resource"])

        return query.all()
    
    @staticmethod
    def delete_course(id):
        course = Cours.query.get(id)
        if course.is_published == 1:
            course.is_published = 2
        else:
            db.session.delete(course)
        db.session.commit()
        
        return course
    
    @staticmethod
    def update_course(id, start_time, end_time, initial_ressource, id_group, name_salle = None,id_enseignant= None, **kwargs):
        course = Cours.query.get(id)


        resp, code = CoursService.can_create_course(start_time=start_time, end_time=end_time, id_group=id_group, name_salle=name_salle, id_enseignant=id_enseignant, id_cours=id)
        if code >= 400:
            return resp, code
        
        course_duplicate = course.duplicate()

        course_duplicate.start_time = start_time
        course_duplicate.end_time = end_time
        course_duplicate.id_enseignant = id_enseignant if id_enseignant else db.null()
        course_duplicate.initial_ressource = initial_ressource
        course_duplicate.id_group = id_group
        course_duplicate.name_salle = name_salle if name_salle else db.null()
        course_duplicate.is_published = 0

        db.session.add(course_duplicate)
        db.session.commit()

        
        CoursService.delete_course(course.id)


        result = course_duplicate.to_dict()
        if code > 200:
            result.update(resp)
            return result, code

        return course_duplicate, 200
    

    @staticmethod
    def can_create_course(start_time, end_time, id_group, name_salle = None, id_enseignant = None,id_cours= None,   **kwargs):

        if type(start_time) != str:
            start_time = start_time.strftime("%Y-%m-%d %H:%M:%S")
        if type(end_time) != str:
            end_time = end_time.strftime("%Y-%m-%d %H:%M:%S")

        if start_time >= end_time:
            return {"response" : "start_time doit être inférieur à end_time"}, 400

        try:
            group_depends = GroupeService.get_tree(id_group)
        except Exception as e:
            print(e)
            return {"response" : "Groupe introuvable"}, 404
            


        warning: str = ""

        for group in group_depends:

            if not id_cours:
                query = Cours.query
            else:
                query = Cours.query.filter(Cours.id != id_cours).filter(Cours.is_published != 2)

            current_group = GroupeService.get_groupe_by_id(group)
            #Si un cours est déjà prévu entre start_time et end_time
            courses = query.filter_by(id_group=group).filter(and_(Cours.start_time > start_time, Cours.start_time < end_time)).all()
            if len(courses) > 0: return {"error" :f"Le groupe {current_group.name} à déjà cours !"}, 409
            courses = query.filter_by(id_group=group).filter(and_(Cours.end_time > start_time, Cours.end_time < end_time)).all()
            if len(courses) > 0: return {"error" :f"Le groupe {current_group.name} à déjà cours !"}, 409

            courses = query.filter_by(id_group=group).filter(and_(Cours.start_time == start_time, Cours.end_time == end_time)).all()
            if len(courses) > 0: return {"error" :f"Le groupe {current_group.name} à déjà cours !"}, 409

            #Si une salle est déjà prise entre start_time et end_time
            if name_salle:
                courses = query.filter_by(name_salle=name_salle).filter(Cours.start_time > start_time).filter(Cours.start_time < end_time).all()
                if len(courses) > 0: return {"error" :"Cette salle est déjà prise"},409

                courses = query.filter_by(name_salle=name_salle).filter(Cours.end_time > start_time).filter(Cours.end_time < end_time).all()
                if len(courses) > 0: return {"error" :"Cette salle est déjà prise"},409


            if id_enseignant:
                courses = query.filter_by(id_enseignant=id_enseignant).filter(Cours.start_time > start_time).filter(Cours.start_time < end_time).all()
                if len(courses) > 0: warning = "Attention ! Ce professeur à déjà un cours dans cette plage horaire"

                courses = query.filter_by(id_enseignant=id_enseignant).filter(Cours.end_time > start_time).filter(Cours.end_time < end_time).all()
                if len(courses) > 0: warning = "Attention ! Ce professeur à déjà un cours dans cette plage horaire"


        if warning != "":
            return {"warning" : warning}, 201
        
        return None, 200
    
    @staticmethod
    def publish():
        courses = Cours.query.filter_by(is_published=0).all()
        for course in courses:
            course.is_published = 1
        db.session.commit()

        courses_delete = Cours.query.filter_by(is_published=2).all()
        for course in courses_delete:
            db.session.delete(course)
        db.session.commit()
        return courses
    
    @staticmethod
    def cancel():
        courses = Cours.query.filter_by(is_published=0).all()
        for course in courses:
            db.session.delete(course)
        db.session.commit()

        courses = Cours.query.filter_by(is_published=2).all()
        for course in courses:
            course.is_published = 1
        db.session.commit()


        return courses
    
    @staticmethod
    def duplicate(start_time, end_time, id_group, start_time_attempt, **kwargs):

        start_time = datetime.strptime(start_time, '%Y-%m-%d')
        print(start_time)
        end_time = datetime.strptime(end_time, '%Y-%m-%d') + timedelta(days=1)
        print(end_time)
        start_time_attempt = datetime.strptime(start_time_attempt, '%Y-%m-%d')
        print(start_time_attempt)

        days_diff = (start_time_attempt - start_time).days
        print(days_diff)


        end_time_attempt = end_time + timedelta(days=days_diff)

        groups = GroupeService.get_tree(id_group)


        for group in groups:
            courses = Cours.query.filter_by(id_group=group).filter(and_(Cours.end_time >= start_time_attempt, Cours.start_time < end_time_attempt)).all()
            for course in courses:
                # return {"error" :f"Le groupe {group} à déjà cours !"}, 409
                db.session.delete(course)
        db.session.commit()



        result = []
        for group in groups:
            courses = Cours.query.filter_by(id_group=group).filter(and_(Cours.end_time >= start_time, Cours.start_time < end_time)).all()
            for course in courses:
                new_course = course.duplicate()
                new_course.start_time = course.start_time + timedelta(days=days_diff)
                new_course.end_time = course.end_time + timedelta(days=days_diff)
                db.session.add(new_course)
                db.session.commit()
                result.append(new_course)

        return result
    
    
    


    

