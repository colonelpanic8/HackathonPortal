import random

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


class BaseFactory(object):

    def __init__(self, model):
        self._model = model

    def create(self, **kwargs):
        model = self._model()
        for column in self._model.itercolumns():
            if column == 'id':
                continue
            setattr(model, column,  kwargs.get(column, generation_functions[column]()))
        return model

    def create_upsert_and_return_id(self, **kwargs):
        model = self.create(**kwargs)
        models.db.session.add(model)
        models.db.session.commit()
        return model.id


HackathonFactory = BaseFactory(models.Hackathon)
ProjectFactory = BaseFactory(models.Project)
PersonFactory = BaseFactory(models.Person)


if __name__ == '__main__':
    ProjectFactory().create()