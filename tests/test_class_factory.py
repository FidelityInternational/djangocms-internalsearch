from django.test import TestCase
from tests.mocks import MockSearchResult
from tests.core.models import MockModel
from djangocms_internalsearch.search_indexes import generate_search_index_classes
from django.core.exceptions import ImproperlyConfigured
from cms.models import CMSPlugin, Page


class SearchResultTestCase(TestCase):
    fixtures = ["elasticsearch_data"]

    def setUp(self):
        super(SearchResultTestCase, self).setUp()

        self.no_data = {}
        self.no_data_sr = MockSearchResult("haystack", "mockmodel", str(1), 2)

    def test_init(self):
        pass
        self.assertEqual(self.no_data_sr.app_label, "haystack")
        self.assertEqual(self.no_data_sr.model_name, "mockmodel")
        self.assertEqual(self.no_data_sr.model, MockModel)


class ClassFactoryUnitTestCase(TestCase):

    def test_passing_just_string(self):
        test_str = 'CMSPlugin'
        with self.assertRaises(ImproperlyConfigured):
            generate_search_index_classes(test_str)

    def test_passing_string_list(self):
        test_str_list = ['CMSPlugin', 'Page']
        with self.assertRaises(ImproperlyConfigured):
            generate_search_index_classes(test_str_list)

    def test_passing_classes(self):
        test_class_list = [CMSPlugin, Page]
        instance_of_class = generate_search_index_classes(test_class_list)
        self.assertTrue(isinstance(instance_of_class, object))
