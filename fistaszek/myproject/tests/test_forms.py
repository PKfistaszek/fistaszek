# -*- coding: utf-8 -*-
"""
Views test
===================
"""

from mock import Mock, MagicMock, patch, sentinel
from morelia.decorators import tags
from smarttest.decorators import no_db_testcase
from unittest import skip

from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files import File
from django.test import TestCase

from myproject.forms import (
    UserForm,
    UploadFileForm
)


@no_db_testcase
@tags(['unit'])
class UserFormTestCase(TestCase):
    u"UserForm unittest class."

    def setUp(self):
        self._email = 'dada@wp.pl'
        self._password = '1234'
        self._data = {
            'email': self._email,
            'password': self._password,
        }

    def test_should_validate_input(self):
        form = UserForm(self._data)
        result = form.is_valid()

        # Assert
        self.assertTrue(result)
        self.assertEqual(form.cleaned_data['email'], self._email)
        self.assertEqual(form.cleaned_data['password'], self._password)

    def test_should_return_email_error(self):
        self._email = 'dadawp.pl'
        self._data = {
            'email': self._email,
            'password': self._password,
        }
        form = UserForm(self._data)
        result = form.is_valid()
        self.assertFalse(result)
        self.assertTrue('Enter a valid email address.' in form.errors['email'])


@no_db_testcase
@tags(['unit'])
class UploadFileFormTestCase(TestCase):
    u"UploadFileForm unittest class."

    def setUp(self):
        self._file = MagicMock(spec=File, name='RestrictedFileField')
        self._file.content_types = ['application/json']
        self._file.name = 'upload/file_name'
        self._private = True
        self._data = {
            'private': self._private,
            'file': self._file
        }

    def test_should_validate_input(self):
        form = UploadFileForm(self._data)
        result = form.is_valid()
        self.assertTrue(result)
        self.assertEqual(form.cleaned_data['file'], self._file)
        self.assertEqual(form.cleaned_data['private'], self._private)
