from unittest.mock import patch

from django.test import TestCase, override_settings
from django.utils.translation import ugettext_lazy as _

from djangocms_internalsearch import constants
from djangocms_internalsearch.forms import *
from djangocms_internalsearch.views import *
from djangocms_internalsearch.utils import get_admin_url

from .utils import BaseViewTestCase


class InternalsearchRequestViewTest(BaseViewTestCase):

    def _assert_render(self, response, page, action, workflow, active_request, form_cls, title):
        view = response.context_data['view']
        form = response.context_data['adminform']
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], 'djangocms_internalsearch/request_form.html')
        self.assertEqual(view.language, 'en')
        self.assertEqual(view.page, page)
        self.assertEqual(view.action, action)
        self.assertEqual(view.workflow, workflow)
        self.assertEqual(view.active_request, active_request)
        self.assertEqual(response.context_data['title'], title)
        self.assertIsInstance(form, form_cls)

    def test_new_request_view_with_form(self):
        response = self.client.get(
            get_admin_url(
                name='cms_Internalsearch_new_request',
                language='en',
                args=(self.pg2.pk, 'en')
            )
        )
        self._assert_render(
            response=response,
            page=self.pg2,
            action=constants.ACTION_STARTED,
            active_request=None,
            workflow=self.wf1,
            form_cls=InternalsearchRequestForm,
            title=_('Submit for Internalsearch')
        )

    def test_new_request_view_with_form_workflow_passed_param(self):
        response = self.client.get(
            '{}?{}'.format(
                get_admin_url(
                    name='cms_Internalsearch_new_request',
                    language='en',
                    args=(self.pg2.pk, 'en')
                ),
                'workflow={}'.format(self.wf2.pk)
            )
        )
        self._assert_render(
            response=response,
            page=self.pg2,
            action=constants.ACTION_STARTED,
            active_request=None,
            workflow=self.wf2,
            form_cls=InternalsearchRequestForm,
            title=_('Submit for Internalsearch')
        )

    def test_cancel_request_view_with_form(self):
        response = self.client.get(get_admin_url(
            name='cms_Internalsearch_cancel_request',
            language='en',
            args=(self.pg1.pk, 'en')
        ))
        self._assert_render(
            response=response,
            page=self.pg1,
            action=constants.ACTION_CANCELLED,
            active_request=self.Internalsearch_request1,
            workflow=self.wf1,
            form_cls=UpdateInternalsearchRequestForm,
            title=_('Cancel request')
        )

    def test_reject_request_view_with_form(self):
        response = self.client.get(get_admin_url(
            name='cms_Internalsearch_reject_request',
            language='en',
            args=(self.pg1.pk, 'en')
        ))
        self._assert_render(
            response=response,
            page=self.pg1,
            action=constants.ACTION_REJECTED,
            active_request=self.Internalsearch_request1,
            workflow=self.wf1,
            form_cls=UpdateInternalsearchRequestForm,
            title=_('Reject changes')
        )

    def test_approve_request_view_with_form(self):
        response = self.client.get(get_admin_url(
            name='cms_Internalsearch_approve_request',
            language='en',
            args=(self.pg1.pk, 'en')
        ))
        self._assert_render(
            response=response,
            page=self.pg1,
            action=constants.ACTION_APPROVED,
            active_request=self.Internalsearch_request1,
            workflow=self.wf1,
            form_cls=UpdateInternalsearchRequestForm,
            title=_('Approve changes')
        )

    def test_get_form_kwargs(self):
        response = self.client.get(get_admin_url(
            name='cms_Internalsearch_new_request',
            language='en',
            args=(self.pg2.pk, 'en')
        ))
        view = response.context_data['view']
        kwargs = view.get_form_kwargs()
        self.assertEqual(kwargs.get('action'), view.action)
        self.assertEqual(kwargs.get('language'), view.language)
        self.assertEqual(kwargs.get('page'), view.page)
        self.assertEqual(kwargs.get('user'), view.request.user)
        self.assertEqual(kwargs.get('workflow'), view.workflow)
        self.assertEqual(kwargs.get('active_request'), view.active_request)

    def test_form_valid(self):
        response = self.client.post(get_admin_url(
            name='cms_Internalsearch_new_request',
            language='en',
            args=(self.pg2.pk, 'en')
        ), {'moderator': '', 'message': 'Some review message'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'reloadBrowser') # check html part

    def test_throws_error_Internalsearch_already_exists(self):
        response = self.client.get('{}?{}'.format(
            get_admin_url(
                name='cms_Internalsearch_new_request',
                language='en',
                args=(self.pg1.pk, 'en')
            ),
            'workflow={}'.format(self.wf1.pk) # pg1 => active request
        ))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b'Page already has an active Internalsearch request.')

    def test_throws_error_invalid_workflow_passed(self):
        response = self.client.get('{}?{}'.format(
            get_admin_url(
                name='cms_Internalsearch_new_request',
                language='en',
                args=(self.pg2.pk, 'en')
            ),
            'workflow=10' # pg2 => no active requests, 10 => workflow does not exist
        ))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b'No Internalsearch workflow exists for page.')

    def test_throws_no_active_Internalsearch_request(self):
        response = self.client.get(get_admin_url(
            name='cms_Internalsearch_cancel_request',
            language='en',
            args=(self.pg2.pk, 'en') # pg2 => no active requests
        ))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b'Page does not have an active Internalsearch request.')

    def test_throws_error_already_approved(self):
        response = self.client.get(get_admin_url(
            name='cms_Internalsearch_approve_request',
            language='en',
            args=(self.pg3.pk, 'en') # pg3 => active request with all approved steps
        ))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b'Internalsearch request has already been approved.')

    def test_throws_error_forbidden_user(self):
        from django.contrib.auth.models import User
        user = User.objects.create_user(username='test1', email='test1@test.com', password='test1', is_staff=True)
        self.client.force_login(user)
        response = self.client.get(get_admin_url(
            name='cms_Internalsearch_approve_request',
            language='en',
            args=(self.pg1.pk, 'en') # pg1 => active request
        ))
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.content, b'User is not allowed to update request.')

    @patch('djangocms_internalsearch.views.get_page_Internalsearch_workflow', return_value=None)
    def test_throws_error_if_workflow_has_not_been_resolved(self, mock_gpmw):
        response = self.client.get(get_admin_url(
            name='cms_Internalsearch_new_request',
            language='en',
            args=(self.pg2.pk, 'en')
        ))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b'No Internalsearch workflow exists for page.')


class SelectInternalsearchViewTest(BaseViewTestCase):

    def test_renders_view_with_form(self):
        response = self.client.get(get_admin_url(
            name='cms_Internalsearch_select_new_Internalsearch',
            language='en',
            args=(self.pg1.pk, 'en')
        ))
        view = response.context_data['view']
        form = response.context_data['adminform']
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], 'djangocms_internalsearch/select_workflow_form.html')
        self.assertEqual(view.page_id, str(self.pg1.pk))
        self.assertEqual(view.current_lang, 'en')
        self.assertIsInstance(form, SelectInternalsearchForm)

    def test_get_form_kwargs(self):
        response = self.client.get(get_admin_url(
            name='cms_Internalsearch_select_new_Internalsearch',
            language='en',
            args=(self.pg1.pk, 'en')
        ))
        view = response.context_data['view']
        kwargs = view.get_form_kwargs()
        self.assertEqual(kwargs.get('page'), self.pg1)

    def test_form_valid(self):
        response = self.client.post(get_admin_url(
            name='cms_Internalsearch_select_new_Internalsearch',
            language='en',
            args=(self.pg1.pk, 'en')
        ), {'workflow': self.wf2.pk})
        form_valid_redirect_url = '{}?{}'.format(
            get_admin_url(
                name='cms_Internalsearch_new_request',
                language='en',
                args=(self.pg1.pk, 'en')
            ),
            'workflow={}'.format(self.wf2.pk)
        )
        self.assertEqual(response.url, form_valid_redirect_url)
