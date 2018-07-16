from haystack import indexes
from cms.models import Placeholder, Page

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


def gen_classes(received_class):

    text = indexes.CharField(document=True)

    def get_model(self):
        return received_class

    def prepare_text(self, obj):
        return "{}".format(obj.plugin_type)

    klass_name = received_class.__name__+'SearchIndex'
    klass_dict = {'text': text, 'get_model': get_model, 'prepare_text': prepare_text}
    klass = type(klass_name, (indexes.SearchIndex, indexes.Indexable), klass_dict)

    def klass__init(self):
        super(klass, self).__init__()

    setattr(klass, "__init__", klass__init)
    this_mod[klass_name] = klass




