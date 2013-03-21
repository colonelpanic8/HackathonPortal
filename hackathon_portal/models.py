from flask.ext.sqlalchemy import SQLAlchemy

from . import app


db = SQLAlchemy(app)
db.Model.itercolumns = classmethod(lambda cls: cls.__table__.columns._data.iterkeys())


def model_init(self, **kwargs):
    super(db.Model, self).__init__()
    for key, value in kwargs.iteritems():
        setattr(self, key, value)
db.Model.__init__ = model_init


class Person(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    yelp_handle = db.Column(db.String(250), unique=True)

    # awards = db.relationship('Award', backref='persons')


class Hackathon(db.Model):

    id = db.Column(db.Integer, primary_key=True)


class Award(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)


ProjectToPerson = db.Table(
    'project_to_person',
    db.Model.metadata,
    db.Column('project_id', db.Integer, db.ForeignKey("project.id")),
    db.Column('person_id', db.Integer, db.ForeignKey("person.id"))
)


AwardToProject = db.Table(
    'award_to_project',
    db.Model.metadata,
    db.Column('award_id', db.Integer, db.ForeignKey('award.id')),
    db.Column('project_id', db.Integer, db.ForeignKey('project.id'))
)


class Project(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True)
    hackathon_id = db.Column(db.Integer, db.ForeignKey(Hackathon.id))
    description = db.Column(db.String(5000))
    link = db.Column(db.String(250))

    persons = db.relationship('Person', secondary=ProjectToPerson, backref='projects')
    awards = db.relationship('Award', secondary=AwardToProject, backref='projects')
