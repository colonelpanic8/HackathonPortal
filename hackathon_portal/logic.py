from . import models


def get_persons_with_handles_starting_with(string):
    return models.Person.query.filter(
    	models.Person.startswith(string)
    ).all()


def add_photo(name, data, format):
    photo_model = models.Photo(name=name, format=format)
    models.db.session.add(photo_model)
    models.db.session.commit()
    with open(photo_model.filepath, 'wb') as photo_file:
        photo_file.write(data)
    return photo_model


def save_photo(file, name, format):
    photo_model = models.Photo(name=name, format=format)
    models.db.session.add(photo_model)
    # TODO: can we move this to after the save?
    models.db.session.commit()
    file.save(photo_model.filepath)
    return photo_model


def associate_photo_with_project(photo_id, project_id):
    project = models.Project.load(project_id)
    photo = models.Photo.load(photo_id)
    project.photos.append(photo)
    models.db.session.commit()
    return project


def update_project_attribute(project_id, attribute_name, attribute_value):
    project = models.Project.load(project_id)
    setattr(project, attribute_name, attribute_value)
    models.db.session.commit()
    return project