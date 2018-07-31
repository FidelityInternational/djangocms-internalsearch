from django.core.exceptions import FieldDoesNotExist

from haystack import indexes


def create_indexes(model_config_list, internalsearch_indexes):
    """
    The below creates classes for haystack to index particular
    model which we have passed in our apps.py file.
    """

    for config in model_config_list:

        search_index_class = None
        if config.index is None:
            search_index_class = class_factory(config)
        else:
            search_index_class = config.index

        internalsearch_indexes.unified_index._indexes[config.model] = search_index_class


def class_factory(config):
    text = indexes.CharField(document=True)

    def get_model(self):
        return config.model

    index_class_dict = {"text": text, "get_model": get_model}

    for field in config.fields:
        f = None
        try:
            f = config.model._meta.get_field(field)
        except FieldDoesNotExist:
            raise
        if f:
            index_class_dict[f.name] = indexes.index_field_from_django_field(f)(
                model_attr=f.name)

    class_name = config.model.__name__ + 'Index'
    new_class = type(
        class_name,
        (indexes.SearchIndex, indexes.Indexable),
        index_class_dict
    )

    return new_class
