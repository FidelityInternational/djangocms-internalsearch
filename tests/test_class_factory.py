from django.apps import apps
from django.test import TestCase

from cms import app_registration
from cms.test_utils.testcases import CMSTestCase
from cms.utils.setup import setup_cms_apps

from djangocms_internalsearch.search_indexes import (
    generate_search_index_classes,
)
from djangocms_internalsearch.test_utils.app_2.cms_config import (
    TestModel1Config,
    TestModel2Config,
)
from djangocms_internalsearch.test_utils.app_1.cms_config import (
    TestModel3Config,
    TestModel4Config,
)


class ClassFactoryUnitTestCase(TestCase):

    def test_passing_just_string(self):
        test_str = 'CMSPlugin'
        with self.assertRaises(TypeError):
            generate_search_index_classes(test_str)

    def test_passing_string_list(self):
        test_str_list = ['CMSPlugin', 'Page']
        with self.assertRaises(TypeError):
            generate_search_index_classes(test_str_list)

    def test_passing_classes(self):
        test_class_list = [TestModel1Config.model, TestModel2Config.model]
        generate_search_index_classes(test_class_list)
        from djangocms_internalsearch.search_indexes import TestModel1Index
        self.assertEqual(TestModel1Index.__name__, 'TestModel1Index')


class InternalSearchIntegrationTestCase(CMSTestCase):

    def setUp(self):
        app_registration.get_cms_extension_apps.cache_clear()
        app_registration.get_cms_config_apps.cache_clear()

    def test_config_with_two_apps(self):
        setup_cms_apps()
        internalsearch_config = apps.get_app_config('djangocms_internalsearch')
        registered_model = internalsearch_config.cms_extension.internalsearch_models

        generate_search_index_classes(registered_model)

        from djangocms_internalsearch.search_indexes import TestModel1Index
        self.assertEqual(TestModel1Index.__name__, 'TestModel1Index')
