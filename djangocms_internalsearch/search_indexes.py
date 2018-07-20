from haystack import indexes
from cms.models import Placeholder, Page, CMSPlugin
from types import ModuleType
from functools import partial
import inspect
from django.core.exceptions import ImproperlyConfigured
from collections import Iterable

this_mod = globals()

'''
The below creates a class for haystack to index 
particular model which we have passed in our 
apps.py file.
'''


# class PageSearchIndex(indexes.SearchIndex, indexes.Indexable):
#
#     text = indexes.CharField(document=True, use_template=True)
#     created_by = indexes.CharField(model_attr="created_by")
#     # placeholders = indexes.MultiValueField()
#
#     def get_model(self):
#         return Page
#
#     def index_queryset(self, using=None):
#         return self.get_model().objects.all()
#
#     def prepare_placeholders(self, object):
#         return [placeholders.slot for placeholders in object.placeholders.all()]
#
#
# class PlaceholderSearchIndex(indexes.SearchIndex, indexes.Indexable):
#
#     text = indexes.CharField(document=True, use_template=True)
#     slot = indexes.CharField(model_attr="slot")
#
#     def get_model(self):
#         return Placeholder
#
#     def index_queryset(self, using=None):
#         return self.get_model().objects.all()
#
#
# class CMSPluginSearchIndex(indexes.SearchIndex, indexes.Indexable):
#
#     text = indexes.CharField(document=True, use_template=True)
#     plugin_type = indexes.CharField(model_attr="plugin_type")
#
#     def get_model(self):
#         return CMSPlugin


def generate_search_index_classes(model_list):

    if not isinstance(model_list, Iterable):
        raise TypeError("expects a list or tuple")

    for model_class in model_list:

        if not inspect.isclass(model_class):
            raise TypeError("not a class object")

        index_class_name = model_class.__name__ + 'Index'
        index_class_created = class_factory(index_class_name, model_class)

        this_mod[index_class_name] = index_class_created

        if not inspect.isclass(index_class_created):
            raise TypeError("not a object instance")
    return index_class_created


class BaseClass:
    def __init__(self, class_type):
        self._type = class_type


def class_factory(name, model_class, BaseClass=BaseClass):

    def __init__(self):
        BaseClass.__init__(self, name)

    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return model_class

    index_class_dict = {"__init__": __init__, "text": text, "get_model": get_model}
    new_class = type(name, (BaseClass, indexes.SearchIndex, indexes.Indexable), index_class_dict)

    return new_class

