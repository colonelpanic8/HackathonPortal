import random

from .. import logic
from .. import models


generation_functions = {}


def add_generation_function(column_name):
    def add_tag_generation_functions_for_column_name(function):
        generation_functions[column_name] = function
        return function
    return add_tag_generation_functions_for_column_name

@add_generation_function('hackathon_id')
def hackathon_id():
    return HackathonFactory.create_upsert_and_return_id()

@add_generation_function('person_id')
def person_id():
    return PersonFactory.create_upsert_and_return_id()

@add_generation_function('project_id')
def project_id():
    return ProjectFactory.create_upsert_and_return_id()

@add_generation_function('yelp_handle')
@add_generation_function('name')
def name():
   return ''.join([chr(random.randint(97, 122)) for _ in range(20)])

@add_generation_function('description')
def description():
   return ' '.join(name() for _ in range(20))

@add_generation_function('link')
def link():
    return "https://github.com/IvanMalison/HackathonPortal"

add_generation_function('number')(lambda: random.randint(1,30))


class BaseFactory(object):

    def __init__(self, model):
        self._model = model

    def create(self, **kwargs):
        model = self._model()
        for column in self._model.itercolumns():
            if column == 'id':
                continue
            value = kwargs.get(column, None)
            if value is None:
                value = generation_functions[column]()
            setattr(model, column, value)
        return model

    def create_upsert_and_return_id(self, **kwargs):
        model = self.create(**kwargs)
        models.db.session.add(model)
        models.db.session.commit()
        return model.id


HackathonFactory = BaseFactory(models.Hackathon)
ProjectFactory = BaseFactory(models.Project)
PersonFactory = BaseFactory(models.Person)
AwardFactory = BaseFactory(models.Award)


def build_hackathon_fixture(hackathon_number):
    hackathon_id = HackathonFactory.create_upsert_and_return_id(
        number=hackathon_number
    )
    projects = [
    	ProjectFactory.create(hackathon_id=hackathon_id)
        for _ in range(random.randint(4,20))
    ]
    for project in projects:
        for i in range(random.randint(2,6)):
            project.persons.append(PersonFactory.create())
        models.db.session.add(project)
    models.db.session.commit()
    return hackathon_id


def build_award_fixtures(hackathon_number):
    hackathon =  models.Hackathon.query.filter(
        models.Hackathon.number == int(hackathon_number)
    ).one()
    photo = logic.add_photo(
        'award',
        logic.download_image_from_url(
            'http://www.visittyler.com/images/award_icon.gif',
        ),
        'gif'
        )
    for _ in range(3):
        award = AwardFactory.create()
        logic.associate_photo_with_model(photo, award)
        project = hackathon.projects[random.randint(0, len(hackathon.projects)-1)]
        project.awards.append(award)
    models.db.session.commit()