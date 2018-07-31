"""

"""

import datetime

from cms.test_utils.testcases import CMSTestCase
from djangocms_internalsearch.test_utils.app_3.models import (
    TestModel5,
    TestModel6,
)

from .utils import TestCase


def populate_model5():
    date = datetime.datetime(2010, 1, 1)
    for i in range(1, 200):
        m = TestModel5()
        m.name = 'model5 name {}'.format(i)
        m.date = date + datetime.timedelta(days=i)
        m.text = 'text five {} {}'.format(i, (i % 2) == 0)
        m.status = 'STATUS{}'.format(i % 3)
        m.save()


def populate_model6():
    date = datetime.datetime(2010, 2, 1)
    for i in range(1, 200):
        m = TestModel6()
        m.name = 'model5 name {}'.format(i)
        m.date = date + datetime.timedelta(days=i)
        m.text = 'text six {} {}'.format(i, (i % 2) == 0)
        m.save()


class InternalSearchIndexingTestCase(CMSTestCase, TestCase):
    def setUp(self):
        populate_model5()
        populate_model6()
