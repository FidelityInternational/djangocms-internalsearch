import inspect
from collections import Iterable

from haystack import indexes


def create_indexes(model_config_list):
    """
    The below creates classes for haystack to index particular
    model which we have passed in our apps.py file.
    """

    for config in model_config_list:

        class_name = config.model.__name__ + 'Index'
        search_index_class = class_factory(class_name, config)

        globals()[class_name] = search_index_class


def class_factory(name, config):
    text = indexes.CharField(document=True)

    def get_model(self):
        return config.model

    index_class_dict = {"text": text, "get_model": get_model}

    if config.index is None:
        for field in config.model._meta.get_fields():
            if field.name in config.fields:
                index_class_dict['%s' % field.name] = indexes.index_field_from_django_field(field)(model_attr='%s' % field.name)

    new_class = type(
        name,
        (indexes.SearchIndex, indexes.Indexable),
        index_class_dict
    )

    return new_class
