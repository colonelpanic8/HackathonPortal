import os

from . import photo_directory
from . import models


def add_photo(name, data, format):
    photo_model = models.Photo(name=name, format=format)
    models.db.session.add(photo_model)
    with open(os.path.join(photo_directory, photo_model.filename), 'wb') as photo_file:
        photo_file.write(data)
    models.db.session.commit()
    return photo_model


def save_photo(file, name, extension):
    photo_model = models.Photo(name=name, format=format)
    models.db.session.add(photo_model)
    file.save(os.path.join(photo_directory, photo_model.filename))
    models.db.session.commit()
    return photo_model

def associate_photo_with_project(photo_id, project_id):
    project = models.Project.load(project_id)
    photo = models.Photo.load(project_id)
    project.photos.append(photo)
    models.db.session.commit()
    return project