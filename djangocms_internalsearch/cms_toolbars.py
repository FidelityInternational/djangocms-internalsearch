# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import override as force_language, ugettext_lazy as _
from cms.toolbar_base import CMSToolbar
from cms.toolbar_pool import toolbar_pool
from django.core.urlresolvers import reverse


@toolbar_pool.register
class InternalSearchToolbar(CMSToolbar):

    def populate(self):
        menu = self.toolbar.get_or_create_menu('internalsearch-app', _('Content Search'))
        url = reverse('search')
        menu.add_sideframe_item(_('Page Template Search'), url='#')
        menu.add_break('Plugin', position=None)
        menu.add_sideframe_item(_('Plugin Search'), url=url)
