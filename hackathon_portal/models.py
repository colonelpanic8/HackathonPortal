from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.types import TypeDecorator, VARCHAR
from sqlalchemy.orm.exc import NoResultFound

from . import app


db = SQLAlchemy(app)
db.Model.itercolumns = classmethod(lambda cls: cls.__table__.columns._data.iterkeys())


class Person(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    yelp_id = db.Column(db.String(250))

    def __init__(self, name="", yelp_id=""):
        self.name = name
        self.yelp_id = yelp_id


class Hackathon(db.Model):

    id = db.Column(db.Integer, primary_key=True)


class Project(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True)
    hackathon = db.Column(db.Integer, db.ForeignKey(Hackathon.id))
    description = db.Column(db.String(5000))
    link = db.Column(db.String(250))

    def __init__(self, name="", hackathon=0, description="", link=""):
        self.name = name
        self.hackathon = hackathon
        self.description = description
        self.link = link


class ProjectToPerson(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey(Project.id))
    person_id = db.Column(db.Integer, db.ForeignKey(Person.id))

    def __init__(self, project_id, person_id):
        self.project_id = project_id
        self.person_id = person_id


class Award(db.model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)

    def __init__(self, name):
        self.name = name


class AwardToProject(db.model):

    id = db.Column(db.Integer, primary_key=True)
    hackathon_id = db.Column(db.Integer, db.ForeignKey(Hackathon.id))
    award_id = db.Column(db.Integer, db.ForeignKey(Award.id))
    project_id = db.Column(db.Integer, db.ForeignKey(project.id))

    def __init__(self, hackathon_id, award_id, project_id):
        self.hackathon_id = hackathon_id
        self.award_id = award_id
        self.project_id = project_id
