# -*- coding: utf-8 -*-
"""
Views test
===================
"""

from mock import Mock, MagicMock, patch, sentinel
from morelia.decorators import tags
from smarttest.decorators import no_db_testcase
from unittest import skip

from django.contrib.auth.models import User
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.urlresolvers import reverse, reverse_lazy
from django.test import TestCase, RequestFactory
from django.views.generic import ListView, FormView

from myproject.factories import (
    UserFactory,
    UserFilesFactory
)
from myproject.forms import (
    UserForm,
    UploadFileForm
)
from myproject.models import (
    UserFiles,

)
from myproject.views import (
    IndexView,
    LogoutView,
    UploadFileView,
    UploadFileList,
)


@no_db_testcase
@tags(['unit'])
class IndexViewTestCase(TestCase):
    u"IndexView unittest class."

    def setUp(self):
        self._form_class = Mock(UserForm)
        self._view = IndexView.as_view(
            form_class=self._form_class,
            success_url='upload'
            )
        self._factory = RequestFactory()

    def test_is_context_data_contains_form(self):
        url = reverse('index')
        request = self._factory.get(url)
        request.user = Mock(User)
        request.user.is_authenticated.return_value = False
        response = self._view(request)
        self.assertTrue('form' in response.context_data)

    @patch('myproject.views.redirect')
    def test_if_user_is_logged_redirect(self, redirect):
        url = reverse('index')
        redirect.return_value = sentinel.url
        request = self._factory.get(url)
        request.user = Mock(User)
        request.user.is_authenticated.return_value = True
        response = self._view(request)
        self.assertEquals(sentinel.url, response)

    @patch.object(User, 'objects')
    @patch('myproject.views.authenticate')
    @patch('myproject.views.login')
    def test_should_valid_form_and_redirect_on_success(
            self, login, authenticate, user_get):
        url = reverse('index')
        form = self._form_class.return_value
        form.cleaned_data = {
            'email': sentinel.email,
            'password': sentinel.password
        }
        form.is_valid.return_value = True

        user = Mock(User)
        user.username = sentinel.username
        authenticate.return_value = sentinel.authenticate
        login.return_value = True
        user_get.get.return_value = user
        data = {
        }
        request = self._factory.post(url, data)
        request.user = Mock(User)
        request.user.is_authenticated.return_value = False
        response = self._view(request)

        self.assertEqual('upload', response.url)
        login.assert_called_with(request, sentinel.authenticate)
        authenticate.assert_called_with(
            username=sentinel.username,
            password=sentinel.password
        )
        user_get.get.assert_called_with(email=sentinel.email)


@no_db_testcase
@tags(['unit'])
class LogoutViewTestCase(TestCase):
    u"LogoutView unittest class."

    def setUp(self):
        self._form_class = Mock(UserForm)
        self._view = LogoutView.as_view()
        self._factory = RequestFactory()

    @patch('myproject.views.logout')
    def test_success_logout_and_redirect(self, logout):
        logout.return_value = True
        url = reverse('logout')
        reverse_lazy.return_value = sentinel.login
        request = self._factory.get(url)
        response = self._view(request)
        self.assertEqual('/', response.url)


@no_db_testcase
@tags(['unit'])
class UploadFileViewTestCase(TestCase):
    u"UploadFileView unittest class."

    def setUp(self):
        self._form_class = Mock(UploadFileForm)
        self._view = UploadFileView.as_view(
            form_class=self._form_class
            )
        self._factory = RequestFactory()

    def test_is_context_data_contains_form(self):
        url = reverse('upload')
        request = self._factory.get(url)
        request.user = Mock(User)
        response = self._view(request)
        self.assertTrue('form' in response.context_data)

    @patch.object(UserFiles, 'save')
    @patch.object(FormView, 'get_form_kwargs')
    @patch('myproject.views.send_upload_email_task')
    @patch.object(UploadFileView, '_send_create_email_message')
    def test_should_save_form_and_redirect_on_success(
            self, send_create_email_message, send_upload_email_task,
            user_save, get_form_kwargs):

        url = reverse('upload')

        # patches
        form = self._form_class.return_value
        file = MagicMock(spec=File, name='RestrictedFileField')
        get_form_kwargs.return_value = {'files': {'file': file}, }
        form.cleaned_data = {'private': True, }
        send_upload_email_task.return_value
        send_create_email_message.return_value
        form.is_valid.return_value = True

        # prepare request
        user = UserFactory(pk=1)
        user_save.return_value
        request = self._factory.post(url)
        request.user = user

        response = self._view(request)

        # asserts
        self.assertEqual(response.url, url)
        self.assertTrue(send_upload_email_task.call)
        self.assertTrue(send_create_email_message.call)
        self.assertTrue(user_save.call)

    def test_send_create_message_private_function(self):
        file = MagicMock(spec=File, name='upload/RestrictedFileField')
        file.name = 'upload/file_name'
        user_file = UserFilesFactory(upload=file, private=True)
        view = UploadFileView()
        result = view._send_create_email_message(user_file)
        self.assertEqual("Private file file_name uploaded.", result)


@no_db_testcase
@tags(['unit'])
class UploadFileListTestCase(TestCase):
    u"UploadFileList unittest class."

    def setUp(self):
        self._form_class = Mock(UserForm)
        self._view = UploadFileList.as_view()
        self._factory = RequestFactory()

    def test_user_is_superuser_and_redirect(self):
        url = reverse('list')
        request = self._factory.get(url)
        request.user = Mock(User)
        request.user.is_superuser = True
        response = self._view(request)
        self.assertEqual('/admin_list/', response.url)

    @patch.object(ListView, 'get')
    def test_user_is_not_superuser_and_redirect(self, l_get):
        url = reverse('list')
        request = self._factory.get(url)
        request.user = Mock(User)
        request.user.is_superuser = False
        self._view(request)
        self.assertTrue(l_get.called)
