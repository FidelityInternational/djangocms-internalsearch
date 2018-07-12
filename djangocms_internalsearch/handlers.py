from django.apps import apps

from .helpers import save_to_index


def update_index(sender, operation, request, token, **kwargs):
    config = apps.get_app_config('djangocms_internalsearch')
    internalsearch_models = config.cms_extension.internalsearch_models
    if sender in internalsearch_models:
        instance = kwargs['new_plugin']
        save_to_index(instance)
