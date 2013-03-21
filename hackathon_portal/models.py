from flask.ext.sqlalchemy import SQLAlchemy
import simplejson
from sqlalchemy.types import TypeDecorator, VARCHAR
from sqlalchemy.orm.exc import NoResultFound

from . import app
from . import common


db = SQLAlchemy(app)
db.Model.itercolumns = classmethod(lambda cls: cls.__table__.columns._data.iterkeys())


class Project(db.model):

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


class Person(db.model):

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(250))
	yelp_id = db.Column(db.String(250))

	def __init__(self, name="", yelp_id=""):
		self.name = name
		self.yelp_id = yelp_id


class Hackathon(db.model):

	id = db.Column(db.Integer, primary_key=True)


class ProjectToPerson(db.model):

	id = db.Column(db.Integer, primary_key=True)
	project_id = db.Column(db.Integer, db.ForeignKey(Project.id))
	person_id = db.Column(db.Integer, db.ForeignKey(Person.id))

	def __init__(self, project_id, person_id):
		self.project_id = project_id
		self.person_id = person_id
