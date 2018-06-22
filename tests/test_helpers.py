from unittest.mock import patch

from django.test import TestCase, override_settings

from djangocms_internalsearch.helpers import *
from djangocms_internalsearch.models import Workflow, PageInternalsearch

from .utils import BaseTestCase


class GetWorkflowOrNoneTest(BaseTestCase):

    def test_existing_workflow(self):
        workflow = Workflow.objects.get(pk=1)
        self.assertEqual(get_workflow_or_none(1), workflow)
        workflow = Workflow.objects.get(pk=2)
        self.assertEqual(get_workflow_or_none(2), workflow)

    def test_non_existing_workflow(self):
        self.assertIsNone(get_workflow_or_none(10))


class GetCurrentInternalsearchRequestTest(BaseTestCase):

    def test_existing_Internalsearch_request(self):
        active_request = get_active_Internalsearch_request(self.pg1, 'en')
        self.assertEqual(active_request, self.Internalsearch_request1)

    def test_no_Internalsearch_request(self):
        active_request = get_active_Internalsearch_request(self.pg2, 'en')
        self.assertIsNone(active_request)


class GetPageOr404Test(BaseTestCase):

    def test_returns_page(self):
        self.assertEqual(get_page_or_404(self.pg1.pk, 'en'), self.pg1)


class IsInternalsearchEnabledTest(BaseTestCase):

    @override_settings(CMS_Internalsearch_ENABLE_WORKFLOW_OVERRIDE=True)
    def test_returns_true_with_override_no_Internalsearch_object(self):
        self.assertTrue(is_Internalsearch_enabled(self.pg1))

    @override_settings(CMS_Internalsearch_ENABLE_WORKFLOW_OVERRIDE=True)
    def test_returns_true_with_override_Internalsearch_object_enabled(self):
        PageInternalsearch.objects.create(extended_object=self.pg1, enabled=True, workflow=self.wf1,)
        self.assertTrue(is_Internalsearch_enabled(self.pg1))

    @override_settings(CMS_Internalsearch_ENABLE_WORKFLOW_OVERRIDE=True)
    def test_returns_false_with_override_Internalsearch_object_disabled(self):
        PageInternalsearch.objects.create(extended_object=self.pg1, enabled=False, workflow=self.wf1,)
        self.assertFalse(is_Internalsearch_enabled(self.pg1))

    @override_settings(CMS_Internalsearch_ENABLE_WORKFLOW_OVERRIDE=True)
    def test_returns_false_with_override_no_workflows(self):
        Workflow.objects.all().delete()
        self.assertFalse(is_Internalsearch_enabled(self.pg1))

    def test_returns_true_default_settings_has_default_workflow(self):
        self.assertTrue(is_Internalsearch_enabled(self.pg1))

    def test_returns_true_default_settings_Internalsearch_object_enabled(self):
        PageInternalsearch.objects.create(extended_object=self.pg1, enabled=True, workflow=self.wf1,)
        self.assertTrue(is_Internalsearch_enabled(self.pg1))

    def test_returns_false_default_settings_Internalsearch_object_disabled(self):
        PageInternalsearch.objects.create(extended_object=self.pg1, enabled=False, workflow=self.wf1,)
        self.assertFalse(is_Internalsearch_enabled(self.pg1))

    @patch('djangocms_internalsearch.helpers.get_page_Internalsearch_workflow', return_value=None)
    def test_returns_false_default_settings_no_workflow(self, mock_gpmw):
        self.assertFalse(is_Internalsearch_enabled(self.pg1))

