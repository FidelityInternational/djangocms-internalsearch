from djangocms_moderation.models import PageModerationRequest, Workflow
from haystack import  indexes

search_models = [{"model": PageModerationRequest, "fields": [PageModerationRequest.page, PageModerationRequest.workflow]},
                 {"model": Workflow, "fields": "__all__"}]


def generate_factory_classes():

    for model_class in search_models:
        if (isinstance(model_class['fields'], str)) and (model_class['fields'] == '__all__'):
            text = indexes.CharField(document=True)

            def get_model(self):
                return model_class['model']

            created_class_name = model_class['model'].__name__+'Index'
            created_class_dict = {'get_model': get_model, 'text': text}
            created_class = type(created_class_name, (indexes.SearchIndex, indexes.Indexable,), created_class_dict)
            print('created_class %s' %created_class)




