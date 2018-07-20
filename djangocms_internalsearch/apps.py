from __future__ import unicode_literals

from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

from .handlers import do_search_action


class InternalsearchConfig(AppConfig):
    name = 'djangocms_internalsearch'
    verbose_name = _('django CMS Internal Search')

    def ready(self):
        from cms.signals import (
            post_obj_operation,
            post_placeholder_operation
        )

        post_obj_operation.connect(do_search_action)
        post_placeholder_operation.connect(do_search_action)
        '''
        We call the generate class function here to 
        generate the model search indexes for haystack.
        '''
        from .search_indexes import generate_search_index_classes
        from cms.models import CMSPlugin, Page, Placeholder
        from djangocms_text_ckeditor.models import Text
        class_list = [CMSPlugin, Page, Placeholder, Text]
        generate_search_index_classes(class_list)
        # from .search_fields import generate_factory_classes
        # generate_factory_classes()
