import inspect
from collections import Iterable

from haystack import indexes


this_mod = locals()


def generate_search_index_classes(model_list):

    # The below creates a class for haystack to index particular model which we have passed in our apps.py file.

    if not isinstance(model_list, Iterable):
        raise TypeError("Generate method expects a list or tuple")

    for model in model_list:

        if not inspect.isclass(model):
            raise TypeError("Model is not a class object")

        index_name = model.__name__ + 'Index'
        index_created = class_factory(index_name, model)

        this_mod[index_name] = index_created

        if not inspect.isclass(index_created):
            raise TypeError("Created search index is not a object instance")


class BaseClass:
    def __init__(self, name):
        self._type = name


def class_factory(name, model, BaseClass=BaseClass):

    text = indexes.CharField(document=True, use_template=True)

    def __init__(self):
        BaseClass.__init__(self, name)

    def get_model(self):
        return model

    index_class_dict = {"__init__": __init__, "text": text, "get_model": get_model}
    new_class = type(name, (BaseClass, indexes.SearchIndex, indexes.Indexable), index_class_dict)

    return new_class