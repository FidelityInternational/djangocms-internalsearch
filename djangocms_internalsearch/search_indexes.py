import inspect
from collections import Iterable

from haystack import indexes


this_module = globals()


def generate_search_index_classes(model_list):

    # The below creates a class for haystack to index particular model which we have passed in our apps.py file.

    if not isinstance(model_list, Iterable):
        raise TypeError("Generate method expects a list or tuple")

    for model in model_list:

        if not inspect.isclass(model):
            raise TypeError("Model is not a class object")

        index_name = model.__name__ + 'Index'
        search_index = class_factory(index_name, model)

        this_module[index_name] = search_index

        if not inspect.isclass(search_index):
            raise TypeError("Created search index is not a object instance")


def class_factory(name, model):

    text = indexes.CharField(document=True)

    def get_model(self):
        return model

    index_class_dict = {"text": text, "get_model": get_model}
    new_class = type(name, (indexes.SearchIndex, indexes.Indexable), index_class_dict)

    return new_class
