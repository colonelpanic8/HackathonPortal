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


def add_project(name, description, member_handles, hackathon_num):
    hackathon_id = load_hackathon(hackathon_num).id
    member_details = [
        {
            'name': None,
            'yelp_handle': handle
        }
        for handle in member_handles
    ]
    project_members = add_persons(member_details)
    project_model = models.Project.new(
        name=name,
        description=description,
        hackathon_id=hackathon_id,
    )
    project_model.persons = project_members

def load_hackathon(hackathon_num):
    try:
        return models.Hackathon.query.filter(
            models.Hackathon.number == int(hackathon_num)
        ).one()
    except:
        return models.Hackathon.new(
            number=int(hackathon_num)
        )

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
