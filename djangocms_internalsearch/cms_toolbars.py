from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from cms.toolbar_pool import toolbar_pool
from cms.toolbar_base import CMSToolbar

@toolbar_pool.register
class InternalSearchToolbar(CMSToolbar):

    def populate(self):
        #TODO: make url dynamic
        menu = self.toolbar.add_button('Internal search', '/admin/djangocms_internalsearch')
