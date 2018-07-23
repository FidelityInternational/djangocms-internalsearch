from django.test import TestCase

from cms import app_registration
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
        self.assertEqual(TestModel1.__name__, 'TestModel1')
        from djangocms_internalsearch.search_indexes import TestModel1Index
        self.assertEqual(TestModel1Index.__name__, 'TestModel1Index')
