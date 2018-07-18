from haystack import indexes
from cms.models import Placeholder, Page
from types import ModuleType
from functools import partial

this_mod = globals()

'''
The below creates a class for haystack to index 
particular model which we have passed in our 
apps.py file.
'''


# class PageSearchIndex(indexes.SearchIndex, indexes.Indexable):
#
#     text = indexes.CharField(document=True)
#     created_by = indexes.CharField(model_attr="created_by", faceted=True)
#     placeholders = indexes.MultiValueField()
#
#     def get_model(self):
#         return Page
#
#     def index_queryset(self, using=None):
#         return self.get_model().objects.all()
#
#     def prepare_placeholders(self, object):
#         return [placeholders.slot for placeholders in object.placeholders.all()]


# class PlaceholderSearchIndex(indexes.SearchIndex, indexes.Indexable):
#
#     text = indexes.CharField(document=True)
#     slot = indexes.CharField(model_attr="slot")
#
#     def get_model(self):
#         return Placeholder
#
#     def index_queryset(self, using=None):
#         return self.get_model().objects.all().values()


def gen_classes(model_list):

    for model_class in model_list:




        #def prepare_text(self, obj):
        #    return "{}".format(obj.plugin_type)

        index_class_name = model_class.__name__ + 'SearchIndex'
        index_class_created = class_factory(index_class_name, model_class) #type(index_class_name, (indexes.SearchIndex, indexes.Indexable), index_class_dict)

        this_mod[index_class_name] = index_class_created


class BaseClass:
    def __init__(self, class_type):
        self._type = class_type


def class_factory(name, model_class, BaseClass=BaseClass):

    def __init__(self):
        BaseClass.__init__(self, name)

    text = indexes.CharField(document=True)

    def get_model(self):
        return model_class

    # def prepare_text(self, obj):
    #    return "{}".format(obj.plugin_type)

    index_class_dict = {"__init__": __init__, "text": text, "get_model": get_model}

    new_class = type(name, (BaseClass, indexes.SearchIndex, indexes.Indexable), index_class_dict)

    return new_class

