from django.test import TestCase
from tests.mocks import MockSearchResult
from tests.core.models import MockModel


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
