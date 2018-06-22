from unittest.mock import MagicMock

from django import forms
from django.contrib.auth.models import User
from django.test import TestCase, override_settings

from djangocms_internalsearch import constants
from djangocms_internalsearch.forms import *
from djangocms_internalsearch.models import Workflow

from .utils import BaseTestCase


class InternalsearchRequestFormTest(BaseTestCase):

    def test_form_init(self):
        form = InternalsearchRequestForm(
            action=constants.ACTION_STARTED,
            language='en',
            page=self.pg2,
            user=self.user,
            workflow=self.wf1,
            active_request=None,
        )
        self.assertIn('moderator', form.fields)
        field_moderator = form.fields['moderator']
        self.assertEqual(field_moderator.empty_label, 'Any Role 1')
        self.assertQuerysetEqual(field_moderator.queryset, User.objects.none())

    def test_form_save(self):
        data = {
            'moderator': None,
            'message': 'Some message'
        }
        form = InternalsearchRequestForm(
            data,
            action=constants.ACTION_STARTED,
            language='en',
            page=self.pg2,
            user=self.user,
            workflow=self.wf1,
            active_request=None,
        )
        form.workflow.submit_new_request = MagicMock()
        self.assertTrue(form.is_valid())
        form.save()
        form.workflow.submit_new_request.assert_called_once_with(
            page=self.pg2,
            by_user=self.user,
            to_user=None,
            language='en',
            message='Some message',
        )


class UpdateInternalsearchRequestFormTest(BaseTestCase):

    def test_form_init_approved_action(self):
        form = UpdateInternalsearchRequestForm(
            action=constants.ACTION_APPROVED,
            language='en',
            page=self.pg1,
            user=self.user,
            workflow=self.wf1,
            active_request=self.Internalsearch_request1,
        )
        self.assertIsInstance(form, InternalsearchRequestForm)
        field_moderator = form.fields['moderator']
        self.assertEqual(field_moderator.empty_label, 'Any Role 2')
        self.assertQuerysetEqual(field_moderator.queryset, User.objects.filter(pk__in=[self.user2.pk]), transform=lambda x: x, ordered=False)

    def test_form_init_cancelled_action(self):
        form = UpdateInternalsearchRequestForm(
            action=constants.ACTION_CANCELLED,
            language='en',
            page=self.pg1,
            user=self.user,
            workflow=self.wf1,
            active_request=self.Internalsearch_request1,
        )
        field_moderator = form.fields['moderator']
        self.assertQuerysetEqual(field_moderator.queryset, User.objects.none())
        self.assertIsInstance(field_moderator.widget, forms.HiddenInput)

    def test_form_init_rejected_action(self):
        form = UpdateInternalsearchRequestForm(
            action=constants.ACTION_REJECTED,
            language='en',
            page=self.pg1,
            user=self.user,
            workflow=self.wf1,
            active_request=self.Internalsearch_request1,
        )
        field_moderator = form.fields['moderator']
        self.assertQuerysetEqual(field_moderator.queryset, User.objects.none())
        self.assertIsInstance(field_moderator.widget, forms.HiddenInput)

    def test_form_save(self):
        data = {
            'moderator': None,
            'message': 'Approved message'
        }
        form = UpdateInternalsearchRequestForm(
            data,
            action=constants.ACTION_APPROVED,
            language='en',
            page=self.pg1,
            user=self.user,
            workflow=self.wf1,
            active_request=self.Internalsearch_request1,
        )
        form.active_request.update_status = MagicMock()
        self.assertTrue(form.is_valid())
        form.save()
        form.active_request.update_status.assert_called_once_with(
            action=constants.ACTION_APPROVED,
            by_user=self.user,
            to_user=None,
            message='Approved message',
        )


class SelectInternalsearchFormTest(BaseTestCase):

    def test_form_init(self):
        form = SelectInternalsearchForm(page=self.pg1,)
        self.assertIn('workflow', form.fields)
        field_workflow = form.fields['workflow']
        self.assertQuerysetEqual(field_workflow.queryset, Workflow.objects.all(), transform=lambda x: x, ordered=False)
        self.assertEqual(field_workflow.initial, self.wf1)
