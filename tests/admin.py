from django.contrib import admin
from tests.core.models import MockModel
from haystack.admin import SearchModelAdmin


class MockModelAdmin(SearchModelAdmin):
    haystack_connection = "elasticsearch"
    list_display = ("foo",)


admin.site.register(MockModel, MockModelAdmin)
