from haystack import indexes
from tests.core.models import MockModel


class MockSearchIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    foo = indexes.CharField(model_attr='foo')

    def get_model(self):
        return MockModel
