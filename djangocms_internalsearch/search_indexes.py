from django.core.exceptions import FieldDoesNotExist


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
        for field in config.fields:
            f = None
            try:
                f = config.model._meta.get_field(field)
            except FieldDoesNotExist:
                raise
            if f:
                index_class_dict[f.name] = indexes.index_field_from_django_field(f)(
                    model_attr=f.name)
    else:
        # TODO; add the fields we get from config
        pass

    new_class = type(
        name,
        (indexes.SearchIndex, indexes.Indexable),
        index_class_dict
    )

    return new_class
