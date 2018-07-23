from django.apps import apps
from django.test import TestCase

from cms import app_registration
from cms.test_utils.testcases import CMSTestCase
from cms.utils.setup import setup_cms_apps

from djangocms_internalsearch.search_indexes import (
    generate_search_index_classes,
)
from djangocms_internalsearch.test_utils.app_2.models import (
    TestModel1,
    TestModel2,
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
        test_class_list = [TestModel1, TestModel2]
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
        model_list = internalsearch_config.cms_extension.internalsearch_models
        generate_search_index_classes(model_list)
        from djangocms_internalsearch.search_indexes import (
            TestModel1Index,
            TestModel2Index,
            TestModel3Index,
            TestModel4Index,
        )
        self.assertEqual(TestModel1Index.__name__, 'TestModel1Index')
        self.assertEqual(TestModel2Index.__name__, 'TestModel2Index')
        self.assertEqual(TestModel3Index.__name__, 'TestModel3Index')
        self.assertEqual(TestModel4Index.__name__, 'TestModel4Index')
