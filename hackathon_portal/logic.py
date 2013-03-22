from contextlib import closing
import urllib2

from PIL import Image

from . import models


def get_persons_with_handles_starting_with(string):
    return models.Person.query.filter(
        models.Person.yelp_handle.startswith(string)
    ).all()


def add_photo(name, data, format):
    photo_model = models.Photo(name=name, format=format)
    models.db.session.add(photo_model)
    models.db.session.commit()
    with open(photo_model.filepath, 'wb') as photo_file:
        photo_file.write(data)
    save_photo_thumbnail(photo_model)
    return photo_model


def save_photo(file, name, format):
    photo_model = models.Photo(name=name, format=format)
    models.db.session.add(photo_model)
    models.db.session.commit()
    file.save(photo_model.filepath)
    save_photo_thumbnail(photo_model)
    return photo_model


def save_photo_thumbnail(photo_model):
    photo = Image.open(photo_model.filepath)
    photo.thumbnail(photo_model.thumbnail_size, Image.ANTIALIAS)
    photo.save(photo_model.thumbnail_filepath)


def associate_photo_with_model(photo, model):
    model.photos.append(photo)
    models.db.session.commit()
    return model


def associate_photo_with_project_from_ids(photo_id, project_id):
    project = models.Project.load(project_id)
    photo = models.Photo.load(photo_id)
    return associate_photo_with_project(photo, project)

def add_project(**kwargs):
    hackathon_id = load_hackathon(kwargs.get('hackathon_num')).id
    project_members = []
    if 'member_handles' in kwargs:
        member_details = [
            {
                'name': None,
                'yelp_handle': handle
            }
            for handle in kwargs['member_handles']
        ]

        project_members = add_persons(member_details)
    project_model = models.Project.new(
        name=kwargs.get('name'),
        description=kwargs.get('description'),
        hackathon_id=hackathon_id,
        link=kwargs.get('link')
    )
    if project_members:
        project_model.persons = project_members
    return project_model

def add_handles_to_project(yelp_handles, project):
    persons = models.Person.query.filter(
        models.Person.yelp_handle.in_(yelp_handles)
    ).all()
    project.persons.extend(persons)
    models.db.session.commit()
    return persons


def remove_handles_from_project(yelp_handles, project):
    persons = models.Person.query.filter(
        models.Person.yelp_handle.in_(yelp_handles)
    ).all()
    for person in persons:
        if person in project.persons:
            project.persons.remove(person)
    models.db.session.commit()
    return persons


def load_hackathon(hackathon_num):
    try:
        return models.Hackathon.query.filter(
            models.Hackathon.number == int(hackathon_num)
        ).one()
    except:
        return models.Hackathon.new(number=int(hackathon_num))


def add_persons(persons):
    existing_persons = models.Person.query.filter(
        models.Person.yelp_handle.in_(
            [person['yelp_handle'] for person in persons]
        )
    ).all()
    existing_yelp_handles = [person.yelp_handle for person in existing_persons]
    missing_persons = [
        person for person in persons
        if person['yelp_handle'] not in existing_yelp_handles
    ]
    new_persons = [
        models.Person(
            yelp_handle=person['yelp_handle'],
            name=person['name']
        ) for person in missing_persons
    ]
    models.db.session.add_all(new_persons)
    models.db.session.commit()
    existing_persons.extend(new_persons)
    return existing_persons


def get_all_persons():
    return models.Person.query.all()


def update_project_attribute(project_id, attribute_name, attribute_value):
    project = models.Project.load(project_id)
    setattr(project, attribute_name, attribute_value)
    models.db.session.commit()
    return project


def download_image_from_url(url):
    with closing(urllib2.urlopen(url)) as conn:
        return conn.read()


def get_hackathon_numbers():
    return [hackathon.number for hackathon in models.Hackathon.query.all()]


def sort_projects_by_awards(projects):
    return sorted(projects, key=lambda project: bool(project.awards), reverse=True)
