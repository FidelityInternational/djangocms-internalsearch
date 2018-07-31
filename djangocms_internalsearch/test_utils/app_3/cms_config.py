from cms.app_base import CMSAppConfig

from .models import TestModel5, TestModel6


class TestModel1Config:
    model = TestModel5
    fields = ['name', 'date', 'text']


class TestModel2Config:
    model = TestModel6
    fields = ['name', 'date', 'text']


class CMSApp2Config(CMSAppConfig):
    djangocms_internalsearch_enabled = True
    internalsearch_config_list = [TestModel1Config, TestModel2Config]
