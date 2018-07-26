from django.utils.translation import ugettext_lazy as _

from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool


@apphook_pool.register
class InternalSearchApphook(CMSApp):
    name = _("Internal Search")
    app_name = "djangocms_internalsearch"

    def get_urls(self, page=None, language=None, **kwargs):
        return ["djangocms_internalsearch.urls"]
