from __future__ import unicode_literals

from django.apps import AppConfig, apps
from django.utils.translation import ugettext_lazy as _

from .handlers import update_index


class InternalsearchConfig(AppConfig):
    name = 'djangocms_internalsearch'
    verbose_name = _('django CMS Internal Search')

    def ready(self):
        from cms.signals import (
            post_obj_operation,
            post_placeholder_operation
        )

        post_obj_operation.connect(update_index)
        post_placeholder_operation.connect(update_index)

        """
        We call the generate class function here to generate the model search indexes for haystack.
        """
        from .search_indexes import generate_search_index_classes
        internalsearch_config = apps.get_app_config('djangocms_internalsearch')
        model_list = internalsearch_config.cms_extension.internalsearch_models
        generate_search_index_classes(model_list)
