from .. import models


generation_functions = {}


def add_generation_function(column_name):
    def add_tog_generation_functions_for_column_name(function):
        generation_functions[column_name] = function
        return function
    return add_generation_function

class ProjectFactory(object):

    def create(**kwargs):
        for column in models.Project.itercolumns():
            print column

if __name__ == '__main__':
    ProjectFactory().create()