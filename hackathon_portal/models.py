from flask.ext.sqlalchemy import SQLAlchemy
import simplejson
from sqlalchemy.types import TypeDecorator, VARCHAR
from sqlalchemy.orm.exc import NoResultFound

from . import app
from . import common


db = SQLAlchemy(app)
db.Model.itercolumns = classmethod(lambda cls: cls.__table__.columns._data.iterkeys())


class ProjectMember(db.Model):
    pass


class Project(db.model):
    pass
