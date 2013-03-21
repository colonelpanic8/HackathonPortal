import mock


generation_functions = {}


def add_generation_function(column_name):
    def add_to_generation_functions_for_column_name(function):
        generation_functions[column_name] = function
        return function
    return add_generation_function


def build_mock_project(**gs)
    