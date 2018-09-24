from __future__ import unicode_literals

from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

from .helpers import save_to_index, page_content_change_receiver


class InternalsearchConfig(AppConfig):
    name = 'djangocms_internalsearch'
    verbose_name = _('django CMS Internal Search')

    def ready(self):
        from cms.signals import (
            post_obj_operation,
            post_placeholder_operation
        )
        from .signals import content_object_change_signal

        post_obj_operation.connect(save_to_index)
        post_placeholder_operation.connect(save_to_index)

        # listen for page content version changes
        content_object_change_signal.connect(page_content_change_receiver)
