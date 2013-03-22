import os

from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.util import classproperty

from . import app
from . import photo_directory


db = SQLAlchemy(app)

def new(cls, **kwargs):
    model = cls(**kwargs)
    db.session.add(model)
    db.session.commit()
    return model

def model_init(self, **kwargs):
    super(db.Model, self).__init__()
    for key, value in kwargs.iteritems():
        setattr(self, key, value)

db.Model.__init__ = model_init
db.Model.itercolumns = classmethod(lambda cls: cls.__table__.columns._data.iterkeys())
db.Model.load = classmethod(lambda cls, id: cls.query.filter(cls.id == id).one())
db.Model.new = classmethod(new)


class Photo(db.Model):

    base_url = os.path.join('/', 'static', 'photo')

    # TODO: make all of these columns write once.
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    format = db.Column(db.String(10))

    @property
    def filename(self):
        return "{name}-{id}.{extension}".format(
            id=str(self.id),
            name=self.name,
            extension=self.format
        )

    @property
    def filepath(self):
        return os.path.join(photo_directory, self.filename)

    @property
    def url(self):
        return os.path.join(self.base_url, self.filename)


class Person(db.Model):

    base_url = os.path.join('/', 'person')

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    yelp_handle = db.Column(db.String(250), unique=True)

    def __str__(self):
        return "{name} {yelp_handle}".format(
            name=self.name or '',
            yelp_handle='<%s>' % self.yelp_handle if self.yelp_handle else ''
        )

    @classproperty
    def get_handles_starting_with_url(cls):
        return os.path.join(cls.base_url, 'get_handles_matching')

    @property
    def url(self):
        return self.view_url(self.yelp_handle)

    @classmethod
    def view_url(cls, identifier):
        return os.path.join(cls.base_url, 'view', identifier)


class Hackathon(db.Model):

    base_url = os.path.join('/', 'hackathon')

    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer)
    projects = db.relationship('Project', backref='hackathon')

    @property
    def project_count(self):
        return len(self.projects)

    @property
    def url(self):
        return self.view_url(str(self.number))

    @classmethod
    def view_url(cls, identifier):
        return os.path.join(cls.base_url, 'view', identifier)


class Award(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)


ProjectToPerson = db.Table(
    'project_to_person',
    db.Model.metadata,
    db.Column('project_id', db.Integer, db.ForeignKey("project.id")),
    db.Column('person_id', db.Integer, db.ForeignKey("person.id"))
)


ProjectToPhoto = db.Table(
    'project_to_photo',
    db.Model.metadata,
    db.Column('project_id', db.Integer, db.ForeignKey("project.id")),
    db.Column('photo_id', db.Integer, db.ForeignKey("photo.id"))
)


ProjectToAward = db.Table(
    'project_to_award',
    db.Model.metadata,
    db.Column('award_id', db.Integer, db.ForeignKey('award.id')),
    db.Column('project_id', db.Integer, db.ForeignKey('project.id'))
)


class Project(db.Model):

    base_url = os.path.join('/', 'project')

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    hackathon_id = db.Column(db.Integer, db.ForeignKey(Hackathon.id))
    description = db.Column(db.String(5000))
    link = db.Column(db.String(250))

    persons = db.relationship('Person', secondary=ProjectToPerson, backref='projects')
    photos = db.relationship('Photo', secondary=ProjectToPhoto, backref='projects')
    awards = db.relationship('Award', secondary=ProjectToAward, backref='projects')

    @property
    def url(self):
        return self.view_url(str(self.id))

    @classmethod
    def update_url(self, attribute_name):
        return os.path.join(self.base_url, 'update', attribute_name)

    @classmethod
    def view_url(cls, identifier):
        return os.path.join(cls.base_url, 'view', identifier)

    @classproperty
    def add_url(cls):
        return os.path.join(cls.base_url, 'add')

    @classproperty
    def add_photo_url(cls):
        return os.path.join(cls.add_url, 'photo')

    @classproperty
    def add_person_url(cls):
        return os.path.join(cls.add_url, 'person')